import uos
import sensor
import image
import lcd
import KPU as kpu
from fpioa_manager import fm
from machine import I2C
from board import board_info
from Maix import GPIO

lcd.init(type=2, freq=20000000, color=lcd.BLACK)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)

fm.register(21, fm.fpioa.GPIOHS0, force=True)
fm.register(22, fm.fpioa.GPIOHS1, force=True)

D21 = GPIO(GPIO.GPIOHS0, GPIO.OUT)
RED = GPIO(GPIO.GPIOHS1, GPIO.OUT)


RED.value(0)
D21.value(1)


task = kpu.load(0x300000)

tid = kpu.load(0x600000)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)

while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            xx = i.x()-10
            yy = i.y()-10
            ww  =  i.w()+15
            hh = i.h()+10
            face_cut=img.cut(xx,yy,ww,hh)
            face_cut=face_cut.resize(128,128)
            a = face_cut.pix_to_ai()
            a = kpu.set_outputs(tid,0,1,1,2)
            fmap = kpu.forward(tid,face_cut)
            plist=fmap[:]
            pmax=max(plist)
            max_index=plist.index(pmax)
            print(plist)

            if plist[0] >= 0.94 :
                a = img.draw_rectangle(xx, yy, ww, hh, color=(255,0,0), thickness=4)
            elif plist[1] >= 0.98 :
                a = img.draw_rectangle(xx, yy, ww, hh, color=(0,255,0), thickness=4)
            else :
                a = img.draw_rectangle(xx, yy, ww, hh, color=(0,0,255), thickness=4)

    else :
        RED.value(0)
        D21.value(1)
    a = lcd.display(img)
a = kpu.deinit(task)








































