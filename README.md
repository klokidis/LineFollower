# Line Follower Robot

This repository contains the code for a simple line follower robot using a microcontroller with IR sensors and motor drivers. The robot is designed to follow a black line on a white surface using three IR sensors to detect the line's position and adjust its movement accordingly.

## Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Pin Configuration](#pin-configuration)
- [Software Setup](#software-setup)
- [Functions and Logic](#functions-and-logic)
- [Usage](#usage)

## Hardware Requirements

- Microcontroller: Cytron Maker Pi RP2040
- IR Sensors (3x) for detecting the line
- Motors (2x DC motors)
- Chassis for the robot
- Batteries for power supply
- Connecting wires

## Pin Configuration

### IR Sensors

- **Right IR Sensor**: Connected to GPIO 17
- **Center IR Sensor**: Connected to GPIO 6
- **Left IR Sensor**: Connected to GPIO 16

### Motor Driver

- **IN1** (Right Forward Motor): Connected to GPIO 9
- **IN2** (Right Backwards Motor): Connected to GPIO 8
- **IN3** (Left Forward Motor): Connected to GPIO 11
- **IN4** (Left Backwards Motor): Connected to GPIO 10

### PWM Setup

- **PWM Frequency**: 490 Hz

## Software Setup

1. **Clone the Repository**: Clone this repository to your local machine.
   ```sh
   git clone https://github.com/klokidis/LineFollower.git
   cd LineFollower
   ```
2. **Upload Code**: Upload the code to your microcontroller using your preferred method (e.g., Thonny IDE for Raspberry Pi Pico).
3. **Run the Code**: Ensure your robot is powered on and the microcontroller is connected to your computer. Run the code on the microcontroller.

## Functions and Logic

### Initialization

- **IR Sensors and Motor Pins**: Set up the GPIO pins for the IR sensors and motor driver.
- **PWM Frequency**: Configure the PWM frequency for smooth motor control.

### Helper Functions

- **`map_value(x, in_min, in_max, out_min, out_max)`**: Map a value from one range to another.
- **`pulsoMotor(speed)`**: Convert speed percentage (0-100) to a 16-bit PWM pulse.
- **`stop()`**: Stop all motors.
- **Movement Functions**: Functions to move the robot forward, turn left, and turn right with varying intensities.

### Main Loop

- **Sensor Reading**: Continuously read the values from the IR sensors.
- **Decision Making**: Based on the sensor values, decide the robot's movement:
  - **All sensors black**: Stop the robot.
  - **Center sensor black**: Move forward.
  - **Left sensor white, others black**: Turn slightly right.
  - **Right sensor white, others black**: Turn slightly left.
  - **All sensors white**: Handle the last known direction to continue moving.

## Usage

1. **Setup the Robot**: Assemble the hardware components and ensure the wiring matches the pin configuration.
2. **Upload and Run**: Upload the provided code to your microcontroller.
3. **Test**: Place the robot on a track with a black line on a white surface and observe its behavior. Adjust sensor positions and thresholds if necessary.
