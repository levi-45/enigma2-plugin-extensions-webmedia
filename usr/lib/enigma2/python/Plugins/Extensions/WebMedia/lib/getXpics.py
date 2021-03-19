from Screens.Screen import Screen
from Components.config import config
from Components.Button import Button
from enigma import getDesktop
from Tools.Directories import fileExists
from Components.Label import Label
from Components.Sources.List import List
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Sources.StaticText import StaticText
from Components.ActionMap import NumberActionMap
from Plugins.Extensions.WebMedia.Utils import *
import urllib2
import os
DESKHEIGHT = getDesktop(0).size() #.height()
THISPLUG = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia"



def getUrlresp(url):
        print "Here in getUrlresp url =", url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
#       link=response.read()
#       response.close()
        return response

def getUrl(url):
        print "Here in client2 getUrl url =", url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
        
def getUrl2(url, referer):
        print "Here in client2 getUrl2 url =", url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link     



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

class GridMainHD(Screen):
        skin = """
                <screen name="GridMainHD" position="0,0" size="1280,720" title="GridMain" >
                <eLabel position="0,0" zPosition="1" size="1280,720" backgroundColor="#0b1a49" /> 


                <widget source="global.CurrentTime" render="Label" position="80,85" size="140,25"  zPosition="2" font="Regular;18" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1">
                <convert type="ClockToText">Default</convert>
                </widget>

                <widget source="global.CurrentTime" render="Label" position="80,80" size="140,25" zPosition="2" font="Regular;18" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1" valign="center">
                <convert type="ClockToText">Format:%d.%m.%Y</convert>
                </widget>

                <widget name="title" position="850,20" size="350,50" zPosition="3" halign="center" valign="top" foregroundColor="#389416" backgroundColor="black" font="Regular;40" transparent="1" /> 
                <widget name="info" position="150,665" zPosition="4" size="900,50" font="Regular;22" foregroundColor="#7bd7f7" backgroundColor="#40000000" transparent="1" halign="left" valign="center" />
                <widget name="frame" position="60,80" size="360,360" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/pic_frameL4.png" zPosition="4" alphatest="on" />   

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
class GridMainFHD(Screen):
        skin = """
                <screen name="GridMainFHD" position="0,0" size="1920,1080" title="GridMain" >
                <eLabel position="0,0" zPosition="1" size="1920,1080" backgroundColor="#0b1a49" /> 


                <widget source="global.CurrentTime" render="Label" position="120,128" size="210,38"  zPosition="2" font="Regular;27" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1">
                <convert type="ClockToText">Default</convert>
                </widget>

                <widget source="global.CurrentTime" render="Label" position="120,120" size="210,38" zPosition="2" font="Regular;27" halign="right" backgroundColor="black" foregroundColor="#ffffff" transparent="1" valign="center">
                <convert type="ClockToText">Format:%d.%m.%Y</convert>
                </widget>

                <widget name="title" position="1275,30" size="525,75" zPosition="3" halign="center" valign="top" foregroundColor="#389416" backgroundColor="black" font="Regular;60" transparent="1" /> 
                <widget name="info" position="225,998" zPosition="4" size="1350,75" font="Regular;33" foregroundColor="#7bd7f7" backgroundColor="#40000000" transparent="1" halign="left" valign="center" />
                <widget name="frame" position="90,120" size="390,390" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/pic_frameL4.png" zPosition="2" alphatest="on" />   

                <widget source="label1" render="Label" position="60,443" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" backgroundColor="black"/>
                <widget name="pixmap1" position="60,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label2" render="Label" position="420,443" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap2" position="420,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label3" render="Label" position="780,443" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap3" position="780,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label4" render="Label" position="1140,443" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap4" position="1140,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label5" render="Label" position="1500,443" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap5" position="1500,105" size="330,330" zPosition="3" transparent="1" alphatest="on" />

                <widget source="label6" render="Label" position="60,893" size="330,90" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap6" position="60,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label7" render="Label" position="420,893" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap7" position="420,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label8" render="Label" position="780,893" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap8" position="780,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label9" render="Label" position="1140,893" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap9" position="1140,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />
                <widget source="label10" render="Label" position="1500,893" size="330,113" font="Regular;33" halign="center" zPosition="4" transparent="1" foregroundColor="white" />
                <widget name="pixmap10" position="1500,555" size="330,330" zPosition="3" transparent="1" alphatest="on" />

                </screen>"""
class GridMain(Screen):


        def __init__(self, session, names, urls, pics = []):
                Screen.__init__(self, session)
                # if DESKHEIGHT > 1280:
                       # print "DESKHEIGHT > 1280 =", DESKHEIGHT
                       # self.skin = GridMainFHD.skin
                # else:
                       # print "DESKHEIGHT < 1280 =", DESKHEIGHT
                       # self.skin = GridMainHD.skin
                       
                       
                sk= 'GridMain.xml'
                if DESKHEIGHT.width() > 1280:
                    skin = skin_path + sk
                else:
                    skin = skin_path + sk
                f = open(skin, 'r')
                self.skin = f.read()
                f.close()   

            
                menuTitle = "WebMedia"       
                title = menuTitle
                self["title"] = Button(title)
                tmpfold = config.plugins.webmedia.cachefold.value + "/webmedia/tmp"
                picfold = config.plugins.webmedia.cachefold.value + "/webmedia/pic"
                pics = getpics(names, pics, tmpfold, picfold)
                print "In Gridmain pics = ", pics
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
                self.name = menuTitle
                dep = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/default.png"
                self.pics = pics
                self.mlist = names
                self.urls1 = urls
                self.names1 = names
#               self.nextmodule = "Videos3"
                self["info"] = Label()
                
                
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
                             

        def exit(self):
          
           self.close()          
           
        


        def paintFrame(self):
                print  "In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry
#               if self.maxentry < self.index or self.index < 0:
#                       return
                ifr = self.index - (10*(self.ipage-1))
                print  "ifr =", ifr
                ipos = self.pos[ifr]
                print  "ipos =", ipos
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
                        blpic = THISPLUG + "/skinpics/images/Blank.png"
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
                    print  "pic =", pic
                    if os.path.exists(pic):
                           print "pic path exists"
                    else:
                           print "pic path exists not"
                    
                    picd = "/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/skinpics/images/default.png"
                    if os.path.exists(picd):
                           print "pic path 2 exists"
                    else:
                           print "pic path 2 exists not"

                    try:
                           self["pixmap" + str(i+1)].instance.setPixmapFromFile(pic)
                    except:
                           self["pixmap" + str(i+1)].instance.setPixmapFromFile(picd)
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
#               if self.index < 0:
#                       self.index = self.maxentry
#               self.paintFrame()
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
          itype = self.index
          self.url = self.urls1[itype]
          self.name = self.names1[itype]
          print "In XbmcPluginScreen self.url =", self.url
          print "In XbmcPluginScreen self.name =", self.name
          print "In XbmcPluginScreen self.index =", self.index   
          if "youtube" in self.url.lower():
               self.getytvid()
          else:    
               self.getvid()

        def getvid(self):            
           print "getvid self.url 2=", self.url
           f1 = urlopen(self.url)
           fpage = f1.read()
           print "getvid fpage =", fpage
           start = 0
           pos1 = fpage.find("source src", start)
           if (pos1 < 0):
                           return
           pos2 = fpage.find("http", pos1)
           if (pos2 < 0):
                           return
           pos3 = fpage.find("'", (pos2+5))
           if (pos3 < 0):
                           return                

           url = fpage[(pos2):(pos3)]
          
           self.vidurl = url            
           self.play()

        def getytvid(self):
           name = "video"
#           url = "https://www.youtube.com/watch?v=" + url
#        print "In getVideos4 url =", url    
##        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/__main__.py' --no-check-certificate -o '/tmp/vid.mp4' -f best '" + url + "'"
#        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/YT/__main__.py -o /tmp/vid.mp4' '" + url + "' > /tmp/txt"

           cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/WebMedia/__main__.py' --no-check-certificate --skip-download -f best --get-url '" + self.url + "' > /tmp/vid.txt"

##        cmd = "python '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugins/plugin.video.youtube/default.py' 9 '?plugin://plugin.video.youtube/play/?video_id=" + url + "' &"
#        cmd = "python '/usr/lib/enigma2/python/__main__.py' --skip-download --get-url '" + url + "' > /tmp/vid.txt"
           print "In getVideos4 cmd =", cmd
           if os.path.exists("/tmp/vid.txt"):
               os.remove("/tmp/vid.txt")
           os.system(cmd)
           self.vidurl = "/tmp/vid.txt"

           if not os.path.exists(self.vidurl):
              os.system("sleep 5")
              self.play()
           else: 
              self.play()
              """     
        os.system("sleep 5")
        self.play()
              """        
          
        def play(self):
                print "Here in play 1 going in Playoptions"
#                system("sleep 2")
                desc = " "
                url = self.vidurl
                name = self.name
                self.session.open(Playoptions, name, url, desc)                
                
