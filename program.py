from nsfw_detector import predict
import os
from flask import Flask, redirect, url_for, request
model = predict.load_model("nsfw_mobilenet2.224x224.h5")
 
    

app = Flask(__name__)

@app.route('/scan')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    if request.method == "GET": 
        url = request.args.get("url")
        file = os.path.realpath(url)
        prediction = predict.classify(model,file)
        score = (prediction[file]["hentai"]+prediction[file]["porn"]+prediction[file]["sexy"])*100
        print("NSFW SCORE:",score,"%")
        if score <= 50:
            return "NSFW PREDICTION: "+str(score)+"%"
        else:
            return  "NSFW PREDICTION: "+str(score)+"%"
  
# main driver function
if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()

