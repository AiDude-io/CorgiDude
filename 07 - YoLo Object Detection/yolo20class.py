#CorgiDude board : https://www.aiiotshop.com/p/58
#refer to http://blog.sipeed.com/p/677.html
import sensor,image,lcd,time
import KPU as kpu

lcd.init()
lcd.rotation(2)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

clock = time.clock()
classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
task = kpu.load(0x500000) 
anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
while(True):
    clock.tick()
    img = sensor.snapshot()
    objects = kpu.run_yolo2(task, img)
    print(clock.fps())
    if objects:
        for obj in objects:
            img.draw_rectangle(obj.rect(),color=(0,255,0),thickness=3)
            img.draw_string(obj.x(), obj.y(), classes[obj.classid()], color=(0,255,0),scale=2)
            img.draw_string(obj.x(), obj.y()+12, '%.3f'%obj.value(), color=(0,255,0),scale=2)
    img = img.resize(240,240)
    lcd.display(img)
kpu.deinit(task)