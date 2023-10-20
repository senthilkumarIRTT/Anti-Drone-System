import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request
import winsound
from playsound import playsound
from time import sleep

app=Flask(__name__)

model=load_model("dronebird.keras")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        basepath=os.path.dirname(__file__)
        filepath=os.path.join(basepath,'uploads',f.filename)
        f.save(filepath)
        img=image.load_img(filepath,target_size=(150,150))
        img = np.array(img)
        img= img.reshape(1,150,150,3)
        label = model.predict(img)
        class_value = label
        print("Predicted Class (0 - Birds , 1- Drones): ",label)
        print(class_value)
        index =['Birds','Drones']
        if class_value==0:
             text = "Only Birds are identified not drones-don't worry"
             print("Only Birds are identified not drones-don't worry")
        else:
            text = "Drones are identified in your zone- Alert everyone"
            print("Drones are identified in your zone- Alert everyone")
            winsound.PlaySound(r'siren.wav', winsound.SND_ASYNC)
            sleep(10)
            winsound.PlaySound(None, winsound.SND_PURGE)
            winsound.PlaySound(r'voicealert.wav', winsound.SND_ASYNC)
            sleep(20)
            winsound.PlaySound(None, winsound.SND_PURGE)
            
    return text
if __name__=='__main__':
    app.run(debug=False)