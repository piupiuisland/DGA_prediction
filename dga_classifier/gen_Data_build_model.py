"""Generates data for train/test algorithms"""
from datetime import datetime
from io import StringIO, BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import pickle
import os
import random
import tldextract
import numpy as np
from tensorflow.keras.preprocessing import sequence


from dga_classifier.dga_generators import banjori, corebot, cryptolocker, \
    dircrypt, kraken, lockyv2, pykspa, qakbot, ramdo, ramnit, simda

# Location of Alexa 1M
ALEXA_1M = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

# Our ourput file containg all the training data
DATA_FILE = 'traindata.pkl'


def get_alexa(num, address=ALEXA_1M, filename='top-1m.csv'):
    """Grabs Alexa 1M"""
    url = urlopen(address)
    # zipfile = ZipFile(StringIO(url.read()))
    # url = urlopen(address)
    zipfile = ZipFile(BytesIO(url.read()))

    generated_list = [tldextract.extract(x.decode('utf-8').split(',')[1]) for x in \
            zipfile.read(filename).split()[:num]]

    generated_label = ['benign'] * len(generated_list)
    return generated_list, generated_label

def gen_malicious(num_per_dga=10000):
    """Generates num_per_dga of each DGA"""
    domains = []
    labels = []

    # We use some arbitrary seeds to create domains with banjori
    banjori_seeds = ['somestring', 'firetruck', 'bulldozer', 'airplane', 'racecar',
                     'apartment', 'laptop', 'laptopcomp', 'malwareisbad', 'crazytrain',
                     'thepolice', 'fivemonkeys', 'hockey', 'football', 'baseball',
                     'basketball', 'trackandfield', 'fieldhockey', 'softball', 'redferrari',
                     'blackcheverolet', 'yellowelcamino', 'blueporsche', 'redfordf150',
                     'purplebmw330i', 'subarulegacy', 'hondacivic', 'toyotaprius',
                     'sidewalk', 'pavement', 'stopsign', 'trafficlight', 'turnlane',
                     'passinglane', 'trafficjam', 'airport', 'runway', 'baggageclaim',
                     'passengerjet', 'delta1008', 'american765', 'united8765', 'southwest3456',
                     'albuquerque', 'sanfrancisco', 'sandiego', 'losangeles', 'newyork',
                     'atlanta', 'portland', 'seattle', 'washingtondc']
    # banjori_seeds = ['somestring',
    #                  'firetruck', 'bulldozer', 'airplane', 'racecar',
                     # 'apartment', 'laptop', 'laptopcomp', 'malwareisbad', 'crazytrain',
                     # 'thepolice', 'fivemonkeys', 'hockey', 'football', 'baseball',
                     # 'basketball', 'trackandfield', 'fieldhockey', 'softball', 'redferrari',
                     # 'blackcheverolet', 'yellowelcamino', 'blueporsche', 'redfordf150',
                     # 'purplebmw330i', 'subarulegacy', 'hondacivic', 'toyotaprius',
                     # 'sidewalk', 'pavement', 'stopsign', 'trafficlight', 'turnlane',
                     # 'passinglane', 'trafficjam', 'airport', 'runway', 'baggageclaim',
                     # 'passengerjet', 'delta1008', 'american765', 'united8765', 'southwest3456',
                     # 'albuquerque', 'sanfrancisco', 'sandiego', 'losangeles', 'newyork',
                     # 'atlanta', 'portland', 'seattle', 'washingtondc'
                     # ]

    segs_size = max(1, num_per_dga/len(banjori_seeds))
    segs_size = int(segs_size)
    assert isinstance(segs_size, int), 'expect nr_domain is a int, get{}'.format(type(segs_size))
    for banjori_seed in banjori_seeds:
        domains += banjori.generate_domains(segs_size, banjori_seed)
        labels += ['banjori']*segs_size

    # print('num_per_dga',num_per_dga)
    domains += corebot.generate_domains(num_per_dga)
    labels += ['corebot']*num_per_dga

    # Create different length domains using cryptolocker
    crypto_lengths = range(8, 32)
    segs_size = max(1, num_per_dga/len(crypto_lengths))
    segs_size = int(segs_size)
    assert isinstance(segs_size, int), 'expect nr_domain is a int, get{}'.format(type(segs_size))

    for crypto_length in crypto_lengths:
        domains += cryptolocker.generate_domains(segs_size,
                                                 seed_num=random.randint(1, 1000000),
                                                 length=crypto_length)
        labels += ['cryptolocker']*segs_size

    domains += dircrypt.generate_domains(num_per_dga)
    labels += ['dircrypt']*num_per_dga

    # generate kraken and divide between configs
    kraken_to_gen = max(1, num_per_dga/2)
    kraken_to_gen = int(kraken_to_gen)
    domains += kraken.generate_domains(kraken_to_gen, datetime(2016, 1, 1), 'a', 3)
    labels += ['kraken']*kraken_to_gen
    domains += kraken.generate_domains(kraken_to_gen, datetime(2016, 1, 1), 'b', 3)
    labels += ['kraken']*kraken_to_gen

    # generate locky and divide between configs
    locky_gen = max(1, num_per_dga/11)
    locky_gen  =  int(locky_gen)
    for i in range(1, 12):
        domains += lockyv2.generate_domains(locky_gen, config=i)
        labels += ['locky']*locky_gen

    # Generate pyskpa domains
    domains += pykspa.generate_domains(num_per_dga, datetime(2016, 1, 1))
    labels += ['pykspa']*num_per_dga

    # Generate qakbot
    domains += qakbot.generate_domains(num_per_dga, tlds=[])
    labels += ['qakbot']*num_per_dga

    # ramdo divided over different lengths
    ramdo_lengths = range(8, 32)
    segs_size = max(1, num_per_dga/len(ramdo_lengths))
    segs_size = int(segs_size)
    for rammdo_length in ramdo_lengths:
        domains += ramdo.generate_domains(segs_size,
                                          seed_num=random.randint(1, 1000000),
                                          length=rammdo_length)
        labels += ['ramdo']*segs_size

    # ramnit
    domains += ramnit.generate_domains(num_per_dga, 0x123abc12)
    labels += ['ramnit']*num_per_dga

    # simda
    simda_lengths = range(8, 32)
    segs_size = max(1, num_per_dga/len(simda_lengths))
    segs_size = int(segs_size)
    for simda_length in range(len(simda_lengths)):
        domains += simda.generate_domains(segs_size,
                                          length=simda_length,
                                          tld=None,
                                          base=random.randint(2, 2**32))
        labels += ['simda']*segs_size


    return domains, labels

def shuffle_in_union(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)


def gen_data(force=False):
    """Grab all data for train/test and save

    force:If true overwrite, else skip if file
          already exists
    """
    if force or (not os.path.isfile(DATA_FILE)):
        domains, labels = gen_malicious(10000)
        print('num of domain data and label:  ', len(domains), len(labels))
        # Get equal number of benign/malicious

        alexa_data, alexa_label = get_alexa(len(domains))
        domains += alexa_data
        labels  += alexa_label

        domains, labels = np.array(domains), np.array(labels)
        shuffle_in_union(domains,labels)
        domains, labels = domains.tolist(),labels.tolist()

        data_and_label = list(zip(labels, domains))
        print('gen_data finished :)')
        pickle.dump(data_and_label, open(DATA_FILE, 'wb'))


def get_data(force=False):
    """Returns data and labels"""
    gen_data(force)

    return pickle.load(open(DATA_FILE,'rb'))



if __name__ ==  '__main__':
    # domains, labels = gen_malicious(10000)
    # assert (len(domains) == len(labels)), print('get different amount of data and labels')
    #
    # indata = get_data()

    get_alexa(1000)

    # gen_data =  pickle.load(open(DATA_FILE,'rb'))
    # indata = gen_data
    #
    # print('DGA load finished')
    # print('DGA load finished')
    #
    # X = [x[1] for x in indata]
    # labels = [x[0] for x in indata]
    #
    # # Generate a dictionary of valid characters
    # valid_chars = {x:idx+1 for idx, x in enumerate(set(''.join(X)))}
    #
    # max_features = len(valid_chars) + 1
    # maxlen = np.max([len(x) for x in X])
    #
    # # Convert characters to int and pad
    # X = [[valid_chars[y] for y in x] for x in X]
    # X = sequence.pad_sequences(X, maxlen=maxlen)
    #
    # # Convert labels to 0-1
    # y = [0 if x == 'benign' else 1 for x in labels]
    #
    # print('data preprocessing finished')
    #
    #
    # data_and_label = list(zip(labels, domains))
    # pickle.dump(data_and_label, open('saved_data.pkl', 'wb'))
    # read_data = pickle.load(open(DATA_FILE,'rb'))