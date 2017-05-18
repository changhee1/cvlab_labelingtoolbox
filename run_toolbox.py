'''
HYU CVLAB
Changhee won
04/20/2017
'''

import os
import os.path as osp
import sys

import Tkinter as tk
from PIL import Image, ImageTk

from cfg import CFG
from scripts.toolbox import BBLabelingToolBox

def main(argv):
    dbname = argv[1]
    if not osp.exists(osp.join(CFG['DATA_DIR'], dbname)):
        sys.exit('\'{}\' does not exists.'.format(
            osp.join(CFG['DATA_DIR'], dbname)))
    toolbox = BBLabelingToolBox(dbname)
    toolbox.start()

if __name__ == '__main__':
    main(sys.argv)