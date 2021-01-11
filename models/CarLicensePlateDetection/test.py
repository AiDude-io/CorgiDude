import sensor,image,lcd,time
import KPU as kpu
sensor.reset(freq=24000000,dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320, 224))
sensor.set_vflip(1)
sensor.run(1)
lcd.init(type=2, freq=20000000, color=lcd.BLACK)
#lcd.rotation(2)
classes = ["license_plate"]
task = kpu.load(0x400000)
a = kpu.set_outputs(task, 0, 10,7,30)
anchor = (1.81,0.85, 2.26,1.07, 3.00,1.46, 4.56,1.95, 7.38,3.45)
a = kpu.init_yolo2(task, 0.3, 0.3, 5, anchor)
while(True):
    timestamp = time.ticks_ms()
    img = sensor.snapshot()
    a = img.pix_to_ai()
    plates = kpu.run_yolo2(task, img)
    if plates:
        plate = plates[0]
        a=img.draw_rectangle(plate.rect(),color = (0, 255, 0),thickness=5)
    a = img.draw_string(70,10,"FPS : %.2f" % (1000/(time.ticks_ms()-timestamp)),color=(0,255,0),scale=2)
    a = lcd.display(img)
a = kpu.deinit(task)