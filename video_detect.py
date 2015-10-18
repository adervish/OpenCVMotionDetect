#!/usr/bin/env python

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import sys
import time

ap = argparse.ArgumentParser("extract frames with motion")
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=200, help="minimum area size")
ap.add_argument("-op", "--output_prefix", default="MOTION", help="output filename prefix")
ap.add_argument("-s", "--show_work", type=str, default=None, help="output filename prefix")

args = vars(ap.parse_args())

print args

if args.get("video", None) is None:
	cap = cv2.VideoCapture(0)
	time.sleep(0.25)
else:
	cap = cv2.VideoCapture(args["video"])

fgbg = cv2.createBackgroundSubtractorMOG2()

output_frame_num = 0
frame_num = 0

fps = cap.get(5) 
if fps == 0:
    fps = 30

print fps

while(True):
    ret, frame = cap.read()

    if ret == False:
        break
        
    frame_num += 1
    # need to resize the image here
    
    small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5 )
    height, width, channels = small.shape
    #print height, width, channels
    
    #cropped = small[10:height-20,10:width-20]
    #cv2.imshow('cropped',cropped)
     
    fgmask = fgbg.apply(small)
    (_, cnts, _) = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

    raw_frame = small.copy()
    
    save_frame = False
    cv2.putText(small, "{file} {frame} {time:003.1f}".format(file=args["video"], frame=frame_num, time=frame_num/fps) , (0,height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
    
    for c in cnts:
        if cv2.contourArea(c) > args["min_area"]:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(small, (x, y), (x + w, y + h), (0, 255, 0), 1 )
            #cv2.rectangle(fgmask, (x, y), (x + w, y + h), (0, 255, 0), 2)
            save_frame = True

    if save_frame:
        output_frame_num += 1
        print "frame {0} {1}".format(output_frame_num, frame_num)
        cv2.imwrite( 'out/%s_%06d.jpg' % (args["output_prefix"], output_frame_num), small)
        cv2.imwrite( 'training/%s_%06d.jpg' % (args["output_prefix"], output_frame_num), raw_frame)
        
            
    if args["show_work"]:
        cv2.imshow('frame',small)
        cv2.imshow('fgmask',fgmask)
    
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

cap.release()
cv2.destroyAllWindows()
