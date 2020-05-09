import glob
import cv2
import time

mp4_files = sorted(glob.glob('../videos/*.mp4'))

# https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(mp4_files[0])

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == True:
        cv2.imshow('Frame',frame)
        time.sleep(0.01)
        
        
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    else: 
        break

cap.release()

# Closes all the frames
cv2.destroyAllWindows()
