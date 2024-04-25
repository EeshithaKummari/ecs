import time
import head_pose
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

# Vibration motor
GPIO.setmode(GPIO.BOARD)
motor_pin = 11  # Change this to the GPIO pin connected to the motor driver or transistor
GPIO.setup(motor_pin, GPIO.OUT)

PLOT_LENGTH = 200

GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.3
XDATA = list(range(200))
YDATA = [0]*200

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return 1 * previous + 0.1 * current

def process():
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT, CHEAT_THRESH
    if GLOBAL_CHEAT == 0:
        if head_pose.X_AXIS_CHEAT == 0:
            if head_pose.Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
        else:
            if head_pose.Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)
    else:
        if head_pose.X_AXIS_CHEAT == 0:
            if head_pose.Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.2, PERCENTAGE_CHEAT)
        else:
            if head_pose.Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)

    if PERCENTAGE_CHEAT > CHEAT_THRESH:
        GLOBAL_CHEAT = 1
        print("CHEATING")
        GPIO.output(motor_pin, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(motor_pin, GPIO.LOW)
        time.sleep(10)
    else:
        GLOBAL_CHEAT = 0
    print("Cheat percent: ", PERCENTAGE_CHEAT, GLOBAL_CHEAT)

def run_detection():
    global XDATA, YDATA
    plt.show()
    axes = plt.gca()
    axes.set_xlim(0, 200)
    axes.set_ylim(0, 1)
    line, = axes.plot(XDATA, YDATA, 'r-')
    plt.title("Suspicious Behavior Detection")
    plt.xlabel("Time")
    plt.ylabel("Cheat Probability")
    while True:
        YDATA.pop(0)
        YDATA.append(PERCENTAGE_CHEAT)
        line.set_xdata(XDATA)
        line.set_ydata(YDATA)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(1/5)
        process()
