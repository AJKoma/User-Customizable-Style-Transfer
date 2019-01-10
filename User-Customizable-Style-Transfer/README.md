Polarbears - Liqi Zhu, Xiaonan Hu, Siqi Xiong

### Install requirements

```shell
$ pip install -r requirements.txt
```

put nst_utils.py under your python lib folder.

Make sure you have the following installed:
tensorflow
keras
flask
pillow
h5py
gevent
werkzeug
hashlib
flask_mail
os
sys
spicy
PIL
requests
io
numpy
pymysql
datetime
random
string
json


Make sure you have the following model in Model Folder. (too large to upload to Blackboard)
imagenet-vgg-verydeep-19.mat 
Download at:
http://www.vlfeat.org/matconvnet/models/imagenet-vgg-verydeep-19.mat 


### Run Api

Please run the api.sin using Visual Studio in Web Api/api/api.sin

Default port: https://localhost:5001
Info of all images : https://localhost:5001/api/Style
Show image : https://localhost:5001/api/Style/{pic_id}/pic
Image info : https://localhost:5001/api/Style/{pic_id}/info


### Run mySQL

Please modify the script in app.py to fit your local data base. 

Table: CREATE TABLE Users (username VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL, password VARCHAR(45) NOT NULL, generated_pic VARCHAR(15000) NULL, PRIMARY KEY (username));
Colums: username, email, password, generated_pic
Primary Key: username 


### Run with Python

Python 3.5+ are supported and tested.

```shell
$ python app.py
```

### Play

Open http://localhost:5050 and have fun. 

