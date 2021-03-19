import os, re
from urllib2 import urlopen
from twisted.web.client import getPage, downloadPage
import base64
THISPLUG = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia"

latest = " "

print "Starting Update-py"

host = 'aHR0cDovL3BhdGJ1d2ViLmNvbQ=='
ServerS1 = base64.b64decode(host)

def updstart():        
        #################
        print "In updstart"
        try:
               from Plugins.Extensions.WebMedia.Update2 import updstart2
        except:       
               from Update2 import updstart2
        try:       
               updstart2()
        except:       
               print "\nError 2 updating some scripts"
        #################
        dest = "/tmp/Execlist.zip"
        xfile = ServerS1 + "/WMupd/Execlist.zip" 
        print "upd_done xfile =", xfile
        downloadPage(xfile, dest).addCallback(upd_last).addErrback(showError)

def showError(error):
        print "ERROR :", error
        upd_done()

def upd_last(fplug): 
        print "In upd_last"
        fdest = THISPLUG
        cmd = "unzip -o -q '/tmp/Execlist.zip' -d " + fdest
        print "cmd A =", cmd
        try:
              os.system(cmd)
              upd_done()
        except:
              upd_done()
        
def upd_done():        
        #################
        print "In upd_done"
        #################
        dest = "/tmp/updates.zip"
        xfile = ServerS1 + "/WMupd/updates.zip" 
        print "upd_done xfile =", xfile
        downloadPage(xfile, dest).addCallback(upd_last2).addErrback(showError2)

def showError2(error):
        print "ERROR :", error
        pass

def upd_last2(fplug): 
        print "In upd_last2"
        fdest = "/usr/lib/enigma2/python/Plugins/Extensions/"
#        cmd = "unzip -o -q '/tmp/updates.zip' -d " + fdest
        cmd = "unzip -o -q /tmp/updates.zip -d /tmp && cp -rf /tmp/WebMedia/* /usr/lib/enigma2/python/Plugins/Extensions/WebMedia && rm -rf /tmp/WebMedia"
        print "cmd B =", cmd
        os.system(cmd)
        pass

"""
    def selected2(self, plug):
            if plug:
                n1 = plug[0].find("-", 0)
                plug1 = plug[0][:n1]
                cmd = "unzip -o -q /tmp/" + plug[0] +" -d /tmp && cp -rf /tmp/" + plug1 + "/* /usr/lib/enigma2/python/Plugins/Extensions/WebMedia"
                print "In selected2 cmd =", cmd
                title = (_("Installing plugin"))
                os.system(cmd)
                ########
                self.openTest()
            
            else:
                self.openTest()
                # self.close()    

"""








