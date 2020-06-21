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

green_threshold   = (42, 89, 19, 59, -4, 40)
while True:
    img=sensor.snapshot()
    blobs = img.find_blobs([green_threshold],area_threshold=40, pixels_threshold=20)
    if blobs:
        for b in blobs:
            tmp=img.draw_rectangle(b[0:4],thickness=2,color=(0,0,255))
            tmp=img.draw_cross(b[5], b[6],thickness=4,color=(0,255,0),size=8)
            c=img.get_pixel(b[5], b[6])
    lcd.display(img)
