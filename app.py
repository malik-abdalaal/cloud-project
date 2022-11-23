from asyncio.windows_events import NULL
import base64
from ctypes import sizeof
from email import policy
from filecmp import clear_cache
from modulefinder import replacePackageMap
from numbers import Number
from optparse import OptionGroup
import os
from pickle import PUT
from wsgiref.validate import validator
from MySQLdb import NUMBER
from click import Option
from colorama import Cursor
from flask import Config, Flask,render_template, request,send_file, url_for,redirect,flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from jinja2 import MemcachedBytecodeCache, clear_caches
from wtforms import FileField,SubmitField,StringField,validators,SelectField
from werkzeug.utils import secure_filename
import datetime
import numpy as np
from sys import getsizeof
from PIL import Image
from io import BytesIO
import base64
import random
from collections.abc import Callable
from typing import Final, Generic, NamedTuple, ParamSpec, TypeVar
from random import randint
from collections import OrderedDict
from typing import Generic, Hashable, Optional, TypeVar
from collections.abc import Callable
from typing import ParamSpec, TypeVar
import sys
from scheduler import Scheduler
import scheduler.trigger as trigger
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/images/'
mysql = MySQL(app)

mycache = {}
#hit=0
#miss=0
class MemCache:
    
    policy = 1
    capacity = 250
    hit =0
    miss  =0
    #250,000,000
    def allowed_file2(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower()

    def image_cache(file_path):
        ext =  MemCache.allowed_file2(file_path)
        prefix = f'data:data:image/{ext};base64,'
        with open(file_path, 'rb') as f:
            img = f.read()
        x = prefix + base64.b64encode(img).decode('utf-8')
        return x

    def refreshConfiguration():
        cursor = mysql.connection.cursor()
        MemCache.capacity = cursor.execute('SELECT capacity FROM cache WHERE id = 2 ')
        MemCache.policy = cursor.execute('SELECT policy FROM cache WHERE id = 2 ')
        mysql.connection.commit()
        cursor.close()
    
        
    def PUT(key,file):
        MemCache.refreshConfiguration() 
        image = file
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT direction FROM uploadedfiles WHERE uniquekeys = '{}' '''.format(key))
        path = cursor.fetchall()   
        mysql.connection.commit()
        
        cursor.close()
        
        ext =  MemCache.allowed_file2(path[0][0])
        data = f'data:data:image/{ext};base64,'
        with open(path[0][0],'rb') as f:
            picture = f.read()
        z = data + base64.b64encode(picture).decode('utf-8')
        mycache[key] = z
        MemCache.fixMemCache(key)
        mycache[key] = z  
        

            
    def fixMemCache():
        if getsizeof(mycache) > (MemCache.capacity*1000000):
            if (len(mycache)>1):
                mycache.popitem()     
            while(getsizeof(mycache) > (MemCache.capacity*1000000)):
                if policy == '2':
                    i = randint(0 , len(mycache) - 1)
                    del mycache[list(mycache)[i]]
                else:
                    del mycache[next(iter(mycache))]


    def GET(key):
        if key not in mycache:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT direction FROM uploadedfiles WHERE uniquekeys = %s',(key))
            mysql.connection.commit()
            cursor.close()
        else:
            mycache.move_to_end(key)
            return mycache[key]
        

    def CLEAR():
        mycache.clear()
        MemCache.hit =0
        MemCache.miss = 0

    def invalidateKey():

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT policy FROM cache WHERE id = 2')
        mysql.connection.commit()
        cursor.close()

        if(cursor == 2):
            mycache.pop(random.choice(mycache.keys()))
        else:
            mycache.popitem()

        
        #del mycache[key]
    def plushit():
        MemCache.hit +=1
        return (MemCache.hit)+1
    
    def plusmiss():
        MemCache.miss +=1
        return (MemCache.miss)+1

    def gethit():
        return MemCache.hit
    def getmiss():
        return MemCache.miss

    def setcapacity(capacity):
        MemCache.capacity = capacity
    
    def setpolicy(policy):
        MemCache.policy = policy

    def fixMemCache(z):
        if getsizeof(mycache)+getsizeof(z) > (MemCache.capacity*1000000):#*1000000
            if (len(mycache)>1):
                mycache.popitem()
            while(getsizeof(mycache) > (MemCache.capacity*1000000)):
                if policy == '2':
                    i = randint(0 , len(mycache) - 1)
                    del mycache[list(mycache)[i]]
                else:
                    del mycache[next(iter(mycache))]

    
    
      
class UploadFileForm(FlaskForm):
    uniquekey = StringField('uniquekey', validators=[validators.input_required()])
    file = FileField("File", validators=[validators.input_required()])
    submit = SubmitField("Upload")

class GetKey(FlaskForm):
    uniquekey = StringField('uniquekey',validators=[validators.input_required()])
    submit = SubmitField("Get Image")
    
class Configration(FlaskForm):
    size = StringField('size', validators=[validators.input_required()])
    submit = SubmitField("Submit")
    clear = SubmitField('Clear')
    
@app.route('/', methods = ['GET', 'POST'])
@app.route("/uploadImage" , methods = ['GET', 'POST'])
def uploadImage():
    
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filedirection = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
        cursor = mysql.connection.cursor()
        uniquekey = form.uniquekey.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        mysql.connection.commit()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM uploadedfiles')     
        records = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        ts = datetime.datetime.now()
        for key in records:
            if key[0] == uniquekey:
                
                path = key[1]
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE uploadedfiles SET direction = %s WHERE uniquekeys = %s',(filedirection,uniquekey))
                cursor.execute('UPDATE uploadedfiles SET updated_at = %s WHERE uniquekeys = %s',(ts,uniquekey))
                cursor.execute('''SELECT * FROM uploadedfiles''')
                newrecord = cursor.fetchall()
                mysql.connection.commit()
                cursor.close()  
                flag = True
                for value in newrecord:
                    if value[1] == path:
                        flag = False
                        break
                if flag == True:
                    os.remove(path)
    
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO uploadedfiles VALUES(%s,%s,%s,%s)''',(uniquekey,filedirection,ts,ts))
        mysql.connection.commit()
        cursor.close()
        MemCache.PUT(uniquekey,file)
    return render_template(
        "uploadImage.html",
        form = form     
    )
     

@app.route("/getImage", methods = ['GET', 'POST'])
def getImage():
    
    form = GetKey()
    if form.validate_on_submit():
        
        uniquekey = form.uniquekey.data
        if(mycache.get(uniquekey) != None):
            image = mycache[uniquekey]
            MemCache.plushit()
            print('from cache')
            return render_template(
                    "getImage.html",
                    form = form,
                    image = image     
            )
        else:
            print('from datatbase')
            MemCache.plusmiss()
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM uploadedfiles")
            records = cursor.fetchall()
            mysql.connection.commit()
            cursor.close() 
            flag = True
            for row in records:
                if row[0] == uniquekey:
                    cursor = mysql.connection.cursor()
                    cursor.execute('''SELECT direction FROM uploadedfiles WHERE uniquekeys = '{}' '''.format(uniquekey))
                    image = cursor.fetchall()
                    mysql.connection.commit()
                    cursor.close()
                    file = MemCache.image_cache(image[0][0])
                    MemCache.PUT(uniquekey,file)
                    return render_template(
                        "getImage.html",
                        form = form,
                        image = image[0][0]
                    )
                else:
                    flag = False
            mysql.connection.commit()
            cursor.close() 
            error = None
            if (flag == False):
                error = 'the key was not found'
                
                return render_template(
                    "getImage.html",
                    error = error,
                    form = form
    )     
    else:
        return render_template(
        "getImage.html",
         form = form   
    )
 

@app.route("/allKeys")
def allKeys():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM `uploadedfiles`")
    records = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    return render_template(
        "allKeys.html",
        len = len(records),
        records = records
    )

@app.route("/configration", methods = ['GET', 'POST'])
def configration():
    form = Configration()
    if form.validate_on_submit():
        size = form.size.data
        policy = request.form['policy']
        MemCache.setcapacity(size)
        MemCache.setpolicy(policy)
        MemCache.fixMemCache()
        cursor = mysql.connection.cursor()
        cursor.execute('''UPDATE cache SET capacity = {} , policy = {} WHERE id = 2; '''.format(size,policy))
        mysql.connection.commit()
        cursor.close()
    return render_template(
        "configration.html",
        form = form
    )

@app.route("/statistics")
def statistics():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT capacity FROM cache WHERE id = 2 ')
    capacity = cursor.fetchall()
    cursor.execute('SELECT policy FROM cache WHERE id = 2 ')
    policykinds = cursor.fetchall()
    policytype = policykinds[0][0]
    cursor.execute('''SELECT name FROM cacheinformation WHERE id = '{}' '''.format(policytype))
    policy = policykinds = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    
    if(MemCache.hit == 0 & MemCache.miss ==0):
        missrate = 0
        hitrate = 0
        #interval_task()
        return render_template(
        "statistics.html",
        number_of_images = len(mycache),
        hitrate = 0,
        missrate = 0,
        capacity = capacity[0][0],
        policy = policy[0][0]
    )
    else:

        hitrate = (MemCache.hit/(MemCache.hit+MemCache.miss))*100
        missrate = (MemCache.miss/(MemCache.hit+MemCache.miss))*100
        #interval_task()
    return render_template(
        "statistics.html",
        number_of_images = len(mycache),
        hitrate = hitrate,
        missrate = missrate,
        capacity = capacity[0][0],
        policy = policy[0][0]
        

        # Cache_Capacity = Cache_Capacity
    )
@app.route('/clear')
def clear():
  try:
    
    MemCache.CLEAR()
    
    return redirect('/configration')
  except:
    flash('Error')
    return redirect('/configration')  
       
# def interval_task():
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT capacity FROM cache WHERE id = 2 ')
#     capacity = cursor.fetchall()
   
#     if(MemCache.hit == 0 & MemCache.miss ==0):
#         missrate = 0
#         hitrate = 0
        
#         with app.app_context():
             
            
#             ts = datetime.datetime.now()
#             cursor = mysql.connection.cursor()
#             cursor.execute(''' INSERT INTO statistics VALUES(%s,%s,%s,%s,%s,%s,%s)''',(0,missrate,hitrate,len(mycache),capacity[0][0],(MemCache.hit+MemCache.miss),ts))
#             mysql.connection.commit()
#             cursor.close()
#     else:
#         hitrate = (MemCache.hit/(MemCache.hit+MemCache.miss))*100
#         missrate = (MemCache.miss/(MemCache.hit+MemCache.miss))*100
#         with app.app_context():
#             cursor = mysql.connection.cursor()
#             cursor.execute('SELECT capacity FROM cache WHERE id = 2 ')
#             cursor.close()
#             ts = datetime.datetime.now()
#             cursor = mysql.connection.cursor()
#             cursor.execute(''' INSERT INTO statistics VALUES(%s,%s,%s,%s,%s,%s,%s)''',(0,missrate,hitrate,len(mycache),capacity[0][0],(MemCache.hit+MemCache.miss),ts))
#             mysql.connection.commit()
#             cursor.close()
# Changes = {}
# def delay_Mins():
    
#     with app.app_context():
#         cursor = mysql.connection.cursor()
#         cursor.execute(''' Select MissRate from statistics ''')
#         rows = cursor.fetchall()
#         for i in rows:
#             Changes[0] = i[0]

#         cursor = mysql.connection.cursor()
#         cursor.execute(''' Select HitRate from statistics ''')
#         rows = cursor.fetchall()
#         for i in rows:
#             Changes[1] = i[0]

#         cursor = mysql.connection.cursor()
#         cursor.execute(''' Select NumberOfItems from statistics ''')
#         rows = cursor.fetchall()
#         for i in rows:
#             Changes[2] = i[0]

#         cursor = mysql.connection.cursor()
#         cursor.execute(''' Select CacheCapacity from statistics ''')
#         rows = cursor.fetchall()
#         for i in rows:
#             Changes[3] = i[0]

#         cursor.execute(''' Select NumberOfReq from statistics ''')
#         rows = cursor.fetchall()
#         for i in rows:
#             Changes[4] = i[0]
# #scheduler.add_job(func=interval_task, trigger="interval", seconds=5)
# #scheduler.add_job(func=delay_Mins, trigger="interval", minutes=10)





