from machine import Pin
from machine import PWM
from utime import sleep as delay

SensorR = Pin(17, Pin.IN) # Right IR Sensor
SensorC = Pin(6, Pin.IN) #Center IR Sensor
SensorL = Pin(16, Pin.IN) # Left IR Sensor

IN1 = Pin(9, Pin.OUT) # IN1 Motor Driver
IN2 = Pin(8, Pin.OUT) # IN2 Motor Driver
IN3 = Pin(11, Pin.OUT) # IN3 Motor Driver
IN4 = Pin(10, Pin.OUT) # IN4 Motor Driver

motorRF = PWM(IN1) # Right Forward Motor
motorRB = PWM(IN2) # Right Backwards Motor
motorLF = PWM(IN3) # Left Forward Motor
motorLB = PWM(IN4) # Left Backwards Motor

motorRF.freq(490)
motorRB.freq(490)
motorLF.freq(490)
motorLB.freq(490)

# Equivalent to map() function
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Function to convert speed from 0 to 100 into 16-bit PWM pulse
def pulsoMotor(speed):
    return map(speed, 0, 100, 0, 65534)

# Function to stop all the motors from moving
def stop():
    motorRF.duty_u16(0)
    motorLF.duty_u16(0)
    motorRB.duty_u16(0)
    motorLB.duty_u16(0)

# 2 second delay to start the "loop"
stop()
delay(2)

while True:    
    valSensorR = SensorR.value()
    valSensorL = SensorL.value()
    valSensorC = SensorC.value()
    
    print("left: ", str(valSensorL) + " middle: " + str(valSensorC) + " right: " + str(valSensorR))
    
    # If all sensors detect Black, stop
    if valSensorR == 1 and valSensorL == 1 and valSensorC == 1 :
        stop()
    
    # If only the left sensor detects White, turn a little right
    if valSensorR == 1 and valSensorL == 0 and valSensorC == 1 :
        motorRF.duty_u16(pulsoMotor(30))
        motorLF.duty_u16(pulsoMotor(95))
    
    # If left and middle sensor detect White, turn right
    if valSensorR == 1 and valSensorL == 0 and valSensorC == 0 :
        motorRF.duty_u16(pulsoMotor(0))
        motorLF.duty_u16(pulsoMotor(95))
    
    # If only the right sensor detects White, turn a little left
    if valSensorR == 0 and valSensorL == 1 and valSensorC == 1 :
        motorRF.duty_u16(pulsoMotor(95))
        motorLF.duty_u16(pulsoMotor(30))
    
    # If right and middle sensor detect White, turn left
    if valSensorR == 0 and valSensorL == 1 and valSensorC == 0 :
        motorRF.duty_u16(pulsoMotor(95))
        motorLF.duty_u16(pulsoMotor(0))
    
    # If only the middle sensor detects Black, move forward
    if valSensorR == 0 and valSensorL == 0 and valSensorC == 1 :
        motorRF.duty_u16(pulsoMotor(85))
        motorLF.duty_u16(pulsoMotor(85))
    
    # If all sensors detect White, move forward
    if valSensorR == 0 and valSensorL == 0 and valSensorC == 0 :
        motorRF.duty_u16(pulsoMotor(85))
        motorLF.duty_u16(pulsoMotor(85))
