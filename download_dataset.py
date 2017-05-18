'''
HYU CVLAB
Changhee won
04/20/2017
'''

import os
import os.path as osp
import sys

from cfg import CFG
from scripts.utils.download import download_dataset

def main():
    dblistfile = osp.join(CFG['DATA_DIR'], CFG['DB'] + '.txt')
    with open(dblistfile) as f:
        dblist = f.readlines()
        dbnames = sorted([x.split('\t')[0].strip() for x in dblist])
        for db in dbnames:
            img_dir = osp.join(CFG['DATA_DIR'], db, 'img')
            if not osp.exists(img_dir):
                download_dataset(db)


if __name__ == "__main__":
    main()