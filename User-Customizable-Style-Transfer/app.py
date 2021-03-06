from __future__ import division, print_function
# coding=utf-8

# Flask utils
from flask import Flask, flash, jsonify, redirect, url_for, request, render_template, session, escape
from werkzeug.utils import secure_filename
import gevent 
from gevent.pywsgi import WSGIHandler, WSGIServer 
from hashlib import md5
import hashlib
#import MySQLdb
from flask_mail import Mail, Message
##from flask_cors import CORS

import os
import sys
import scipy.io
import scipy.misc
#import matplotlib.pyplot as plt
#from matplotlib.pyplot import imshow
from PIL import Image
import requests
from io import BytesIO
from nst_utils import *
import numpy as np
import tensorflow as tf
import pymysql
import datetime
import random
import string
import json

#%%
os.chdir("/Users/ajkoma/Documents/GitHub/Web-Application-Development/User-Customizable-Style-Transfer")
db = pymysql.connect("127.0.0.1","AJKoma","614114Aj","polarbears")
g_path_all = str("default")

#%% Image Reading
def imread(path):
    img = scipy.misc.imread(path).astype(np.float)
    if len(img.shape) == 2:
        # grayscale
        img = np.dstack((img,img,img))
    elif img.shape[2] == 4:
        # PNG with alpha channel
        img = img[:,:,:3]
    return img

#%% GRADED FUNCTION: compute_content_cost
def compute_content_cost(a_C, a_G):
    """
    Computes the content cost
    
    Arguments:
    a_C -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing content of the image C 
    a_G -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing content of the image G
    
    Returns: 
    J_content -- scalar that you compute using equation 1 above.
    """
    
    # Retrieve dimensions from a_G (≈1 line)
    m, n_H, n_W, n_C = a_G.get_shape().as_list()
    
    # Reshape a_C and a_G (≈2 lines)
    a_C_unrolled = tf.transpose(tf.reshape(a_C, (n_H*n_W, n_C)))
    a_G_unrolled = tf.transpose(tf.reshape(a_G, (n_H*n_W, n_C)))
    
    # compute the cost with tensorflow (≈1 line)
    J_content = 1/(4*n_H*n_W*n_C)*tf.reduce_sum(tf.square(tf.subtract(a_C_unrolled, a_G_unrolled)))
    
    return J_content

#%% GRADED FUNCTION: gram_matrix
def gram_matrix(A):
    """
    Argument:
    A -- matrix of shape (n_C, n_H*n_W)
    
    Returns:
    GA -- Gram matrix of A, of shape (n_C, n_C)
    """
    
    GA = tf.matmul(A, A, transpose_b=True)
    
    return GA

#%% GRADED FUNCTION: compute_layer_style_cost
def compute_layer_style_cost(a_S, a_G):
    """
    Arguments:
    a_S -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing style of the image S 
    a_G -- tensor of dimension (1, n_H, n_W, n_C), hidden layer activations representing style of the image G
    
    Returns: 
    J_style_layer -- tensor representing a scalar value, style cost defined above by equation (2)
    """
    
    # Retrieve dimensions from a_G (≈1 line)
    m, n_H, n_W, n_C = a_G.get_shape().as_list()
    
    # Reshape the images to have them of shape (n_C, n_H*n_W) (≈2 lines)
    a_S = tf.transpose(tf.reshape(a_S, (n_H*n_W, n_C)))
    a_G = tf.transpose(tf.reshape(a_G, (n_H*n_W, n_C)))

    # Computing gram_matrices for both images S and G (≈2 lines)
    GS = gram_matrix(a_S)
    GG = gram_matrix(a_G)

    # Computing the loss (≈1 line)
    J_style_layer = 1/(4*n_C*n_C*n_H*n_W*n_H*n_W)*tf.reduce_sum(tf.square(tf.subtract(GS, GG)))
        
    return J_style_layer

#%%
STYLE_LAYERS = [
    ('conv1_1', 0.2),
    ('conv2_1', 0.2),
    ('conv3_1', 0.2),
    ('conv4_1', 0.2),
    ('conv5_1', 0.2)]

def compute_style_cost(sess, model, STYLE_LAYERS):
    """
    Computes the overall style cost from several chosen layers
    
    Arguments:
    model -- our tensorflow model
    STYLE_LAYERS -- A python list containing:
                        - the names of the layers we would like to extract style from
                        - a coefficient for each of them
    
    Returns: 
    J_style -- tensor representing a scalar value, style cost defined above by equation (2)
    """
    
    # initialize the overall style cost
    J_style = 0

    for layer_name, coeff in STYLE_LAYERS:

        # Select the output tensor of the currently selected layer
        out = model[layer_name]

        # Set a_S to be the hidden layer activation from the layer we have selected, by running the session on out
        a_S = sess.run(out)

        # Set a_G to be the hidden layer activation from same layer. Here, a_G references model[layer_name] 
        # and isn't evaluated yet. Later in the code, we'll assign the image G as the model input, so that
        # when we run the session, this will be the activations drawn from the appropriate layer, with G as input.
        a_G = out
        
        # Compute style_cost for the current layer
        J_style_layer = compute_layer_style_cost(a_S, a_G)

        # Add coeff * J_style_layer of this layer to overall style cost
        J_style += coeff * J_style_layer

    return J_style

#%% GRADED FUNCTION: total_cost
def total_cost(J_content, J_style, alpha = 10, beta = 40):
    """
    Computes the total cost function
    
    Arguments:
    J_content -- content cost coded above
    J_style -- style cost coded above
    alpha -- hyperparameter weighting the importance of the content cost
    beta -- hyperparameter weighting the importance of the style cost
    
    Returns:
    J -- total cost as defined by the formula above.
    """
    
    J = alpha*J_content + beta*J_style
    
    return J

#%%
def model_nn(sess, train_step, input_image, J, J_content, J_style, num_iterations = 200, ):
    
    # Initialize global variables (you need to run the session on the initializer)
    sess.run(tf.global_variables_initializer())
    
    # Run the noisy input image (initial generated image) through the model. Use assign().
    sess.run(model["input"].assign(input_image))
    
    for i in range(num_iterations):
    
        # Run the session on the train_step to minimize the total cost
        sess.run(train_step)
        
        # Compute the generated image by running the session on the current model['input']
        generated_image = sess.run(model["input"])

        # Print every 20 iteration.
        if i%20 == 0:
            Jt, Jc, Js = sess.run([J, J_content, J_style])
            print("Iteration " + str(i) + " :")
            print("total cost = " + str(Jt))
            print("content cost = " + str(Jc))
            print("style cost = " + str(Js))
            
            # save current generated image in the "/output" directory
            #save_image("output/" + str(i) + ".png", generated_image)
    
    # save generated image
    if 'g_path_all' in globals():
        global g_path_all
        print (g_path_all) 
    
        file_path = str(username_session+id_generator())+'.jpg'
        g_path = "static/img/" + file_path
        save_image(g_path, generated_image)
    
        if g_path_all == "":
            g_path_all = file_path
        else:
            g_path_all = g_path_all + ","+ file_path

        print(g_path_all)
    
        cur = db.cursor()
        cur.execute("UPDATE Users SET generated_pic = %s WHERE username = %s",(g_path_all,session['username']))
        db.commit()
    
    else:
        g_path = "static/img/generated_image.jpg"
        save_image(g_path, generated_image)

    return g_path  

#%%
model = load_vgg_model("models/imagenet-vgg-verydeep-19.mat")
print('Model loaded. Check http://127.0.0.1:5050/')
#print(model)

#%%
def transfer(style_image, content_image):
    generated_image = generate_noise_image(content_image)
    sess = tf.InteractiveSession()
    sess.run(model['input'].assign(content_image))
    out = model['conv4_2']
    a_C = sess.run(out)
    a_G = out
    J_content = compute_content_cost(a_C, a_G)
    sess.run(model['input'].assign(style_image))
    J_style = compute_style_cost(sess, model, STYLE_LAYERS)
    J = total_cost(J_content, J_style, alpha = 10, beta = 40)
    optimizer = tf.train.AdamOptimizer(2.0)
    train_step = optimizer.minimize(J)
        
    result = model_nn(sess, train_step, generated_image, J, J_content, J_style)
    
    return result


#%%
def my_md5(pwd):
    my_md5=hashlib.md5()
    my_md5.update(pwd.encode('utf-8'))
    return my_md5.hexdigest()

#%%
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#%%
#style_image = scipy.misc.imread("images/monet.jpg")
#imshow(style_image)
#style_image = reshape_and_normalize_image(style_image)

#%% Define a flask app
app = Flask(__name__)
##CORS(app)

# email configuration
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'xsq74185@gmail.com'
app.config['MAIL_PASSWORD'] = 'Xsq63549347'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#%%
@app.route('/', methods=['GET'])
def index():
    #session['username'] = "Kiran"
    if 'username' in session:
        global username_session
        global g_path_all
        username_session = escape(session['username']).capitalize()
        cur = db.cursor()
        cur.execute("SELECT generated_pic FROM Users WHERE username = %s", (session['username']))
        g_path_all = cur.fetchone()[0]
        
        if g_path_all == None:
            g_path_all = str("")

        return render_template('index.html', session_user_name=username_session)
    #return (url_for('login'))
    # Main page
    return render_template('index.html')

#%%
@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/signUp",methods=['GET', 'POST'])
def signUp():
	username = str(request.form["susername"])
	password = str(request.form["spassword"])
	email = str(request.form["semail"])
	#print(username, password, email)
	cur = db.cursor()
	cur.execute("INSERT INTO Users(username,password,email) VALUES(%s,%s,%s) ON DUPLICATE KEY update username = username ",(username,my_md5(password),email))
	db.commit()
	return render_template('form.html')

class ServerError(Exception):pass
	
@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    username  = str(request.form["lusername"])
    password  = str(request.form['lpassword'])
    cursor = db.cursor()
#    sql = "SELECT COUNT(*) FROM Users WHERE username = %s AND password = %s"
#    try:
#        cursor.execute(sql, (username,my_md5(password)))
#        results = cursor.fetchone()
#        print (results)
#
#        if results[0]>0:
#            session['username'] = username
#            print('sucess')
#            return redirect('/')
#            #return render_template('index.html', error= None)
#        else:
#            #raise ServerError('Invalid username or password!')
#            print('Username or password not match!') 
#        
#        
#    except: 
#         db.rollback()
#    
#    return render_template('form.html', error=error)
    
    if 'username' in session:
        flash('You have already logged in')
        return redirect('/')
    
    error = None
    try:
        if request.method == 'POST':
            cursor.execute("SELECT COUNT(*) FROM Users WHERE username = %s AND password = %s", (username,my_md5(password)))
            if cursor.fetchone()[0]>0:
                session['username'] = username
                session['password'] = my_md5(password)
                cursor.execute("SELECT email FROM Users WHERE username = %s", (username))
                session['email'] = cursor.fetchone()[0]
                #flash('You were successfully logged in')
                return redirect('/')
            else:
                cursor.execute("SELECT COUNT(*) FROM Users WHERE username = %s", (username))
                if cursor.fetchone()[0]>0:
                    raise ServerError('Invalid password!')
                else:
                    raise ServerError('Invalid username!')
            
    except ServerError as e:
        error = str(e)
        
    return render_template('form.html', error=error)

#%%
@app.route("/reset")
def reset():
    return render_template('reset.html')

@app.route('/reset', methods=['GET', 'POST'])
def newpwd():
    username = str(request.form["rusername"])
    email = str(request.form["remail"])
    # password = str(request.form["rpassword"])
    cursor = db.cursor()
    sql = "SELECT count(*) FROM Users WHERE username = %s and email = %s"
    cursor.execute(sql, (username,email))
    results = cursor.fetchone()
    try:
        if results[0]>0:
            cursor.execute("select password from Users where username = %s and email = %s",(username, email))
            password = cursor.fetchone()[0]
            msg = Message('Hello', sender = 'kiranhxn@gmail.com', recipients = [email])
            msg.body = "Hello Flask message sent from Flask-Mail, your password is: %s" % password
            mail.send(msg)
            return render_template('update.html')
        else:
            cursor.execute("SELECT COUNT(*) FROM Users WHERE username = %s or email = %s",(username, email))
            if cursor.fetchone()[0]>0:
                raise ServerError('Invalid username or email, please check!')
            else:
                raise ServerError('Invalid username and email, please sign up!')
            
    except ServerError as e:
        error = str(e)
        
    return render_template('reset.html', error=error)
    
@app.route('/update', methods=['GET','POST'])
def update():
    rusername = str(request.form["rusername"])
    opassword = str(request.form["opassword"])
    newpassword = str(request.form["npassword"])
    confpassword = str(request.form["confpassword"])
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users where password = %s and username = %s",(opassword, rusername))
    
    try:
        if cursor.fetchone()[0]>0:
            if newpassword==confpassword:
                sql = "UPDATE Users SET password = %s where password = %s and username = %s"
                result = cursor.execute(sql,(my_md5(newpassword),opassword, rusername))
                db.commit()
                return render_template('form.html')
            else: 
                raise ServerError('New passwords do not match!')
        else:
            raise ServerError('Invalid username or old password!')
    
    except ServerError as e:
        error = str(e)
        
    return render_template('update.html', error=error)
    
#%%
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

#%%
@app.route('/profile')
def profile():
    #global g_path_all
    global files
    files = {}
    email_session = escape(session['email']).capitalize()
    password_session = escape(session['password']).capitalize()
    username_session = escape(session['username']).capitalize()

    if g_path_all != str(""):
        files = g_path_all.split(',')
        #print (files)        

#    if request.method == 'GET':
#        data = {}
#        try:
#            data['username'] = session['username']
#            data['password'] = session['password']
#            data['email'] = session['email']
#            
#    #return render_template('profile.html', session_user_name = username_session, session_email = email_session, session_password = password_session)
#S
#        except:
#            pass
#        #return jsonify(data)
    return render_template('profile.html', imgfiles = json.dumps(files), session_user_name = username_session, session_email = email_session, session_password = "*" * len(password_session))

@app.route('/profile', methods=['GET','POST'])
def editPwd():
    password = str(request.form["password"])
    newpassword = str(request.form["npassword"])
    confirm = str(request.form["cpassword"])
    username_session = escape(session['username']).capitalize()
    email_session = escape(session['email']).capitalize()
    password_session = escape(session['password']).capitalize() 
    cursor = db.cursor()
    try:
        if request.method == 'POST':
            if my_md5(password) == session['password'] and newpassword == confirm:
                sql = "UPDATE Users SET password = %s WHERE username = %s"
                cursor.execute(sql,(my_md5(newpassword),session['username']))
                db.commit()
                session['password'] = my_md5(newpassword)
                password_session = escape(session['password']).capitalize()
                return redirect('/profile')
            else:
                if my_md5(password) == session['password']:
                    raise ServerError('The two passwords you typed do not match!')
                else:
                    raise ServerError('Wrong password!')
            
    except ServerError as e:
        error = str(e)

    return render_template('profile.html', error=error, imgfiles = json.dumps(files), session_user_name = username_session, session_email = email_session, session_password = "*" * len(password_session))

#@app.route('/profile', methods=['GET','POST'])
#def sendNew():
#    email = str(request.form["email"])
#    password_session = escape(session['password']).capitalize()
#    
#    msg = Message('Hello', sender = 'kiranhxn@gmail.com', recipients = [email])
#    msg.body = "Hello Flask message sent from Flask-Mail, your confirmation number is: %s" % password_session
#    mail.send(msg)
#
#    return None
#    
#@app.route('/profile', methods=['GET','POST'])
#def confirmNew():
#    email = str(request.form["email"])
#    confirmation = str(request.form["confirmation"])
#    username_session = escape(session['username']).capitalize()
#    password_session = escape(session['password']).capitalize()
#    cursor = db.cursor()
#    try:
#        if confirmation == password_session:
#            sql = "update Users SET email = %s where username = %s"
#            cursor.execute(sql,(email,username_session))
#            db.commit()
#        else:
#            raise ServerError('Wrong confirmation number!')
#
#    except ServerError as e:
#        error = str(e)
#        
#    return render_template('profile.html', error=error)
#%%
@app.route('/transfer', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
                basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        img = Image.open(file_path)
        img = img.resize((400, 300), Image.ANTIALIAS)
        content_image = np.array(img.getdata()).reshape([300,400,3])
        ##Load images and reshape
        #content_image = scipy.misc.imread(file_path)
        #imshow(content_image)
        content_image = reshape_and_normalize_image(content_image)
        
        result = transfer(style_image, content_image)

        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode
        # result = str(pred_class[0][0][1])               # Convert to string
        return result
    return None            

#%%
@app.route('/customize', methods=['GET', 'POST'])
def customize():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
                basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        
        global style_image
        img = Image.open(file_path)
        img = img.resize((400, 300), Image.ANTIALIAS)
        style_image = np.array(img.getdata()).reshape([300,400,3])
        style_image = reshape_and_normalize_image(style_image)
        return "Style Ready"
    return None   

@app.route('/choose', methods=['GET', 'POST'])
def choose():
    if request.method == 'POST':
        # Get the file from post request
        print(request.data.decode('utf-8'))
        response = requests.get(request.data.decode('utf-8'),verify=False)
        img = Image.open(BytesIO(response.content))
        img = img.resize((400, 300), Image.ANTIALIAS)
        
        global style_image
        style_image = np.array(img.getdata()).reshape([300,400,3])
        style_image = reshape_and_normalize_image(style_image)
        return "Style Ready"
    return None            

#%%
class MyServer(WSGIServer): 
    
    def handle(self, socket, address): 
        socket.settimeout(100000.0) 
        return WSGIServer.handle(self, socket, address) 

if __name__ == '__main__':
    #db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
    #cur = db.cursor()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    server = MyServer(('', 5050), app) 
    server.start() 
    print (server.server_port) 
    gevent.sleep(99999) 
    server.serve_forever() 

