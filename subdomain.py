from argparse import ArgumentParser, FileType
from threading import Thread
from time import time

def prepare_args():
    '''Prepare Arguments

        return:
            args(argparse.Namespace)

    '''
    parser = ArgumentParser(description="Python Based Subdomain Sccanner", usage="%(prog)s google.com", epilog="Example - %(prog)s -w /usr/share/wordlist.txt -t 500 -V google.com")
    parser.add_argument(metavar="Domain", dest="domain", help="Domain Name")
    parser.add_argument("-w","--wordlist",dest="wordlist", metavar="", type = FileType("r"), help="wordlist of subdomains")
    parser.add_argument("t", "--thread", dest="thread", metavar="", type=int, help="threads to use")
    parser.add_argument("-V", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-v", "--version", action="version", help="print version")
    args = parser.parse_args()
    return args
    

if __name__ == "__main__":
    arguments = prepare_args()