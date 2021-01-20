import hashlib
from datetime import datetime, timedelta
import argparse
import random

def generate_morufet(date, key):
    moru_list = []
    for index in range(1500):
        seed = 8*[0]
        seed[0] = ((date.year & 0xFF) + 0x30) & 0xFF
        seed[1] = date.month & 0xFF
        seed[2] = date.day & 0xFF
        seed[3] = 0
        r = (index) & 0xFFFFFFFE
        for i in range(4):
            seed[4+i] = r & 0xFF
            r >>= 7

        seed_str = ""
        for i in range(6):
            k = (key >> (6*(i%4))) & 0xF0 if key else 0
            seed_str += chr((seed[i] ^ k))

        m = hashlib.md5()
        m.update(str(seed_str).encode('utf-8'))
        md5 = m.digest()

        domain = ""
        for m in md5:
            tmp = str((m) & 0xF) + str((m) >> 4) + str('a')
            if tmp <= str('z'):
                domain += str(tmp)

        # tlds = [".biz", ".info", ".org", ".net", ".com"]
        tlds=['']
        for i, tld in enumerate(tlds):
            m = len(tlds) - i
            if not index % m:

                end_point = random.randint(25, len(domain))
                domain = domain[:end_point]
                domain += tld
                # print(len(domain))
                moru_list.append(domain)
                break
        # print(domain)

    return moru_list

# if __name__=="__main__":
#     # known keys:
#     # -k D6D7A4BE
#     # -k DEADC2DE
#     # -k D6D7A4B1
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-d", "--date", help="date for which to generate domains")
#     parser.add_argument("-k", "--key", help="key", default=None)
#     args = parser.parse_args()
#     if args.key:
#         key = int(args.key, 16)
#     else:
#         key = None
#     if args.date:
#         d = datetime.strptime(args.date, "%Y-%m-%d")
#     else:
#         d = datetime.now()
#     # print(d, key)
#
#
#     re_1 = generate_morufet(d, key)
#     re_2 = generate_morufet(d, key=16)
#
#     re = re_1 + re_2
#     print(len(re))