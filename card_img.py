"""
Card Recognition using OpenCV
Code from the blog post 
http://arnab.org/blog/so-i-suck-24-automating-card-games-using-opencv-and-python

Usage: 

  ./card_img.py filename num_cards training_image_filename training_labels_filename num_training_cards

Example:
  ./card_img.py test.JPG 4 train.png train.tsv 56
  
Note: The recognition method is not very robust; please see SIFT / SURF for a good algorithm.  

"""

import sys
import numpy as np
sys.path.insert(0, "/usr/local/lib/python2.7/site-packages/") 
import cv2
import time


###############################################################################
# Utility code from 
# http://git.io/vGi60A
# Thanks to author of the sudoku example for the wonderful blog posts!
###############################################################################

def rectify(h):
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)

  add = h.sum(1)
  hnew[0] = h[np.argmin(add)]
  hnew[2] = h[np.argmax(add)]
   
  diff = np.diff(h,axis = 1)
  hnew[1] = h[np.argmin(diff)]
  hnew[3] = h[np.argmax(diff)]

  return hnew

###############################################################################
# Image Matching
###############################################################################
def preprocess(img):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  return gray
  
def imgdiff(img1,img2):
  return (cv2.matchTemplate(img2.astype(np.float32), img1.astype(np.float32), cv2.TM_CCOEFF_NORMED) * 100).astype(int)

def find_closest_card(training,img):
  features = preprocess(img)
  return sorted(training.values(), key=lambda x: 1 - imgdiff(x[1],features))[0][0]
  

def contour_area(contour):
  area = cv2.contourArea(contour)
  #print area
  return area
   
###############################################################################
# Card Extraction
###############################################################################  
def getCards(im, numcards=4, isTrain = True):
  gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(1,1),1000)
  flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY) 
       
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  #cv2.imshow('image',im)
  #cv2.waitKey(0) 

  contours = sorted(contours, key=contour_area, reverse=True)[:numcards]  

  idx = 0
  for card in contours:
    peri = cv2.arcLength(card,True)
    approx = rectify(cv2.approxPolyDP(card,0.02*peri,True))

    #box = np.int0(approx)
    #cv2.drawContours(im,[box],0,(255,255,0),6)
    #imx = cv2.resize(im,(1000,600))
    #cv2.imshow('a',imx)      
    #cv2.waitKey(0)
    
    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)

    transform = cv2.getPerspectiveTransform(approx,h)
    warp = cv2.warpPerspective(im,transform,(450,450))
    
    if not isTrain:
      cv2.imwrite("capture_processed.jpg", warp)

    idx = idx + 1

    yield warp


def get_training(training_labels_filename,training_image_filename,num_training_cards,avoid_cards=None):
  training = {}
  
  labels = {}
  for line in file(training_labels_filename): 
    key, num, suit = line.strip().split()
    labels[int(key)] = (num,suit)
    
  print "Training"

  im = cv2.imread(training_image_filename)
  for i,c in enumerate(getCards(im,num_training_cards)):
    if avoid_cards is None or (labels[i][0] not in avoid_cards[0] and labels[i][1] not in avoid_cards[1]):
      training[i] = (labels[i], preprocess(c))
  
  print "Done training"
  return training  

def setup():
  global training
  training = get_training('chip_train_1.tsv','chip_train_1.jpg',52)
  global cam
  cam = cv2.VideoCapture(0)

def get_cards(num_cards):
  frame = {}
  for x in range(1,10):
    ret, frame = cam.read()
  cv2.imwrite("capture.jpg", frame)
  

  try:
    #frame = cv2.transpose(frame)
    #frame = cv2.flip(frame,1)
    #cv2.imshow(";fsdf", frame)
    #cv2.waitKey(0)
    cards = [find_closest_card(training, c) for c in getCards(frame, num_cards, False)]
        
    if cards.count > 0:
      print cards
    return cards
  except:
    return []

if __name__ == '__main__':

  if len(sys.argv) == 6:
    filename = sys.argv[1]
    num_cards = int(sys.argv[2])
    training_image_filename = sys.argv[3]
    training_labels_filename = sys.argv[4]    
    num_training_cards = int(sys.argv[5])
    
    training = get_training(training_labels_filename,training_image_filename,num_training_cards)

    #width = im.shape[0]
    #height = im.shape[1]
    #if width < height:
    #  im = cv2.transpose(im)
    #  im = cv2.flip(im,1)

    # Debug: uncomment to see registered images
    #for i,c in enumerate(getCards(im,num_cards)):
    #  card = find_closest_card(training,c,)
    #  cv2.imshow(str(card),c)
    #cv2.waitKey(0) 
    
    cam = cv2.VideoCapture(1)

    while True:
      ret, frame = cam.read()   

      try:
        #frame = cv2.transpose(frame)
        #frame = cv2.flip(frame,1)
        #cv2.imshow(";fsdf", frame)
        #cv2.waitKey(0)
        cards = [find_closest_card(training, c) for c in getCards(frame, num_cards, False)]
           
        if cards.count > 0:
          print cards
      except:
        pass
      #time.sleep(1)
    
  else:
    print __doc__
