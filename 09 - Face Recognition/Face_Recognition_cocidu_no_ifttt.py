# Face Recognition by Maker Asia Co., Ltd.
# Distributed by AiIoTShop.com
# Author by Comdet
import sensor, image, time, lcd, os
import KPU as kpu
import ulab as np
from Maix import GPIO
from fpioa_manager import fm
from machine import I2C
from Maix import FPIOA, GPIO
#import touchscreen as ts
#fm.register(16,fm.fpioa.GPIO0)
#bootx=GPIO(GPIO.GPIO0,GPIO.IN)
#from Corgi85 import corgi85
from Dude import dude
#=== setup camera ===#
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(0)
sensor.set_hmirror(0)
sensor.run(1)

#=== setup LCD screen ===#
lcd.init()
lcd.rotation(2)
#=== setup LCD ts ===#
#i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
#ts.init(i2c, 1)
#=== Helper Function ===#
face_dataset = []
last_face_id = 0;

def clear_dataset(file_name,dataset):
    os.remove(file_name)
    dataset = []

def match(tester,dataset):
    codex = np.array(dataset)
    t = np.array(tester)
    for i in range(codex.shape()[0]):
        codex[i,0:128] = codex[i,0:128] - t
    data = np.sum(codex * codex, axis=1)
    data = np.sqrt(data)
    if codex.shape()[0] == 1:
        return data,dataset[0][128]
    ind = np.argmin(data)
    return data[ind][0],dataset[ind][128]

def read_dataset():
    data = []
    num = 0
    numx = 0
    file_names = os.listdir("/flash")
    file_namesdata = []
    for x in file_names:
        if x[0:3] == "ID_" :
            num = num+1
            file_namesdata.append(x)
    if num != 0 :
        for x in file_namesdata:
            print(x)
            f = open(x,"r")
            for line in f:
                line = line.rstrip('\n').rstrip('\r')
                rows = [float(row) for row in line.split(',')]
                data.append(rows)
            f.close()
    return data,num

def append_dataset(data,numid):
    global face_dataset
    listx = list(data)
    #use different ways to add items in list
    listx.append(float(numid))
    dataxo = tuple(listx)
    print(dataxo)

    lendata = len(face_dataset)
    numdel = -1
    #face_dataset.append(dataxo)
    for x in range(lendata):
        if face_dataset[x][128] == numid :
            numdel = x
    if numdel != -1 :
        face_dataset.pop(numdel)
    face_dataset.append(dataxo)
    #file_names = len(face_dataset)
    str_list_target = ["{:0.4f}".format(x) for x in dataxo]
    str_target = ','.join(str_list_target)

    f = open("ID_"+str(numid)+".txt","w")
    f.write(str_target)
    time.sleep_ms(2000)
    #f.flush()
    f.close()
    print("save to dataset success")
def d_dataset(numid):
    global face_dataset
    lendata = len(face_dataset)
    numdel = -1
    #face_dataset.append(dataxo)
    for x in range(lendata):
        if face_dataset[x][128] == numid :
            numdel = x
    if numdel != -1 :
        face_dataset.pop(numdel)
        os.remove("ID_"+str(numid)+".txt")
    time.sleep_ms(2000)
    print("save to dataset success")
def send_sheet(face_id):
    return

#=== AI Models ===#
task_face_detect = kpu.load(0x200000)
task_face_encode = kpu.load(0x300000)
kpu.set_outputs(task_face_encode,0,1,1,128)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
kpu.init_yolo2(task_face_detect, 0.5, 0.1, 5, anchor)

#====== config ======#
face_threshold = 20
dataset_filename = "faces.txt"
nameID = 1
nameIDMAX = 10
#====================#

#=== SETUP ===#
#clear_dataset(dataset_filename,face_dataset)
face_dataset,numxxs = read_dataset();
nameID = numxxs
#corgi85.IFTTT_init("corgi_detect","0hI55mQkUiimG6RIjpWhp")
print(face_dataset,numxxs)
#while(True):
    #img = sensor.snapshot()
#=== wait wifi connect ===#
#while corgi85.wifi_check() == 0:
    #print("WIFI Connecting ...")
    #time.sleep(1)

while(True):
    img = sensor.snapshot()
    #--- face detect ---#
    faces = kpu.run_yolo2(task_face_detect, img)
    if faces:
        #--- check face size ---#
        x1 = faces[0].x() - 10
        y1 = faces[0].y() - 10
        w = faces[0].w() + 20
        h = faces[0].h() + 10
        if w > 80 and h > 80:
            #--- crop target face ---#
            face = img.cut(x1,y1,w,h)
            face = face.resize(112,112)
            a = img.draw_rectangle(x1,y1,w,h,color = (255,0,0), thickness=2)
            a = face.pix_to_ai()

            #--- encode face ---#
            fmap = kpu.forward(task_face_encode,face)
            encoded = fmap[:]
            #print(encoded)
            #--- save new face ---#
            if dude.IsBootPressed() : # User pressed BOOT button เพิ่ม ID
                time.sleep_ms(500)
                nameID = nameID+1
                if nameID > nameIDMAX :
                    nameID = 0
                lcd.clear((0,255,0))
                append_dataset(encoded,nameID)
                print("saved")
            #if status == 2 and x > 0 and x < 50 and y >220 : # User pressed BOOT button
                #nameID = nameID-1
                #if nameID < 1 :
                    #nameID = 1

            #if status == 2 and x > 80 and x < 120 and y >220 : # User pressed BOOT button
                #nameID = nameID+1
                #if nameID > nameIDMAX :
                    #nameID = 10

            #if status == 2 and x > 200 and x < 230 and y >220 : # User pressed BOOT button  ลบ ID
                #time.sleep_ms(500)
                #lcd.clear((255,0,0))
                #d_dataset(nameID)
                #print("delete")

            if face_dataset:
                #--- find match ---#
                score, pid = match(encoded,face_dataset)
                print(score,pid)
                print("Match ID %d score = %.3f" % (int(pid),score))
                if score < face_threshold : # recognized
                    a = img.draw_rectangle(x1,y1,w,h,color = (0,255,0), thickness=2)
                    a = img.draw_string(x1+5,y1+10,"ID:%d" % pid,color=(0,255,0),scale=3)
                    # ... DO SOMETHING HERE ...
                    if last_face_id != pid:
                        last_face_id = pid
                        print("======= send data =======")
                        #corgi85.IFTTT_setParam(1,str(pid))
                        #corgi85.IFTTT_fire()
    #a = img.draw_string(20,200,"<",color=(0,255,0),scale=3)
    #a = img.draw_string(70,200,str(nameID),color=(0,255,0),scale=3)
    #a = img.draw_string(130,200,">",color=(0,255,0),scale=3)
    #a = img.draw_string(200,200,"S",color=(0,255,0),scale=3)
    #a = img.draw_string(280,200,"D",color=(0,255,0),scale=3)

    img = img.resize(240,240)
    lcd.display(img)
