from ctypes import c_uint
import argparse

class Rand():

    def __init__(self, seed):
        self.r = c_uint(seed)
        self.m = 1103515245
        self.a = 12345

    def rand(self):
        self.r.value = self.r.value*self.m + self.a
        self.r.value &= 0x7FFFFFFF
        return self.r.value


def generate_vawtrak(r):
    length = r.rand()%5 + 7
    domain = ""
    for i in range(length):
        domain += chr(r.rand() % 26 + ord('a'))
    # domain += ".top"
    # print(domain)
    return domain
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", help="e.g. DEADBEEF", default='DEADBEEF')
    args = parser.parse_args()
    r = Rand(int(args.seed, 16))

    re = []
    for nr in range(3000):
        domain = generate_vawtrak(r)
        re.append(domain)
    print(len(re))
    print(re)