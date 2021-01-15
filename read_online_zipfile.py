"""Generates data for train/test algorithms"""
from datetime import datetime
from io import StringIO, BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import pickle
import os
import random
import tldextract


# address of online zipfile
file_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

# Our ourput file containg all the training data
DATA_FILE = 'traindata.pkl'

def get_alexa(num, address=file_url, filename='top-1m.csv'):
    """Grabs Alexa 1M"""
    # url = urlopen(address)
    # zipfile = ZipFile(StringIO(url.read()))
    url = urlopen(address)
    zipfile = ZipFile(BytesIO(url.read()))

    return [tldextract.extract(x.split(',')[1]).domain for x in \
            zipfile.read(filename).split()[:num]]


from io import StringIO, BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

if __name__ ==  '__main__':
    file_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    url = urlopen(file_url)
    zipfile = ZipFile(BytesIO(url.read()))        #
    file_name = zipfile.namelist()[0]             # .namelist 结果就会得到这个url 下有多少个文件的list
    for line in zipfile.open(file_name).readlines():
        print(line.decode('utf-8'))               #  这个line就是zipfile 里面保存数据

