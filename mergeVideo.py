#!/usr/bin/env python
#----------------------------------------------------------#
# Written by Mrinal Haloi, NTU, Singapore                  #
# Copyright (c) 2016 Mrinal Haloi                          #
# Licensed under The MIT License [see LICENSE for details] #
#----------------------------------------------------------#


import numpy as np
import cv2
import os
import argparse

class MergeVideo(object):
    def __init__(self):
        print 'Starting up'
    def mergeVideo(self, video_files):
        num_videos = len(video_files)
        video_index = 0
        cap = cv2.VideoCapture(video_files[0])
        if(cv2.__version__ == '3.0.0'):
            fps_vid = cap.get(cv2.CAP_PROP_FPS)
            fourcc = cap.get(cv2.CAP_PROP_FOURCC)
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            #print 'Total Frame no: {}'.format(cv2.CAP_PROP_FRAME_COUNT)
        else:
            fps_vid = cap.get(cv2.cv.CV_CAP_PROP_FPS)
            fourcc = cap.get(cv2.cv.CV_CAP_PROP_FOURCC)
            width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

        out = cv2.VideoWriter("merged_video.avi", cv2.cv.CV_FOURCC('F','M','P', '4'), int(fps_vid), (int(width), int(height)), 1)

        while(cap.isOpened()):
            ret, frame = cap.read()
            if frame is None:
                print "End of current video " + str(video_index) + " Starting next..."
                video_index += 1
                if video_index >= num_videos:
                     break
                cap = cv2.VideoCapture(video_files[ video_index ])
                ret, frame = cap.read()
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

def get_args():
    input_args = argparse.ArgumentParser(description="Video Merging")

    input_args.add_argument("-f", "--files", dest = "filenames",nargs="*",
                      help = "filles to merge sample1.mp4 sample2.mp4 sample3.mp4i no comma in betwee filenames just space",)

    inputs = input_args.parse_args()
    if inputs.filenames:
        return inputs

    else:
        input_args.print_help()
        raise SystemExit

if __name__ == '__main__':
    args = get_args()
    video_merger = MergeVideo()
    video_merger.mergeVideo(args.filenames)
