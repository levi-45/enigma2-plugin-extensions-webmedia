
#20200329
from Plugins.Extensions.WebMedia.lib.Utils import *
from Components.ConfigList import *
from Components.config import *
from Components.Sources.List import List
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Sources.StaticText import StaticText
from Tools.Directories import resolveFilename, SCOPE_SKIN, SCOPE_SKIN_IMAGE, SCOPE_FONTS, SCOPE_CURRENT_SKIN, SCOPE_CONFIG, fileExists
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from enigma import eConsoleAppContainer, loadPNG, loadPic
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Screens.InputBox import PinInput
from twisted.web.client import downloadPage
import os, sys
import urllib2
import base64

##### updated 20200222 #####

DESKHEIGHT = getDesktop(0).size().height()
# import httplib
# httplib.HTTPConnection.debuglevel = 2

if DESKHEIGHT > 1000:
      from skin import *
else:
      from skin1 import *
############################################################
#                                                          #
#   Coded by pcd@Sept 2019             #                   #
#                                                          #
############################################################


THISPLUG= '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia'

def InfoVersion():
    version = THISPLUG+'/version.txt'
    v1 = open(version, 'r')
    version = v1.read()
    print 'version:', version
    return version
   
    
host = 'aHR0cDovL3BhdGJ1d2ViLmNvbQ=='
ServerS1 = base64.b64decode(host)


def getUrl(url):
      print "Here in getUrl url =", url
      req = urllib2.Request(url)
      req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link


config.plugins.webmedia = ConfigSubsection()
config.plugins.webmedia.elog= ConfigYesNo(True)
config.plugins.webmedia.tempdel = ConfigYesNo(True)
config.plugins.webmedia.cachefold = ConfigText("/media/hdd", False)
config.plugins.webmedia.thumb = ConfigSelection(default = "True", choices = [("True", _("yes")),("False", _("no"))]) 
config.plugins.webmedia.adult = ConfigYesNo(False)
config.plugins.webmedia.useragent = NoSave(ConfigText(default="Mozilla/5.0 (Windows; U; Windows NT 6.1; de; rv:1.9.2.17) Gecko/20110420 Firefox/3.6.17"))
config.plugins.webmedia.pixpage = NoSave(ConfigText(default = "None"))
config.plugins.webmedia.skinres = ConfigSelection(default = "fullhd", choices = [("fullhd", _("Full-HD 1920x1080")), ("hd", _("HD 1280x720"))])  
config.plugins.webmedia.directpl = NoSave(ConfigYesNo(False))
config.plugins.webmedia.wait = ConfigSelection(default = "10", choices = [("10", _("10sec")),("20", _("20sec")),("30", _("30sec")),("40", _("40sec")),("60", _("60sec")), ("120", _("120sec")), ("180", _("180sec")), ("240", _("240sec")), ("300", _("300sec"))])  
config.plugins.webmedia.vlcip = ConfigText("192.168.1.1", False)
#################################
                    

#################################
class WMConfigScreen(Screen, ConfigListScreen):
            
    def __init__(self, session, args = 0):
            Screen.__init__(self, session)
            self.session = session
            ##########################
            
            self.skin = ConfWebmed.skin

            self.list = []
            self['config'] = List(self.list)
            
#            self['info'] = Label(_("by PCD ") + InfoVersion())
            self.setup_title = _("Plugin Configuration")            
            # cfg = config.plugins.webmedia 
            # self.list = [
                        # getConfigListEntry(_("Enigma log (/tmp/e.log) ?"), cfg.elog),
                        # getConfigListEntry(_("Skin resolution ?"), cfg.skinres),
                        # getConfigListEntry(_("Show thumpics ?"), cfg.thumb),
                        # getConfigListEntry(_("Stop download at Exit from plugin ?"), cfg.tempdel),
                        # getConfigListEntry(_("Cache folder"), cfg.cachefold),
                        # ]
                  
                  
            ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
            self["status"] = Label()
            self["statusbar"] = Label()
            self["key_red"] = Button(_("Exit"))
            self["key_green"] = Button(_("Save"))
#           self["key_yellow"] = Button(_("Kategorier"))
#           self["key_blue"] = Button(_("Play"))
            self["description"] = Label(_(' '))
            
            self["setupActions"] = ActionMap(["SetupActions",'DirectionActions', "ColorActions", "TimerEditActions"],
            {
                  "red": self.cancel,
                  "green": self.save,
#                 "yellow": self.start,
#                 "blue": self.play,
                  "cancel": self.cancel,
                  "ok": self.save,
            }, -2)
            self.onChangedEntry = []
            
            self.createSetup()
            
#            self.onLayoutFinish.append(self.layoutFinished)            
                
		
    def layoutFinished(self):
                self.setTitle(self.setup_title)
        
        
    def createSetup(self):
        self.list = []
        cfg = config.plugins.webmedia 
        self.list.append(getConfigListEntry(_("Enigma log (/tmp/e.log) ?"), cfg.elog, _("Produce Log")))
        self.list.append(getConfigListEntry(_("Skin resolution ?"), cfg.skinres, _("Resolution Skin")))
        self.list.append(getConfigListEntry(_("Show thumpics ?"), cfg.thumb, _("Show thumpics")))
#       self.list.append(getConfigListEntry(_("Stop download at Exit from plugin ?"), cfg.tempdel)),
        self.list.append(getConfigListEntry(_("Cache folder"), cfg.cachefold, _("Cache folder")))
        self.list.append(getConfigListEntry(_("Wait time for lists (sec)"), cfg.wait, _("Wait time for lists (sec)")))
        self.list.append(getConfigListEntry(_("vlc server ip"), cfg.vlcip, _("vlc server ip")))
        self["config"].list = self.list
        self["config"].setList(self.list)

    def changedEntry(self):
          for x in self.onChangedEntry:
                  x()
          
    def getCurrentEntry(self):
          return self["config"].getCurrent()[0]
          
    def getCurrentValue(self):
          return str(self["config"].getCurrent()[1].getText())
          
    def createSummary(self):
          from Screens.Setup import SetupSummary
          return SetupSummary

    def save(self):
          self.saveAll()
          self.session.open(TryQuitMainloop, 3) 

    def cancel(self):
          for x in self["config"].list:
                  x[1].cancel()
          self.close()

    def keyLeft(self):
            ConfigListScreen.keyLeft(self)
            print "current selection:", self["config"].l.getCurrentSelection()
            self.createSetup()

    def keyRight(self):
            ConfigListScreen.keyRight(self)
            print "current selection:", self["config"].l.getCurrentSelection()
            self.createSetup()


############################################################
class Webmedia(Screen):

    def __init__(self, session):
            Screen.__init__(self, session)    
            print "In WebMedia 1"
            self.session = session    
            
            self.skin = WM.skin
            title = "WebMedia"
            self["title"] = Button(title)
            self.setup_title = _('Main Menu')
            self.info = " "   
            self["info"] = Label()
            self["info"].setText(" ")
#############################################                
            self.list = []
            self["list"] = List(self.list)
            self["list"] = RSList([])
            self.pinst = []
#############################################               
            self["key_red"] = Button(_("Delete plugins"))
            self["key_green"] = Button(_("Install plugins"))
            self["key_menu"] = Button(_("Menu"))            
            self["key_yellow"] = Button(_("Conf"))
            self["key_blue"] = Button(_("Install adult plugins"))
            self["actions"] = NumberActionMap(["OkCancelActions", "HelpActions", "DirectionActions", "NumberActions", "ColorActions","MenuActions"],
                  {
                        "ok": self.okbuttonClick,
                        "cancel": self.cancel,
                        "red": self.delete,
                        "green": self.install,
                        "yellow": self.conf, #another command free
                        "blue": self.allow,
                        "menu": self.pluginfo,
#                       "displayHelp": self.info
                  })
            self.html = " "   
#            self.onLayoutFinish.append(self.layoutFinished)    
            print "In WebMedia 2"
            self.openTest()

                
                
    def layoutFinished(self):
                self.setTitle(self.setup_title)
        
    def openTest(self):
                print "In openTest 1"
                self.names = []
                path = THISPLUG + "/plugins"
                for name in os.listdir(path):
                              print "In openTest 2"
                              if ".pyo" in name: continue
                              if "init" in name: continue
                              if not ".py" in name: continue                                                             
                              name = name.replace(".py", "")
                              self.names.append(name)
                              
                showlist(self.names, self["list"])        
                
    def install(self):
                fpage = getUrl(ServerS1 + '/WebMedia/PLUGS/list.txt')
                print "In install fpage =", fpage
                lines = fpage.splitlines()
                self.names = []
                for name in lines:
                    print "In install name =", name
                    if name.endswith(".zip"):
                             self.names.append((name, name))
                             print "In install self.names =", self.names
                    else:
                             continue
                print "In install self.names 2=", self.names
                self.session.openWithCallback(self.selected2, ChoiceBox, title="Select plugin to install", list=self.names)   
                              
    def selected2(self, plug):
            if plug: 
                xurl = ServerS1 + '/WebMedia/PLUGS/' + plug[0]                
                print "In selected2 xurl =", xurl
                xdest = "/tmp/plug.zip"
                downloadPage(xurl, xdest).addCallback(self.install3).addErrback(self.showError)
            else:
                # self.close()
                self.openTest()                

    def install3(self, plug):
                cmd = "rm -rf /tmp/WebMedia && unzip -o -q /tmp/plug.zip -d /tmp && cp -rf /tmp/WebMedia/* /usr/lib/enigma2/python/Plugins/Extensions/WebMedia && rm -rf /tmp/WebMedia"
                print "In install3 cmd =", cmd
                title = (_("Installing plugin"))
                os.system(cmd)
                ########
                self.openTest()
            

###########################################
    def allow(self):	        
             perm = config.ParentalControl.configured.value
             print "perm =", perm 
                
             if config.ParentalControl.configured.value:
                  #####print "Here Ad 1"
#                        from Screens.InputBox import InputBox, PinInput
                  self.session.openWithCallback(self.pinEntered, PinInput, pinList = [config.ParentalControl.setuppin.value], triesEntry = config.ParentalControl.retries.servicepin, title = _("Please enter the parental control pin code"), windowTitle = _("Enter pin code"))

             else:
                  #####print "Here Ad 2"
                        self.pinEntered(True)
#            return
       
    def pinEntered(self, result):
            #####print "Here Ad 3 result =", result
                if result:
                        self.adults()
                        # self.close()
                        self.openTest()
                else:
                  self.session.openWithCallback(self.close, MessageBox, _("The pin code you entered is wrong."), MessageBox.TYPE_ERROR)
                  # self.close()
	        
    def adults(self):                
#                path = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/adults"
                fpage = getUrl(ServerS1 + '/WebMedia/ADULT/list.txt')
                lines = fpage.splitlines()
                self.names = []
                for name in lines:
                    print "In adults name =", name
                    if name.endswith(".zip"):
                             self.names.append((name, name))
                             print "In adults self.names =", self.names
                    else:
                             continue
                print "In adults self.names 2=", self.names
                self.session.openWithCallback(self.selected1, ChoiceBox, title="Select plugin to install", list=self.names)   

    def selected1(self, plug):
            if plug: 
                xurl = ServerS1 + '/WebMedia/ADULT/' + plug[0]                
                print "In adults xurl =", xurl
                xdest = "/tmp/plug.zip"
                downloadPage(xurl, xdest).addCallback(self.install3).addErrback(self.showError)
            else:
                # self.close()
                self.openTest()                

    def install2(self, fplug):
                fdest = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia"
                cmd = "unzip -o -q '/tmp/plug.zip' -d " + fdest
                
                print "In install cmd =", cmd
                title = (_("Installing plugin"))
                os.system(cmd)
                #########
                self.openTest()                

    def showError(self, error):
                print "ERROR :", error
                 
###########################################
    def delete(self):
                self.names = []
                path = THISPLUG + "/plugins"
                for name in os.listdir(path):
                              print "In openTest 2"
                              if ".pyo" in name: continue
                              if "init" in name: continue                                                             
                              name = name.replace(".py", "")
                              self.names.append((name, name))
                self.session.openWithCallback(self.selected, ChoiceBox, title="Select plugin to remove", list=self.names)              
       
    def selected(self, selection):     
            if selection:    
                print "In selected selection =", selection              
                adn = THISPLUG + "/plugins/"+ selection[0] + ".py" 
                print "In selected adn =", adn
                if os.path.exists(adn):
                       os.remove(adn)
                adn = THISPLUG + "/plugins/"+ selection[0] + ".pyo" 
                print "In selected adn =", adn
                if os.path.exists(adn):
                       os.remove(adn)
                adn = THISPLUG + "/plugins/"+ selection[0]
                print "In selected adn =", adn
                if os.path.exists(adn):
                       cmd = "rm -rf " + adn
                       os.system(cmd)               
                ########
                self.openTest()
                # self.close()
            
            else:
                self.openTest()
                # self.close()

    def conf(self):
                self.session.open(WMConfigScreen) 

    def pluginfo(self):
                txt = _("WebMedia.v.16\n\nDevelop Team: pcd, Lululla\n\nFor new plugins or any errors or suggestions\nplease visit the WebMedia thread in Linuxsat-support forum")
#                self.session.open(MessageBox, txt, timeout = 20)
#                self.session.openWithCallback(self.close, MessageBox, _("WebMedia.v.16"), MessageBox.TYPE_ERROR)
                self.session.open(MessageBox, txt, MessageBox.TYPE_INFO, timeout = 10)

################################################
    def cancel(self):
                stopDload = config.plugins.webmedia.tempdel.value
                cmd1 = "killall -9 rtmpdump"
                cmd2 = "killall -9 wget"
#                if self.ipage == 1:
                ###print "cancel : self.ipage =", self.ipage
                if stopDload is True:
                        os.system(cmd1)
                        os.system(cmd2)
                        self.close()
                else:
                        self.close()
                      

    def okbuttonClick(self):
                 idx = self["list"].getSelectionIndex()
                 plug = self.names[idx]
                 print "Here in WebMedia plug =", plug
                 from Plugins.Extensions.WebMedia.Execlist import Execlist
                 Execlist(self.session, plug)
                 
class ShowPage(Screen):

    def __init__(self, session, newstext):
		Screen.__init__(self, session)
                self.session=session
#                self.skinName = "Getcats"
                self.skinName = "ShowPage"
#        	self["list"] = MenuList([])
                self.ftext = newstext #global
                self["menu"] = RSList([])
		self["info"] = Label()
		self.info = (_("Press OK if you want to see this message again."))
                self["info"].setText(self.info)
		self.list = []
                self["pixmap"] = Pixmap()
                self["list"] = List(self.list)
                self["list"] = RSList([])
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.cancel,
			"red": self.cancel,
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("OK"))
		title = " "
		self["title"] = Button(title)		
                self.icount = 0
                self.errcount = 0
                print "In showPage 1"
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                print "In showPage 2"
                if config.plugins.kodiplug.skinres.value == "fullhd":
                              pic1 = THISPLUG + "/skin/images/defaultL.png"
                else:
                              pic1 = THISPLUG + "/skin/images/default.png"
                self["pixmap"].instance.setPixmapFromFile(pic1)
                self.data = []
                self.data = self.ftext.splitlines()
                print "In showPage self.data =", self.data
		showlist(self.data, self["menu"])
                       

    def cancel(self):
                       file = open("/etc/wmnodl", "w")
                       file.write(date)
                       file.write("\n") 
	               file.close()
                       self.close()
                       
    def okClicked(self):                   
                       os.system("rm /etc/wmnodl &")
                       self.close()

    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		#print "pressed", number
		self["text"].number(number)
                 

######################
	
_session = None
date = " "

def main(session, **kwargs):
                       global _session 
                       _session = session
                       log = config.plugins.webmedia.elog.value 
                       if log is True:
                              logf = open('/tmp/e.log', 'w')
                              sys.stdout = logf
                       else:       
                              if os.path.exists("/tmp/e.log"):
                                     os.remove("/tmp/e.log")
                       os.system("mkdir -p "+ config.plugins.webmedia.cachefold.value+"/webmedia")
                       os.system("mkdir -p "+ config.plugins.webmedia.cachefold.value+"/webmedia/vid")
                       os.system("mkdir -p "+ config.plugins.webmedia.cachefold.value+"/webmedia/pic")
                       os.system("mkdir -p "+ config.plugins.webmedia.cachefold.value+"/webmedia/tmp")
                       try:
                                from Plugins.Extensions.WebMedia.Update import updstart
                       except:       
                                from Update import updstart
                       try:       
                                updstart()
                       except:       
                                print "\nError updating some scripts"
                       print "Here in WebMedia def main going in WebMedia"
                       session.open(Webmedia)
                       """
###                       session.open(Webmedia)
                       
#######################################################################
######################################
#mmmmmmmmmmmmmmmmmmmmmmmmm
                       xurl = ServerS1 + "/WebMedia/WM-news.txt"
                       xdest = "/tmp/WM-news.txt"
	               downloadPage(xurl, xdest).addCallback(gotNews).addErrback(showNewsError)

def showNewsError(error):
               print "In def main 6 error =", error
               menustart()

def gotNews(txt=" "):
                       print "In def main 7"
                       global date
                       session = _session
                       indic = 0
                       date = ""
                       olddate = ""
                       if not os.path.exists("/tmp/WM-news.txt"):
                               indic = 0
                       else:
                               myfile = file(r"/tmp/WM-news.txt")
                               icount = 0
                               for line in myfile.readlines():
                                   if icount == 0:
                                           date = line
                                           break
                                   icount = icount+1
                               myfile.close()
                               myfile = file(r"/tmp/WM-news.txt") 
                               global newstext   
                               newstext = myfile.read()
                               print "In gotNews newstext =", newstext
                               myfile.close()
                               news = newstext
                               n1 = news.find("update2", 0)
                               if n1 > -1:
                                      upd = news[n1:(n1+14)]
		               else:
		                      upd = "None"
		               global NewUpdate
                               NewUpdate = upd       
		               if fileExists("/etc/wmupd"): 
		                      myfile = file(r"/etc/wmupd")
                                      icount = 0
                                      for line in myfile.readlines():
                                             if icount == 0:
                                                    upd1 = line
                                                    break
                                             icount = icount+1
                                      myfile.close()
                               else:   
                                      upd1 = "None"
                                     
                               n2 = upd1.find(".", 0)
                               if n2 > -1:   
                                      upd1 = upd1[:n2]
                               print "upd =", upd
                               print "upd1 =", upd1
                               if upd != "None":
                                   if upd1 != upd:
                                      txt = _("New ") + upd + _(" is available. \nAfter update - gui will restart.\nUpdate Now ?")
                                      session.openWithCallback(do_upd, MessageBox, txt, type = 0)
                                   else:
                                      check_news()
                               else:
                                      check_news()
                               
def do_upd(answer):
        print "In def main 8"
        session = _session
        if answer is None:
                check_news()
        else:
            if answer is False:
                check_news()
            else:        
                picfold = config.plugins.webmedia.cachefold.value+"/xbmc/pic"
                cmd = "rm -rf " + picfold
                os.system(cmd)
                global plug
                plug = NewUpdate + ".zip"
                if "update" in plug:
                        f=open("/etc/wmupd", 'w')
                        txt = plug + "\n"
                        f.write(txt)
                xdest = "/tmp/" + plug
#                cmd1 = "wget -O '" + dest + "' 'http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Software/" + plug + "'"
##                cmd1 = "wget -O '" + dest + "' 'http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/KodiDirect/Software2/" + plug + "'"
##############################################
                xurl = ServerS1 + "/WebMedia/" + plug
	        downloadPage(xurl, xdest).addCallback(gotUpd).addErrback(showNewsError)
	        
def gotUpd(answer):	        
##############################################
                session = _session
                if ".ipk" in plug:
                        cmd2 = "opkg install --force-overwrite '/tmp/" + plug + "'"
                elif ".deb" in plug:
                        cmd2 = "dpkg --install '/tmp/" + plug + "'"

                elif ".zip" in plug:        
                        cmd2 = "unzip -o -q '/tmp/" + plug + "' -d /"
                title = _("Installing %s" %(plug))
                session.openWithCallback(done_upd,Console,_(title),[cmd2])
                
def done_upd():
                print "In def main 9"
                from Restart import Restart
                session = _session                
                Restart(session)
                
                
def check_news():
                       print "In check_news"
                       session = _session
                       olddate = " "
                       if not os.path.exists("/etc/wmnodl"):
                              indic = 1
                       else:
                              myfile2 = file(r"/etc/wmnodl")  
                              icount = 0
                              for line in myfile2.readlines():
                                    if icount == 0:
                                           olddate = line
                                           break
                                    icount = icount+1
                              if olddate != date :
                                    indic = 1
                              else:
                                    indic = 0      
                              myfile2.close()
                       print "In check_news indic =", indic
                       if indic == 0:
                             menustart()
                       else:             
                             session.openWithCallback(menustart, ShowPage, newstext)
                
#####################################################                         
                       """ 
def menustart():
        global date
        session = _session
        session.open(Webmedia)
        
def wmpanel(menuid, **kwargs):
	if menuid == "mainmenu":
		return [("WebMedia", main, "Web media", 10)]
	else:
		return []
		
def Plugins(**kwargs):
        list = []
        list.append(PluginDescriptor(name="WebMedia", description="Web media streamer", where = PluginDescriptor.WHERE_MENU, fnc=wmpanel))
        list.append(PluginDescriptor(name="WebMedia", description="Web media streamer", where = [ PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU ], fnc=main, icon='plugin.png'))
        return list


