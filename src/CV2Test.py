# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 10:27:00 2018

@author: 주환
"""

import pylab
import imageio
import glob 
import numpy as np
import cv2

#%%

filename = glob.glob('../data/*.mp4')

#%%
filename

#%%
vid = imageio.get_reader(filename[0],  'ffmpeg')

#%%


cap = cv2.VideoCapture(filename[0])
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

    # Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break
            
#When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# Define the fps to be equal to 10. Also frame size is passed.
 