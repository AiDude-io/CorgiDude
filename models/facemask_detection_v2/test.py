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
classes = ["face", "face_mask"]
task = kpu.load(0x400000)
a = kpu.set_outputs(task, 0, 10,7,35)
anchor = (0.212104,0.261834, 0.630488,0.706821, 1.264643,1.396262, 2.360058,2.507915, 4.348460,4.007944)
a = kpu.init_yolo2(task, 0.5, 0.5, 5, anchor)
while(True):
    timestamp = time.ticks_ms()
    img = sensor.snapshot()
    a = img.pix_to_ai()
    faces = kpu.run_yolo2(task, img)
    if faces:
        for face in faces:
            if face.classid() == 0 :
                a=img.draw_rectangle(face.rect(),color = (255, 0, 0),thickness=5)
            elif face.classid() == 1 :
                a=img.draw_rectangle(face.rect(),color = (0,255, 0),thickness=5)
    a = img.draw_string(70,10,"FPS : %.2f" % (1000/(time.ticks_ms()-timestamp)),color=(0,255,0),scale=2)
    a = lcd.display(img)
a = kpu.deinit(task)