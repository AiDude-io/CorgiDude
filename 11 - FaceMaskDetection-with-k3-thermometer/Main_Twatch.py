import sensor,image,lcd,time
import KPU as kpu
from Maix import I2S, GPIO
from fpioa_manager import fm
from machine import UART
import struct
from time import sleep_ms, ticks_ms, ticks_diff
######## UART for Temperature
fm.register (2, fm.fpioa.UART1_TX)
fm.register (3, fm.fpioa.UART1_RX)
uart_temp = UART (UART.UART1, 115200, 8, None, 1, timeout = 1000, read_buf_len = 4096)
######## GPIO For trig thermometer
fm.register(10,  fm.fpioa.GPIO1, force=True)
triger=GPIO(GPIO.GPIO1,GPIO.OUT)
triger.value(0)

######## Config Camera and Display
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((320, 224))
sensor.set_vflip(1)
sensor.run(1)
lcd.init(type=2, freq=20000000, color=lcd.BLACK)
######### config facemask detection
task = kpu.load(0x400000)
a = kpu.set_outputs(task, 0, 10,7,35)
anchor = (0.212104,0.261834, 0.630488,0.706821, 1.264643,1.396262, 2.360058,2.507915, 4.348460,4.007944)
a = kpu.init_yolo2(task, 0.5, 0.5, 5, anchor)
######### config detection
stage = 0
# 0 = init
# 1 = wait for user waring mask
# 2 = ask for approching
# 3 = wait for approching
# 4 = check temperature

# time out unmask
timestamp = 0
timeout_wait_mask = 5000 # ms
timeout_wait_approch = 5000 # ms
timeout_wait_check = 6000 # ms
face_size_threshold_w = 80
face_size_threshold_h = 80

while(True):
    img = sensor.snapshot()
    a = img.pix_to_ai()
    # face detection
    faces = kpu.run_yolo2(task, img)
    classid = -1
    if faces: #found face in screen
        face = faces[0] # first face only
        classid = face.classid()
        x,y,w,h = face.rect()
        if classid == 0:
            a=img.draw_rectangle(face.rect(),color = (255, 0, 0),thickness=5)
        else:
            a=img.draw_rectangle(face.rect(),color = (0, 255, 0),thickness=5)

    #--------- stage
    if classid == 0 and stage == 0: # detect face not wearing mask
        #player.play(0, 1)
        stage = 1
        timestamp = time.ticks_ms()#stamp time
    elif stage == 1: # wait for user waring mask
        if classid == 1: #user wearing mask
            stage = 2
            timestamp = time.ticks_ms()#stamp time
        elif time.ticks_ms() - timestamp > timeout_wait_mask:
            stage = 0 # reset
    elif classid == 1 and (stage == 2 or stage == 0): # ask for approching
        #player.play(0, 2)
        stage = 3
        timestamp = time.ticks_ms()#stamp time
    elif classid == 1 and stage == 3: # wait for approching
        if w > face_size_threshold_w and h > face_size_threshold_h:
            stage = 4
            timestamp = time.ticks_ms()#stamp time
        elif time.ticks_ms() - timestamp > timeout_wait_approch:
            stage = 0 # reset
    elif stage == 4: # check temperature
        a = img.draw_circle(112+49,112+8,50,(128, 128, 128), 3)
        #####################################
        triger.value(1)
        time.sleep(0.005)
        triger.value(0)
        rx = uart_temp.read(7)
        if rx != None :
            if rx[0] == 85 and rx[1] == 170 and rx[2] == 7 and rx[3] == 4 :
                temperature = int(struct.unpack("<H",rx[4:6])[0])/10
                print(temperature)
                if temperature < 37.5 :
                    #player.play(0, 3)
                    stage = 0 # reset
                elif temperature >= 37.5 :
                    player.play(0, 4)
                    stage = 0 # reset
                img.draw_string(2,2, ("%2.1f C" %(temperature)), color=(0,255,0), scale=4)
        ######################################
        if time.ticks_ms() - timestamp > timeout_wait_check:
            stage = 0 # reset
    #---------------
    print("Stage : %d , Timeout %d" %(stage,time.ticks_ms() - timestamp))
    a = lcd.display(img)

a = kpu.deinit(task)
