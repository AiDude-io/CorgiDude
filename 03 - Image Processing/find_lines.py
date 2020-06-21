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
    lines = img.find_lines(
        threshold = 1300,
        theta_margin = 25,
        rho_margin = 25
    )
    for l in lines:
        img.draw_line(l.line(), color = (255, 0, 0),thickness=4)
    lcd.display(img)
