encoding = 'utf-8'
from typing import Tuple
import hashlib
import sys
import ast

def generate_tf():
    with open('./scripts/new-uid.txt') as f:
        uid_list = f.read().splitlines()
    tf_payload = open('./template/ec2-tf-cdm-template.txt', 'r').read()

    idx = 100
    for uid in uid_list:
        tf_payload2 = tf_payload
        tf_payload2 = tf_payload2.replace("REPLACEUID", uid)
        tf_payload2 = tf_payload2.replace("REPLACEIP", str(arguments['baseip'])+str(idx))
        tf_payload2 = tf_payload2.replace("REPLACEIDX", str(idx))

        tf_payload2 = tf_payload2.replace("REPLACEURL", str(arguments['url']))
        tf_payload2 = tf_payload2.replace("REPLACEAMI", str(arguments['ami']))

        tf_payload2 = tf_payload2.replace("REPLACEENV", str(arguments['env']))

        idx += 1
        print(tf_payload2)
        print("\n\n")

def gen_pass(password: str): # -> Tuple[bytes, bytes]:
    hashed_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(hashed_pwd)

if __name__ == '__main__':
    #gen_pass("fooPass!")
    arguments = ast.literal_eval(sys.argv[1])
    generate_tf()

