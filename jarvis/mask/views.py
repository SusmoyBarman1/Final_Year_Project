from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .models import User

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import mtcnn

BASE = os.path.dirname(os.path.abspath(__file__))
data = BASE.split('\\')[:-1]
base = ''

for i in range(len(data)):  
    if i == 0:
        base = base + data[i]
    else:
        base = base + '\\' + data[i]


#maskImgSaveRoot = base + '\\mask\\' + 'maskImg'


def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1, y1), (x2, y2)


face_detector = mtcnn.MTCNN()

# Create your views here.
def mask(request):
    return render(request, 'mask/mask.html')

def maskRecognize(img, model):

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_detector.detect_faces(img_rgb)

    maskcheck = 'No Mask'
    
    for res in results:
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        check = False
        name = 'No mask'
    
        if res['confidence'] > .9:
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = np.array(face, dtype="float32")
            face = np.expand_dims(face, axis=0)
            val = model.predict(face)[0]
            if val > .5:
                check = True
                name = 'Mask'
                maskcheck = name
        
            #print(face.shape)
    
        
        if check:        
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    return img, maskcheck

def maskUpload(request):
    
    photo = request.FILES['image']
    user = User(pic = photo)
    user.save()
    photo = user.pic

    maskModel = load_model('./mask/mask_no_mask.h5')

    photoUrl = photo.url
    phot = photoUrl.split('/')[-1]
    photMask = 'mask' + phot

    
    imgUrl = os.path.join(base, 'media')
    imgUrl = os.path.join(imgUrl, 'images')

    photoPath = os.path.join(imgUrl, photMask)
    imgUrl = os.path.join(imgUrl, phot)


    img = cv2.imread(imgUrl)
    frame, maskcheck = maskRecognize(img, maskModel)

    cv2.imwrite(photoPath, frame)

    imgRead = '/media/images/mask' + phot
    #print('\n\n\n\n check:', maskcheck,'\n\n\n\n')

    return render(request, 'mask/result.html', {'pic': imgRead, 'check': maskcheck})