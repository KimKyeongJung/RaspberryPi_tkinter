from tkinter import *
from RPLCD.i2c import CharLCD
from tkinter import messagebox
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT) # LED R
GPIO.setup(20,GPIO.OUT) # LED G
GPIO.setup(21,GPIO.OUT) # LED B
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP) # BUTTON
GPIO.setup(24,GPIO.IN)  # PIR
GPIO.setup(25,GPIO.IN)  # BUZZER
GPIO.setup(25,GPIO.OUT) # BUZZER

GPIO.output(16,False)
GPIO.output(20,False)
GPIO.output(21,False)

root = Tk()

#제목 지정
root.title("Button Interface")
#윈도우 사이즈 지정
root.geometry("500x400")

cb1 = IntVar() #pCheck가 체크되면 cb1 값은 1 아니면 0
cb2 = IntVar() #bCheck가 체크되면 cb2 값은 1 아니면 0
txt = StringVar()
lcd = CharLCD('PCF8574', 0x27)

# 버튼 클릭 이벤트 핸들러
def rClick():
    if GPIO.input(16) == False:
        GPIO.output(16,True) # 16번 ON
        txt.set('Red ON')
        lcd.clear()
        lcd.write_string('Red ON')
    else:
        GPIO.output(16,False) # 16번 OFF
        txt.set('Red OFF')
        lcd.clear()
        lcd.write_string('Red OFF')
    
def gClick():
    if GPIO.input(20) == False:
        GPIO.output(20,True) # 20번 ON
        txt.set('Green ON')
        lcd.clear()
        lcd.write_string('Green ON')
    else:
        GPIO.output(20,False) # 20번 OFF
        txt.set('Green OFF')
        lcd.clear()
        lcd.write_string('Green OFF')

def bClick():
    if GPIO.input(21) == False:
        GPIO.output(21,True) # 21번 ON
        txt.set('Blue ON')
        lcd.clear()
        lcd.write_string('Blue ON')
    else:
        GPIO.output(21,False) # 21번 OFF
        txt.set('Blue OFF')
        lcd.clear()
        lcd.write_string('Blue OFF')
        
def mClick():
    pwm_led = GPIO.PWM(16, 500)
    pwm_led.start(0)
    for i in range(101):
        if(i==100):
            i=0
        pwm_led.ChangeDutyCycle(i)
        time.sleep(0.02)
    txt.set('Modulation')
    lcd.clear()
    lcd.write_string('Modulation')
    
        
def xClick():
    GPIO.output(16,True) # 16번 ON
    time.sleep(0.2) # 0.1초간 Delay
    GPIO.output(16,False) # 16번 OFF
    time.sleep(0.2)
    GPIO.output(20,True) # 20번 ON
    time.sleep(0.2)
    GPIO.output(20,False) # 20번 OFF
    time.sleep(0.2)
    GPIO.output(21,True) # 21번 ON
    time.sleep(0.2)
    GPIO.output(21,False) # 21번 OFF
    time.sleep(0.2)
    txt.set('Blink')
    lcd.clear()
    lcd.write_string('Blink')
           
def sClick():
    scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]
    #도 레 미 파 솔 라 시 도
    p = GPIO.PWM(25, 100)
    list = [0,2,4,0,2,4,5,5,5,4,3,3,3,2,2,2,1,1,1,0] #똑같아요 동요
    p.start(100) # pwm 시작
    p.ChangeDutyCycle(90) # dutycycle 변경
    for i in range(len(list)): #len() => 길이 추출
        p.ChangeFrequency(scale[list[i]]) #주파수 변경
        if (i+1)%10 == 0: # 10번째,20번째 음 박자 변경
            time.sleep(1.5)
        else :
            time.sleep(0.5)
    p.stop() #pwm 종료
    txt.set('Music')
    lcd.clear()
    lcd.write_string('Music')
    
def oClick():
    GPIO.output(16,False)
    GPIO.output(20,False)
    GPIO.output(21,False)
    GPIO.output(25,False)
    txt.set('All OFF')
    lcd.clear()
    lcd.write_string('All OFF')
    
def qClick():
    Msgbox = messagebox.askquestion('종료', '종료하겠습니까?')
    if Msgbox == 'yes':
        GPIO.cleanup()
        root.destroy()
    
def pCheck():
    if cb1.get() == 1:
        Msgbox = messagebox.askquestion('PIR', 'PIR 기능 ON?')
        if Msgbox == 'yes':
            while True:
                if GPIO.input(16) == False and GPIO.input(24) == True:
                    txt.set("PIR ON -> Red")
                    lcd.clear()
                    lcd.write_string('PIR ON -> Red')
                    GPIO.output(16,True) # LED를 켠다
                    break
                elif GPIO.input(16) == True and GPIO.input(24) == True:
                    txt.set("PIR ON -> Blink")
                    lcd.clear()
                    lcd.write_string('PIR ON -> Blink')
                    GPIO.output(16,False) # 16번 OFF
                    time.sleep(0.2) # 0.2초간 Delay
                    GPIO.output(16,True) # 16번 ON
                    time.sleep(0.2)
                    GPIO.output(16,False) # 16번 OFF
                    time.sleep(0.2)
                    GPIO.output(20,True) # 20번 ON
                    time.sleep(0.2)
                    GPIO.output(20,False) # 20번 OFF
                    time.sleep(0.2)
                    GPIO.output(21,True) # 21번 ON
                    time.sleep(0.2)
                    GPIO.output(21,False) # 21번 OFF
                    time.sleep(0.2)
                    break
        else:
            pCheckButton.deselect()
            
def bCheck():
    def buzz():
        pitch=700
        duration=0.1
        period=1.0/pitch
        delay=period/2
        cycles=int(duration * pitch)
                
        for i in range(cycles):
            GPIO.output(25,True)
            time.sleep(delay)
            GPIO.output(25,False)
            time.sleep(delay)
            
    control = False
    if cb2.get() == 1:
        Msgbox = messagebox.askquestion('버튼', 'Push 버튼 기능 ON?')
        if Msgbox == 'yes':
            while True:
                if GPIO.input(12) == False:
                    if control==True:
                        control=False
                    else:
                        control=True
                    txt.set('Button Pressed')
                    lcd.clear()
                    lcd.write_string('Button Pressed')

                if control == True:
                    buzz()
                elif control == False and GPIO.input(12)==False:
                    GPIO.output(16,False)
                    GPIO.output(20,False)
                    GPIO.output(21,False)
                    GPIO.output(25,False)
                    break
                
                time.sleep(0.2)
        else:
            bCheckButton.deselect()

# 버튼 인스턴스 생성
rButton = Button(root, text="R", command=rClick, bg="red", fg="white", width=5, height=2)
gButton = Button(root, text="G", command=gClick, bg="green", fg="white", width=5, height=2)
bButton = Button(root, text="B", command=bClick, bg="blue", fg="white", width=5, height=2)
mButton = Button(root, text="M", command=mClick, width=5, height=2, repeatdelay=10, repeatinterval=10)
xButton = Button(root, text="X", command=xClick, width=5, height=2, repeatdelay=10, repeatinterval=10)
sButton = Button(root, text="S", command=sClick, width=5, height=2)
oButton = Button(root, text="O", command=oClick, width=5, height=2)
qButton = Button(root, text="Quit", command=qClick, width=5, height=2)
pCheckButton = Checkbutton(root, text="PIR 감지 on", variable=cb1, command=pCheck)
bCheckButton = Checkbutton(root, text="Push Button 감지 on", variable=cb2, command=bCheck)

#버튼 위치 조절
rButton = Button(root, text="R", command=rClick, bg="red", fg="white", width=5, height=10)
gButton = Button(root, text="G", command=gClick, bg="green", fg="white", width=5, height=10)
bButton = Button(root, text="B", command=bClick, bg="blue", fg="white", width=5, height=10)
mButton = Button(root, text="M", command=mClick, bg="gray", fg="white", width=5, height=10, repeatdelay=10, repeatinterval=10)
xButton = Button(root, text="X", command=xClick, bg="gray", fg="white", width=5, height=10, repeatdelay=10, repeatinterval=10)
sButton = Button(root, text="S", command=sClick, bg="gray", fg="white", width=5, height=10)
oButton = Button(root, text="O", command=oClick, bg="gray", fg="white", width=5, height=10)
qButton = Button(root, text="Quit", command=qClick, bg="black", fg="white", width=56, height=3)
pCheckButton = Checkbutton(root, text="PIR 감지 on", variable=cb1, command=pCheck)
bCheckButton = Checkbutton(root, text="Push Button 감지 on", variable=cb2, command=bCheck)
textEntry = Entry(root, textvariable = txt)

#버튼 위치 조절
rButton.grid(row=0, column=0)
gButton.grid(row=0, column=1)
bButton.grid(row=0, column=2)
mButton.grid(row=0, column=3)
xButton.grid(row=0, column=4)
sButton.grid(row=0, column=5)
oButton.grid(row=0, column=6)
pCheckButton.place(x=0,y=300)
bCheckButton.place(x=0,y=320)
qButton.place(x=0, y=200)
textEntry.place(x=310, y=320)

root.mainloop()
