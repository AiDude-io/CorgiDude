#CorgiDude board : https://www.aiiotshop.com/p/58
import sensor
import image
import lcd
import KPU as kpu

lcd.init()
lcd.rotation(2)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

task = kpu.load(0x300000)
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
while(True):
    img = sensor.snapshot()
    faces = kpu.run_yolo2(task, img)
    if faces:
        for face in faces:
            img.draw_rectangle(face.rect(),color=(255,0,0),thickness=4)
    img = img.resize(240,240)
    lcd.display(img)
kpu.deinit(task)