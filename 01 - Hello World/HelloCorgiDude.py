# Hello CorgiDude | From AiDude.io, aiiotshop.com/p/58
import sensor, image, lcd, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
#sensor.set_windowing((224, 224))
sensor.skip_frames(time = 100)
sensor.set_vflip(1)
lcd.init()
lcd.rotation(2)
timep = 0
while(True):
    #calculate fps
    fps = 1000/(time.ticks_ms() - timep)
    timep = time.ticks_ms()
    #display image on screen
    img = sensor.snapshot()
    img = img.cut(0,0,240,240)
    img.draw_string(5,5, "fps = %2.1f" % fps,color=(0,255,0),scale=2)
    lcd.display(img)
