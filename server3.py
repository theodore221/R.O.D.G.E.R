### Server Test Sending

from flask import *
#from selenium import webdriver
#import time
#import urllib
#import urllib2

#url = "172.19.19.204:5000"
#refreshrate = 1
#driver = webdriver.Firefox()
#driver.get("http://"+url)

app = Flask (__name__)
@app.route ("/")
def hello():
    while 1:
        object = raw_input ("Is there an object in the way? ")
        if object == "yes":
            status = "Object Detected"
        else:
            status = "Go for it mateeeee"
        return render_template('hello.html', status = status)
    
