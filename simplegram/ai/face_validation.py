import os
import cv2

path_model = os.path.join(os.getcwd(), 'simplegram/ai/haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier(path_model)

def validation_face(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) >= 1:
        return True
    else:
        return False