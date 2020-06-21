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
    #img = img.cut(0,0,240,240)
    circles = img.find_circles(
        threshold = 3500,
        x_margin = 10,
        y_margin = 10,
        r_margin = 10,
        r_min = 2,
        r_max = 100,
        r_step = 2,
    #    roi=(30,30,150,150)
    )
    #img.draw_rectangle(30,30,150,150)
    for c in circles:
        img.draw_circle(c.x(), c.y(), c.r(), color = (0, 255, 0), thickness=5)
    lcd.display(img)
