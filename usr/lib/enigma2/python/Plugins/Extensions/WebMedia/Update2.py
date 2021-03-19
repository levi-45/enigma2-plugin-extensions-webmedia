import os, re
from urllib2 import urlopen
from twisted.web.client import getPage, downloadPage
from enigma import addFont 
############20171004##########################
THISPLUG = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia"
HOSTS = ["allvid", "cloudy", "daclips", "exashare", "filebox", "filehoot", "filenuke", "flashx", "nosvideo", "streamcloud", "streaminto", "thevideo", "uploadc", "uptobox", "vidbull", "videomega", "vidhog", "vidlockers", "vidspot", "vidto", "vidx", "vidzi", "vodlocker", "youwatch"]

LATEST = " "

print "Starting Update2-py"

#fontpath = THISPLUG
#addFont('%s/font_default.otf' % fontpath, 'TSmediaFont', 100, 1)

def updstart2():
        
        tfile = THISPLUG + "/youtube_dl/version.py"
        if not os.path.exists(tfile):
                upd_done()
        else:
                url2 = "https://ytdl-org.github.io/youtube-dl/download.html"
                print "In Update-py checkvers url2 =", url2
                #fpage = urlopen(url2).read()
                xdest = "/tmp/down.txt"
                downloadPage(url2, xdest).addCallback(getdown).addErrback(showError)

def getdown(fplug):                
                fpage = open("/tmp/down.txt", "r").read()
                print "In checkvers fpage =", fpage
                txt = fpage
                n1 = txt.find('<h2><a href=', 0)
                n2 = txt.find('">', (n1+15))
                n3 = txt.find('</a>', (n2+4))
                latest = txt[(n2+2):n3]
                print  "checkvers latest =", latest
                
                global LATEST
                LATEST = latest
                
                tfile = THISPLUG + "/youtube_dl/version.py"
                f = open(tfile, "r")       
                txt = f.read()
                print "In upd_done1 txt = ", txt
                n1 = txt.find('__version__ = ', 0)
                n2 = txt.find("'", (n1+18))
                
                version = txt[(n1+15):n2]
                f.close()
                print "In upd_done1 version youtube.dl= ", version
                newvers = latest
                print "In upd_done1 newvers youtube.dl= ", newvers
                if newvers == " ":
                       upd_done()
                elif newvers != version:
#                       fdest = THISPLUG + "/scripts//script.module.youtube.dl/lib"
                       dest = "/tmp/youtube-dl.zip"
#                       xfile = "https://yt-dl.org/downloads/" + newvers + "/youtube-dl" 
                       xfile = "https://yt-dl.org/downloads/latest/youtube-dl"
                       downloadPage(xfile, dest).addCallback(ytdl).addErrback(showError)
                else:       
                       upd_done()        

def showError(error):
                print "ERROR :", error
                cmd = "wget https://yt-dl.org/downloads/" + LATEST + "/youtube-dl -O /tmp/youtube-dl.zip"
                
                os.system(cmd)
                ytdl()

def ytdl(fplug=" "):
        try:
                fdest = THISPLUG
                import zipfile
                zip_ref = zipfile.ZipFile('/tmp/youtube-dl.zip', 'r')
                zip_ref.extractall(fdest)
                zip_ref.close()
                upd_done()
        except:
                upd_done()               
########################################   

def upd_done():
        pass










              






































