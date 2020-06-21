# CorgiDude | From AiDude.io, aiiotshop.com/p/58
import sensor, image, lcd, time

lcd.init()
lcd.rotation(2)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224,224))
sensor.set_vflip(1)
sensor.run(1)
sensor.skip_frames(30)

while True:
    img = sensor.snapshot()
    rects = img.find_rects(threshold = 18000,roi=(80,60,160,120))
    for r in rects:
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        for p in r.corners():
            img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
    img.draw_rectangle(80,60,160,120)
    lcd.display(img)
