# Face Recognition by Maker Asia Co., Ltd.
# Distributed by AiIoTShop.com
# Author by Comdet
import sensor, image, time, lcd, os
import KPU as kpu
import ulab as np
from Corgi85 import corgi85
from Dude import dude
#=== setup camera ===#
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

#=== setup LCD screen ===#
lcd.init()
lcd.rotation(0)

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
        codex[i,:] = codex[i,:] - t
    data = np.sum(codex * codex, axis=1)
    data = np.sqrt(data)
    if codex.shape()[0] == 1:
        return data,1
    ind = np.argmin(data)
    return data[ind][0],ind + 1

def read_dataset(file_name):
    data = []
    if file_name not in os.listdir():
        open(file_name, 'x').close()
    f = open(file_name,"r")
    for line in f:
        line=line.rstrip('\n').rstrip('\r')
        rows = [float(row) for row in line.split(',')]
        data.append(rows)
    f.close()
    return data

def append_dataset(file_name,data):
    face_dataset.append(data)
    f = open(file_name,"a")
    str_list_target = ["{:0.4f}".format(x) for x in data]
    str_target = ','.join(str_list_target)
    f.write(str_target)
    f.close()
    print("save to dataset success")

def send_sheet(face_id):
    return

#=== AI Models ===#
task_face_detect = kpu.load(0x200000)
task_face_encode = kpu.load(0x300000)
kpu.set_outputs(task_face_encode,0,1,1,128)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
kpu.init_yolo2(task_face_detect, 0.5, 0.3, 5, anchor)

#====== config ======#
face_threshold = 15
dataset_filename = "faces.csv"
#====================#

#=== SETUP ===#
#clear_dataset(dataset_filename,face_dataset)
face_dataset = read_dataset(dataset_filename);
corgi85.IFTTT_init("corgi_detect","0hI55mQkUiimG6RIjpWhp")

#=== wait wifi connect ===#
while corgi85.wifi_check() == 0:
    print("WIFI Connecting ...")
    time.sleep(1)

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

            #--- save new face ---#
            if dude.IsBootPressed() : # User pressed BOOT button
                time.sleep_ms(500)
                lcd.clear((0,255,0))
                time.sleep_ms(2000)
                append_dataset(dataset_filename,encoded)
                print("saved")
            if face_dataset:
                #--- find match ---#
                score, pid = match(encoded,face_dataset)
                print(score)
                print("Match ID %d score = %.3f" % (pid,score))
                if score < face_threshold : # recognized
                    a = img.draw_rectangle(x1,y1,w,h,color = (0,255,0), thickness=2)
                    a = img.draw_string(x1+5,y1+10,"ID:%d" % pid,color=(0,255,0),scale=3)
                    # ... DO SOMETHING HERE ...
                    if last_face_id != pid:
                        last_face_id = pid
                        print("======= send data =======")
                        corgi85.IFTTT_setParam(1,str(pid))
                        corgi85.IFTTT_fire()

    img = img.resize(240,240)
    lcd.display(img)
