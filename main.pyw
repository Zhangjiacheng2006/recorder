# here are some constants you need to set (begin)

GRAB_TIME_INTERVAL = 10 # grab once every 10 seconds. note that this number can't be too small
PICTURE_SAVED_PATH = 'D:\\log\\' # where those images will be saved, better in a bigger disk

# (end)

import threading
import os

PATH_0=os.path.dirname(__file__)

if not os.path.exists(PATH_0):
	os.makedirs(PATH_0)

import cv2
cam1=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
cam1=cv2.resize(cam1,dsize=(480,360))
cam2=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
cam2=cv2.resize(cam1,dsize=(480,360))
scn=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
scn=cv2.resize(scn,dsize=(1440,810))
timp=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
timp=cv2.resize(timp,dsize=(500,120))

def getCam1(): # camera 1
	global cam1
	cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
	f, cam1 = cap.read()
	if not f:
		cam1=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
	cap.release()
	cam1=cv2.resize(cam1,dsize=(480,360))

def getCam2(): # camera 2
	global cam2
	cap=cv2.VideoCapture(1,cv2.CAP_DSHOW)
	f, cam2 = cap.read()
	if not f:
		cam2=cv2.imread(PATH_0+"\\assets\\pictures\\invalid-camera.jpg")
	cap.release()
	cam2=cv2.resize(cam2,dsize=(480,360))

from PyQt5.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)

def getScr():
	global scn
	screen=QApplication.primaryScreen()
	img=screen.grabWindow(0).toImage()
	img.save(PATH_0+"\\temp\\scncov.png")
	scn=cv2.imread(PATH_0+"\\temp\\scncov.png")
	scn=cv2.resize(scn,dsize=(1440,810))

def getTim():
	global timp
	timel=time.strftime("%H:%M:%S")
	texp=font.render(timel,True,(0,0,0),(255,255,255))
	pygame.image.save(texp,PATH_0+"\\temp\\timcrd.png")
	timp=cv2.imread(PATH_0+"\\temp\\timcrd.png")
	timp=cv2.resize(timp,dsize=(500,120))

import PyHook3
hm=PyHook3.HookManager()
mslt=0
msrt=0
msmt=0
kyt=0
def MLe(event):
	global mslt
	mslt=mslt+1
	return True
def MRe(event):
	global msrt
	msrt=msrt+1
	return True
def MMe(event):
	global msmt
	msmt=msmt+1
	return True
def ke(event):
	global kyt
	kyt=kyt+1
	return True

hm.MouseLeftDown=MLe
hm.MouseRightDown=MRe
hm.MouseMiddleDown=MMe
hm.KeyDown=ke

hm.HookMouse()
hm.HookKeyboard()

import pythoncom
import time

import pygame
pygame.init()
font=pygame.font.Font(os.path.join("C:\\Windows\\Fonts", "Consola.ttf"), 64)

while True:
	t1=threading.Thread(target=getCam1)
	t2=threading.Thread(target=getCam2)
	t3=threading.Thread(target=getScr)
	t4=threading.Thread(target=getTim)
	t1.start()
	t2.start()
	t3.start()
	t4.start()

	t=time.time()
	while time.time()-t<GRAB_TIME_INTERVAL:
		pythoncom.PumpWaitingMessages()
		time.sleep(0.01)

	t1.join()
	t2.join()
	t3.join()
	t4.join()

	bkg=cv2.imread(PATH_0+"\\assets\\pictures\\bg.jpg")
	x,y=bkg.shape[0::2]
	
	bkg[96:906,0:1440]=scn
	bkg[96:456,1440:1920]=cam1
	bkg[546:906,1440:1920]=cam2
	bkg[960:1080,1400:1900]=timp

	lnum=str(mslt); mslt=0
	ltx=font.render(lnum,True,(0,0,0),(255,255,255))
	rnum=str(msrt); msrt=0
	rtx=font.render(rnum,True,(0,0,0),(255,255,255))
	mnum=str(msmt); msmt=0
	mtx=font.render(mnum,True,(0,0,0),(255,255,255))
	pygame.image.save(ltx,PATH_0+"\\temp\\ltcrd.png")
	pygame.image.save(rtx,PATH_0+"\\temp\\rtcrd.png")
	pygame.image.save(mtx,PATH_0+"\\temp\\mtcrd.png")
	limp=cv2.imread(PATH_0+"\\temp\\ltcrd.png")
	limp=cv2.resize(limp,dsize=(80,120))
	bkg[945:1065,120:200]=limp
	rimp=cv2.imread(PATH_0+"\\temp\\rtcrd.png")
	rimp=cv2.resize(rimp,dsize=(80,120))
	bkg[945:1065,520:600]=rimp
	mimp=cv2.imread(PATH_0+"\\temp\\mtcrd.png")
	mimp=cv2.resize(mimp,dsize=(80,120))
	bkg[945:1065,320:400]=mimp
	
	knum=str(kyt); kyt=0
	ktx=font.render(knum,True,(0,0,0),(255,255,255))
	pygame.image.save(ktx,PATH_0+"\\temp\\kpcrd.png")
	kimp=cv2.imread(PATH_0+"\\temp\\kpcrd.png")
	lx,ly=kimp.shape[:2]
	xyd=ly/lx
	kimp=cv2.resize(kimp,dsize=(int(xyd*120),120))
	bkg[945:1065,920:920+int(xyd*120)]=kimp
	
	# the time on the image show begin time
	# the time on filename show when be saved (end time)
	dir=time.strftime("%Y-%m-%d")
	if not os.path.exists(PICTURE_SAVED_PATH+dir):
		os.makedirs(PICTURE_SAVED_PATH+dir)
	dt=time.strftime("%H-%M-%S")
	cv2.imwrite(PICTURE_SAVED_PATH+dir+'\\'+dt+'.jpg',bkg)
