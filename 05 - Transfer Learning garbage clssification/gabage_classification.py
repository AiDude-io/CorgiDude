import sensor, image, time, lcd
import KPU as kpu
#setup camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)


#setup LCD screen
lcd.init()
lcd.rotation(2)

#read label file
f=open("labels.txt","r")
labels=f.readlines()
f.close()

#setup CNN
task = kpu.load(0x200000)

#Kmodel V4 need set output shape manually
#set_outputs(int idx, int w, int h, int ch)
kpu.set_outputs(task,0,6,1,1)

timep = 0
while(True):
    fps = 1000/(time.ticks_ms() - timep)
    timep = time.ticks_ms()

    img = sensor.snapshot()

    img = img.resize(224,224)
    a = img.pix_to_ai()

    fmap = kpu.forward(task,img)
    plist = fmap[:]
    pmax = max(plist)
    max_index = plist.index(pmax)
    result = labels[max_index].strip()

    img.draw_string(0,5,"%.2f:%s" % (pmax,result),scale=2,color=(0,255,0))
    img.draw_string(0,200,"%.1fFPS" % fps,scale=2,color=(255,0,0))
    lcd.display(img)


