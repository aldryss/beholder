import cv2
import json
import pytesseract
import keyboard
import pyautogui
from PIL import Image

import accessible_output2.outputs.auto
      
class GameReader:
    """ Class to read the game screen and output the text to screen reader """  
    
    config = None   #Config file
    camera = None   #Video device
    image = None    #PIL image
    ROI = None      #Region of interest
  
    def __init__(self, configFile = "config.json"):
        self.config = json.load(open('config.json'))
        self.camera = self.config['camera']

    def capture(self, mode): 
        """ Capture the image from the selected mode """
        #@ToDO : Move to config
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        if(mode is "screenshot"):
            image = pyautogui.screenshot()
        else:
            image = self.captureVideoDevice()

        image = image.convert('L')
        image = image.point(lambda x: 0 if x<170 else 255, '1')
        self.image = image

    def captureVideoDevice(self):
        """ Capture the image from the video device """
        return_value, image = self.camera.read()
        self.image = self.CV2PIL(image)
        del(camera)
            
    def crop(self, save = True):
        """ Crop the image to the region of interest """
        img = self.PIL2CV(self.image)
        cv2.imshow('image', img)
        if(self.ROI is None or save == False):
           self.ROI = cv2.selectROI(img)
        imCrop = img[int(self.ROI[1]):int(self.ROI[1]+self.ROI[3]), int(self.ROI[0]):int(self.ROI[0]+self.ROI[2])]
        self.image = self.CV2PIL(imCrop)
        cv2.destroyAllWindows()
    
    def PIL2CV(img):
        """ PIL image to CV2 image """
        return img
      
    def CV2PIL(img):
        """ CV2 image to PIL image """
        return img

    def read(self):
        """ Read the image and output the text to screen reader """
        text = pytesseract.image_to_string(self.CV2PIL(self.image))
        #print(text)
        engine = accessible_output2.outputs.auto.Auto()
        engine.speak(text)


if __name__ == '__main__':
    reader = GameReader()
    while True:
        #Improve with an input mapper, maybe?
        if keyboard.is_pressed('insert'):
            reader.capture("camera")
            reader.crop()
        elif keyboard.is_pressed('end'):
            reader.capture("screenshot")
            reader.crop()
        elif keyboard.is_pressed('home'):
            reader.capture("screenshot")
            reader.crop(False)
        reader.read()