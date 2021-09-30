import sensor,image,lcd,time
import KPU as kpu
from Maix import I2S, GPIO
from fpioa_manager import fm
from machine import UART
from time import sleep_ms, ticks_ms, ticks_diff

######## Config Camera and Display
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320, 224))
sensor.set_vflip(0)
sensor.run(1)
lcd.init(type=1, freq=15000000, color=lcd.BLACK)
lcd.rotation(0)

######### config facemask detection
task = kpu.load(0x300000)
a = kpu.set_outputs(task, 0, 10,7,35)
anchor = (0.212104,0.261834, 0.630488,0.706821, 1.264643,1.396262, 2.360058,2.507915, 4.348460,4.007944)
a = kpu.init_yolo2(task, 0.5, 0.5, 5, anchor)

while(True):
    img = sensor.snapshot()
    a = img.pix_to_ai()
    # face detection
    faces = kpu.run_yolo2(task, img)
    classid = -1
    if faces: #found face in screen
        for face in faces:
            classid = face.classid()
            x,y,w,h = face.rect()
            if classid == 0:
                a=img.draw_rectangle(face.rect(),color = (255, 0, 0),thickness=5)
            else:
                a=img.draw_rectangle(face.rect(),color = (0, 255, 0),thickness=5)
    a = lcd.display(img)

a = kpu.deinit(task)

