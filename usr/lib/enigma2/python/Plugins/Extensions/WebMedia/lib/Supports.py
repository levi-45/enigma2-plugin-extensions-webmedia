#!/usr/bin/python
# -*- coding: utf-8 -*-
from Plugins.Extensions.WebMedia.lib.Utils import *
from Plugins.Extensions.WebMedia.lib.getpics import getpics
from Plugins.Extensions.WebMedia.lib.getpics import GridMain
from Components.config import config

import urllib, urllib2
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest
import re
from Screens.InputBox import InputBox, PinInput

from enigma import getDesktop
from Plugins.Extensions.WebMedia.Spinner import Spinner
from os import system
import sys
import time
from enigma import eConsoleAppContainer,gPixmapPtr

DESKHEIGHT = getDesktop(0).size().height()

if DESKHEIGHT > 1000:
       from Plugins.Extensions.WebMedia.skin import *
else:
      from Plugins.Extensions.WebMedia.skin1 import *


THISPLUG= '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia'
THISADDON = ""
newstext = ""
DEBUG = 1
ADDONCAT = "plugins"
dtext1 = " "
HANDLE = 1
DESKHEIGHT = getDesktop(0).size().height()
     
##########       
       
from Plugins.Extensions.WebMedia.lib.VirtualKeyBoard import WMVirtualKeyBoard
       
def getUrl(url):
      print "Here in getUrl url =", url
      req = urllib2.Request(url)
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link=response.read()
#      print "Here in getUrl link =", link
      response.close()
      return link
       
def getUrl2(url, referer):
            print "Here in getUrl2 url =", url
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            req.add_header('Referer', referer)
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            return link
            
def getUrlresp(url):
        print "Here in getUrlresp url =", url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
#       link=response.read()
#       response.close()
        return response
        
def buildBilder():
                cursel = THISPLUG+"/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                
                return Bilder        
            
def getpics(names, pics, tmpfold, picfold):
              print "In getpics tmpfold =", tmpfold
              print "In getpics picfold =", picfold
              if config.plugins.webmedia.skinres.value == "fullhd":
                    nw = 300
              else:
                    nw = 200      
              pix = []
              if config.plugins.webmedia.thumb.value == "False":
                      if config.plugins.webmedia.skinres.value == "fullhd":
                                defpic = THISPLUG + "/skinpics/images/defaultL.png" 
                      else:       
                                defpic = THISPLUG + "/skinpics/images/default.png"    
                      npic = len(pics)
                      i = 0
                      while i < npic:
                             pix.append(defpic)
                             i = i+1
                      return pix
              cmd = "rm " + tmpfold + "/*"
              os.system(cmd)
              npic = len(pics)
              j = 0
              print "In getpics names =", names
              while j < npic:
                   name = names[j]
                   print "In getpics name =", name
                   if name is None:
                          name = "Video"
                   try:
                          name = name.replace("&", "")
                          name = name.replace(":", "")
                          name = name.replace("(", "-")
                          name = name.replace(")", "")
                          name = name.replace(" ", "")
                   except:
                          pass       
                   url = pics[j]
                   if url is None:
                          url = ""
                   url = url.replace(" ", "%20")
                   url = url.replace("ExQ", "=")       
                   print "In getpics url =", url      
                   if ".png" in url:
                          tpicf = tmpfold + "/" + name + ".png"
#                          picf = picfold + "/" + name + ".png"
                   else:       
                          tpicf = tmpfold + "/" + name + ".jpg"
#                          picf = picfold + "/" + name + ".jpg"
                   picf = picfold + "/" + name + ".png"       
                   if fileExists(picf):
                          cmd = "cp " + picf + " " + tmpfold
                          print "In getpics fileExists(picf) cmd =", cmd
                          os.system(cmd)
                   
                   if not fileExists(picf):
                       print "In getpics not fileExists(picf) url =", url
                       if THISPLUG in url:
                          try:
                                  cmd = "cp " + url + " " + tpicf
                                  print "In getpics not fileExists(picf) cmd =", cmd
                                  os.system(cmd)
                          except:
                                  pass
                       else:
                          print "In getpics not THISPLUG"
                          try:
                               if "|" in url:
                                  n3 = url.find("|", 0)
                                  n1 = url.find("Referer", n3)
                                  n2 = url.find("=", n1)
                                  url1 = url[:n3]
                            #      print "In getpics not fileExists(picf) url1 =", url1
                                  referer = url[n2:]
                            #      print "In getpics not fileExists(picf) referer =", referer
                                  p = getUrl2(url1, referer)
                                  f1=open(tpicf,"wb")
                                  f1.write(p)
                                  f1.close() 
                               else:
                                  print "Going in urlopen url =", url
                                  f = getUrlresp(url)
                                  print "f =", f
                                  p = f.read()
                                  f1=open(tpicf,"wb")
                                  f1.write(p)
                                  f1.close() 
                                      
                          except:
                                  if config.plugins.webmedia.skinres.value == "fullhd":
                                          cmd = "cp " + THISPLUG + "/skinpics/images/defaultL.png " + tpicf
                                  else:       
                                          cmd = "cp " + THISPLUG + "/skinpics/images/default.png " + tpicf      
                                  os.system(cmd)
                                        

                       if not fileExists(tpicf): 
                                  print "In getpics not fileExists(tpicf) tpicf=", tpicf
                                  """
                                  if ".png" in tpicf:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.png " + tpicf
                                  else:
                                          cmd = "cp " + THISPLUG + "/skin/images/default.jpg " + tpicf
                                  """        
                                  if config.plugins.webmedia.skinres.value == "fullhd":
                                          cmd = "cp " + THISPLUG + "/skinpics/images/defaultL.png " + tpicf
                                  else:       
                                          cmd = "cp " + THISPLUG + "/skinpics/images/default.png " + tpicf           
                                          
                                  print "In getpics not fileExists(tpicf) cmd=", cmd        
                                  os.system(cmd)

                       try:
                          try:
                                import Image
                          except:
                                from PIL import Image
                          im = Image.open(tpicf)
                          imode = im.mode
                          if im.mode != "P":
                                 im = im.convert("P")
                          w = im.size[0]
                          d = im.size[1]
                          r = float(d)/float(w)
                          d1 = r*nw
                          if w != nw:        
                                 x = int(nw)

                                 y = int(d1)
                                 im = im.resize((x,y), Image.ANTIALIAS)
                          tpicf = tmpfold + "/" + name + ".png"
                          picf = picfold + "/" + name + ".png"
                          im.save(tpicf)
                          
                       except:
                          tpicf = THISPLUG + "/skinpics/images/default.png" 
                   pix.append(j)
                   pix[j] = picf
                   j = j+1       
              cmd1 = "cp " + tmpfold + "/* " + picfold + " && rm " + tmpfold + "/* &"
              print "In getpics final cmd1=", cmd1  
              os.system(cmd1)
              return pix
            
def up(names, tmppics, pos, menu, pixmap):
                menu.up()
                pos = pos - 1
                num = len(names)
                if pos == -1:
                              pos = num - 1
                              menu.moveToIndex(pos)  
                name = names[pos]
                if name == "Exit":
                         if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1)
                else:
                        try: 
                         pic1 = tmppics[pos]
                         pixmap.instance.setPixmapFromFile(pic1)
                        except:
                         pass 
                return pos
                
def down(names, tmppics, pos, menu, pixmap):
                menu.down()
                pos = pos + 1
                num = len(names)
                if pos == num:
                              pos = 0
                              menu.moveToIndex(pos) 
                name = names[pos]
                if name == "Exit":
                         if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1)
                else:
                        try:
                         pic1 = tmppics[pos]
                         pixmap.instance.setPixmapFromFile(pic1)
                        except:
                         pass 
                return pos
                      
def left(names, tmppics, pos, menu, pixmap):
         menu.pageUp()
         pos = menu.getSelectionIndex()
         name = names[pos]
         
         if name != "Exit":
                pic1 = tmppics[pos]
                pixmap.instance.setPixmapFromFile(pic1)

         else:      
                try:
                         if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                         else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                         pixmap.instance.setPixmapFromFile(pic1) 
                except:
                  pass       
         return pos
         
def right(names, tmppics, pos, menu, pixmap):
         menu.pageDown()
         pos = menu.getSelectionIndex()
         name = names[pos]
         if name != "Exit":
                pic1 = tmppics[pos]
                pixmap.instance.setPixmapFromFile(pic1)
         else:      
                try:
                       if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitLL.png" 
                       else:       
                                pic1 = THISPLUG + "/skin/images/ExitL.png"     
                       pixmap.instance.setPixmapFromFile(pic1)
                except:
                       pass                       
         return pos     
                     
            
def parameters_string_to_dict(parameters):
    paramDict = {}
#    print "Here in parameters =", parameters
    if parameters:
        paramPairs = parameters.split("&")
        for paramsPair in paramPairs:
#            print "Here in paramPairs =", paramPairs
            if not "=" in paramsPair:
                    continue
            paramSplits = paramsPair.split('=')
            if paramSplits[0]=="?url":
               paramSplits[0]='url'
            paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict
            
def startspinner():
                cursel = THISPLUG+"/spinner"
    		Bilder = []
		if cursel:
			for i in range(30):
				if (os.path.isfile("%s/wait%d.png"%(cursel,i+1))):
					Bilder.append("%s/wait%d.png"%(cursel,i+1))
		else:
		        Bilder = []
                #self["text"].setText("Press ok to exit")
                return Spinner(Bilder)             
            

###################################################################################################   
class Videos3(Screen):
    def __init__(self, session, name, url, nextrun,progressCallBack=None):
                Screen.__init__(self, session)
                self.name = name
                self.session=session
                self.url = url
                self.nextrun = nextrun

                self.onShown.append(self.start)
                self.error=None
                self.data1=''
########################
                self.updateTimer = eTimer()
                try:
                      self.updateTimer_conn = self.updateTimer.timeout.connect(self.updateStatus)
                except AttributeError:
                      self.updateTimer.callback.append(self.updateStatus)
                self.timecount = 0
                ncount = config.plugins.webmedia.wait.value 

#                nc = int(ncount)*1000
#                timeint = int(float(nc/120))
#                print "timeint =", timeint
                self.timeint = 1000
                self.nct = int(ncount)
#                self.nct = int(float(nc/self.timeint))
#                print "self.nct =", self.nct
#		self.updateTimer.start(timeint)
#		self.updateStatus()
########################                
                self.error=''                
                self.progressCallBack=progressCallBack
                self.progress=(_('Please wait...\n'))
                if os.path.exists("/tmp/stopaddon"):
                   os.remove("/tmp/stopaddon")
    def start(self):
                url = self.url
                name = self.name
                if DEBUG == 1:
                       print "In Videos3 name =", name
                       print "In Videos3 url =", url
                       print "In Videos3 self.nextrun =", self.nextrun
#                print "In Videos3 url B=", url       
                if (THISPLUG not in url):
                        desc = " "
                        self.progressCallBack("Finished")
                        self.updateTimer.stop()
                        self.session.open(Playoptions, name, url, desc)
                        self.close()
                        
                else:		
########################pictures?###########
                   n1 = url.find("default.py?", 0)
                   urla = url[(n1+11):]
                   print "In Videos3 urla =", urla
                   plugin_id=os.path.split(THISADDON)[1]
                   if ("plugin.image" in plugin_id) or ("plugin.picture" in plugin_id) and ("url=" not in urla) and ("plugin://" not in urla):
                        print "In Videos3 going in picshow"
                        self.picshow(urla)
                   else:
#######################pictures#############
                        global HANDLE
                        hdl = int(HANDLE)
                        hdl = hdl+1
                        HANDLE = str(hdl)
                        n1 = url.find('?', 0)
                        if n1<0:
                                return
                                
                        url1 = url[:n1]
                        url2 = url[n1:]
                        url2 = url2.replace(" ", "%20") 
                        if "plugin://plugin.video.youtube/" in url:
                               url1 = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/" + ADDONCAT + "/plugin.video.youtube/default.py"
                               url2 = url2.replace("plugin://plugin.video.youtube/?", "path=/root/video&")

#                        url2 = url[n1:]
#                        url2 = url2.replace(" ", "%20")        
                        arg = url1 + " " + HANDLE + " '" + url2 + "'"
                        if DEBUG == 1:
                               print "Videos3 arg =", arg
                        self.arg = arg
                        self.stream()
                        
    def picshow(self, urla):
                xurl = urla
                xdest = "/tmp/picture.png"
	        downloadPage(xurl, xdest).addCallback(self.picture).addErrback(self.showError)

    def showError(self, error):
                print "ERROR :", error

    def picture(self, fplug):                        
                pic = "/tmp/picture.png"
##                self.session.open(Showpic, pic)
#                self.close()        
                self.session.open(Splash3, pic)        
                        
                   
    def stoprun(self):
                self.close() 
		try:
			
			self.container.appClosed.remove(self.runFinished)
			self.container.dataAvail.remove(self.dataAvail)
                        self.progressCallBack("Finished")    
                except:
                        pass
    
                                         

    def dataAvail(self,rstr):
            if os.path.exists("/tmp/stopaddon"):
                self.stoprun()
                return
            if rstr:
               self.data1=self.data1+rstr
               if self.progressCallBack is not None:
                  self.progress=self.progress+"..."
                  self.progressCallBack(self.progress)
            #if self.progress_callback is not None:
               #self.progress_callback('Please wait..")
    
                                                   
    def stream(self):

                self.picfold = config.plugins.webmedia.cachefold.value+"/xbmc/pic"
                self.tmpfold = config.plugins.webmedia.cachefold.value+"/xbmc/tmp"
#                cmd = "rm -rf " + self.tmpfold
#                system(cmd)
                
                if os.path.exists("/tmp/stopaddon"):
                   self.stoprun()
                   return
                
                if DEBUG == 1:
                       print "In rundef self.arg =", self.arg
                cmd = "python " + self.arg
                print "In rundef cmd A=", cmd
#                cmd = cmd.replace("&", "\\&")
#                cmd = cmd.replace("(", "\\(")
#                cmd = cmd.replace(")", "\\)")
                afile = file("/tmp/test.txt","w")       
                afile.write("going in default.py")
                afile.write(cmd)
                fdef = 'default'#NEWDEFPY[:-3]
                args = cmd.split(" ")
                arg1 = args[1]
                arg2 = args[2]
                arg3 = args[3]
                arg4=config.plugins.webmedia.cachefold.value
                sys.argv = [arg1,arg2, arg3,arg4]                
                self.plugin_id=os.path.split(THISADDON)[1]
#                dellog()
                
                print "539arg3 =",arg3
                if 'select=true' in arg3 :
                      f = open("/tmp/result.txt", "w")
	              line = arg3.replace("'?", "")
	              params=parameters_string_to_dict(line)
	              print  "Here in select writing result.txt params =", params
	              for key in params.keys():
	                     if "url" in key:
	                             url = params[key]
	                             break
#	              url = params.get("url","0")
                      text = url + "\n"
                      print  "Here in select writing result.txt text =", text
                      f.write(text)
                      f.close()
        
                      myfile = file(r"/tmp/arg1.txt")       
                      icount = 0
                      for line in myfile.readlines(): 
                            sysarg = line
                            sysarg = sysarg.replace("\n", "")
                            icount = icount+1
                            if icount > 0:
                                 break
#                      if os.path.exists("/tmp/arg1.txt"):
#                            os.remove("/tmp/arg1.txt")  
                      print  "sysarg =", sysarg
                      args = sysarg.split(" ")
#              
                      cmd = "python '" + args[0] +"' '1' '" + args[2] + "'"
                  
                  
                else:
                   
                   xpath_file=THISPLUG+"/" + ADDONCAT + "/"+self.plugin_id+"/xpath.py"
                   fixed2_file=THISPLUG+"/" + ADDONCAT + "/"+self.plugin_id+"/fixed2"
                   default_file=THISPLUG+"/" + ADDONCAT + "/"+self.plugin_id+"/default.py" 
#                   if not os.path.exists(xpath_file): 
#                   os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
#                      os.system("touch " + fixed2_file)                                       
#                   if not os.path.exists(fixed2_file):
#                      os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
#                      os.system("touch " + fixed2_file)

                   print  "In rundef cmd B=", cmd
###                   cmd='python '+default_file+' 1 '+"'"+arg3+"'" 
                   print  "In rundef cmd C=", cmd
                       
                ###############################

               
                 
                #cmd='python '+xpath_file+' 1 '+arg3      
                self.container = eConsoleAppContainer()
#		self.container.appClosed.append(self.action)
##                try:
##		       self.container.appClosed.append(self.finad)
##                except:       
##                       self.container.appClosed.connect(self.finad) 			        
#		self.container.dataAvail.append(self.dataAvail)
##		try:
##		       self.container.dataAvail.append(self.dataAvail)
##                except:       
##                       self.container.dataAvail.connect(self.dataAvail) 	
		self.data1=''		
#                if os.path.exists("/tmp/WebMedia_log"):
#                    os.remove("/tmp/WebMedia_log")
                    
                if os.path.exists("/tmp/data.txt"):
                   os.remove("/tmp/data.txt")                    		
#                if DEBUG == 1:
                self.lastcmd = cmd
                global LAST
                LAST = self.lastcmd
                cmd = cmd + " &"
                print  "In Videos3 cmd =", cmd
###################################################                
###################################################                
                timen = time.time() 
                global NTIME 
                timenow = timen - NTIME
                NTIME = timen
                print  "In Videos3 1 timenow", timenow
##                os.system(cmd)
#                       self.action(" ")
#                self.container.execute(cmd) 
                self.dtext = " "
                print "cmd 2=", cmd
                self.p = os.popen(cmd)
                self.timecount = 0
                self.updateTimer.start(self.timeint)

    def showback(self):
                      myfile = file(r"/tmp/arg1.txt")       
                      icount = 0
                      for line in myfile.readlines(): 
                            sysarg = line
                            sysarg = sysarg.replace("\n", "")
                            icount = icount+1
                            if icount > 0:
                                 break
#                      if os.path.exists("/tmp/arg1.txt"):
#                            os.remove("/tmp/arg1.txt")  
                      print  "sysarg =", sysarg
                      args = sysarg.split(" ")
#              
                      cmd = "python '" + args[0] +"' '1' '" + args[2] + "' &"
                      os.system(cmd)
    
    def updateStatus(self):
         ncount = config.plugins.webmedia.wait.value
         self.timecount = self.timecount + 1 
         print  "In rundef updateStatus self.timecount =", self.timecount
         self.dtext = self.p.read()
         print "In rundef updateStatus self.dtext =", self.dtext
         global dtext1
         if len(self.dtext) > 0:
                dtext1 = dtext1 + self.dtext
         if "data B" in self.dtext:
                self.updateTimer.stop()
                self.action(" ")
         print  "In rundef self.timecount =", self.timecount 
         if self.timecount > self.nct:     
              self.updateTimer.stop()
              f1=open("/tmp/e.log","a")
#              f1.write(dtext1)
              f1.close()
              self.action(" ")
              
#         elif self.timecount > 10:
#              print  "No /tmp/data.txt", b
#              self.updateTimer.stop()
#              self.close()
              
              
    def callback(self,result):
        if result:
           self.stream()		
    def action(self,retval):
            print  "In Videos3 action 1"
            if os.path.exists("/tmp/stopaddon"):
                   self.stoprun()
                   return    
            #######################
            str = self.data1
            print  "In Videos3 action 2"
            ########################  
              
            self.data = []
            self.names = []
            self.urls = []
            self.pics = []
            self.names.append("Exit")
            self.urls.append(" ")
            if config.plugins.webmedia.skinres.value == "fullhd":
                                exitpic = THISPLUG + "/skin/images/ExitL.png"
            else:
                                exitpic = THISPLUG + "/skin/images/Exit.png"
            self.pics.append(exitpic)
            self.tmppics = []
            self.lines = []
            self.vidinfo = []
            afile = open("/tmp/test.txt","w")       
            afile.write("\nin action=")
            datain =""
            parameters = []
            print  "In Videos3 action 3"
            self.data = []
#            dtext = self.p.read()
            data = self.dtext.splitlines()
            for line in data:
                   print  "In Videos3 line =", line
                   if not "data B" in line: continue
                   else: 
                         i1 = line.find("&", 0)
                         line1 = line[i1:]
                         self.data.append(line1)
            print  "In Videos3 self.data =", self.data 
            ln = len(self.data)
            if ln == 0:
                 cmd = LAST + " > /tmp/error.log 2>&1 &"
                 os.system(cmd)
                 self.error=(_("Error! Try another item OR exit and submit log /tmp/e.log and /tmp/error.log"))
                 self.progressCallBack((_("Error! Try another item OR exit and submit log /tmp/e.log and /tmp/error.log")))
                 return
                    

            n1 = 0
            if n1==0:    
                 inum = len(self.data)
                 i = 0
                 while i < inum:
                        name = " "
                        url = " "
                        line = self.data[i]
                        if DEBUG == 1:
                               print  "In rundef line B=", line
                        if line.startswith("&"):
                               line = line[1:]
#                        print  "In rundef line C=", line       
                        params = parameters_string_to_dict(line)
                        if DEBUG == 1:
                               print  "Videos3 params=", params
                        self.lines.append(line)
                        try:
                               name = params.get("name")
                               name = name.replace("AxNxD", "&")
                               name = name.replace("ExQ", "=")
                               if DEBUG == 1:
                                       print  "Videos3 name=", name       
                        except:
                               pass
                        try:
                               url = params.get("url")
                               url = url.replace("AxNxD", "&")
                               url = url.replace("ExQ", "=")
                               if DEBUG == 1:
                                       print  "Videos3 url=", url      
                        except:
                              pass
                        thumbnailImage = params.get("thumbnailImage") 
                        print  "Videos3 thumbnailImage=", thumbnailImage   
                        iconImage = params.get("iconImage") 
                        print  "Videos3 iconImage=", iconImage
                        try:
                           if thumbnailImage.startswith("http"):
                               pic = thumbnailImage
                               print  "Videos3 pic A=", pic
                           elif iconImage.startswith("http"):
                               pic = iconImage
                               print  "Videos3 pic B=", pic
                           else:
                               if config.plugins.webmedia.skinres.value == "fullhd":
                                       pic = THISPLUG + "/skin/images/defaultL.png" 
                               else:       
                                       pic = THISPLUG + "/skin/images/default.png"    
                        except:
                               if config.plugins.webmedia.skinres.value == "fullhd":
                                       pic = THISPLUG + "/skin/images/defaultL.png" 
                               else:       
                                       pic = THISPLUG + "/skin/images/default.png" 
                        if DEBUG == 1:
                                       print  "Videos3 pic=", pic              
                        self.names.append(name)
                        self.urls.append(url)
                        self.pics.append(pic)
                        i = i+1
                 if DEBUG == 1:
                        print  "Videos3 self.names=", self.names
                        print  "Videos3 self.urls=", self.urls
                        print  "Videos3 self.pics=", self.pics

                 if 'showtext=true' in self.urls[1] :
                      f = open("/tmp/show.txt", "r")
                      fpage = f.read() 
                      self.session.openWithCallback(self.showback, ShowPage2, fpage) 
                        
                 elif (len(self.names) == 2) and (self.urls[1] is None) and (THISPLUG not in self.names[1]):
                        if "*download*" in self.names[1]:
                                url = self.names[1].replace("*download*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid, name, url, desc)
                                self.close()
                        elif "*download2*" in self.names[1]:
                                url = self.names[1].replace("*download2*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid2, name, url, desc)
                                self.close()
                        elif ("stack://" in self.names[1]):
                                stkurl = self.names[1]
                                self.playstack(stkurl)

                        elif ("rtmp" in self.names[1]):
                            if "live" in name:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp2, name, url, desc)
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playoptions, name, url, desc)
                                self.close()
                           
                            else:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp, name, url, desc)
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playoptions, name, url, desc)
                                self.close()        
                                
                        else:        
                                name = self.name                                
                                desc = " "
                                url = self.names[1]
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playoptions, name, url, desc)
                                self.close()
                 elif (len(self.names) == 2) and (self.urls[1] is not None) and (THISPLUG not in self.urls[1]):
                        url = self.urls[1]
                        if "*download*" in url:
                                url = url.replace("*download*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Getvid, name, url, desc)
                                self.close()
                        elif "*download2*" in url:
                                url = url.replace("*download2*", "")
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("")
                                self.updateTimer.stop()
                                self.session.open(Getvid2, name, url, desc)
                                self.close()
                                       
                        else:
                                name = self.name                                
                                desc = " "
                                self.progressCallBack("Finished")
                                self.updateTimer.stop()
                                self.session.open(Playoptions, name, url, desc)
                                self.close()    
#                 else:        
#                        self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                        #if int(self.nextrun) == 2:
#                        self.progressCallBack("")
#                        self.session.open(Videos2,self.name,self.names, self.urls, self.tmppics,self.nextrun)
#                        self.close()
                        
                        
                        
                 else:  
                    inm = 0 
                    for name in self.names:
                                if name is None:
                                      self.names[inm] = "Video"
                                self.names[inm] = self.names[inm].replace(":", "-")
                                self.names[inm] = self.names[inm].replace("&", "-")
                                self.names[inm] = self.names[inm].replace("'", "-")
                                self.names[inm] = self.names[inm].replace("?", "-")
                                self.names[inm] = self.names[inm].replace("/", "-")
                                self.names[inm] = self.names[inm].replace("#", "-")
                                self.names[inm] = self.names[inm].replace("|", "-")
                                self.names[inm] = self.names[inm].replace("*", "")
                                inm = inm+1
                    ipic = 2 
                    npic = len(self.pics)
                    cpic = self.pics[1]
                    print  "cpic =", cpic
                    print  "self.pics A=", self.pics
                    while ipic < npic:
                          pic = self.pics[ipic]
                          if pic == cpic:
                                if config.plugins.webmedia.skinres.value == "fullhd":
                                       self.pics[ipic] = THISPLUG + "/skin/images/defaultL.png" 
                                else:       
                                       self.pics[ipic] = THISPLUG + "/skin/images/default.png" 
                          ipic = ipic+1
                          
                    print  "self.pics B=", self.pics
                    if config.plugins.webmedia.thumb.value == "True":
                               self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                               self.session.open(Videos4,self.name,self.names, self.urls, self.tmppics,self.nextrun)
                    else:                       
                               self.tmppics = getpics(self.names, self.pics, self.tmpfold, self.picfold)
                               self.session.open(Videos2,self.name,self.names, self.urls, self.tmppics,self.nextrun)

class Videos4FHD(Screen):
        skin = """
               <screen name="XbmcPluginPics" position="0,0" size="1920,1080" title="WebMedia" >
                <eLabel position="0,0" zPosition="1" size="1920,1080" backgroundColor="#000000" /> 

                        <widget source="global.CurrentTime" render="Label" position="120,127" size="210,37"  zPosition="2" font="Regular;27" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1">
                        <convert type="ClockToText">Default</convert>
                        </widget>
       
                        <widget source="global.CurrentTime" render="Label" position="120,120" size="210,37" zPosition="2" font="Regular;27" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1" valign="center">
                        <convert type="ClockToText">Format:%d.%m.%Y</convert>
                        </widget>
                        
		        <widget name="title" position="1275,30" size="525,75" zPosition="3" halign="center" valign="top" foregroundColor="#389416" backgroundColor="black" font="Regular;60" transparent="1" /> 
                        <widget name="info" position="225,997" zPosition="4" size="1350,75" font="Regular;33" foregroundColor="#7bd7f7" backgroundColor="#40000000" transparent="1" halign="left" valign="center" />
                        <widget name="bild" position="720,975"  size="150,150" transparent="1" zPosition="5" />
                <widget name="frame" position="90,120" size="390,390" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/pic_frameL4.png" zPosition="2" alphatest="on" />   

                <widget source="label1" render="Label" position="60,442" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" backgroundColor="black"/>
                <widget name="pixmap1" position="60,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label2" render="Label" position="420,442" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap2" position="420,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label3" render="Label" position="780,442" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap3" position="780,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label4" render="Label" position="1140,442" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap4" position="1140,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label5" render="Label" position="1500,442" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap5" position="1500,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />

                <widget source="label6" render="Label" position="60,892" size="330,90" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap6" position="60,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label7" render="Label" position="420,892" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap7" position="420,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label8" render="Label" position="780,892" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap8" position="780,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label9" render="Label" position="1140,892" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap9" position="1140,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label10" render="Label" position="1500,892" size="330,112" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap10" position="1500,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />

                </screen>"""

class Videos4HD(Screen):
        skin = """
<screen name="XbmcPluginPics" position="0,0" size="1280,720" title="WebMedia" >
                <eLabel position="0,0" zPosition="1" size="1280,720" backgroundColor="#000000" /> 

                        <widget source="global.CurrentTime" render="Label" position="80,85" size="140,25"  zPosition="2" font="Regular;18" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1">
                        <convert type="ClockToText">Default</convert>
                        </widget>
       
                        <widget source="global.CurrentTime" render="Label" position="80,80" size="140,25" zPosition="2" font="Regular;18" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1" valign="center">
                        <convert type="ClockToText">Format:%d.%m.%Y</convert>
                        </widget>
                        
		        <widget name="title" position="850,20" size="350,50" zPosition="3" halign="center" valign="top" foregroundColor="#389416" backgroundColor="black" font="Regular;40" transparent="1" /> 
                        <widget name="info" position="150,665" zPosition="4" size="900,50" font="Regular;22" foregroundColor="#7bd7f7" backgroundColor="#40000000" transparent="1" halign="left" valign="center" />
                        <widget name="bild" position="480,650"  size="100,100" transparent="1" zPosition="5" />
                <widget name="frame" position="60,80" size="260,260" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/pic_frame2.png" zPosition="2" alphatest="on" />   

                <widget source="label1" render="Label" position="40,295" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" backgroundColor="black"/>
                <widget name="pixmap1" position="40,70" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label2" render="Label" position="280,295" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap2" position="280,70" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label3" render="Label" position="520,295" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap3" position="520,70" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label4" render="Label" position="760,295" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap4" position="760,70" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label5" render="Label" position="1000,295" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap5" position="1000,70" size="220,220" zPosition="3" transparent="1" alphatest="on" />

                <widget source="label6" render="Label" position="40,595" size="220,60" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap6" position="40,370" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label7" render="Label" position="280,595" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap7" position="280,370" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label8" render="Label" position="520,595" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap8" position="520,370" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label9" render="Label" position="760,595" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap9" position="760,370" size="220,220" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label10" render="Label" position="1000,595" size="220,75" font="Regular;22" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap10" position="1000,370" size="220,220" zPosition="3" transparent="1" alphatest="on" />

                </screen>"""
class Videos4(Screen):

	def __init__(self, session, name, names, urls, tmppics,curr_run):
#		self.skinName = "Videos4"
                if DESKHEIGHT > 1000:
                       self.skin = Videos4FHD.skin
                else:
                       self.skin = Videos4HD.skin
		Screen.__init__(self, session)
		title = "WebMedia"
		self["title"] = Button(title)
		self["bild"] = startspinner()
		self.curr_run = curr_run
		self.nextrun=self.curr_run+1
		self.pos = []		
                if config.plugins.webmedia.skinres.value == "fullhd": 
                       self.pos.append([35,80])
                       self.pos.append([395,80])
                       self.pos.append([755,80])
                       self.pos.append([1115,80])
                       self.pos.append([1475,80])
                       self.pos.append([35,530])
                       self.pos.append([395,530])
                       self.pos.append([755,530])
                       self.pos.append([1115,530])
                       self.pos.append([1475,530])
                else:       
                       self.pos.append([20,50])
                       self.pos.append([260,50])
                       self.pos.append([500,50])
                       self.pos.append([740,50])
                       self.pos.append([980,50])
                
                       self.pos.append([20,350])
                       self.pos.append([260,350])
                       self.pos.append([500,350])
                       self.pos.append([740,350])
                       self.pos.append([980,350])                       

                print  " self.pos =", self.pos
		
		list = []
                self.name = name
		self.pics = tmppics
		self.mlist = names
		self.urls1 = urls
		self.names1 = names
		self["info"] = Label()
		
		self.curr_run=curr_run
		txt = str(SELECT[self.curr_run])
		print "In Videos2 SELECT[self.curr_run] A=", SELECT[self.curr_run]
		self.nextrun=self.curr_run+1
	 	print  "2028",txt	
		self.select=txt
		self.rundef=None
		self.plug=''
		self.keylock=False
		self.spinner_running=False

		
		print  "self.mlist =", self.mlist
                list = names
                self["menu"] = List(list)
                
                for x in list:
                       print  "x in list =", x

                ip = 0
                print  "self.pics = ", self.pics

		self["frame"] = MovingPixmap()

                self["label1"] = StaticText()
                self["label2"] = StaticText()
                self["label3"] = StaticText()
                self["label4"] = StaticText()
                self["label5"] = StaticText()
                self["label6"] = StaticText()
                self["label7"] = StaticText()
                self["label8"] = StaticText()
                self["label9"] = StaticText()
                self["label10"] = StaticText()
                self["label11"] = StaticText()
                self["label12"] = StaticText()
                self["label13"] = StaticText()
                self["label14"] = StaticText()
                self["label15"] = StaticText()
                self["label16"] = StaticText()


                self["pixmap1"] = Pixmap()
                self["pixmap2"] = Pixmap()
                self["pixmap3"] = Pixmap()
                self["pixmap4"] = Pixmap()
                self["pixmap5"] = Pixmap()
                self["pixmap6"] = Pixmap()
                self["pixmap7"] = Pixmap()
                self["pixmap8"] = Pixmap()
                self["pixmap9"] = Pixmap()
                self["pixmap10"] = Pixmap()
                self["pixmap11"] = Pixmap()
                self["pixmap12"] = Pixmap()
                self["pixmap13"] = Pixmap()
                self["pixmap14"] = Pixmap()
                self["pixmap15"] = Pixmap()
                self["pixmap16"] = Pixmap()
                i = 0

                self["actions"] = NumberActionMap(["OkCancelActions", "MenuActions", "DirectionActions", "NumberActions"],
			{
				"ok": self.okClicked,
				"cancel": self.cancel,
				"left": self.key_left,
			        "right": self.key_right,
			        "up": self.key_up,
			        "down": self.key_down,
			})

                self.index = 0
                ln = len(self.names1)
                self.npage = int(float(ln/10)) + 1
                print  "self.npage =", self.npage
                self.ipage = 1
                self.icount = 0
                print  "Going in openTest"
                self.onLayoutFinish.append(self.openTest)
                
        def cancel(self):
                       self.close()
                             
        def startSpinner(self):
            if self.spinner_running==False:
                Bilder=buildBilder()
                self["bild"].start(Bilder)
                self.spinner_running=True
                return    
        def stopSpinner(self):
            if self.spinner_running==True:
                self["bild"].stop()
                self.spinner_running=False
                self['bild'].instance.setPixmap(gPixmapPtr())
            return            

        def exit(self):
          if self.spinner_running==True:
           self.stopSpinner()
           self.keylock=False
           
           afile=open("/tmp/stopaddon","w")
           afile.write("stop execution")
           afile.close()
           
           self.progressCallBack("Finished")           
           try:self.rundef.stoprun()
           except:pass
          else:
           self.stopSpinner()   
           #self['bild']=None 
#           dellog()
           self.close()          
           
        
        #self['bild']=None
        
        def progressCallBack(self,progress):
          try:
             if progress is not None:
                if progress.startswith("Error"):
                   self.keylock=False
                   self["info"].setText(progress)
                   self.stopSpinner() 
                   return       
                if  progress=="Finished":
                   self.keylock=False
                   self.selection_changed()
                   self.stopSpinner()
                   return
           
             self["info"].setText(progress)
          except:
                  pass  
        
        def selection_changed(self):
          self.keylock=False
          try:self["info"].setText(self.select)
          except:pass
    
        def showerror(self):
          try:
                 from Plugins.Extensions.WebMedia.lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
          except:       
                 from lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
          self.session.open(XBMCAddonsinfoScreen,None)
                 

        def paintFrame(self):
                print  "In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry
#		if self.maxentry < self.index or self.index < 0:
#			return
                ifr = self.index - (10*(self.ipage-1))
		ipos = self.pos[ifr]
		print  "ifr, ipos =", ifr, ipos
		self["frame"].moveTo( ipos[0], ipos[1], 1)
		self["frame"].startMoving()

        def openTest(self):
#                coming in self.ipage=1, self.shortnms, self.pics
                 print  "self.ipage, self.npage =", self.ipage, self.npage
		 if self.ipage < self.npage:
                        self.maxentry = (10*self.ipage)-1
                        self.minentry = (self.ipage-1)*10
                        #self.index 0-11
                        print  "self.ipage , self.minentry, self.maxentry =", self.ipage, self.minentry, self.maxentry     

                 elif self.ipage == self.npage:
                        print  "self.ipage , len(self.pics) =", self.ipage, len(self.pics)
                        self.maxentry = len(self.pics) - 1
                        self.minentry = (self.ipage-1)*10
                        print  "self.ipage , self.minentry, self.maxentry B=", self.ipage, self.minentry, self.maxentry   
                        i1 = 0
                        blpic = THISPLUG + "/skin/images/Blank.png"
                        while i1 < 12:
                              self["label" + str(i1+1)].setText(" ")
                              self["pixmap" + str(i1+1)].instance.setPixmapFromFile(blpic)
                              i1 = i1+1
                 print  "len(self.pics) , self.minentry, self.maxentry =", len(self.pics) , self.minentry, self.maxentry        

                 i = 0
                 i1 = 0
                 self.picnum = 0
                 print  "doing pixmap"
                 ln = self.maxentry - (self.minentry-1)
                 """
                 while i1 < ln:
                    idx = self.minentry + i1 
                    print  "i1, idx =", i1, idx
                    
                    if os.path.exists(self.pics[idx]):
                           self.picnum = self.picnum+1
                    i1 = i1+1
                 print  "self.picnum  =", self.picnum 
                 print  "self.icount A=", self.icount
                 if self.icount < 15:   
                      self.icount = self.icount+1
                      if (self.picnum < 9):
                           print  "pic not ready self.icount =", self.icount
                           os.system("sleep 1")
                           self.openTest()
                      else:   
                           print  "pics ready"
                           self.icount = 15
                           pass
                 """
                 while i < ln:
                    idx = self.minentry + i 
                    print  "i, idx =", i, idx
##################################
                    print  "self.names1[idx] B=", self.names1[idx]
                    self["label" + str(i+1)].setText(self.names1[idx])
#################################

                    print  "idx, self.pics[idx]", idx, self.pics[idx]
                    pic = self.pics[idx]
                    if not os.path.exists(self.pics[idx]):
                           pic = THISPLUG + "/skin/images/default.png"
                    self["pixmap" + str(i+1)].instance.setPixmapFromFile(self.pics[idx])
                    i = i+1  
                 self.index = self.minentry
                 self.paintFrame()
                           
                 
        def key_left(self):
		self.index -= 1
		if self.index < 0:
			self.index = self.maxentry
		self.paintFrame()

        def key_right(self):
		self.index += 1
		if self.index > self.maxentry:
			self.index = 0
		self.paintFrame()

        def key_up(self):
		self.index = self.index - 5
#		if self.index < 0:
#			self.index = self.maxentry
#		self.paintFrame()
                print  "keyup self.index, self.minentry = ", self.index, self.minentry
		if self.index < (self.minentry):
                    if self.ipage > 1:
                        self.ipage = self.ipage - 1
                        self.openTest()
                         
		    elif self.ipage == 1:	
                        self.close()
                else:
		        self.paintFrame()



        def key_down(self):
                self.index = self.index + 5
                print  "keydown self.index, self.maxentry = ", self.index, self.maxentry
		if self.index > (self.maxentry):
                    if self.ipage < self.npage:
                        self.ipage = self.ipage + 1
                        self.openTest()
                         
		    elif self.ipage == self.npage:	
                        self.index = 0
                        self.ipage = 1
                        self.openTest()

                else:
		        self.paintFrame()


#########################
###############################	
        def okClicked(self):
          #self["bild"] = startspinner()
          
          if self.keylock:
                   return     
    
          if DEBUG == 1:
                print "screen number"+str(self.curr_run)+"okClicked"
          itype = self.index
          url = self.urls1[itype]
          name = self.names1[itype]
          self.name = name
          global SELECT
#          SELECT.append(self.name)
          print "screen number"+str(self.curr_run)+"okClicked SELECT[0]=", SELECT[0]
#          SELECT[self.curr_run] = SELECT[self.curr_run-1] + " -> " + self.name
          SELECT.append(SELECT[self.curr_run] + " -> " + self.name)
          self.next_select=SELECT[self.curr_run]
          print "In Videos2 self.curr_run =", self.curr_run
          print "In Videos2 SELECT[self.curr_run] =", SELECT[self.curr_run]
          print "In Videos2 SELECT =", SELECT
          self.url = url
          print "In Videos2 self.name =", self.name
          if ('search' in self.name.lower()) or ('insert' in self.name.lower()):
                     #ShowSearchDialog(self.session)
                     print  "In Videos2 search" 
#                     from  Screens.VirtualKeyBoard import VirtualKeyBoard
                     try:
                            from Plugins.Extensions.WebMedia.lib.VirtualKeyBoard import VirtualKeyBoard
                     except:       
                            from lib.VirtualKeyBoard import VirtualKeyBoard
#                     import os
                     try:
                        txt=open('/tmp/xbmc_search.txt','r').read()
                        #os.remove("/tmp/xbmc_search.txt") 
                     except:
       
                           txt=''
                     self.name=name
                     self.url=url      
                     self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Enter your search term(s)")), text = txt)           

          else:
            if itype == 0:
                  self.close()
            elif itype == 1 and self.curr_run==1:
              if name == "Setup":###to generate e2 e2sett.py
                d = THISPLUG + "/plugins/" + self.plug
                settings_file=d+"/resources/settings.xml"
                
                import sys,os
                if not os.path.exists(settings_file):
                   self['info'].setText(_("No settings available"))
                   return
                
                try:
                       from Plugins.Extensions.WebMedia.lib.XBMCAddonsSetup import AddonsettScreen
                except:       
                       from lib.XBMCAddonsSetup import AddonsettScreen               
                
                self.session.open(AddonsettScreen,self.plug)
                
                return
            elif itype == 2 and self.name == "Favorites":

#            elif itype == 1 and self.name == "Favorites":
                favorites_xml="/etc/WebMedia/favorites.xml"
                import os
                if not os.path.exists(favorites_xml):
                       try:   
                        if not os.path.exists("/etc/WebMedia"):
                           os.makedirs("/etc/WebMedia")
                        copyfile(THISPLUG+"/lib/defaults/favorites.xml",favorites_xml)
                       except:
                        return 
                try:        
                       from Plugins.Extensions.WebMedia.lib.favorites import getfavorites
                except:       
                       from lib.favorites import getfavorites
                favlist=getfavorites(self.plug)
                names2=[]
                urls2=[]
                names2.append("Exit")
                urls2.append("")
                for fav in favlist:
                     names2.append(fav[0])
                     urls2.append(fav[1])
                self.session.open(Favorites, names2, urls2)
                return

                                    
            else:
                  self["info"].setText("Please wait ...")
##                  self.keylock=True
                  self.startSpinner()
                  self.rundef = Videos3(self.session, name, url, self.nextrun,self.progressCallBack)
                  self.rundef.start()
                  
                  
##################################                  
#    plugin://plugin.video.youtube/kodion/search/query/?q=adele             
        def searchCallback(self,search_txt): 
          if search_txt:
               print  "In Videos2 self.url 2=", self.url
               print  "In Videos2 search_txt 1=", search_txt
               n1 = self.url.find("?", 0)
#               if "plugin.video.youtube" in THISADDON:
#                       self.url = self.url[:(n1+1)] + "plugin://plugin.video.youtube/kodion/search/query/?q=" + search_txt
               
 #              else:
#                       print  "In Videos2 search_txt 2=", search_txt
               file=open("/tmp/xbmc_search.txt",'w')
               file.write(search_txt)
               file.close()
               self["info"].setText(_("Please wait.."))
##                       self.keylock=True 
               rundef = Videos3(self.session, self.name, self.url, 2,self.progressCallBack)
               rundef.start() 
               if rundef.error:
                      self["info"].setText(_("Error:")+rundef.error)  
#################################### 

             
class Videos2(Screen):


    def __init__(self, session, name, names, urls, tmppics,curr_run):
		Screen.__init__(self, session)
		sk= 'wm1.xml'
                skin = skin_path + sk
                f = open(skin, 'r')
                self.skin = f.read()
                f.close()
		self["bild"] = startspinner()
		title = "WebMedia"
		self["title"] = Button(title)
                self.session=session
		self.list = []                
                self["list"] = List(self.list)
                self["list"] = RSList([])
		self["info"] = Label()
		self.curr_run=curr_run
		txt = str(SELECT[self.curr_run])
#		print "In Videos2 SELECT[self.curr_run] A=", SELECT[self.curr_run]
		self.nextrun=self.curr_run+1
	 	print  "2028",txt	
#		self.select=txt
		self.rundef=None
		self.plug=''
		self.keylock=False
		self.spinner_running=False
		print  "name =", name
		name1 = name.replace("plugin.video.", "")
		name1 = name1.replace("plugin.audio.", "")
		name1 = name1.replace("plugin.image.", "")
		name1 = name1.replace("plugin.picture.", "")
		print  "name1 =", name1
		self.select = name1
		self["info"].setText(self.select)
		self["pixmap"] = Pixmap()

	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))		
	
                self["actions"] = NumberActionMap(["OkCancelActions", "DirectionActions", "ColorActions", "EPGSelectActions"],{
                       "upRepeated": self.up,
                       "downRepeated": self.down,
                       "up": self.up,
                       "down": self.down,
                       "info":self.showerror,
                       "left": self.left,
                       "right":self.right,
		       "red": self.cancel,
		       "green": self.okClicked,                       
                       "ok": self.okClicked,                                            
                       "cancel": self.cancel,}, -1)
                self.plug = name
                self.handle = 1
                self.names1 = []
                for nam in names:
                       if nam is None:
                               nam = "Video"
                       self.names1.append(nam)        
#                self.names1 = names
                self.urls1 = urls
                self.tmppics1 = tmppics
                if DEBUG == 1:

                       print  "screen number"+str(self.curr_run)+"self.names1 =", self.names1
                       print  "screen number"+str(self.curr_run)+"self.urls1 =", self.urls1
                       print  "screen number"+str(self.curr_run)+"self.tmppics1 =", self.tmppics1
                ####################################  
#screen number4self.urls1 = [' ', '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/" + ADDONCAT + "/plugin.video.IPTVupdater/default.py?plugin://plugin.video.IPTVupdater/?url=+&name=Information&showtext=true&mode=3']
                     
                if "showtext=true" in self.urls1[1]: 
                      """
                      f = open("/tmp/show.txt", "r")
                      fpage = f.read() 
#                      self.session.openWithCallback(self.showback, ShowPage2, fpage) 
                      self.onShown.append(ShowPage2, fpage)
                      """
                      pass 
                self.names = []
                self.urls = []
                self.pics = []
                self.tmppics = []
                self.sett = []
                self.lines = []
                self.vidinfo = []                
                self.data = []
                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                system("rm /tmp/data.txt")
                self.pos = 0
                self.missed = " "
                self.shlist = " "
                self["list"].onSelectionChanged.append(self.selection_changed)
                self.onShown.append(self.selection_changed)
                self.onLayoutFinish.append(self.action)

    def cancel(self):
                       self.close()
                       
    def startSpinner(self):
        if self.spinner_running==False:
          
          #self["bild"] = startspinner()
          
          Bilder=buildBilder()
          self["bild"].start(Bilder)
          self.spinner_running=True
          return    
    def stopSpinner(self):
       if self.spinner_running==True:
          self["bild"].stop()
          self.spinner_running=False
          self['bild'].instance.setPixmap(gPixmapPtr())
          #self["bild"].instance=None
       #self["bild"]=None
       return            
    def exit(self):
        if self.spinner_running==True:
           self.stopSpinner()
           self.keylock=False
           
           afile=open("/tmp/stopaddon","w")
           afile.write("stop execution")
           afile.close()
           
           self.progressCallBack("Finished")           
           try:self.rundef.stoprun()
           except:pass
        else:
           self.stopSpinner()   
           #self['bild']=None 
#           dellog()
           self.close()          
           
        
        #self['bild']=None
        
    def progressCallBack(self,progress):
      try:
        if progress is not None:
          if progress.startswith("Error"):
              self.keylock=False
              self["info"].setText(progress)
              self.stopSpinner() 
              return       
          if  progress=="Finished":
              self.keylock=False
              self.selection_changed()
              self.stopSpinner()
              return
           
        self["info"].setText(progress)
      except:
        pass  
        
    def selection_changed(self):
        self.keylock=False
        try:self["info"].setText(self.select)
        except:pass
    
    def showerror(self):
       try:
              from Plugins.Extensions.WebMedia.lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
       except:       
              from lib.XBMCAddonsinfo import XBMCAddonsinfoScreen
       self.session.open(XBMCAddonsinfoScreen,None)
    
    def home(self):
                
                self.session.open(StartPlugin)
                self.close()

    def action(self):
                       try:
                         if os.path.exists("/tmp/netstat.txt"):
                             os.remove("/tmp/netstat.txt")
                         os.system("netstat -np > /tmp/netstat.txt && sleep 1")
                         f1=open('/tmp/netstat.txt',"r+")
                         for line in f1.readlines():
                             if '55333' in line:
                                    n1 = line.find("/", 0)
                                    if n1<0:
                                           continue
                                    n2 = line.rfind(" ", 0, n1)
                                    pid = line[(n2+1):n1]
                                    print  "In Videos3 pid =", pid
                                    cmdnet = "kill " + str(pid)
                                    self.container = eConsoleAppContainer()
#                                    self.container.appClosed.append(self.action)
#                                    self.container.dataAvail.append(self.dataAvail)
                                    self.container.execute(cmdnet)

                       except:
                                    pass

                       if config.plugins.webmedia.thumb.value == "False":
		                picthumb = THISPLUG + "/skin/images/default.png"
#                                self["pixmap"].instance.setPixmapFromFile(picthumb)
#                        print  "In Videos2 self.names1 =", self.names1
                       showlist(self.names1, self["list"])
#                        self.selection_changed()
                
    def up(self):
                if self.keylock:
                   return
                self.pos = up(self.names1, self.tmppics1, self.pos, self["list"], self["pixmap"])

    def down(self):
                if self.keylock:
                   return    
    
                self.pos = down(self.names1, self.tmppics1, self.pos, self["list"], self["pixmap"])
                
    def left(self):
                if self.keylock:
                   return    
    
                self.pos = left(self.names1, self.tmppics1, self.pos, self["list"], self["pixmap"])

    def right(self):
                if self.keylock:
                   return    
                self.pos = right(self.names1, self.tmppics1, self.pos, self["list"], self["pixmap"])

    def cancelX(self):
                self.keylock=False
                afile=open("/tmp/stopaddon","w")
                afile.write("stop execution")
                afile.close()
                self.close()  
	
    def keyRight(self):
                if self.keylock:
                   return     
    
		self["text"].right()


    def vidError(self, reply):
                return

    def okClicked(self):
          #self["bild"] = startspinner()

          if self.keylock:
                   return     
    
          if DEBUG == 1:
                print  "screen number"+str(self.curr_run)+"okClicked"
          itype = self["list"].getSelectionIndex()
          url = self.urls1[itype]
          name = self.names1[itype]
          self.name = name
          global SELECT
#          SELECT.append(self.name)
          print  "screen number"+str(self.curr_run)+"okClicked SELECT[0]=", SELECT[0]
#          SELECT[self.curr_run] = SELECT[self.curr_run-1] + " -> " + self.name
          SELECT.append(SELECT[self.curr_run] + " -> " + self.name)
          self.next_select=SELECT[self.curr_run]
          print  "In Videos2 self.curr_run =", self.curr_run
          print  "In Videos2 SELECT[self.curr_run] =", SELECT[self.curr_run]
          print  "In Videos2 SELECT =", SELECT
          self.url = url
          self.url = url
          print  "In Videos2 self.name =", self.name
          if ('search' in self.name.lower()) or ('insert' in self.name.lower()):
                     #ShowSearchDialog(self.session)
                     print "In Videos2 search" 
#                     from  Screens.VirtualKeyBoard import VirtualKeyBoard
                     try:
                            from Plugins.Extensions.WebMedia.lib.VirtualKeyBoard import VirtualKeyBoard
                     except:       
                            from lib.VirtualKeyBoard import VirtualKeyBoard
#                     import os
                     try:
                        txt=open('/tmp/xbmc_search.txt','r').read()
                        #os.remove("/tmp/xbmc_search.txt") 
                     except:
       
                           txt=''
                     self.name=name
                     self.url=url      
                     self.session.openWithCallback(self.searchCallback, VirtualKeyBoard, title = (_("Enter your search term(s)")), text = txt)           

          else:
            if itype == 0:
                  self.close()
            elif itype == 1 and self.curr_run==1:
              if name == "Setup":###to generate e2 e2sett.py
                d = THISPLUG + "/plugins/" + self.plug
                settings_file=d+"/resources/settings.xml"
                
                import sys,os
                if not os.path.exists(settings_file):
                   self['info'].setText(_("No settings available"))
                   return
                
                try:
                       from Plugins.Extensions.WebMedia.lib.XBMCAddonsSetup import AddonsettScreen
                except:
                       from lib.XBMCAddonsSetup import AddonsettScreen
                self.session.open(AddonsettScreen,self.plug)
                
                return
            elif itype == 2 and self.name == "Favorites":

#            elif itype == 1 and self.name == "Favorites":

                
                favorites_xml="/etc/WebMedia/favorites.xml"
                import os
                if not os.path.exists(favorites_xml):
                       try:   
                        if not os.path.exists("/etc/WebMedia"):
                           os.makedirs("/etc/WebMedia")
                        copyfile(THISPLUG+"/lib/defaults/favorites.xml",favorites_xml)
                       except:
                        return 
                try:        
                       from Plugins.Extensions.WebMedia.lib.favorites import getfavorites
                except:       
                       from lib.favorites import getfavorites
                favlist=getfavorites(self.plug)
                names2=[]
                urls2=[]
                names2.append("Exit")
                urls2.append("")
                for fav in favlist:
                     names2.append(fav[0])
                     urls2.append(fav[1])
                self.session.open(Favorites, names2, urls2)
                return

                                    
            else:

                  self["info"].setText("Please wait..")
                  self.keylock=True
                  self.startSpinner()
#                  dellog()
                  self.rundef = Videos3(self.session, name, url, self.nextrun,self.progressCallBack)
                  self.rundef.start()
                  
                  
##################################                  
#    plugin://plugin.video.youtube/kodion/search/query/?q=adele             
    def searchCallback(self,search_txt): 
          if search_txt:
               print "In Videos2 self.url 2=", self.url
               print "In Videos2 search_txt 1=", search_txt
               n1 = self.url.find("?", 0)
#               if "plugin.video.youtube" in THISADDON:
#                       self.url = self.url[:(n1+1)] + "plugin://plugin.video.youtube/kodion/search/query/?q=" + search_txt
               
#               else:
#                       print "In Videos2 search_txt 2=", search_txt
               file=open("/tmp/xbmc_search.txt",'w')
               file.write(search_txt)
               file.close()
               self["info"].setText(_("Please wait.."))
               self.keylock=True 
               rundef = Videos3(self.session, self.name, self.url, 2,self.progressCallBack)
               rundef.start() 
               if rundef.error:
                      self["info"].setText(_("Error:")+rundef.error)  
####################################                                 

#mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm                
#class StartPlugin_mainmenu(Screen):
class Supports(Screen):
    def __init__(self, session, name):
		Screen.__init__(self, session)
		
                self.skin = WM.skin
                self.name = name
                title = (_("Addons"))
                print "StartPlugin_mainmenu 1"
                self.setTitle(title)
                self.session=session
                self["bild"] = startspinner()
                self.spinner_running=False
                self["label1"] = StaticText("")
		self["label2"] = StaticText("")
		self["label20"] = StaticText("")
		self["label3"] = StaticText("")
		self["label30"] = StaticText("")
		self["label4"] = StaticText("")
		self["info"] = Label()
		global newstext
		news = newstext
		self.cancel=False
		self.data1=''
		self.keylock=False
		self.progress=(_(" "))
#		print "In StartPlugin_mainmenu newstext =", newstext

                self["info"].setText("Addons")

		self["pixmap"] = Pixmap()
		self["pixmap1"] = Pixmap()
		self.list = []                
                self["list"] = List(self.list)
                self["list"] = RSList([])
#		self["info"] = Label()
		self["pixmap"] = Pixmap()
		self.progress=(_(" "))
		self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Select"))
		self["key_yellow"] = Button(_(" "))
		self["key_blue"] = Button(_(" "))
                system("rm /tmp/select.txt")
                
                
                self["list"].onSelectionChanged.append(self.selection_changed)
                self.onShown.append(self.selection_changed)                
                self["actions"] = NumberActionMap(["OkCancelActions", "ColorActions", "DirectionActions","EPGSelectActions"],{
                        "upRepeated": self.up,
                       "downRepeated": self.down,
                       "up": self.up,
                       "down": self.down,
                       "left": self.left,
                       "right":self.right,
                       "red": self.close,
		       "green": self.okClicked,
		       "yellow": self.close,
		       "blue": self.close,
                       "ok": self.okClicked,
                       "info":self.close,                     
                       "cancel": self.exit,}, -1)
########################
                self.updateTimer = eTimer()
                try:
                      self.updateTimer_conn = self.updateTimer.timeout.connect(self.updateStatus)
                except AttributeError:
                      self.updateTimer.callback.append(self.updateStatus)
                self.timecount = 0
                ncount = config.plugins.webmedia.wait.value 
                nc = int(ncount)*1000
                timeint = int(float(nc/120))
                print "timeint =", timeint
                self.timeint = 1000
                self.nct = int(float(nc/self.timeint))
                print "self.nct =", self.nct
########################                
                self.pos = 0
                self.num = 0
                self.urls = []
                self.names = []
                self.shortnms = []
                self.data = []
                self.missed = " "
                self.shlist = " "
                """
                try:
                       self.fixscripts()
                except:       
                       pass
                """       
                print "StartPlugin_mainmenu 2"
#                self.onLayoutFinish.append(self.listplugs)
                self.onShown.append(self.okClicked)
#                self.onLayoutFinish.append(self.okClicked)        
    def exit(self):          
           self.close()
           
    def fixscripts(self):
                url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/list.txt"
                self.fixlist = getUrl(url)
                print "self.fixlist =", self.fixlist
                pathsh = THISPLUG + "/scripts"
                for name in os.listdir(pathsh):
                        self.name = name
                        self.checkfixsh()
                return                  

    def delete(self):
                global ADDONCAT
                ADDONCAT = "plugins"
                self.session.openWithCallback(self.listplugs, DelAdd)           

    def addon(self):
                global ADDONCAT
                ADDONCAT = "plugins"
                self.session.openWithCallback(self.listplugs, Getadds)           

            
    def conf(self):            
          self.session.open(XbmcConfigScreen)

    def selection_changed(self):
      self.keylock=False
      
      
      try:
        pos = self["list"].getSelectionIndex()
        name = self.names[pos]    
      except:
        pass

    def up(self):
         if self.keylock:
                   return
         dedesc = " "
         endesc = " "
         itdesc = " "
         self["list"].up()
         self.pos = self.pos - 1
         num = len(self.names)
         if self.pos == -1:
                self.pos = num - 1
                self["list"].moveToIndex(self.pos) 
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/" + ADDONCAT + "/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc= self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")  
                
    def down(self):
         if self.keylock:
                   return    
    
         dedesc = " "
         endesc = " "
         itdesc = " "

         self["list"].down()
         self.pos = self.pos + 1
         num = len(self.names)
         if self.pos == num:
                self.pos = 0
                self["list"].moveToIndex(0)  
         name = self.names[self.pos]
         if DEBUG == 1:
                print "name =", name
         if self.pos > 0:
                pic1 = THISPLUG + "/" + ADDONCAT + "/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                if DEBUG == 1:
                       print "name B=", name
                pname, version, prov, desc= self.getinfo(name)

                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                desc = desc.replace(":", "-")
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")  
                
    def left(self):
         if self.keylock:
                   return
         self["list"].pageUp()
         self.pos = self["list"].getSelectionIndex()
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/" + ADDONCAT + "/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc = self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap1"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ")                        
                self.error=None
    def right(self):
         if self.keylock:
                   return
         self["list"].pageDown()
         self.pos = self["list"].getSelectionIndex()
         name = self.names[self.pos]
         if self.pos > 0:
                pic1 = THISPLUG + "/" + ADDONCAT + "/" + name + "/icon.png"
                self["pixmap1"].instance.setPixmapFromFile(pic1)
                pname, version, prov, desc = self.getinfo(name)
                
                self["label1"].setText(pname)
                self["label20"].setText("Version :")
                self["label2"].setText(version)
                self["label30"].setText("Provider :")
                self["label3"].setText(prov)
                self["label4"].setText(desc)
         else:      
                if self.pos == 0:
                       if config.plugins.webmedia.skinres.value == "fullhd":
                                pic1 = THISPLUG + "/skin/images/ExitL.png"
                       else:
                                pic1 = THISPLUG + "/skin/images/Exit.png"
                       self["pixmap"].instance.setPixmapFromFile(pic1)
                self["label1"].setText(" ")
                self["label20"].setText(" ")
                self["label2"].setText(" ")
                self["label30"].setText(" ")
                self["label3"].setText(" ")
                self["label4"].setText(" ") 
                                      

    def getinfo(self, name):            
                xfile = THISPLUG + "/" + ADDONCAT + "/" + name + "/addon.xml"
                dedesc = ' '
                endesc = ' '
                itdesc = ' '
                try:tree = xml.etree.cElementTree.parse(xfile)
                except: return "", "", "", ""
                root = tree.getroot()
                pname = str(root.get('name'))
                version = str(root.get('version'))
                prov = str(root.get('provider-name'))
                try:
                    for description in root.iter('description'):
                        lang = description.get('lang')
                        desc = str(description.text)
                        if lang == "de":
                              dedesc = desc
                        elif lang == "it":
                              itdesc = desc      
                        else:      
                              endesc = desc
                except:
                    for description in root.getiterator('description'):
                        lang = description.get('lang')
                        desc = str(description.text)
                        if lang == "de":
                              dedesc = desc
                        elif lang == "it":
                              itdesc = desc      
                        else:      
                              endesc = desc
                              
                if config.osd.language.value == "de_DE":
                              desc2 = dedesc
                elif config.osd.language.value == "it_IT":
                              desc2 = itdesc                               
                else:
                              desc2 = endesc
                if desc2 == ' ':
                              desc2 = endesc               
                              
                return pname, version, prov, desc2
                
    def listplugs(self):
                print "In listplugs 1"
                self.urls = []
                self.names = []
                self.shortnms = []
                path = THISPLUG + "/plugins"
                self.names.append("Exit")
                self.shortnms.append("Exit")
                self.urls.append("0")
                i = 1

                for name in os.listdir(path):
                   
                    if "__init__" in name:
                       continue
                    if "plugin.video" not in name:
                       continue
                    else:      
                              print "In listplugs 2"
                              self.names.append(name)
#                              name1 = name[13:]
                              print "In listplugs name =", name
                              if "plugin.video." in name:
                                     name1 = name.replace("plugin.video.", "")
                              print "In listplugs name1 =", name1
                              self.shortnms.append(name1) 
                              self.urls.append(i)
                              i = i+1
                self.num = i
                showlist(self.shortnms, self["list"])
##################################  
    def checkfixsh(self):
                print "self.name =", self.name
                if not self.name in self.fixlist:
                        return
                else:
                        plug = self.name + "-fix.1.0.0.zip"
                        xurl = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/" + plug
                        print "xurl =", xurl
                        xdest = "/tmp/plug.zip"
                        cmd1 = "wget -O " + xdest + " " + xurl
                        fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/scripts"
                        cmd2 = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                        cmd = cmd1 + " && " + cmd2                
                        print "In checkfixsh cmd =", cmd
                        title = (_("Installing addon fix"))
                        os.system(cmd)
                        return
##################################               
    def checkUpd(self):           
                ltxt = "In checkUpd self.name = "+ self.name
                print ltxt
                tfile = THISPLUG + "/" + ADDONCAT + "/" + self.name + "/addon.xml"
                f = open(tfile, "r")       
                txt = f.read()
                print "In checkUpd txt = ", txt
                n1 = txt.find('<addon', 0)
                n11 = txt.find('id', n1)
                n2 = txt.find("version", n11)
                n3 = txt.find('"', n2)
                n31 = txt.find("'", n2)
                if n31 > -1:
                       if n31 < n3:
                              n4 = txt.find("'", (n31+2))
                              version = txt[(n31+1):n4]
                       else:
                              n4 = txt.find('"', (n3+2))
                              version = txt[(n3+1):n4]
                else:       
                       n4 = txt.find('"', (n3+2))
                       version = txt[(n3+1):n4]
                print "In checkUpd version = ", version
                f.close()
                try:
                       file1 = THISPLUG + "/adlist.txt"
                       f1=open(file1,"r+")
                       fpage = f1.read()
                except:       
                       fpage = " "
                
                self.fpage = fpage
#                tfile2 = THISPLUG + "/adlist.txt"      
#                f2 = open(tfile2, "r")
#                fpage = f2.read()
                lines = fpage.splitlines()
                
#                f2.close()
                nlist = 0
                for line in lines: 
#                       log("\nIn checkUpd line ="+ line)
#                       log("\nIn checkUpd self.name B="+ self.name)   
                       if line.startswith("#####"):
                             continue
                       elif "###" not in line:
                             continue  
#                       elif (not self.name in line) and (not "pelisalacarta" in line) and (not "tvalacarta" in line):
                       elif not self.name in line:
                             continue
                       else:        
                             nlist = 1 #addon in adlist.txt    
                             print "In checkUpd line B=", line
                             print "In checkUpd self.name c=", self.name   
                             items = line.split("###")
                             n = len(items)
                             print "In checkUpd items =", items
                             name = items[0]
                             url1 = items[1]
                             if items[2] != '': 
                                   url2 = items[2]
                                   self.checkLine(line, version) 
                                   break
                             else:      
                                   print "In checkUpd going in self.okClicked2 "
                                   self.okClicked2()

                if nlist == 0: # user added addon
                       self.okClicked2()


    def checkLine(self, line, version):
           print "In checkLine line =", line
           items = line.split("###")
           print "In checkLine items =", items
           name = items[0]
           url1 = items[1]
           url2 = items[2]
           if url2 == '':
                self.okClicked2()
           else:       
                url2 = items[2]
                n2 = url1.find(".zip", 0)
                n3 = url1.rfind(name, 0, n2)
                n4 = n3 + len(name) + 1
                url0 = url1[:n4] 
                print  "url0 =", url0
                xurl = url2
                xdest = "/tmp/down.txt"
                self.line = line
                self.version = version
                self.name = name
                self.url1 = url1
                self.url2 = url2
                self.url0 = url0 
#                fpage = urlopen(url2).read()
                downloadPage(xurl, xdest).addCallback(self.getdown).addErrback(self.showError)

    def showError(self, error):
                print "ERROR :", error

    def getdown(self, fplug):                
                fpage = open("/tmp/down.txt", "r").read()
                
                if self.url2.endswith(".xml"):
                        rx = 'addo.*?id="' + self.name + '".*?version="(.*?)"'
                else:
                        rx = self.name + '-(.*?).zip'
                match = re.compile(rx,re.DOTALL).findall(fpage)
                print  "match =", match
                if len(match) == 0:
                        rx = self.name + '_(.*?).zip'
                        match = re.compile(rx,re.DOTALL).findall(fpage)
                        print  "match 2=", match
                try:        
                        latest = findmax(match)
                except:        
                        latest = max(match) 
                latest = latest.replace("%7E", "~")                       
                print "latest =", latest
                print  "self.version =", self.version
                if latest != self.version:
#                    if not self.url1.endswith(".zip"):  #datadirectory zip false
#                        self.session.open(GetaddonsA3, self.line)           
#                    else:
                        self.xurl = self.url0 + latest + ".zip"
                        print  "self.xurl =", self.xurl
                        txt = _("New version ") + latest + _(" is available. Update Now ?")
                        print txt
                        self.session.openWithCallback(self.do_update, MessageBox, txt, type = 0)
                else:
                        self.okClicked2()
                               

    def do_update(self, answer):
                if answer is None:
                       self.okClicked2()
                else:
                       if answer is False:
                               self.okClicked2()
                       else:
                               xurl = self.xurl
                               print  "self.xurl=", self.xurl
                               xdest = "/tmp/plug.zip"
	                       downloadPage(xurl, xdest).addCallback(self.install).addErrback(self.showError)

    def install(self, fplug):
                fdest = THISPLUG + "/" + ADDONCAT + ""
                addon = THISPLUG + "/" + ADDONCAT + "/" + self.name
                cmd1 = "rm -rf '" + addon + "'" 
                cmd2 = " unzip -o -q '/tmp/plug.zip' -d '" + fdest + "'"
                cmd3 = " cp -f '" + THISPLUG + "/xpath.py' " + addon 
                cmd = cmd1 + " && " + cmd2 + " && " + cmd3
                print "cmd =", cmd
                title = _("Installing ") + self.name
#                self.session.open(Console,_(title),[cmd])
                print "self.session 1=", self.session
                self.session.openWithCallback(self.checkName,Console,_(title),[cmd])
                
    def checkName(self):
                path = THISPLUG + "/" + ADDONCAT 
                for name in os.listdir(path):
                       print "name =", name
                       if "plugin" not in name:
                           if "__init" in name:
                               continue
                           elif "E2" in name:
                               self.close()
                           else:    
                               newname = "plugin.video." + name
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if "-master" in name:
                               newname = name.replace("-master", "")
                               cmd = "mv " + path + "/" + name + " " + path + "/" + newname + " &"
                               os.system(cmd) 
                       if ("pelisalacarta" in name) or ("tvalacarta" in name):
                               cmd = "rm '" + path + "/" + name + "/fixed2'"        
                               os.system(cmd)
                               
                self.close()
#                self.checkfix() Not necessary as okclick2 calls it.

    def checkfix(self):
                url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/list.txt"
                self.fixlist = getUrl(url)
                print "In checkfix self.fixlist =", self.fixlist
                print "In checkfix self.name =", self.name
                if self.name in self.fixlist:
                        plug = self.name + "-fix.1.0.0.zip"
                        xurl = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Fix/" + plug
                        print "xurl =", xurl
                        xdest = "/tmp/plug.zip"
	                downloadPage(xurl, xdest).addCallback(self.installB).addErrback(self.showError)
                else:
                        print "No fix to install"
                        self.stream()
                                      
    def installB(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/" + ADDONCAT
                cmd = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                
                print "In installB cmd =", cmd
                title = (_("Installing addon fix"))
                os.system(cmd)
                self.stream()

##nnnnnnnnnnnnnnnnnnnnnnnnnnnnn
    def checkImports(self):
                pass
                
    def checkImportsX(self):
                self["info"].setText("Please wait...")
                """
                xmfile = THISPLUG+"/" + ADDONCAT + "/"+self.id+"/resources/settings.xml"
                tmpfile = THISPLUG+"/ofile.xml"
                if os.path.exists(xmfile):
                       f = open(xmfile, "r")
                       f1 = open(tmpfile, "w")
                       ftxt = f.read()
                       ftxt = ftxt.decode("ISO-8859-1")
                       f1.write(ftxt)
                       f.close()
                       f1.close()
                       print "Here in checkImports copying tmpfile to ", xmfile 
                       cmd = "cp -f " + tmpfile + " " + xmfile + " && rm " + tmpfile
                       print "Here in checkImports cmd ", cmd 
                       os.system(cmd)
                """
###################################################### 
                print "In checkImports 1"
                self.shlist = " "
                self.plugins = " "
                scripts = THISPLUG + "/scripts"
                for name in os.listdir(scripts):
                              self.shlist = self.shlist + name + " "
                              
                plugins = THISPLUG + "/" + ADDONCAT
                for name in os.listdir(plugins):
                              self.plugins = self.plugins + name + " "                              
                print "In checkImports 2"              
                import xbmcaddon
                try:
                  sys.argv[0]=THISPLUG+"/" + ADDONCAT + "/"+self.id+"/default.py"
                except:
                  import sys
                  sys.argv=[]
                  sys.argv.append(THISPLUG+"/" + ADDONCAT + "/"+self.id+"/default.py")
                update_xbmc_text(self.id) 
                print "In checkImports 3"                 
                addon = xbmcaddon.Addon(self.id)
                path = addon.getAddonInfo("path")
                print "In checkImports self.id =", self.id 
                print "In checkImports path =", path            
                xfile = path + "/addon.xml" 
                tree = xml.etree.cElementTree.parse(xfile)
                root = tree.getroot()
                self.missed = ""
                i = 0
                try:
                  for x in root.iter('import'):
                    addon = x.get('addon') + " " #to get xbmcswift not xbmcswift2
                    if "xbmc.python" in addon:
                          continue
                    if "xbmc.addon" in addon:
                          continue   
                    if "repository." in addon:
                          continue
                    if "artwork" in addon:
                          continue               
                    if addon in self.shlist or addon in self.plugins:
                          continue
                    self.missed = self.missed + " " + addon
                    i = 1                 
                except:
                  for x in root.getiterator('import'):
                    addon = x.get('addon') + " "
                    if "xbmc.python" in addon:
                          continue
                    if "xbmc.addon" in addon:
                          continue          
                    if addon in self.shlist or addon in self.plugins:
                          continue
                    self.missed = self.missed + " " + addon
                    i = 1
                if i == 0:
                    arg = "'" + THISPLUG.strip() + "/" + ADDONCAT + "/" + self.name.strip() + "/default.py' '1' ''"
                    self.arg = arg
#                    self.stream() 
                    self.checkfix()
                else:
                    self["info"].setText("Please wait.......\nChecking required scripts......")
                    self.shlist = " "
                    self.plugins=" "
#####################################################
                    url ="http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Script-modules/kodi/list.txt"
                    try:
                       self.sclist = getUrl(url)
                    except:
                       self.sclist = " "
#                    print "self.sclist =", self.sclist
                ########################
                    url1 ="http://mirrors.kodi.tv/addons/krypton/addons.xml"
                    getPage(url1).addCallback(self.gotPage).addErrback(self.getfeedError)
          
    def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error
		html = " "
                self.gotPage(html)
                
    def gotPage(self, html):
                    self.fdlist = html
###################################################### 
                    file1 = THISPLUG + "/adlist.txt"
                    f1=open(file1,"r")
                    adlst = f1.read()
                    f1.close()
######################################################
                    missed = self.missed
                    print "missed = [", missed
                    items = missed.split(" ") 
                    print "items =", items
                    i1 = 0
                    for item in items:
#                        if item == "":
#                             continue  
                        print "In checkImports item =", item
                        ###################################
                        """
                        if item in adlst:
                             file1 = THISPLUG + "/adlist.txt"
                             f1=open(file1,"r")
                             for line in f1.readlines():
                                    if item in line:
                                            print "In checkImports line =", line
                                            getaddon = GetaddonsA2(self.session, "scripts")
                                            getaddon.checkLine(line)
                                            f1.close() 
                                            self.close()
                        """                    
                        ###################################
                        sitem = 'addon id="' + item + '"'
                        n1 = self.fdlist.find(sitem, 0)
                        if item == "":
                             continue  

                        if n1 >-1:
                             i1 = i1+1
                             print "In checkImports i1 =", i1
                             if i1>1:
                                    break
                             print "In checkImports item 4=", item
                             n2 = self.fdlist.find('version="', n1)
                             n3 = self.fdlist.find('"', (n2+10))
                             ver = self.fdlist[(n2+9):n3]      
                             itemurl = "http://mirrors.kodi.tv/addons/krypton/" + item + "/" + item + "-" + ver + ".zip"
                             commands = []
                             if "script." in item:
                                     print "In download item 5=", item
                                     self.plug = item + ".zip"
                                     fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/scripts"
                                     dest = "/tmp/" + self.plug
                                     xurl = itemurl
#                                     self.item = item
                                     downloadPage(xurl, dest).addCallback(self.installsc).addErrback(self.showError2)
                                     
#                             elif "plugin.video" in item:
                             else:

                                     self.plug = item + ".zip"
                                     fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/" + ADDONCAT
                                     dest = "/tmp/" + self.plug
                                     xurl = itemurl
#                                     self.item = item
                                     downloadPage(xurl, dest).addCallback(self.installpl).addErrback(self.showError2)
                                     
                        else:
                                     i1 = i1+1
                                     print "In checkImports i1 =", i1
                                     if i1>1:
                                             break
                                     txt = "Missing : " + item + "\nGet from Install addon->WebMedia list or the internet."
                                     print "In checkimports not in krypton", txt 
                                     self["info"].setText(txt)
                        
    def showError2(self, error=""):
		error = str(error)
		print "Download error =", error
		print "Download failed for ", self.item
		self["info"].setText(txt)
		self.listplugs()
		
    def installC(self, fplug):
                cmd = "unzip -o -q '" + self.dest + "' -d " + self.fdest
                
                print "In installC cmd =", cmd
                title = (_("Installing missing ")) + self.item
                self.session.openWithCallback(self.close,Console,_(title),[cmd])
                self.close()
          
    def installsc(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/scripts"
                dest = "/tmp/" + self.plug    
                cmd = "unzip -o -q '" + dest + "' -d " + fdest
                print "In installsc cmd =", cmd
#                title = (_("Installing missing ")) + self.item
                title = (_("Installing missing ")) + self.plug
                self.session.openWithCallback(self.close,Console,_(title),[cmd])
                self.close()

    def installpl(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/" + ADDONCAT
                dest = "/tmp/" + self.plug    
                cmd = "unzip -o -q '" + dest + "' -d " + fdest
                print "In installpl cmd =", cmd
                title = (_("Installing missing ")) + self.plug
                self.session.openWithCallback(self.close,Console,_(title),[cmd])
                self.close()
          
#mmmmmmmmmmmmmmmmmmmmmmmmmm            
##################################
    def okClicked(self):
                       """
                if self.keylock:
                   return    
    
                print "In StartPlugin_mainmenu okClicked"
                idx = self["list"].getSelectionIndex()
                if DEBUG == 1:
                       print "idx =", idx
                if idx == 0:
                       self.close()
#                elif "Get more" in self.names[idx]:       
#                       self.addon()
                else:       
                       self.name = self.names[idx]
                       """
#                       self.name = "videodevil"
                       self.nameplug = self.name
                       
                       print "In StartPlugin_mainmenu okClicked B self.name =", self.name
########################################
                       """
                       print "In StartPlugin_mainmenu okClicked B ADDONCAT =", ADDONCAT
                       if ADDONCAT == "plugins":
                             if self.name.endswith("E2"):
                                     self.runE2plug(self.name) 
                             else:        
#                                     self.checkUpd()
                                     self.okClicked2()
                       else:
                             self.okClicked2()
                       """
                       self.okClicked2()       
                                     
    def runE2plug(self, name):
        try:
           from Plugins.Extensions.WebMedia.Execlist import Execlist
           Execlist(self.session, name)
        except:
           from Execlist import Execlist
           Execlist(self.session, name)

    def okClicked2(self):
                       global SELECT
                       SELECT=[]
                       SELECT.append(self.name)
                       SELECT.append("1")
                       SELECT[1] = self.name
                       print "In StartPlugin_mainmenu SELECT[0] =", SELECT[1]
		       self.id = self.nameplug
		       self.name = self.nameplug
		       f = open("/tmp/kodiplug.txt", "w")
		       tplug = self.id + "\n"
		       f.write(tplug)
		       f.close()
		       """
		       if ADDONCAT == "plugins":
#		              self.defaultpy()
#		              self.checkImports()
#		       else:  
                       """
		       arg = "'" + THISPLUG.strip() + "/plugins/" + self.name.strip() + "/default.py' '1' ''"
                       self.arg = arg
                       print "In StartPlugin_mainmenu going in stream self.arg =", self.arg
                       self.stream() 
                       
###############################
    def defaultpy(self):
        pass
        
    def defaultpyX(self):
        global THISADDON
        THISADDON = THISPLUG + "/plugins/" + self.id
        print "In defaultpy THISADDON =", THISADDON
        dpath = THISADDON + "/default.py"
        if not os.path.exists(dpath):
               fmod = self.findmod()
               cmd = "mv " + THISADDON + "/" + fmod + " " + THISADDON + "/default.py"
               print "cmd =", cmd
               os.system(cmd)

        tfile = THISPLUG + "/added.txt"
        f = open(tfile, 'r')
        addtxt = f.read()
        f.close()

        fpath1 = THISPLUG + "/plugins/" + self.id 
        fpath2 = fpath1 + "/fixed2"
        fpathf = fpath1 + "/default.py"
        f = open(fpathf, 'r')
        deftxtf = f.read()
        f.close()
        if fileExists(fpath2):
#        if "import sys, xpath, xbmc" in deftxtf:
            addtxt2 = "\nf = file('/tmp/e.log', 'a')\nsys.stdout = f\n"
            fpath = fpath1 + "/default.py"
            f = open(fpath, 'r')
            deftxt = f.read()
            f.close()
            if addtxt2 in deftxt:
               f1 = open('/tmp/default.txt', 'w')
               icount =0
               deftxt3 = deftxt.replace(addtxt2, "\n")
               f1.write(deftxt3)
               
               f.close()
               f1.close()
               cmd = "rm " + fpath + " && cp /tmp/default.txt " + fpath  
               os.system(cmd)
              
            else:
               pass  
               
        else:                   
            fpath = fpath1 + "/default.py"
            f = open(fpath, 'r')
            deftxt = f.read()
            print "In defaultpy deftxt =", deftxt
            x = ord(deftxt[0])
            x1 = ord(deftxt[1])
            x2 = ord(deftxt[2])
            x3 = ord(deftxt[3])
            xm = max([x,x1,x2,x3]) 
            print "In defaultpy nonasci xm =",  xm
            if xm > 127:
                   n1 = deftxt.find("#", 0)
                   if n1 == -1:
                          n1 = 1000
                   n2 = deftxt.find("import", 0)
                   if n2 == -1:
                          n2 = 1000
                   n3 = deftxt.find("from", 0)
                   if n3 == -1:
                          n3 = 1000
                   nmin = min(n1, n2, n3)
                   print "nmin =", nmin
                   deftxt = deftxt[nmin:]

            print "In defaultpy deftxt B=", deftxt
            data = []
            data = deftxt.splitlines()
            f.close()            
            if addtxt not in deftxt:
               cmdrm = "rm " + fpath1 + "/xpath.py"
               os.system(cmdrm)
               f1 = open('/tmp/default.txt', 'w')
               icount =0
#               f = open(fpath, 'r')
               for line in data:
#                   line = line.decode("ISO-8859-1")
                   line = line + "\n"
                   if not (line.startswith("#")):
                       if icount==0:
                          f1.write(addtxt)
                          icount = 1
                       else:
                          pass   
                   f1.write(line)
               f.close()
               f1.close()
               cmd = "rm " + fpath + " && cp /tmp/default.txt " + fpath  
               os.system(cmd)
            cmd1 = "touch " + fpath2
            os.system(cmd1)


    def findmod(self):
                xfile = THISADDON + "/addon.xml"
                print "In plugin-py findmod xfile =", xfile
                f = open(xfile, "r")
                ftext = f.read()
                n1 = ftext.find("<extension", 0)
                n2 = ftext.find("library", n1)
                n3 = ftext.find('"', n2)
                n4 = ftext.find('"', (n3+1))
                fmod = ftext[(n3+1):n4]
                print "Newmod =", fmod
                return fmod



###############################
###############################
    def stream(self):
                print "In StartPlugin_mainmenu stream"
                self.picfold = config.plugins.webmedia.cachefold.value+"/xbmc/pic"
                self.tmpfold = config.plugins.webmedia.cachefold.value+"/xbmc/tmp"
                cmd = "rm " + self.tmpfold + "/*"
                system(cmd)
                system("rm /tmp/data.txt")
                system("rm /tmp/data.txt")
                system("rm /tmp/vidinfo.txt")
                system("rm /tmp/type.txt")
                if DEBUG == 1:
                       print "DEBUG =", DEBUG
                if DEBUG == 1:
                       print "StartPlugin_mainmenu self.arg =", self.arg
                cmd = "python " + self.arg
                cmd = cmd.replace("&", "\\&")
#                afile = file("/tmp/test.txt","w")       
#                afile.write("going in default.py")
#                afile.write(cmd)
#                if DEBUG == 1:
#                       print "going in default-py Now =", datetime.datetime.now()
#                system(cmd)
#######################################
                fdef ='default'# NEWDEFPY[:-3]
                arg1 = THISPLUG + "/" + ADDONCAT + "/" + self.name + "/default.py"
                arg2 = "1"
                arg3 = ""
                arg4=config.plugins.webmedia.cachefold.value
                sys.argv = [arg1,arg2, arg3,arg4]
                d = THISPLUG + "/" + ADDONCAT + "/" + self.name
                global THISADDON
                THISADDON = d
                self.plugin_id=self.name
                
                
                sys.argv = [arg1,arg2, arg3,arg4]
                d = THISADDON
                
#                dellog()       
                ###############################
                xpath_file=THISPLUG+"/" + ADDONCAT + "/"+self.name+"/xpath.py"
                fixed2_file=THISPLUG+"/" + ADDONCAT + "/"+self.name+"/fixed2"
                default_file=THISPLUG+"/" + ADDONCAT + "/"+self.name+"/default.py"
#                if not os.path.exists(xpath_file): 
                os.system("cp -f "+THISPLUG+"/lib/xpath.py "+xpath_file)
                cmd='python '+default_file+' 1 '+"'"+arg3+"'" 
                print cmd 
#######################
                            
                    
                if os.path.exists("/tmp/data.txt"):
                   os.remove("/tmp/data.txt")                
                timen = time.time() 
                global NTIME 
                NTIME = timen
                timenow = timen - NTIME
                print "In StartPlugin_mainmenu timenow", timenow
                print "In StartPlugin_mainmenu cmd =", cmd
                self.dtext = " "
                self.lastcmd = cmd
                global LAST
                LAST = self.lastcmd
                print "cmd = ", cmd
                self.p = os.popen(cmd)
                self.timecount = 0
                self.updateTimer.start(self.timeint)

              
    def updateStatus(self):
         ncount = config.plugins.webmedia.wait.value
#         nct = int(ncount)/4
         self.timecount = self.timecount + 1
         print "In StartPlugin_mainmenu updateStatus self.timecount =", self.timecount
         self.dtext = self.p.read()
         print "In StartPlugin_mainmenu updateStatus self.dtext =", self.dtext
         global dtext1
         if len(self.dtext) > 0:
                dtext1 = dtext1 + self.dtext
         if "data B" in self.dtext:
                self.updateTimer.stop()
                self.action(" ")
         print "In StartPlugin_mainmenu self.timecount =", self.timecount 
         if self.timecount > self.nct:     
              self.updateTimer.stop()
              f1=open("/tmp/e.log","a")
#              f1.write(dtext1)
              f1.close()
              self.action(" ")
    
    def action(self,retval):
    
                            
            self.keylock=False
            self.names2 = []
            self.urls2 = []
            self.pics2 = []
            self.names2.append("Exit")
            self.urls2.append(" ")
            self.pics2.append(" ")
            self.names2.append("Setup")
            self.urls2.append(" ")
            self.pics2.append(" ")
            self.names2.append("Favorites")
            self.urls2.append(" ")
            self.pics2.append(" ")            
            
            self.tmppics2 = []
            self.lines = []
            self.vidinfo = []
            afile = open("/tmp/test.txt","w")       
            afile.write("\nin action=")
            datain = " "
            parameters = []
            self.data = []
            print "StartPlugin_mainmenu self.dtext =", self.dtext
            data = self.dtext.splitlines()
            for line in data:
                   print "StartPlugin_mainmenu line =", line
                   if not "data B" in line: continue
                   else: 
                         i1 = line.find("&", 0)
                         line1 = line[i1:]
                         self.data.append(line1)
            print "StartPlugin_mainmenu self.data =", self.data
            

            if len(self.data) == 0:
                 cmd = LAST + " > /tmp/error.log 2>&1 &"
                 os.system(cmd)
                 self.error=(_("Error! Submit logs /tmp/e.log and /tmp/error.log."))
                 self["info"].setText(self.error)
                 return
            inum = len(self.data)
            print "StartPlugin_mainmenu inum =", inum
            n1 = 0
            if n1 == 0:
                 i = 0
                 while i < inum:
                        name = " "
                        url = " "
                        line = self.data[i]
                        print "StartPlugin_mainmenu line =", line
                        params = parameters_string_to_dict(line)
                        self.lines.append(line)
                        try:
                               name = params.get("name")
                               name = name.replace("AxNxD", "&")
                               name = name.replace("ExQ", "=")
                        except:
                               pass
                        try:
                              url = params.get("url")
                              url = url.replace("AxNxD", "&")
                              url = url.replace("ExQ", "=")
                        except:
                              pass
                        try:
                              pic = params.get("thumbnailImage")
                              if (pic == "DefaultFolder.png") or (pic is None):
                                     pic = THISPLUG + "/skin/images/default.png"
                              print "StartPlugin_mainmenu pic 1 =", pic       
                        except:
                              pic = THISPLUG + "/skin/images/default.png"
                        print "StartPlugin_mainmenu pic 2 =", pic         
                        self.name = name
                        self.names2.append(name)
                        self.urls2.append(url)
                        self.pics2.append(pic)
                        i = i+1
                 if (len(self.names2) == 2) and (self.urls2[1] is None) and (THISPLUG not in self.names2[1]):
                        if ("rtmp" in self.names2[1]):
                            if "live" in name:
                                name = self.name
                                desc = " "
                                url = self.names2[1]
#                                self.session.open(Showrtmp2, name, url, desc)
                                self.progressCallBack("Finished")
                                self.session.open(Playoptions, name, url, desc)
                                self.close()
                           
                            else:
                                name = self.name
                                desc = " "
                                url = self.names[1]
#                                self.session.open(Showrtmp, name, url, desc)
                                self.progressCallBack("Finished")
                                self.session.open(Playoptions, name, url, desc)
                                self.close()  

                        else:        
                                name = self.name                                
                                desc = " "
                                url = self.names2[1]
                                self.progressCallBack("Finished")
                                self.session.open(Playoptions, name, url, desc)
                                self.close()
                 elif (len(self.names2) == 2) and (self.urls2[1] is not None) and (THISPLUG not in self.urls2[1]):
                                name = self.name                                
                                desc = " "
                                url = self.urls2[1]
                                self.progressCallBack("Finished")
                                self.session.open(Playoptions, name, url, desc)
                                self.close()
                 else:        
                        if DEBUG == 1:
                                print "StartPlugin_mainmenu self.names2 =", self.names2
                                print "StartPlugin_mainmenu self.urls2 =", self.urls2
                                print "StartPlugin_mainmenu self.pics2 =", self.pics2
                        self.tmppics2 = self.pics2
                        if self.cancel==True:
                           return
                        
                        if ("plugin.image" in self.id) or ("plugin.picture" in self.id):
                                print "StartPlugin_mainmenu going in Videos2P"
                                from picture import Videos2P
                                self.session.open(Videos2P, self.id, self.names2, self.urls2, self.tmppics2,1, SELECT)
                        else:
                                print "StartPlugin_mainmenu going in Videos2"
                                self.session.open(Videos2, self.id, self.names2, self.urls2, self.tmppics2,1)
                         

##################################################################################################
































