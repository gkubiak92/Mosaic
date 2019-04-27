from flask import Flask, request, Response, jsonify, render_template
from urllib.parse import urlparse
from PIL import Image
import requests
from decimal import localcontext, Decimal, ROUND_HALF_UP
from random import shuffle
from pathlib import Path


app = Flask(__name__)


@app.after_request
def add_header(response):
    # wyłączenie cache z racji na problem braku odświeżania mozaiki
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/mozaika')
def mosaic():
    # argumenty
    randomly = request.args.get('losowo', default=0, type=int)
    resolution = request.args.get(
        'rozdzielczosc', default='2048x2048', type=str)
    images = request.args.get('zdjecia', default='', type=str)

    if(images == ''):
        return 'Nie podałeś żadnych zdjęć'

    # lista urlów zdjęć
    images_list = [str(img) for img in images.split(',')]

    # tablica zdjęć
    imgs = []
    for url in images_list[:8]:
        if is_url_image(url):
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            new_img = Image.open(response.raw)
            imgs.append(new_img)

    if(len(imgs) < 1):
        return 'Żaden z podanych linków w parametrze zdjęcia nie jest obrazem'
    if(randomly):
        shuffle(imgs)
    # tworzenie kolażu
    w, h = resolution.split('x')
    width, height = int(w), int(h)
    collage = Image.new('RGB', (width, height), (244, 89, 1))

    x_offset = 0
    y_offset = 0

    if(len(imgs) == 1):
        img = imgs[0]
        x_offset = int(width / 2)
        y_offset = int(height / 2)
        half_x_img = int(img.size[0] / 2)
        half_y_img = int(img.size[1] / 2)
        x = x_offset - half_x_img
        y = y_offset - half_y_img
        # wklejenie zdjecia centralnie na środku
        collage.paste(img, (x, y))
    elif(len(imgs) == 2):
        for img in imgs:
            max_width = int(width / 2)
            max_height = int(height / 2)
            img = resize_image(img, max_width, max_height)
            y_offset = int(height / 2)
            half_y_img = int(img.size[1] / 2)
            y = y_offset - half_y_img
            collage.paste(img, (x_offset, y))
            x_offset += img.size[0]
    else:
        # ustawienie dzielnika ekranu do poprawnego ustawienia rozmiaru zdjęć
        # zaokrąglenie zgodnie z zasadą od 0.5 w górę
        divider = Decimal(len(imgs)) / 2
        divider = divider.to_integral_value(rounding=ROUND_HALF_UP)
        max_width = int(width / divider)
        max_height = int(height / divider)
        max_y_offset = 0
        for img in imgs:
            img = resize_image(img, max_width, max_height)
            if(img.size[0] > (width - x_offset)):
                y_offset = max_y_offset
                x_offset = 0
            collage.paste(img, (x_offset, y_offset))
            x_offset += img.size[0]
            if(img.size[1] > y_offset):
                max_y_offset = img.size[1]
    pathToStaticFolder = Path("static/")
    pathToSaveFile = pathToStaticFolder / "collage.jpeg"
    collage.save(pathToSaveFile)
    return render_template('mozaika.html', filename=pathToSaveFile.name)
    # zapis zebranych danych i zwrócenie w formacie JSON
    # data = {
    #     'losowosc': randomly,
    #     'rozdzielczosc': resolution,
    #     'images URLs': images_list
    # }
    # return jsonify(data)


def is_url_image(image_url):
    url = urlparse(image_url)
    if(url.scheme):
        img_formats = ['image/png', 'image/jpeg', 'image/jpg']
        r = requests.head(image_url)
        if r.headers['content-type'] in img_formats:
            return True
        return False
    return False


def resize_image(img, max_width, max_height):
    # zmiana rozmiaru obrazu zachowując aspect ratio
    ratio = min(max_width / img.size[0], max_height / img.size[1])
    width = int(img.size[0] * ratio)
    height = int(img.size[1] * ratio)
    new_img = img.resize((width, height))
    return new_img


if __name__ == '__main__':
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['CACHE_TYPE'] = 'null'
    app.run()
