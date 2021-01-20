import argparse
from ctypes import c_int
import random

# Vawktrak DGA v2
# sample for seed 0x5884c3c4: md5 3868082e4daa93d34a3fe5d7df9d1d72
# sample for seed 0x5542b2:   md5 edfc8653b93c693a51c57caac9e715f7

def prng(r):
    r.value = (1103515245 * r.value + 12345) % 2**31
    return r

def generate_vawtrak2(seed, nr_domains):
    consonants = "cdfghlmnrstw"
    vowels = "aeiou"
    r = c_int(seed)
    re = []
    for n in range(nr_domains):
        r = prng(r)
        length = r.value % 5 + 7
        length_list = [r.value % 5 + 7, r.value % 5 + 23]
        leng = random.randint(length_list[0],length_list[1])
        r = prng(r)
        p = r.value % 2
        domain = ""
        for _ in range(leng):
            r.value = (r.value + 2)
            r = prng(r)
            tmp = r.value
            if p:
                wordlist = consonants
                p -= 1
            else:
                wordlist = vowels
                r = prng(r)
                p = r.value % 2 + 1
            domain += wordlist[tmp % len(wordlist)]
        # domain += ".com"
        # print(domain)
        re.append(domain)
    return re

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", choices = {'0x5542b2', '0x5884c3c4'},
            default=0x5884c3c4, help="seed value")
    parser.add_argument("-n", "--nr", help="nr of domains", default=3000, type=int)
    args = parser.parse_args()
    if type(args.seed) == str:
        seed = int(args.seed, 16)
    else:
        seed = args.seed
    re = generate_vawtrak2(seed, args.nr)
    print(re)
    print(len(set(re)))