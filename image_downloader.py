# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 22:04:56 2015

@author: u
"""

import urllib2
from urllib2 import URLError, HTTPError
import re
import os.path
import sys
import threading
from imgdl_UI1 import Ui_Form


class Img_DLClass(threading.Thread):
    def __init__(self, url,directry):
        super(Img_DLClass, self).__init__()
        self.url = url
        self.lock = threading.Lock()
        self.workdir = self.makedir(directry)
        self.img_pattern = re.compile(r"(https?:\/\/|\/|\/\/)[a-zA-Z0-9-_.~\/:%+#?=\&;]+.(jpg|png|gif|jpeg)")
        self.Atagpattern = re.compile(r"<a.+?>")
        self.imgtagpattern = re.compile(r"<img.+?>")
        self.htmlpattern = re.compile(r"https?:\/\/[a-zA-Z0-9-_.~\/:%+#?=\&;]+")
        self.domain = re.search(r"https?:\/\/[a-zA-Z0-9-_.~:%+#]+", url)
        self.protocol = re.search(r"https?:", url)
        print self.domain.group()
        self.header = {"User-Agent": "Magic Browser"}
        print "取得開始:" + self.url
        
    def __del__(self):
        print "終了:" + self.url
        if not os.path.exists(self.workdir):
            os.rmdir(self.workdir)

    def run(self):
        self.ImgDL()
        

    #urlからHTMLテキスト取得
    def get_html_txt(self, url):
        req = urllib2.Request(url, headers=self.header)
        try:
            fp = urllib2.urlopen(req)
        except HTTPError, e:
            print "-----HTTP Error----\n"
            print "ERROR CODE:", e.code ,e.reason
            sys.exit(1)
        except URLError, e:
            print "----URL Error----\n"
            print "ERROR REASON:", e.reason
            sys.exit(1)
        html = fp.read()
        fp.close()
        return html
    
    #htmlテキストからaタグを検索しリストに
    def iteToList(self, htmltxt):
        list = []
        count = 1
        iterator = self.Atagpattern.finditer(htmltxt)
        for match in iterator:
            list.append(match.group())
            #print count,match.group()
            count += 1
        return list

    def htmltextToimgtagList(self, htmltext):
        list = []
        count = 1
        iterator = self.imgtagpattern.finditer(htmltext)
        for match in iterator:
            list.append(match.group())
            count += 1
        return list
    
    #htmllistからimgurlを取り出しlistへ(mode/1:繰り返す 2:繰り返さない)
    def getImgUrlList(self, urllist, mode=1):
        buf = []
        for str in urllist:
            ite = self.img_pattern.finditer(str)
            for match in ite:
                buf.append(match.group())
                print match.group()
        
        if not buf and mode == 1:
            print mode,"繰り返しモード"
            for str in urllist:
                if str.startswith(self.domain.group()):
                    htmltxt = self.get_html_txt(str)
                    Atags = self.iteToList(htmltxt)
                    imgurls = self.getImgUrlList(Atags, mode=2)
                for url in imgurls:
                    buf.append(url)
        return buf
        
    #aタグの中からurlを抽出    
    def getUrlList(self, ataglist):
        buf = []
        for str in ataglist:
            ite = self.htmlpattern.finditer(str)
            for match in ite:
                buf.append(match.group())
                #print match.group(),2
        return buf
    
    #listから重複する要素を削除andドメイン名の付け加え
    def check_urls(self,list):
        output = []
        for url in list:
            if url.startswith(r"//"):
                url = self.protocol.group() + url
            elif url.startswith(r"/"):
                url = self.domain.group() + url
            if not url in output:
                output.append(url)
        return output
    
    def writeTotxt(self, list, file_name):
        f = open(file_name , "w")
        for str in list:
            f.write(str+"\n")
        f.close
        
    def imgDownload(self, urlList):
        i = 1
        total = len(urlList)
        for url in urlList:
            print str(i) + "/" + str(total) + ":" + url
            i += 1
            req = urllib2.Request(url, headers=self.header)
            try:
                img = urllib2.urlopen(req)
            except HTTPError, e:
                print "-----HTTP Error----\n"
                print "ERROR CODE:", e.code ,e.reason
                #sys.exit(1)
                continue
            except URLError, e:
                print "----URL Error----\n"
                print "ERROR REASON:", e.reason
                #sys.exit(1)
                continue
            localfile = open(self.workdir+"/"+os.path.basename(url)+".jpg", "wb")
            localfile.write(img.read())
            img.close()
            localfile.close()        
    
    def makedir(self, directry):
        if directry == "":
            counter = 1
            while os.path.isdir("/Users/hara/Pictures/img" + str(counter)):
                counter += 1
            else:
                os.mkdir("/Users/hara/Pictures/img" + str(counter))
                return "/Users/hara/Pictures/img" + str(counter)
        else:
            if not os.path.isdir(directry):
                try:
                    os.makedirs(directry)
                except OSError:
                    print "directry error"
                    sys.exit(1)
            return directry                
    
    #######開始
    def ImgDL(self):        
        htmltxt = self.get_html_txt(self.url)
        print htmltxt
        #Atags = self.iteToList(htmltxt)
        #self.listprint(Atags)
        #urls = self.getUrlList(Atags)
        imgtags = self.htmltextToimgtagList(htmltxt)
        self.listprint(imgtags)
        urls = self.check_urls(self.getUrlList(imgtags))
        print "a"
        self.listprint(urls)
        imgurls = self.getImgUrlList(htmltxt,2)
        print "b"
        self.listprint(imgurls)
        imgurls = self.check_urls(imgurls)
        #sys.exit(1)
        print "cSs"
        #self.imgDownload(imgurls)
        self.imgDownload(imgurls)

    def listprint(self, list):
        for youso in list:
            print youso

    if __name__ == "__main__":
        for url in sys.argv[1:]:
            imgdl = Img_DLClass(url,"/Users/hara/Pictures/imgs")
            imgdl.ImgDL()