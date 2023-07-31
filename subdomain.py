#!/usr/bin/python3
from argparse import ArgumentParser, FileType
from threading import Thread, Lock
from time import time
from requests import get, exceptions

subdomains = []
words = []
lock = Lock()

def prepare_args():
    '''Prepare Arguments

        return:
            args(argparse.Namespace)

    '''
    parser = ArgumentParser(description="Python Based Subdomain Scanner", usage="%(prog)s google.com", epilog="Example - %(prog)s -w /usr/share/wordlist.txt -t 500 -V google.com")
    parser.add_argument(metavar="Domain", dest="domain", help="Domain Name")
    parser.add_argument("-w","--wordlist",dest="wordlist", metavar="", type = FileType("r"), help="wordlist of subdomains", default="wordlist.txt")
    parser.add_argument("-t", "--threads", dest="threads", metavar="", type=int, help="threads to use", default = 500)
    parser.add_argument("-V", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-v", "--version", action="version", help="print version", version="%(prog)s 1.0")
    args = parser.parse_args()
    return args

def prepare_words(wordlist_file):
    """generate wordlist"""
    with open(wordlist_file, "r") as file:
        global words
        words = file.read().split()

def get_next_word():
    with lock:
        if words:
            return words.pop(0)
        else:
            return None

def check_subdomain(domain):
    """check subdomain for 200"""

    while True:
        word = get_next_word()
        if word is None:
            break

        try:
            url = f"https://{word}.{domain}"
            request = get(url, timeout=5, allow_redirects=False)  # Limit redirects
            if request.status_code == 200:
                subdomains.append(url)
                if arguments.verbose:
                    print(url)

        except (exceptions.ConnectionError, exceptions.ReadTimeout):
            continue
        
        except StopIteration:
            break
    
def prepare_threads(domain):
    
    thread_list = []
    
    for i in range(arguments.threads):
        thread_list.append(Thread(target=check_subdomain, args=(domain,)))

    for thread in thread_list:
        thread.start()
    
    for thread in thread_list:
        thread.join()
    

if __name__ == "__main__":
    arguments = prepare_args()
    prepare_words(arguments.wordlist.name)
    start_time = time()
    prepare_threads(arguments.domain)
    end_time = time()
    print("Sub Domains Found - \n", "\n".join(i for i in subdomains))
    print(f"Time Taken: {round(end_time-start_time,2)}")