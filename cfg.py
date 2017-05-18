'''
HYU CVLAB
Changhee won
04/20/2017
'''

import os
import os.path as osp
import sys

CFG = dict()

CFG['ROOT_DIR'] = osp.abspath('.')
CFG['DATA_DIR'] = osp.join(CFG['ROOT_DIR'], 'data')
CFG['OUT_DIR'] = osp.join(CFG['ROOT_DIR'], 'output') 
CFG['IMG_EXTS'] = ['png', 'jpg']
CFG['DB'] = 'tb50'
CFG['DOWNLOAD_URL'] = "http://cvlab.hanyang.ac.kr/tracker_benchmark/seq_new/{0}.zip"

CFG['LABEL_STEP'] = 5	# imgs
CFG['MOVE_STEP'] = 1	# px
CFG['ASPECT_STEP'] = 3	# px
CFG['ROTATE_STEP'] = 1	# degree
