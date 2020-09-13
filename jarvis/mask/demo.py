import os
import cv2

BASE = os.path.dirname(os.path.abspath(__file__))
print('\nBase',BASE)
data = BASE.split('\\')[:-1]
print('\n', data)
base = ''

for i in range(len(data)):
    
    if i == 0:
        base = base + data[i]
    else:
        base = base + '\\' + data[i]

    print(base)

print()
'''
phot = '1_8La0TvU.jpg'

imgUrl = os.path.join(base, 'media')
imgUrl = os.path.join(imgUrl, 'images')
imgUrl = os.path.join(imgUrl, phot)

print('\nImgUrl',imgUrl, '\n')


img = cv2.imread(imgUrl)
cv2.imshow('image', img)
cv2.waitKey(0)
'''
#C:\Users\SuSu\Desktop\jarvis\media\images
#c:Users\SuSu\Desktop\jarvis\media\images\1_8La0TvU.jpg
