# CorgiDude GPIO | From AiDude.io, aiiotshop.com/p/58
import image, lcd, time
from Dude import dude,PORT

lcd.init()
lcd.rotation(1)

dude.BeginADC(PORT.INPUT2)
dude.BeginAHT(PORT.INPUT2)

while(True):
    img = image.Image(size=(240,240))
    #read sensor
    adc = dude.AnalogRead(PORT.INPUT2,2)
    temp,humid = dude.ReadAHT(PORT.INPUT2)

    img.draw_rectangle(0,0,240,240, fill=True, color=(int(adc/3.5*255),0,0))
    img.draw_string(5,5, "T=%2.2f" % temp,color=(0,255,0),scale=3)
    img.draw_string(5,35, "H=%2.2f" % humid,color=(0,255,0),scale=3)
    img.draw_string(5,65, "ADC=%2.2f" % adc,color=(0,255,0),scale=3)

    '''
    if dude.DigitalRead(PORT.INPUT1,4) == 1:
        img.draw_rectangle(0,0,240,240, fill=True, color=(0,0,255))
    '''
    lcd.display(img)
    time.sleep(0.1)
