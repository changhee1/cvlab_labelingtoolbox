'''
HYU CVLAB
Changhee won
04/20/2017
'''

import os
import os.path as osp
import sys
import urllib2
import zipfile
import shutil
import copy

from cfg import CFG

def download_dataset(dataset):
    file_name = osp.join(CFG['DATA_DIR'], dataset + '.zip')
    url = CFG['DOWNLOAD_URL'].format(dataset)
    download_and_extract_file(url, file_name, CFG['DATA_DIR'])
    macdummy = osp.join(CFG['DATA_DIR'], '__MACOSX')
    if osp.exists(macdummy):
        shutil.rmtree(macdummy)

def download_and_extract_file(url, dst, ext_dst):  
    print 'Connecting to {0} ...'.format(url)
    try:
        u = urllib2.urlopen(url)
    except:
        print 'Cannot download {0} : {1}'.format(
            url.split('/')[-1], sys.exc_info()[1])
        sys.exit(1)
    f = open(dst, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading {0} ({1} Bytes)..".format(url.split('/')[-1], file_size)
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"{0:d} ({1:3.2f}%)".format(
            file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()

    f = open(dst, 'rb')
    z = zipfile.ZipFile(f)
    print '\nExtracting {0}...'.format(url.split('/')[-1])
    z.extractall(ext_dst)
    f.close()
    os.remove(dst)