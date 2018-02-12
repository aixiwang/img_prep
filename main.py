# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2017-2018, Aixi Wang <aixi.wang@hotmail.com>
#
#=========================================================

import sys
import os.path
import os

import time
import img_utils
from PIL import Image


if len(sys.argv) != 3:
    print "%s input_file output_file" % (sys.argv[0])
    sys.exit()
else:
    input_file = sys.argv[1]
    output_file = sys.argv[2]#

#if not os.path.isfile(input_file):
#    print "No such file '%s'" % input_file
#    sys.exit()



TASK_DURATION = 60

#====================================
# main  
#====================================
if __name__ == "__main__":
    img_utils.do_img_prep(input_file,output_file)
    
