import time
import board
import busio
import adafruit_adxl34x
from pushbullet import Pushbullet
from twilio.rest import Client

# Initialize Pushbullet API with your access token
PB_ACCESS_TOKEN = "o.3hNPT2adFWtEw8C02Zk92ETDbD6mcrow" #our access token from anishas account
pb = Pushbullet(PB_ACCESS_TOKEN)

# Initialize I2C bus and accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Thresholds for acceleration in m/s^2
X_THRESHOLD = 10  # Adjust according to your needs
Y_THRESHOLD = 10  # Adjust according to your needs
Z_THRESHOLD = 10  # Adjust according to your needs

# Function to detect accident based on acceleration
def detect_accident():
    x, y, z = accelerometer.acceleration
    if abs(x) > X_THRESHOLD or abs(y) > Y_THRESHOLD or abs(z) > Z_THRESHOLD:
        return True
    return False

# Function to send notification using Pushbullet
    
# Function to send SMS notification using Pushbullet
'''
def send_notification(title, message, phone_number):
    try:
        print(pb.devices)
        push = pb.push_sms(pb.devices[0].iden, phone_number, message)
        if push.get("active"):
            print("SMS notification sent successfully!")
        else:
            print("Failed to send SMS notification.")
    except Exception as e:
        print(f"Error sending SMS notification: {e}")
send_notification("Accident Alert", "An accident has been detected!", "+918860607907")
'''

def send_notification(title, message):
    pb.push_note(title, message)


# Main function to continuously monitor acceleration
def main():
    try:
        while True:
            if detect_accident():
                print("Accident detected!")
                send_notification("Accident Alert", "An accident has been detected!")
                # You can customize the message or include additional information
            time.sleep(5)  # Adjust sampling frequency as needed
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
