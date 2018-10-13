#!/usr/bin/env python

import requests, argparse, os, urlparse, io, time

class Urler(object):
    def __init__(self, url):
        urlparser = urlparse.urlparse(url)
        self.url = url
        self.scheme = urlparser.scheme
        self.netloc = urlparser.netloc
        self.path = os.path.dirname(urlparser.path)[1:]
        self.filename = os.path.basename(urlparser.path)

class Cloner(object):
    def __init__(self):
        self.pathname = ""
        self.headers = {}
        self.urlp = {}
    
    def setSavePath(self, pathname):
        self.pathname = pathname + "/"

    def webParser(self, parserline):
        parserline = parserline.strip()
        if parserline.find(".js") != -1:
            return parserline
        elif parserline.find(".css") != -1:
            return parserline
        else:
            return None

    def getConnect(self, url):
        Response = requests.get(url, headers=self.headers)
        if Response.text != "":
            urler = Urler(url)
            if not os.path.exists(self.pathname + urler.path):
                os.makedirs(self.pathname + urler.path)
            try:
                with io.open(self.pathname + urler.path + "/" + urler.filename, "w", encoding="utf-8") as fwrite:
                    fwrite.write(Response.text)
                    print "[+] Getting file: %s" % url
            except IOError as e:
                print "[-] I/O Error. Permission failed or Disk of full. %s" % e
        
    def getFile(self, filename):
        with open(filename, "r") as targets:
            for target in targets:
                target = self.webParser(target)
                if target != None:
                    self.getConnect(target)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Set file of URL paths.")
    parser.add_argument("path", help="Set path of URL paths to write.")
    args = parser.parse_args()
    if args.file == "":
        print "[-] Please set file of URL paths."
    else:
        cloner = Cloner()
        if args.path != "":
            cloner.setSavePath(args.path)
        cloner.headers = {
            "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0",
            "Accept": "*/*",
            "Cookie": ""
        }
        cloner.getFile(args.file)

if __name__ == '__main__':
    main()

