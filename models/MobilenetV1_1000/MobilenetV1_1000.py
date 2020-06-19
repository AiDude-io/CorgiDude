import sensor, image, lcd, time
import KPU as kpu
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
lcd.init(type=2, freq=20000000, color=lcd.BLACK)
lcd.rotation(2)
f=open('/sd/labels.txt','r')
labels=f.readlines()
f.close()

task = kpu.load(0x200000)
clock = time.clock()
while(True):
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    a = lcd.display(img)
    lcd.draw_string(0, 0, "%.2f:%s                            "%(pmax, labels[max_index].strip()))
    print(fps)
a = kpu.deinit(task)