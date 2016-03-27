#!/usr/bin/env python
#----------------------------------------------------------#
# Written by Mrinal Haloi, NTU, Singapore                  #
# Copyright (c) 2016 Mrinal Haloi                          #
# Licensed under The MIT License [see LICENSE for details] #
#----------------------------------------------------------#

import os
import sys
import subprocess
import re
import math
import argparse

class SplitVideo(object):
    def __init__(self):
        self.length_regexp = 'Duration: (\d{2}):(\d{2}):(\d{2})\.\d+,'
        self.re_length = re.compile(self.length_regexp)


    def getmp4(self, inputfile, outfile):
        os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input = inputfile, output=outfile))
        return

    def getSingleVideo(self, inputfile, outputfile, start, end):
        os.popen("ffmpeg -i '{input}' -ss '{start}' -to '{end}' -c copy '{output}'".format(input = inputfile, start = start, end = end, output = outputfile))

    def splitVideo(self, inputfile, split_length):
        output = subprocess.Popen("ffmpeg -i '"+inputfile+"' 2>&1 | grep 'Duration'", shell = True,stdout = subprocess.PIPE).stdout.read()
        matches = self.re_length.search(output)
        fname, ext = inputfile.rsplit(".", 1)
        if matches:
            video_length = int(matches.group(1)) * 3600 + int(matches.group(2)) * 60 + int(matches.group(3))
            print "Video length in seconds: "+str(video_length)
        else:
            print "Can't determine video length."
            raise SystemExit

        split_count = int(math.ceil(video_length/float(split_length)))
        print split_count
        for i in range(split_count - 1):
            start = i*int(split_length)
            end = (i+1)*int(split_length)
            self.getSingleVideo(inputfile, fname +str(i)+"."+ext , start, end)
         
        start = (split_count - 1)*int(split_length)
        self.getSingleVideo(inputfile, fname + str(split_count - 1)+"."+ext, start, video_length)

def get_args():
    input_args = argparse.ArgumentParser(description="Video Splitting")    

    input_args.add_argument("-f", "--file",
                        dest = "filename",
                        help = "file to split, for example sample.avi or sample.mp4",
                        )
    input_args.add_argument("-s", "--split-size",
                        dest = "split_size",
                        help = "split or chunk size in seconds, for example 90",
                        )

    inputs = input_args.parse_args()
    if inputs.filename and (inputs.split_size != None):
        return inputs

    else:
        input_args.print_help()
        raise SystemExit

if __name__ == '__main__':
    args = get_args()
    split_vid = SplitVideo()
    split_vid.splitVideo(args.filename, args.split_size)
