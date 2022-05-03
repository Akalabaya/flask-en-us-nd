from nsfw_detector import predict
import os
from flask import Flask, redirect, url_for, request
import urllib.request
model = predict.load_model("nsfw_mobilenet2.224x224.h5")
import time
import requests
import base64
from flask_cors import CORS
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
@app.route('/scan')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    if request.method == "GET": 
        url = request.args.get("url")
        fn = str(time.time())
        f = open(fn+'.jpg','wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
        file = os.path.realpath(fn+".jpg")
        prediction = predict.classify(model,file)
        score = (prediction[file]["hentai"]+prediction[file]["porn"]+prediction[file]["sexy"])*100
        print("NSFW SCORE:",score,"%")
        os.remove(fn+'.jpg')
        return "NSFW PREDICTION: "+str(score)+"%"
       
@app.route('/scanurl',methods = ['POST',"GET"])
def login():
   if request.method == 'GET':
      user = request.form['nm']
      return (user)
   else:
      f = request.files['file']
      r = "SAFE PAGE!"
      images = []
      soup = BeautifulSoup(f.read())
      w = 0
      for img in soup.findAll('img'):
            
            if not ( str(img.get('src')).startswith("http://") or str(img.get('src')).startswith("https://")):
                         if str(img.get('src')).startswith("data:image"):
                             pass
                         else:
                            try:
                                print(requests.compat.urljoin(request.args.get('url'),img.get('src')))
                                images.append(requests.compat.urljoin(request.args.get('url'),img.get('src')))
                                fn = str(time.time())
                                f = open(fn+'.jpg','wb')
                                f.write(urllib.request.urlopen(str(requests.compat.urljoin(request.args.get('url'),img.get('src')))).read())
                                f.close()
                                file = os.path.realpath(fn+".jpg")
                                prediction = predict.classify(model,file)
                                score = (prediction[file]["hentai"]+prediction[file]["porn"]+prediction[file]["sexy"])*100
                                print(score,"%")
                                if score > 50:
                                    w += 1
                                    if w > 3:
                                        r = "NSFW FOUND!"
                                        break
                                os.remove(fn+'.jpg')
                            except:
                                pass
                            continue
            else:
                try:
                    images.append(img.get('src'))
                    fn = str(time.time())
                    f = open(fn+'.jpg','wb')
                    f.write(urllib.request.urlopen(str(img.get('src'))).read())
                    f.close()
                    file = os.path.realpath(fn+".jpg")
                    prediction = predict.classify(model,file)
                    score = (prediction[file]["hentai"]+prediction[file]["porn"]+prediction[file]["sexy"])*100
                    print(score,"%")
                    if score > 50:
                        w += 1
                        if w > 3:
                            r = "NSFW FOUND!"
                            break
                    os.remove(fn+'.jpg')
                except:
                    pass
       
      return r
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

