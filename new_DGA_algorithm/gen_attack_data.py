from itertools import product
from datetime import datetime
from io import StringIO, BytesIO
import argparse
import random
from collections import namedtuple
from urllib.request import urlopen
from zipfile import ZipFile
import tldextract
import pickle
import os
import numpy as np

from dga_generators_2 import barzarbackdoor, chinad, fobber, fosniw, gozi,\
    momerodwon,morufet,mydoom,nercus, nymaim, pizd, pushdo, qsnatch, ramnit,\
    reconyc, shiotob, tempedreve,vawtrak, vawtrak2, zloader

ALEXA_1M = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

def get_alexa(num_range, address=ALEXA_1M, filename='top-1m.csv'):
    """Grabs Alexa 1M"""
    url = urlopen(address)
    # zipfile = ZipFile(StringIO(url.read()))
    # url = urlopen(address)
    zipfile = ZipFile(BytesIO(url.read()))

    start, end = num_range[0], num_range[1]
    generated_list = [tldextract.extract(x.decode('utf-8').split(',')[1]).domain for x in \
            zipfile.read(filename).split()[start: end]]

    generated_label = ['benign'] * len(generated_list)
    print('length of benign domain: ',len(generated_list),'||', 'length of benign label: ', len(generated_label))

    return generated_list, generated_label


def add_data(domain_l, label_l, add_domain_l, add_label_l):
    assert len(add_domain_l) == len(add_label_l), print('new domains and new labels {} have different length'.
                                                  format(add_label_l[0]))

    # print('{} add {} samples'.format(add_label_l[-1],len(add_label_l)))
    domain_l += add_domain_l
    label_l += add_label_l
    # print('check duplicated: ', len(domain_l), len(set(domain_l)))
    return domain_l, label_l

def generate_some_samples():
    domains = ['ywvghcqe', 'tcwmbd', 'ljhpxtu', 'erxinltmjru', 'qqduvt', 'pzawocbhc', 'mvnmnqp', 'nubpwvzf', 'dkyklbrs', 'jqwhnrb', 'wuynuvxjv', 'bzdxmnx', 'mkbszlcis', 'oostcy', 'uiusnqu', 'mvqqzjugcr', 'krffne', 'qkjcada', 'ycrwbbgvr', 'mqnqyuegaa', 'gmhqczyc', 'agpkvzt', 'bbkalbj', 'trsbay', 'oerjmvbpmc', 'rqycuz', 'uctkcmop', 'gozxcc', 'qhxfwg', 'aebvdvqecdl', 'tvywpjjujqd', 'fqifodmp', 'quzuuu', 'iavlssdol', 'pzwxmmuoz', 'dpzwvfvaum', 'vslmdcehygv', 'mzrgvfutqdn', 'dpohzwcuvo', 'fzpztnuuwqu', 'kmccdp', 'vpznjwl', 'hymwjqeix', 'zehgvvfmef', 'yybpwflpxij', 'zolqvjzvda', 'teslwgcqza', 'zzkhxpjnq',]
    TLDS = ['.com', '.org', '.net', '.biz', '.info', '.ru', '.cn']


    domainss = []
    for i in domains:
        idx = random.randint(0, len(TLDS)-1)
        i += TLDS[idx]
        domainss.append(i)
    print(domainss)
    return domainss


def generate_malig_domains(d, nr):

    domain_all, label_all = [], []

    ## barzarbackdoor
    domain_bb = []
    domain_bb += barzarbackdoor.generate_barzarBackdoor(d)
    label_bb = ['barzarbackdoor'] * len(domain_bb)
    domain_all,label_all = add_data(domain_all,label_all,domain_bb,label_bb)
    # print('barzarbackdoor finished')


    ## chinad
    domain_c = []
    domain_c += chinad.generate_chinad(d)
    label_c = ['chinad'] * len(domain_c)
    domain_all,label_all = add_data(domain_all,label_all,domain_c,label_c)
    # print('chinad finished')


    ## fobber
    domain_f1 = fobber.generate_fobber(1)
    domain_f2 = fobber.generate_fobber(2)
    domain_f = domain_f1 + domain_f2
    label_f = ['fobber'] * len(domain_f)
    domain_all,label_all = add_data(domain_all,label_all,domain_f,label_f)
    # print('fobber finished')


    ## gozi
    domain_g = []
    domain_g += gozi.generate_gozi(d, 'luther')
    label_g = ['gozi'] * len(domain_g)
    # print('fobber finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_g,label_g)


    ## momerodwon
    domain_m = []
    domain_m += momerodwon.generate_momerodwon(d)
    label_m = ['momerodwon'] * len(domain_m)
    # print('momerodwon finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_m,label_m)

    ## morufet
    domain_mo = morufet.generate_morufet(d, key=None, nr=nr)
    label_mo = ['morufet'] * len(domain_mo)
    # print('morufet finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_mo,label_mo)


    ## nercus
    domain_ne = nercus.generate_nercus(nr)
    label_ne = ['nercus'] * len(domain_ne)
    # print('nercus finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_ne,label_ne)


    ## nymaim
    domain_ny = nymaim.generate_nymaim(d, nr)
    label_ny = ['nymaim'] * len(domain_ny)
    # print('nymaim finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_ny,label_ny)

    #
    # ## pizd
    # domain_pi = pizd.generate_pizd(d, nr)
    # label_pi = ['pizd'] * len(domain_pi)
    # # print('pizd finished')
    # domain_all,label_all = add_data(domain_all,label_all,domain_pi,label_pi)
    #

    ## pushdo
    domain_pu1, domain_pu2 = [], []
    domain_pu1 += pushdo.generate_pushdo(d, 'kz_v1')
    domain_pu2 += pushdo.generate_pushdo(d, 'kz_v2')
    domain_pu = domain_pu1 + domain_pu2
    label_pu = ['pushdo'] * len (domain_pu)
    # print('pushdo finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_pu, label_pu)


    ## ramnit
    ramnit_seed = 'E706B455'
    domain_ra = []
    domain_ra += ramnit.generate_ramnit(ramnit_seed, nr, None)
    label_ra = ['ramnit'] * len(domain_ra)
    # print('ramnit finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_ra, label_ra)


    ## reconyc
    reconyc_seed = random.randint(0, 1000 * 3600 * 24)
    domain_re = reconyc.generate_reconyc(reconyc_seed, nr)
    label_re = ['reconyc'] * len(domain_ra)
    # print('reconyc finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_re, label_re)


    ## shiotob
    domain_sh = shiotob.generate_shiotob(nr)
    label_sh = ['shiotob'] * len(domain_ra)
    # print('reconyc finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_sh, label_sh)


    ## vawtrak
    vaw_seed = 'DEADBEEF'
    domain_va = vawtrak.generate_vawtrak(vaw_seed,nr)
    label_va = ['vawtrak'] * len(domain_va)
    # print('vawtrak finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_va, label_va)


    ## vawtrak2
    vaw2_seed = '0x5884c3c4'
    domain_va2 = vawtrak2.generate_vawtrak2(vaw2_seed, nr)
    label_va2 = ['vawtrak2'] * len(domain_va2)
    # print('vawtrak2 finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_va2, label_va2)


    ## zloader
    zloader_seed = zloader.seeding(d,"q23Cud3xsNf3")
    domain_z = zloader.generate_zloader(zloader_seed, nr)
    label_z = ['zloader'] * len(domain_z)
    # print('zloader finished')
    domain_all, label_all = add_data(domain_all, label_all, domain_z, label_z)


    # print(domain_all)
    print('length of malignant domain: ',len(domain_all),'||', 'length of malignant label: ', len(label_all))
    # print(len(set(domain_all)))
    # print(label_all[-1])
    return domain_all, label_all

def shuffle_in_union(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)


def get_data(d,nr,DATA_FILE='saved_data2.pkl'):
    malig_domain, malig_label = generate_malig_domains(d, nr)
    benig_range = [130000, 130000+len(malig_domain)+1500]
    benig_domain, benig_label = get_alexa(benig_range)

    domains =  malig_domain + benig_domain
    labels = malig_label + benig_label
    shuffle_in_union(domains,labels)

    data_and_label = list(zip(domains, labels))
    print('saving data :)')
    pickle.dump(data_and_label, open(DATA_FILE, 'wb'))
    return domains, labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--date", help="date used for seeding, e.g., 2021-01-1",
        default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d")
    nr = 7000

    domains, labels = get_data(d, nr)

    print('DGA data finished', )