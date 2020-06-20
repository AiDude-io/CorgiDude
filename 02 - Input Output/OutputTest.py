# CorgiDude GPIO | From AiDude.io, aiiotshop.com/p/58
import image, lcd, time
from Dude import dude,PORT

lcd.init()
lcd.rotation(1)

while(True):
    img = image.Image(size=(240,240))
    #Test Servo
    img.draw_rectangle(0,0,240,240, fill=True, color=(255,0,0))
    img.draw_string(5,5, "Test Servo",color=(0,255,0),scale=3)
    lcd.display(img)
    
    dude.Servo(PORT.OUTPUT1,1,-90)
    time.sleep(2)
    dude.Servo(PORT.OUTPUT1,1,0)
    time.sleep(2)
    dude.Servo(PORT.OUTPUT1,1,90)
    time.sleep(2)
    #Test Motor
    img.draw_rectangle(0,0,240,240, fill=True, color=(255,0,0))
    img.draw_string(5,5, "Test Motor",color=(0,255,0),scale=3)
    lcd.display(img)

    dude.Motor(PORT.OUTPUT2,1,-80)
    dude.Motor(PORT.OUTPUT2,2,-80)
    time.sleep(2)
    dude.Motor(PORT.OUTPUT2,1,80)
    dude.Motor(PORT.OUTPUT2,2,-80)
    time.sleep(2)
    dude.Motor(PORT.OUTPUT2,1,-80)
    dude.Motor(PORT.OUTPUT2,2,80)
    time.sleep(2)
    dude.Motor(PORT.OUTPUT2,1,80)
    dude.Motor(PORT.OUTPUT2,2,80)
    time.sleep(2)
    dude.Motor(PORT.OUTPUT2,1,80)
    dude.Motor(PORT.OUTPUT2,2,80)
    time.sleep(2)
    dude.Motor(PORT.OUTPUT2,1,0)
    dude.Motor(PORT.OUTPUT2,2,0)
    time.sleep(2)
    #Test RGB
    img.draw_rectangle(0,0,240,240, fill=True, color=(255,0,0))
    img.draw_string(5,5, "Test RGB",color=(0,255,0),scale=3)
    lcd.display(img)
    for r in range(100):
        dude.LED(r,0,0)
        time.sleep(0.02)
    for g in range(100):
        dude.LED(0,g,0)
        time.sleep(0.02)
    for b in range(100):
        dude.LED(0,0,b)
        time.sleep(0.02)
    
    time.sleep(2)
