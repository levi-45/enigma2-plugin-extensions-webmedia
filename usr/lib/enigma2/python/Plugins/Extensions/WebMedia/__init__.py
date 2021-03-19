from enigma import getDesktop
DESKHEIGHT = getDesktop(0).size().height()

if DESKHEIGHT > 1000:
      from skin import *
else:
      from skin1 import *
