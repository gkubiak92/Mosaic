# Mosaic

Short app written in Python and Flask which combines up to 8 images in one photo collage. 

## Getting Started

To download this project simply clone this repo using command below
```
git clone https://github.com/gkubiak92/Mosaic
```

### Prerequisites

Make sure you have installed all needed Python libraries to successfully test this app.
All needed libraries are specified at the top of app.py file

### Running

To run application use command below from main folder of project
```
python app.py
```

Then open link below (if you running this project on local machine)
```
http://127.0.0.1:5000/
```

You will see welcome screen in polish language with simple manual how to use parameters.
There are three parameters you can use:
* losowo - optional parameter (default: 0), when value is different from 0 than images in mosaic are in random order
* rozdzielczosc - optional parameter (default: 2048x2048), here you can define resolution of final image using WIDTHxHEIGHT for example 1600x1024
* zdjecia - required parameter, you have to provide at least 1 link to generate image. You can add from 1 up to 8 direct links separated by comma

To make a mosaic from images use /mozaika with at least 1 image as parameter "zdjecia=".
Image parameter have to be a direct link to image. Example shown below:

```
http://localhost:5000/mozaika?zdjecia=https://boygeniusreport.files.wordpress.com/2016/05/scared-surprised-cat-face.jpg
```

Here is an example using all parameteres specifide above

```
http://localhost:5000/mozaika?zdjecia=https://boygeniusreport.files.wordpress.com/2016/05/scared-surprised-cat-face.jpg,https://boygeniusreport.files.wordpress.com/2015/06/funny-cat.jpg,https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720__340.jpg,http://restlessnationradio.com/wp-content/uploads/2018/01/1516956465_hqdefault-480x330.jpg&losowo=1&rozdzielczosc=800x800
```



## Images used for test purposes*

* https://boygeniusreport.files.wordpress.com/2016/05/scared-surprised-cat-face.jpg
* https://boygeniusreport.files.wordpress.com/2015/06/funny-cat.jpg
* https://cdn.pixabay.com/photo/2017/11/09/21/41/cat-2934720__340.jpg
* http://restlessnationradio.com/wp-content/uploads/2018/01/1516956465_hqdefault-480x330.jpg

*No cat suffered while designing this application :)

## Authors

* **Grzegorz Kubiak** - *Initial work* - [gkubiak92](https://github.com/gkubiak92)
