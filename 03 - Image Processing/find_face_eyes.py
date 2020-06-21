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

# Load Haar Cascade
face_cascade = image.HaarCascade("frontalface", stages=25)
eyes_cascade = image.HaarCascade("eye", stages=24)

while True:
    img = sensor.snapshot()
    objects = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)
    for face in objects:
        img.draw_rectangle(face,color=(0,255,0),thickness=5)
        eyes = img.find_features(eyes_cascade, threshold=0.5, scale_factor=1.2, roi=face)
        for e in eyes:
            img.draw_rectangle(e, color=(255,0,0), thickness=5)
    lcd.display(img)
