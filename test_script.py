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

def main():
    test_data_length()

def test_data_length():
    dblistfile = osp.join(CFG['DATA_DIR'], CFG['DB'] + '.txt')
    total = 0
    with open(dblistfile) as f:
        dblist = f.readlines()
        dbnames = sorted([x.split('\t')[0].strip() for x in dblist])
        for db in dbnames:
            img_dir = osp.join(CFG['DATA_DIR'], db, 'img')
            img_path = [f for f in os.listdir(img_dir) if any(
                f.endswith(ext) for ext in CFG['IMG_EXTS'])]
            print '{} : {} images.'.format(db, len(img_path))
            total += len(img_path)
    print '* total {} images. for {} datasets'.format(total, len(dbnames))

if __name__ == "__main__":
    main()