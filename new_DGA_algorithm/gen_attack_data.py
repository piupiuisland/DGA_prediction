from itertools import product
from datetime import datetime
import argparse
import random
from collections import namedtuple

from dga_generators_2 import barzarbackdoor, chinad, fobber, fosniw, gozi,\
    momerodwon,morufet,mydoom,nercus, nymaim, pizd, pushdo, qsnatch, ramnit,\
    reconyc, shiotob, tempedreve,vawtrak, vawtrak2, zloader


def add_data(domain_l, label_l, add_domain_l, add_label_l):
    assert len(add_domain_l) == len(add_label_l), print('new domains and new labels {} have different length'.
                                                        format(add_label_l[0]))
    domain_l += add_domain_l
    label_l += add_label_l
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--date", help="date used for seeding, e.g., 2021-01-1",
        default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d")
    nr = 3000
    # print(d)

    domain_all, label_all = [], []

    ## barzarbackdoor
    domain_bb = []
    domain_bb += barzarbackdoor.generate_barzarBackdoor(d)
    label_bb = ['barzarbackdoor'] * len(domain_bb)

    domain_all,label_all = add_data(domain_all,label_all,domain_bb,label_bb)
    print('barzarbackdoor finished')


    ## chinad
    domain_c = []
    domain_c += chinad.generate_chinad(d)
    label_c = ['chinad'] * len(domain_c)

    domain_all,label_all = add_data(domain_all,label_all,domain_c,label_c)
    print('chinad finished')


    ## fobber
    domain_f1 = fobber.generate_fobber(1)
    domain_f2 = fobber.generate_fobber(2)
    domain_f = domain_f1 + domain_f2
    label_f = ['fobber'] * len(domain_f)

    domain_all,label_all = add_data(domain_all,label_all,domain_f,label_f)
    print('fobber finished')


    ## gozi
    domain_g = []
    domain_g += gozi.generate_gozi(d, 'luther')
    label_g = ['gozi'] * len(domain_g)
    print('fobber finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_g,label_g)


    ## momerodwon
    domain_m = []
    domain_m += momerodwon.generate_momerodwon(d)
    label_m = ['momerodwon'] * len(domain_m)
    print('momerodwon finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_m,label_m)

    ## morufet
    domain_mo1 = morufet.generate_morufet(d, key=None)
    domain_mo2 = morufet.generate_morufet(d, key=16)
    domain_mo = domain_mo1 + domain_mo1
    label_mo = ['morufet'] * len(domain_mo)
    print('morufet finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_mo,label_mo)


    ## nercus
    domain_ne = nercus.generate_nercus(nr)
    label_ne = ['nercus'] * len(domain_ne)
    print('nercus finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_ne,label_ne)


    ## nymaim
    domain_ny = nymaim.generate_nymaim(d, nr)
    label_ny = ['nymaim'] * len(domain_ny)
    print('nymaim finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_ny,label_ny)


    ## pizd
    domain_pi = pizd.generate_pizd(d, nr)
    label_pi = ['pizd'] * len(domain_pi)
    print('pizd finished')
    domain_all,label_all = add_data(domain_all,label_all,domain_pi,label_pi)


    ## pushdo

    domain_pu1, domain_pu2 = [], []
    configs = pushdo.get_puConfig()
    parser.add_argument("-c", "--config", default="kz_v1", choices=configs.keys())
    domain_pu1 += pushdo.generate_pushdo(d, 'kz_v1')
    domain_pu2 += pushdo.generate_pushdo(d, 'kz_v2')
    domain_pu = domain_pu1 + domain_pu2
    label_pu = ['pushdo'] * len (domain_pu)
    domain_all, label_all = add_data(domain_all, label_all, domain_pu, label_pu)


    print(domain_all)
    print('length of domain_all: ',len(domain_all),'||', 'length of label_all: ', len(label_all))
    print(label_all[-1])

