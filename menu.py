#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO 
import os
import subprocess
import base64

#import qrcode
# variable boutons GPIOs
#GPIO for UP
BUP=20
#GPIO for DOWN
BDOWN=26
#GPIO for LEFT
BLEFT=16
#GPIO for Right
BRIGHT=21
#GPIO for button
BFIRE=12
# sample default setup.cfg values
USE_ECM="false"
USE_RNDIS="true"
USE_HID="true"
USE_HID_MOUSE="true"
USE_RAWHID="true"
USE_UMS="true"
WIFI_NEXMON="true"
WIFI_ACCESSPOINT="true"
WIFI_CLIENT="true"
HID_KEYBOARD_TEST="true"
AUTOSSH_ENABLED="false"
BLUETOOTH_NAP="false"
HTTP_SERVER="true"
FTP_SERVER="false"
MOUNT_UMS="true"
ACTIVE_PAYLOAD="No payload activated"
HID_DELAY="0" #default extra delay between duckyscript commands 
#keyboard language from hid
#read ini
filename="/home/pi/menu.ini"
ligne=""
with open(filename) as file_object:
    lines=file_object.readlines()
for line in lines:
    ligne=ligne+line.rstrip()+"\n"
inis=ligne.split("\n")
lang=inis[1].replace("lang=","")
boothid=inis[2].replace("boothid=","")
preset=inis[3].replace("preset=","")
HID_BOOT_DELAY=inis[4].replace("HID_BOOT_DELAY=","")
#print(inis) #debug
# dans inis ona les valeurs exemple inis[1]--> lang=xx
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
maxline=int(height/8)
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
#font = ImageFont.load_default()
font = ImageFont.truetype('/home/pi/font2.ttf', 8)
# Draw a black filled box to clear the image.
def send_ducky(command):
    '''
    Send command rubber duck syntax to keyboard
    exemple GUI r 
    '''
    os.system('echo '+command+' | python /home/pi/P4wnP1/duckencoder/duckencoder.py -l '+lang+' -p | python /home/pi/P4wnP1/hidtools/transhid.py')

def send_file_ducky_delayed(file):    
    '''
    Send ducky script file to keyboard with extra delay value
    exemple /home/pi/preset.txt 
    '''
    if HID_DELAY!="0":
        with open(file) as file_object:
            duckys=file_object.readlines()
        DELCOM="DELAY "+HID_DELAY
        for line in duckys:
            if len(lines)>2:
                if line[0:2]!="//" and line[0:3]!="REM":
                    #print(line.replace("\n",""))
                    send_ducky(line.replace("\n",""))
                    if HID_DELAY!="1":
                        #print(DELCOM)
                        send_ducky(DELCOM)
    else:
        send_file_ducky(file)
        
    
#
def send_file_ducky(file):
    '''
    Send ducky script file to keyboard
    exemple /home/pi/preset.txt 
    '''
    os.system('cat '+file+' | cat  |  python /home/pi/P4wnP1/duckencoder/duckencoder.py -l '+lang+' -p | python /home/pi/P4wnP1/hidtools/transhid.py')
     
def clearlcd():
    "Draw a black filled box to clear the image."
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    disp.image(image)
    disp.clear()
    disp.display()
def centretxt( str ):
    if len(str)>21:
        return (str)
    else:
        esp=int((21-len(str))/2)
        for n in range(0,esp,1):
            str=" "+str
        return (str)
def ralign(str):
    if len(str)>21:
        return (str)
    else:
        esp=21-len(str)
        for n in range(0,esp,1):
            str=" "+str
        return (str)    
def ptext( str , line):
   "This prints a passed string into lines 0 to 3"
   draw.rectangle((0,line*8+1,width,(line*8)+7), outline=0, fill=0) # delete line
   draw.text((x, top+line*8+1), str ,  font=font, fill=255)  # write line
   disp.image(image)
   disp.display()
   return
def sptext(str, line,fonte,couleur):
   "This prints a passed string into lines 0 to 3, font and color 0 or 255"
   #draw.rectangle((0,line*8+1,width,(line*8)+7), outline=0, fill=0) # delete line
   draw.text((x, top+line*8+1), str ,  font=fonte, fill=couleur)  # write line
   return    
def owptext(str, line):
   "This prints a passed string into lines 0 to 3"
   #draw.rectangle((0,line*8+1,width,(line*8)+7), outline=0, fill=0) # delete line
   draw.text((x, top+line*8+1), str ,  font=font, fill=255)  # write line
   return   
def prtext( str , line):
   "This prints a passed string into lines 0 to 3"
   draw.rectangle((0,line*8+1,len(str)*6,(line*8)+7), outline=1, fill=1) # delete line
   draw.text((x, top+line*8+1), str ,  font=font, fill=0)  # write line
   disp.image(image)
   disp.display()
   return
def seltext(str,line):
   "This prints a passed string into lines 0 to 3"
   #draw.rectangle((0,line*8,128,(line*8)+7), outline=0, fill=0) # delete line
   draw.text((x, top+line*8+1), ">" ,  font=font, fill=255)  # write line
   disp.image(image)
   disp.display()
def hjauge( valeur, ligne):
    "fait une jauge"
    valaff = int((valeur*width/100))
    draw.rectangle((0,ligne*8,width-1,(ligne*8)+6), outline=1, fill=0)
    draw.rectangle((0,ligne*8,valaff,(ligne*8)+6), outline=1, fill=1)
    disp.image(image)
    disp.display()
def menu(liste,sel,oldsel):
    "Affiche le menu sur 8 lignes et retourne la selection"
    max=len(liste) #nombre max d'elements dans la liste 
    page=int(sel/maxline)*maxline #determine le point de départ de la page
    pos=sel-page #détermine la ligne de la selection
    oldpage=int(oldsel/maxline)*maxline #determine le point de départ de la page old
    oldpos=oldsel-page #détermine la ligne de la selection old
    if page!=oldpage:
        ref=False
    else:
        ref=True
    if ref==False:
        clearlcd()
    #on affiche
    if page+maxline>max:
        butee=max
    else:
        butee=page+maxline
    if ref==False:
        # on redessine le menu
        for n in range(page, butee):
            owptext(" "+liste[n].replace("_"," "),n-page)
    for n in range(page,butee):
        if n==sel:
            draw.text((x, top+(n-page)*8+1), ">" ,  font=font, fill=255)
        else:
            draw.text((x, top+(n-page)*8+1), ">" ,  font=font, fill=0)
    disp.image(image)
    disp.display() 
    
def showmenu( liste, sel):
    "Affiche le menu sur 4 lignes et retourne la selection"
    max=len(liste)
    page=int(sel/maxline)*maxline
    pos=sel-page
    clearlcd()
    if max>maxline:
        #grande liste
        depart=sel
        if sel<maxline:depart=0
        butee=sel+maxline
        if butee>max:butee=max
        li=0
        lisel=0
        for n in range(depart,depart+maxline):
            if n<max:
                owptext(" "+liste[n].replace("_"," "),li)
            else:
                owptext("",li)
            if n==sel:lisel=n
            li=li+1
        if sel<maxline:
            seltext(liste[sel].replace("_"," "),sel)
            #prtext(liste[sel],sel)
        else:
            seltext(liste[sel].replace("_"," "),0)
            #prtext(liste[sel],0 )       
    else:
        #petite liste
        for n in range(0,maxline):
            if n<max:
                owptext(" "+liste[n].replace("_"," "),n)
            else:
                owptext("",n)
        seltext(liste[sel].replace("_"," "),sel)
        #prtext(liste[sel],sel)
 
def showlist( liste, sel):
    "Affiche le menu sur 4 lignes et retourne la selection"
    max=len(liste)
    clearlcd()
    if max>maxline:
        #grande liste
        depart=sel
        if sel<maxline:depart=0
        butee=sel+maxline
        if butee>max:butee=max
        li=0
        lisel=0
        for n in range(depart,depart+maxline):
            if n<max:
                owptext(liste[n].replace("_"," "),li)
            else:
                owptext("",li)
            if n==sel:lisel=n
            li=li+1       
    else:
        for n in range(max):
            owptext(liste[n].replace("_"," "),n)
    disp.image(image)
    disp.display()
def writesetup():
    filename="/home/pi/P4wnP1/setup.cfg"
    with open(filename, 'w') as fsetup:
        ind=0 
        for line in lines:
            fsetup.write(lines[ind])
            ind=ind+1
def refresh_setup_menu():
    #refresh values for setmenu
    #setupmenu=[,,,,,,,,,,,,,,]
    setupmenu[1]='USE_ECM : '+USE_ECM.upper()
    setupmenu[2]='USE_RNDIS : '+USE_RNDIS.upper()
    setupmenu[3]='USE_HID : '+USE_HID.upper()
    setupmenu[4]='USE_HID_MOUSE : '+USE_HID_MOUSE.upper()
    setupmenu[5]='USE_RAWHID : '+USE_RAWHID.upper()
    setupmenu[6]='USE_UMS : '+USE_UMS.upper()
    setupmenu[7]='WIFI_NEXMON : '+WIFI_NEXMON.upper()
    setupmenu[8]='WIFI_ACCESSPOINT : '+WIFI_ACCESSPOINT.upper()
    setupmenu[9]='WIFI_CLIENT : '+WIFI_CLIENT.upper()
    setupmenu[10]='HID_KEYBOARD_TEST : '+HID_KEYBOARD_TEST.upper()
    setupmenu[11]='AUTOSSH_ENABLED : '+AUTOSSH_ENABLED.upper()
    setupmenu[12]='BLUETOOTH_NAP : '+BLUETOOTH_NAP.upper()
    #setupmenu[13]='HTTP_SERVER : '+HTTP_SERVER.upper()
    #setupmenu[14]='FTP_SERVER : '+FTP_SERVER.upper()
    #setupmenu[15]='MOUNT_UMS : '+MOUNT_UMS.upper()
    
def writeini():
    filename="/home/pi/menu.ini"
    with open(filename, 'w') as fsetup: 
        for ind in range(0,5):
            fsetup.write(inis[ind]+"\n")   
    
def writekarma():
    filename="/home/pi/P4wnP1/payloads/nexmon/karma.txt"
    with open(filename, 'w') as fsetup:
        ind=0 
        for karmline in karmacfg:
            fsetup.write(karmacfg[ind])
            ind=ind+1
# boot image
#image2 = Image.open('/home/pi/bootdefcon.ppm').convert('1')
image2 = Image.open('/home/pi/p4wnp1_inv.ppm').convert('1')
#image2 = Image.open('/home/pi/code.png').resize((64, 64), Image.ANTIALIAS).convert('1')
disp.image(image2)
disp.display()
time.sleep(5)
clearlcd()
# here we go
screensaver=0
mprincipal = ['      .:: P4wnP1 ::. ','SYSTEM ACTIONS','HID ATTACKS','STAND ALONE ATTACKS','EXIT TO SYSTEM']
msystem = ['BACK HOME MENU','REBOOT','INFORMATIONS','SHOW SSID AROUND','EDIT SETUP.CFG VARS','SET BOOT PAYLOAD']
mhid =['BACK HOME MENU ['+lang.upper()+']','RUN AN ATTACK','TYPE TEXT FROM PRESET.TXT','SET HID TO LANGUAGE','SET HID EXTRA DELAY','BOOT HID AUTORUN SELECTION']
malone=['BACK HOME MENU','HONEY POT WIFI SPOT #WIP#','FAKE WIFI AP KARMA EDITOR']
keylang=['BACK HOME MENU','be','br','ca','ch','cs','de','dk','es','fi','fr','gb','hr','it','no','pt','tu','si','sv','tr','us']
delais=['BACK HOME MENU','0','1','250','500','750','1000','1250','1500','1750','2000','2500','3000','3500','4000','4500','5000']
setupmenu=['BACK HOME MENU','USE_ECM','USE_RNDIS','USE_HID','USE_HID_MOUSE','USE_RAWHID','USE_UMS','WIFI_NEXMON','WIFI_ACCESSPOINT','WIFI_CLIENT','HID_KEYBOARD_TEST','AUTOSSH_ENABLED','BLUETOOTH_NAP']
bootauto=['BACK HOME MENU ['+str(HID_BOOT_DELAY)+' ms]','SELECT HID PAYLOAD','SELECT BOOT WAITING TIME','CLEAR HID AUTO RUN']
#--------------------------------------------------------------------
#read karma
with open("/home/pi/P4wnP1/payloads/nexmon/karma.txt") as file_object:
    karmacfg=file_object.readlines()
#read setup.cfg
with open("/home/pi/P4wnP1/setup.cfg") as file_object:
    lines=file_object.readlines()
#reading lines for values
xxx=0    
payloads=[]
payloads.append('BACK HOME MENU')
for line in lines:
    if "USE_UMS=" in line:USE_UMS=lines[xxx].split("=")[1].split(" ")[0]
    if "USE_ECM=" in line:USE_ECM=lines[xxx].split("=")[1].split(" ")[0]
    if "USE_RNDIS=" in line:USE_RNDIS=lines[xxx].split("=")[1].split(" ")[0]
    if "USE_HID=" in line:USE_HID=lines[xxx].split("=")[1].split(" ")[0]
    if "USE_HID_MOUSE=" in line:USE_HID_MOUSE=lines[xxx].split("=")[1].split(" ")[0]
    if "USE_RAWHID=" in line:USE_RAWHID=lines[xxx].split("=")[1].split(" ")[0]
    if "WIFI_NEXMON=" in line:WIFI_NEXMON=lines[xxx].split("=")[1].split(" ")[0]
    if "WIFI_ACCESSPOINT=" in line:WIFI_ACCESSPOINT=lines[xxx].split("=")[1].split(" ")[0]
    if "WIFI_CLIENT=" in line:WIFI_CLIENT=lines[xxx].split("=")[1].split(" ")[0]
    if "HID_KEYBOARD_TEST=" in line:HID_KEYBOARD_TEST=lines[xxx].split("=")[1].split(" ")[0]
    if "AUTOSSH_ENABLED=" in line:AUTOSSH_ENABLED=lines[xxx].split("=")[1].split(" ")[0]
    if "BLUETOOTH_NAP=" in line:BLUETOOTH_NAP=lines[xxx].split("=")[1].split(" ")[0]
    # Special BeBoX functions addon
    if "PAYLOAD=" in line:
        tagselect=lines[xxx][0]
        if tagselect=="#":
            tagselect="OFF"
        else:
            tagselect="ON "
            ACTIVE_PAYLOAD=lines[xxx].split(" ")[0].replace("#","").replace("PAYLOAD=","").replace("\n","").replace(".txt","")
        payread=lines[xxx].split(" ")[0].replace("#","").replace("PAYLOAD=","").replace("\n","").replace(".txt","")
        payloads.append(tagselect+" "+payread)
        #print(tagselect+" "+payread)
    #if "python -m SimpleHTTPServer" in line:
    #    if lines[xxx][0]=="#":
    #        HTTP_SERVER="false"
    #    else:
    #        HTTP_SERVER="true"
    #if "sudo service vsftpd" in line:
    #    if lines[xxx][0]=="#":
    #        FTP_SERVER="false"
    #    else: 
    #        FTP_SERVER="true"
    #if "sudo mount -o" in line:
    #    if lines[xxx][0]=="#":
    #        MOUNT_UMS="false"
    #    else:
    #        MOUNT_UMS="true"            
    # ----END Special BeBoX functions addon
    xxx=xxx+1   
#------------------------------------------------------------------------------
current = mprincipal
cur=1
lvl=0
clearlcd()
GPIO.setwarnings(False)                 #désactive le mode warning
GPIO.setmode(GPIO.BCM)                  #utilisation des numéros de ports du
GPIO.setup(BUP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BLEFT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BRIGHT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BFIRE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#AUTO RUN COMMAND BEFORE MENU
if boothid!="":
    time.sleep(int(HID_BOOT_DELAY)/1000)
    send_file_ducky(boothid)
    
menu(current,cur,18)
if boothid.replace("boothid=","")!="":
    owptext("RUN HID: "+boothid.replace("boothid=","").replace("/home/pi/ducky/","").replace(".txt","").replace("_"," "),maxline-2)
else:
    owptext("RUN HID: Nothing to run",maxline-2)
owptext("PAYLOAD: "+ACTIVE_PAYLOAD,maxline-1)
disp.image(image)
disp.display()
u=1 
d=1  
l=1
r=1
f=1    
clic=""
exit=0 
while exit==0: 
    if screensaver<100005:screensaver=screensaver+1
    if screensaver==100000:
        clearlcd()
    entree = GPIO.input(BUP)
    if (entree == True and u==1):
        # press
        u=0
    if (entree == False and u==0):
        # release
        u=1
        clic="UP"
        if screensaver>100000:menu(current,cur,cur+10)
        screensaver=0
        if cur>0:
            cur=cur-1
            menu(current,cur,cur+1)
    entree = GPIO.input(BDOWN)
    if (entree == True and d==1):
        # press
        d=0
    if (entree == False and d==0):
        # release
        d=1
        clic="DOWN"
        if screensaver>100000:menu(current,cur,cur+10)
        screensaver=0
        if cur<len(current)-1:
            cur=cur+1
            menu(current,cur,cur-1)
    entree = GPIO.input(BLEFT)
    if (entree == True and l==1):
        # press
        l=0
    if (entree == False and l==0):
        # release
        l=1
        clic="LEFT"
        if screensaver>100000:menu(current,cur,cur+10)
        screensaver=0
        if cur-maxline>=0:
            cur=cur-maxline
            menu(current,cur,cur+maxline)
    entree = GPIO.input(BRIGHT)
    if (entree == True and r==1):
        # press
        r=0
    if (entree == False and r==0):
        # release
        r=1
        if cur+maxline<len(current):
            cur=cur+maxline
            menu(current,cur,cur-maxline)
        clic="RIGHT"
        if screensaver>100000:menu(current,cur,cur+10)
        screensaver=0
    entree = GPIO.input(BFIRE)
    if (entree == 1 and f==1):
        # press
        f=0
    if (entree == 0 and f==0):
        # release
        f=1
        if screensaver>100000:menu(current,cur,cur+10)
        screensaver=0
        if cur==0 and lvl>0:
            #BACK TO MAIN
            current=mprincipal
            cur=0
            lvl=0
        if cur==1 and lvl==0:
            #system
            current=msystem
            cur=0
            lvl=1
        if cur==1 and lvl==1:
            #REBOOT
            clearlcd()
            os.system("sudo reboot")
        if cur==2 and lvl==1:
            #INFORMATIONS
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True )
            cmd = "hostname -I"
            IP2 = subprocess.check_output(cmd, shell = True ).split(" ")[1]
            clearlcd()
            owptext("IP: " + str(IP).replace("\n","")+" - "+str(IP2).replace("\n",""),0)
            HOST_UP  = True if os.system("ping -c 1 -W 150 8.8.8.8 > /dev/null") is 0 else False
            if HOST_UP==True:
                owptext("    INTERNET ACCESS IS OK",1)
            else:
                owptext("    NO ACCESS TO INTERNET",1)
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            owptext(str(Disk),2)
            hjauge(int(str(Disk).replace("%","").split(" ")[2].split(".")[0]),3)
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            owptext(str(MemUsage),4)
            hjauge(int(str(MemUsage).replace("%","").split(" ")[2].split(".")[0]),5)
            ptext("HID LANGUAGE = "+lang.upper(),6)
            time.sleep(5)
        if cur==3 and lvl==1:
            #SSID LIST 
            cmd ="sudo iwlist wlan0 scan | grep ESSID"
            SSID=subprocess.check_output(cmd, shell = True )
            SSID=SSID.replace("                    ESSID:","")
            SSID=SSID.replace("\"","")
            ssidlist=SSID.split("\n")
            cmd ="sudo iwlist wlan0 scan | grep Encryption"
            Ekey=subprocess.check_output(cmd, shell = True )
            Ekey=Ekey.replace("                    Encryption ","")
            Ekeylist=Ekey.split("\n")     
            for n in range(0,len(ssidlist)):
                if ssidlist[n]=="":ssidlist[n]="Hidden"
                ssidlist[n]=ssidlist[n]+" ["+Ekeylist[n]+"]"
                #print(ssidlist[n])  #debug
            for n in range(0,len(ssidlist),maxline):
                showlist(ssidlist,n)
                time.sleep(5)
        if cur==4 and lvl==1:
            #setup.cfg editor
            refresh_setup_menu()
            current=setupmenu
            cur=0
            lvl=6
        if cur==2 and lvl==0:
            #HID ATTACK
            current=mhid
            cur=0
            lvl=2
        if cur>0 and lvl==5:
            #fire on attaque
            attaque="/home/pi/ducky/"+listattack[cur]+".txt"
            #print(attaque)
            send_file_ducky_delayed(attaque)
            #os.system('cat '+attaque+' | cat | python /home/pi/P4wnP1/duckencoder/duckencoder.py -l '+lang+' -p | python /home/pi/P4wnP1/hidtools/transhid.py')
        if cur==1 and lvl==2:
            #RUN HID ATTACK
            cmd = "ls -F --format=single-column  /home/pi/ducky/*.txt"
            listattack=subprocess.check_output(cmd, shell = True )
            listattack=listattack.replace("/home/pi/ducky/","/home/pi/ducky/BACK TO MAIN\n/home/pi/ducky/",1)
            listattack=listattack.replace(".txt","")
            listattack=listattack.replace("/home/pi/ducky/","")
            listattack=listattack.split("\n")
            current=listattack
            lvl=5   
        if cur==5 and lvl==1:
            #SET BOOT PAYLOAD
            current=payloads
            lvl=4
            cur=0
        if cur>0 and lvl==4:
            #fire on payload
            if payloads[cur].split(" ")[0]=="ON":
                new="OFF"
            else:
                new="ON"
            ind=0        
            for line in lines:
                if payloads[cur].split(" ")[1] in line:
                    if new=="ON":
                        lines[ind]=lines[ind].replace("#PAYLOAD=","PAYLOAD=")
                    else:
                        if lines[ind][0]!="#":
                            lines[ind]=lines[ind].replace("PAYLOAD=","#PAYLOAD=")
                else:
                    if lines[ind][0]!="#":
                        lines[ind]=lines[ind].replace("PAYLOAD=","#PAYLOAD=")
                ind=ind+1
            for truc in range(1,len(payloads)):
                if truc==cur:
                    if new=="ON":
                        payloads[cur]=payloads[cur].replace("OFF","ON ")
                        ACTIVE_PAYLOAD=payloads[cur].split(" ")[2]
                    else:
                        payloads[cur]=payloads[cur].replace("ON ","OFF")
                        ACTIVE_PAYLOAD="No payload activated"
                else:
                    payloads[truc]=payloads[truc].replace("ON ","OFF")
            writesetup()
        if cur>0 and lvl==6:
            #edit setups
            #print(setupmenu[cur].replace(" : ","="))
            key=setupmenu[cur].split(":")[0].replace(" ","")+"="
            value=setupmenu[cur].split(":")[1].replace(" ","").lower()
            ind=0
            for line in lines:
                #print(key+" / "+line[0-len(key)])
                if key in line:
                    #print("found "+str(ind))
                    #print(lines[ind])
                    if value=="true":
                        lines[ind]=lines[ind].replace(key+value,key+"false")
                        setupmenu[cur]=setupmenu[cur].replace("TRUE","FALSE")
                    else:
                        lines[ind]=lines[ind].replace(key+value,key+"true")
                        setupmenu[cur]=setupmenu[cur].replace("FALSE","TRUE")
                    #print(lines[ind])
                ind=ind+1
            #print(setupmenu[cur].split(":")[0].replace(" ","")+"="+setupmenu[cur].split(":")[1].replace(" ","").lower())
            writesetup()
            #print(setupmenu[cur].split(":")[1].replace(" ",""))
        if cur==2 and lvl==2:
	        #preset text
            attaque="/home/pi/preset.txt"
            send_file_ducky(attaque)
            #os.system('cat '+attaque+' | cat  | python /home/pi/P4wnP1/duckencoder/duckencoder.py -l '+lang+' -p | python /home/pi/P4wnP1/hidtools/transhid.py')
        if cur==3 and lvl==2:
            # set to fr
            current=keylang
            cur=0
            lvl=8
        if cur>0 and lvl==8:
            # language selection
            lang=keylang[cur]
            mhid[0]='BACK HOME MENU ['+lang.upper()+']'
            current=mhid
            cur=0
            lvl=2
        if cur==4 and lvl==2:
            #call delay selection menu
            current=delais
            cur=0
            lvl=9
        if cur==5 and lvl==2:  
            #call auto boot hid menu
            current=bootauto
            cur=0
            lvl=10
        if cur==1 and lvl==10:
            #select hid to run at boot
            cmd = "ls -F --format=single-column  /home/pi/ducky/*.txt"
            listattack=subprocess.check_output(cmd, shell = True )
            listattack=listattack.replace("/home/pi/ducky/","/home/pi/ducky/BACK TO MAIN\n/home/pi/ducky/",1)
            listattack=listattack.replace(".txt","")
            listattack=listattack.replace("/home/pi/ducky/","")
            listattack=listattack.split("\n")
            current=listattack
            cur=0
            lvl=11
        if cur>0 and lvl==11:
            #write payload on ini for running on next boot
            #boothid=inis[2].replace("boothid=","")
            print("/home/pi/ducky/"+listattack[cur]+".txt")
            inis[2]="boothid=/home/pi/ducky/"+listattack[cur]+".txt"
            boothid=inis[2]
            writeini()
            clearlcd()
            ptext("BOOT HID: " + listattack[cur],4)
            current=mprincipal
            cur=0
            lvl=0
            time.sleep(3)
        if cur==2 and lvl==10:
            #select extra time to wait at boot
            #normaly to 0ms but this can go up to 5000 ms wait
            #before run the attack
            current=delais
            cur=0
            lvl=12
        if cur==3 and lvl==10:
            #reset auto boot to empty value
            boothid="boothid="
            inis[2]="boothid="
            writeini()
            clearlcd()
            ptext("BOOT HID: Empty, nothing",4)
            current=mprincipal
            cur=0
            lvl=0
            time.sleep(3)
        if cur>0 and lvl==12:
            # boot delay selected
            # need to write on menu.ini the value
            #HID_BOOT_DELAY=inis[4].replace("HID_BOOT_DELAY=","")
            HID_BOOT_DELAY=delais[cur]
            inis[4]="HID_BOOT_DELAY="+str(HID_BOOT_DELAY)
            bootauto[0]='BACK HOME MENU ['+str(HID_BOOT_DELAY)+' ms]'
            writeini()
            current=bootauto
            cur=0
            lvl=10
            clearlcd()
            ptext("BOOT DELAY SET TO : " + str(HID_BOOT_DELAY)+" ms",4)
            time.sleep(3)
        if cur>0 and lvl==9:
            #delay selection
            HID_DELAY=delais[cur]
            cur=0
            lvl=2
            current=mhid
            clearlcd()
            ptext("EXTRA DELAY SET TO : " + HID_DELAY+" ms",4)
            time.sleep(3)
        if cur==3 and lvl==0:
            #ALONE ATTACK
            current=malone
            cur=0
            lvl=3
        if cur==2 and lvl==3:
            #KARMA EDITOR
            #step 1 get all wifi with encryption off arround
            #SSID LIST 
            clearlcd()
            ptext("Scanning for OPEN WIFI AP ...",3)
            ptext("       Please wait.",5)
            cmd ="sudo iwlist wlan0 scan | grep ESSID"
            SSID=subprocess.check_output(cmd, shell = True )
            SSID=SSID.replace("                    ESSID:","")
            SSID=SSID.replace("\"","")
            ssidlist=SSID.split("\n")
            cmd ="sudo iwlist wlan0 scan | grep Encryption"
            Ekey=subprocess.check_output(cmd, shell = True )
            Ekey=Ekey.replace("                    Encryption ","")
            Ekeylist=Ekey.split("\n")  
            cmd ="sudo iwlist wlan0 scan | grep Channel:"
            channel=subprocess.check_output(cmd, shell = True )
            channel=channel.replace("                    ","")
            channels=channel.split("\n")              
            freewifis=[]
            freewifis.append('BACK HOME MENU')
            for n in range(0,len(ssidlist)):
                if Ekeylist[n]=="key:off":
                    #we have a candidate
                    freewifis.append(ssidlist[n]+"-("+channels[n].replace("Channel:","")+")")
                    #print(ssidlist[n]+" "+channels[n])  #debug
            nbcandidate=len(freewifis)
            if nbcandidate>1:
                #we found one or more candidate to karma
                current=freewifis
                cur=0
                lvl=7
            else:
                clearlcd()
                prtext("NO OPEN WIFI AP FOUND SORRY",4)
                time.sleep(3)
        if cur>0 and lvl==7:
            #karma.txt editing with new AP pref
            AP=freewifis[cur].split("-")[0]
            CH=freewifis[cur].split("-")[1].replace("(","").replace(")","")
            clearlcd()
            ptext("KARMA IS NOW SET TO",1)
            ptext(AP,3)
            ptext("On Channel : "+str(CH),5)
            time.sleep(3)
            print("AP ="+AP)
            print("Channel = "+str(CH))
            ind=0
            for karmline in karmacfg:
                if "WIFI_ACCESSPOINT_CHANNEL=" in karmline:
                    karmacfg[ind]="WIFI_ACCESSPOINT_CHANNEL="+str(CH)+"\n"
                if "WIFI_ACCESSPOINT_NAME=" in karmline:
                    karmacfg[ind]="WIFI_ACCESSPOINT_NAME=\""+AP+"\"\n"
                ind=ind+1
            writekarma()
            #for karmline in karmacfg:
            #    print(karmline.replace("\n",""))
            #Done now go directly in payloads to activate if you want
            current=payloads
            lvl=4
            cur=2
        if cur==4 and lvl==0:
            #EXIT  
            exit=1
        #showmenu(current,cur)
        menu(current,cur,cur+18)
        if current==mprincipal:
            if boothid!="":
                owptext("RUN HID: "+boothid.replace("boothid=","").replace("/home/pi/ducky/","").replace(".txt","").replace("_"," "),maxline-2)
            else:
                owptext("RUN HID: Nothing to run",maxline-2)
            ptext("PAYLOAD: "+ACTIVE_PAYLOAD,maxline-1)
        clic="FIRE"		
    if clic<>"":
        #print(clic)
        clic=""
GPIO.cleanup()        
clearlcd()

