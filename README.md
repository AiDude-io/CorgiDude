# Document and resources for CorgiDude 

## Board 
board preview
<img src="https://github.com/AiDude-io/CorgiDude/blob/master/images/front-back.png?raw=true" width="700">

board pinout
<img src="https://github.com/AiDude-io/CorgiDude/blob/master/images/corgidude-pinout.png?raw=true" width="700">

## Firmware
Download : [https://github.com/AiDude-io/CorgiDude/releases](https://github.com/AiDude-io/CorgiDude/releases)
## Driver
Please search Google for "CH340 driver"
## Python IDE
MaixPy IDE download : [https://dl.sipeed.com/MAIX/MaixPy/ide/_/](https://dl.sipeed.com/MAIX/MaixPy/ide/_/) 
## Flash tool
KFlash GUI : download : [https://github.com/sipeed/kflash_gui/releases](https://github.com/sipeed/kflash_gui/releases)
## GPIOs and Sensors
All GPIO ports in CorgiDude can be controlled by Dude class

    from Dude import dude, PORT
    dude.BeginADC(PORT.INPUT1)
    dude.BeginAHT(PORT.INPUT1)
    #input
    adc = dude.AnalogRead(port=PORT.INPUT1,channel=1)
    temp,humid = dude.ReadAHT(port=PORT.INPUT1)
    digitalData = dude.DigitalRead(port=PORT.INPUT2,pin=1)
    #output
    dude.PWMWrite(port=PORT.OUTPUT1,pin=2,value=50) #value 0-100
    dude.DigitalWrite(port=PORT.OUTPUT1,pin=2,value=1) #value 0-1
    dude.Servo(port=PORT.OUTPUT1,pin=3,value=80) #value -90 to 90 angle
    dude.Motor(port=PORT.OUTPUT2,pin=1,speed=50)#speed -100 to 100
	dude.LED(r=10,100,50) #onboard led 0-100 %
**Note :** This class occupied GPIOHS , I2C, and TIMER by this reference
**GPIO for ADC** 
	

 - GPIOHS14 - GPIOHS16

**GPIO Input**
	

 - GPIOHS21 - GPIOHS25

**I2C for INPUT1**
	

 - I2C1, freq=100000, pin SCL = 15, pin SDA = 14

**I2C for INPUT2**

 - I2C2, freq=100000, pin SCL = 10, pin SDA = 3

**GPIOOutput**
	

 - GPIOHS17-GPIOHS20

**Timer for PWM**
	

 - TIMER1, CHANNEL0-3 for OUTPUT1 	
 - TIMER2, CHANNEL0-3 for OUTPUT2

**Timer for RGB**

 - TIMER0, CHANNEL1-3

## Image Processing References

 - [https://maixpy.sipeed.com/en/libs/machine_vision/image.html](https://maixpy.sipeed.com/en/libs/machine_vision/image.html)
 - [https://docs.openmv.io/library/omv.image.html](https://docs.openmv.io/library/omv.image.html)

# Transfer Learning Garbage Classification with Google Colab
 - [https://colab.research.google.com/drive/1K4uUOvTLzuHXmsEIBNosj46h_miCPKD0?usp=sharing](https://colab.research.google.com/drive/1K4uUOvTLzuHXmsEIBNosj46h_miCPKD0?usp=sharing)
 - แก้ใข[https://colab.research.google.com/gist/apinuntong/70f930663858710346a488b8470f1c0c/corgidude-transfer-learning.ipynb](https://colab.research.google.com/gist/apinuntong/70f930663858710346a488b8470f1c0c/corgidude-transfer-learning.ipynb)
   

# Train MobileNet to classify road object.
 - [https://colab.research.google.com/drive/1UV08GRbFwW5HZBi_XcM8SwPGJNZlNfar?usp=sharing](https://colab.research.google.com/drive/1UV08GRbFwW5HZBi_XcM8SwPGJNZlNfar?usp=sharing)

## Where To Buy
Board : https://www.aiiotshop.com/p/58
