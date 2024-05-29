from machine import Pin, PWM
from utime import sleep as delay
import time

# Pin setup for IR Sensors
SensorR = Pin(17, Pin.IN)  # Right IR Sensor
SensorC = Pin(6, Pin.IN)   # Center IR Sensor
SensorL = Pin(16, Pin.IN)  # Left IR Sensor

# Pin setup for Motor Driver
IN1 = Pin(9, Pin.OUT)  # IN1 Motor Driver
IN2 = Pin(8, Pin.OUT)  # IN2 Motor Driver
IN3 = Pin(11, Pin.OUT) # IN3 Motor Driver
IN4 = Pin(10, Pin.OUT) # IN4 Motor Driver

# PWM setup for motors
motorRF = PWM(IN1)  # Right Forward Motor
motorRB = PWM(IN2)  # Right Backwards Motor
motorLF = PWM(IN3)  # Left Forward Motor
motorLB = PWM(IN4)  # Left Backwards Motor

# Setting PWM frequency
PWM_FREQUENCY = 490
motorRF.freq(PWM_FREQUENCY)
motorRB.freq(PWM_FREQUENCY)
motorLF.freq(PWM_FREQUENCY)
motorLB.freq(PWM_FREQUENCY)

hardTurn = 100
lightTurn = 95
forward = 95

lastError = 0
integral = 0

# Equivalent to map() function
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - out_min) + out_min

# Function to convert speed from 0 to 100 into 16-bit PWM pulse
def pulsoMotor(speed):
    return map_value(speed, 0, 100, 0, 65534)

# Function to stop all the motors from moving
def stop():
    motorRF.duty_u16(0)
    motorLF.duty_u16(0)
    motorRB.duty_u16(0)
    motorLB.duty_u16(0)

# Functions to move the motors
def move_forward(speed):
    pulse = pulsoMotor(speed)
    motorRF.duty_u16(pulse)
    motorLF.duty_u16(pulse)

def turn_right(speed):
    motorRF.duty_u16(pulsoMotor(20))
    motorLF.duty_u16(pulsoMotor(speed))

def turn_left(speed):
    motorRF.duty_u16(pulsoMotor(speed))
    motorLF.duty_u16(pulsoMotor(20))
    
def turn_left_light(speed):
    motorRF.duty_u16(pulsoMotor(speed))
    motorLF.duty_u16(pulsoMotor(speed-60))
    
def turn_right_light(speed):
    motorRF.duty_u16(pulsoMotor(speed-60))
    motorLF.duty_u16(pulsoMotor(speed))

# Function to handle the car stopping and turning to the last detected turn direction
def handle_all_white(last_turn):
    if last_turn == "left":
        turn_left(100)
        last_turn = "left"
    elif last_turn == "right":
        turn_right(100)
        last_turn = "right"
    elif last_turn == "forward":
        move_forward(45)
        last_turn = "forward"
    else:
        print("Unknown last turn direction: Stopping for safety")
        stop()

# Initial delay to start the loop
stop()
delay(2)

# Variable to keep track of the last turn direction
last_turn = None

while True:
    valSensorR = SensorR.value()
    valSensorL = SensorL.value()
    valSensorC = SensorC.value()

    # Debugging: Print the current state of sensors
    print(f"left: {valSensorL}, middle: {valSensorC}, right: {valSensorR}")

    # Sensor logic
    if valSensorR == 1 and valSensorL == 1 and valSensorC == 1:
        print("All black: Stopping")
        stop()
        break
    elif valSensorR == 0 and valSensorL == 0 and valSensorC == 1:
        print("Middle black: Moving forward")
        move_forward(forward)
        last_turn = "forward"
    elif valSensorR == 1 and valSensorL == 0 and valSensorC == 1:
        print("Left white, others black: Turning slightly right")
        turn_right_light(lightTurn)
        last_turn = "right"
    elif valSensorR == 1 and valSensorL == 0 and valSensorC == 0:
        print("Left and middle white: Turning right")
        turn_right(hardTurn)
        last_turn = "right"
    elif valSensorR == 0 and valSensorL == 1 and valSensorC == 1:
        print("Right white, others black: Turning slightly left")
        turn_left_light(lightTurn)
        last_turn = "left"
    elif valSensorR == 0 and valSensorL == 1 and valSensorC == 0:
        print("Right and middle white: Turning left")
        turn_left(hardTurn)
        last_turn = "left"
    elif valSensorR == 0 and valSensorL == 0 and valSensorC == 0:
        print("All white: Handling situation")
        handle_all_white(last_turn)
    else:
        print("Unknown state: Stopping for safety")
        stop()

    time.sleep_ms(10)  # Small delay to stabilize the sensor readings
