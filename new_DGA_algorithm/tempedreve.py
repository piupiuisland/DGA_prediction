import string
import argparse
from datetime import datetime, timedelta
import random

def rand(r):
    r = (16843009 * r) & 0xFFFFFFFF
    r = (r + 65805) & 0xFFFFFFFF
    return r

def shuffle(letters, seed):
    r = seed
    for j in range(len(letters)):
        i = r % len(letters)
        r = rand(r)
        letters[j], letters[i] = letters[i], letters[j]
    return letters

def generate_tempedreve(d):
    enddate = datetime.strptime("2021-01-11", "%Y-%m-%d")
    while d >= enddate:
        days = days_since_unix_epoch(d)
        seed = (((1664525*days) & 0xFFFFFFFF) + 1013904223) & 0xFFFFFFFF
        tlds = ['.com', '.net', '.org', '.info']
        letters = list(string.ascii_lowercase)
        letters = shuffle(letters, seed)
        length =[seed % 5 +9,seed % 5 +21]
        leng = random.randint(length[0],length[1])
        domain = ""
        r = seed
        for i in range(leng):
            domain += letters[r % len(letters)]
            r = rand(r)
        tld = tlds[seed & 3]
        # domain += tld       # no tld
        d -= timedelta(days=1)
        yield domain

def days_since_unix_epoch(dt):
    return (dt - datetime(1970,1,1)).days

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", help="date for which to generate domains")
    args = parser.parse_args()
    if args.date:
        d = datetime.strptime(args.date, "%Y-%m-%d")
    else:
        d = datetime.now()
    # print(d)

    days = 300
    base = datetime.today()
    date_list = [base - timedelta(days=x) for x in range(days)]
    print(len(date_list))
    re = []
    for d in date_list:
        print(d)
        for domain in generate_tempedreve(d):
            # re += domain
            re.append(domain)
            # print(domain)

    print(re)
    print(len(re))
