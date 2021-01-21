import argparse

def ror32(v, n):
    return ((v >> n) | (v << (32-n))) & 0xFFFFFFFF

def next_domain(r, c, l, tld):
    domain = ""
    for _ in range(l):
        r = ror32((321167 * r + c) & 0xFFFFFFFF, 16)
        domain += chr( (r & 0x17FF) % 26 + ord('a') )

    # domain += tld
    # print('domain', domain)
    return r, domain

def generate_fobber(version):
    re = []
    if version == 1:
        r = 0xC87C8A78
        c = -1719405398
        l = 17
        tld = '.net'
        nr = 3500
    elif version == 2:
        r = 0x851A3E59
        c = -1916503263
        l = 10
        tld = '.com'
        nr = 3500
    for _ in range(nr):
        # print(_)
        r , domain= next_domain(r, c, l, tld)
        # print('domain in DGA: ', domain)
        re.append(domain)
    return re

# if __name__=="__main__":
#     parser = argparse.ArgumentParser(description="DGA of Fobber")
#     parser.add_argument("version", choices=[1,2], type=int)
#
#     #  will generate 3000 samples
#     fobber_domain_1 = generate_fobber(1)
#     fobber_domain_2 = generate_fobber(2)
#     fobber_domain = fobber_domain_1 + fobber_domain_2
#     print(fobber_domain)
#     print(len(fobber_domain))
