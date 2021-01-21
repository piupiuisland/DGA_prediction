import string
import hashlib
import argparse
from datetime import datetime

def generate_chinad(date):
    TLDS = ['.com', '.org', '.net', '.biz', '.info', '.ru', '.cn']
    alphanumeric = string.ascii_lowercase + string.digits

    """
        Chinad generates 1000 domains, but only 256 different domains possible
    """

    ## here 0x1000 will generate 4096 samples;
    for nr in range(0x2000):
        data = "{}{}{}{}".format(
                chr(date.year % 100),
                chr(date.month),
                chr(date.day),
                chr(nr)) + 12*"\x00"

        h = hashlib.sha1(str(data).encode('utf-8')).digest()

        h_le = []
        for i in range(5):
            for j in range(4):
                h_le.append(h[i*4 + (3-j)])

        domain = ""
        for r in h_le[:16]:
            domain += alphanumeric[(r & 0xFF) % len(alphanumeric)]

        r = h_le[-4]
        # domain += TLDS[r % len(TLDS)]
        yield domain

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="gozi dga")
#     parser.add_argument(
#         "-d", "--date", help="date used for seeding, e.g., 2021-01-1",
#         default=datetime.now().strftime('%Y-%m-%d'))
#     args = parser.parse_args()
#
#     ## here will generate 4096 samples;
#     d = datetime.strptime(args.date, "%Y-%m-%d")
#     print(d)
#     l = []
#     l += generate_chinad(d)
#     print(len(l))
#     # for domain in generate_chinad(d):
#     #     print(domain)