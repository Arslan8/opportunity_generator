import serial
import time
import numpy as np
from ahrs.filters import Madgwick

location=["BACK", "RUA", "RLA", "LUA", "LLA"]
idx =    [38, 51, 64, 77, 90]
port = input("Enter port of your device: [Default is /dev/ttyACM0]")
if not port:
    port = '/dev/ttyACM0'
baudrate = input("Enter buadrate of your device: [Default is 115200]")
if not baudrate:
    baudrate = 115200
else:
	baudrate = int(baudrate)
sensor_loc = input("Enter location of sensor. \nPossible Values: " + str(location) +"\n[Default is Right Lower Arm(RLA)]:")
if not sensor_loc:
	sensor_loc = "RLA"

# Configure the serial port
ser = serial.Serial(
    port=port,         # Replace with your port name (e.g., '/dev/ttyUSB0' on Linux)
    baudrate=baudrate,       # Set the baud rate (must match the device)
    timeout=1            # Timeout in seconds for read operations
)

location=["BACK", "RUA", "RLA", "LUA", "LLA"]
idx =    [38, 51, 64, 77, 90]

loc_idx = dict(zip(location, idx))
LOCATION = loc_idx[sensor_loc]
accX =0 
accX =1
accY =2
accZ =3
gyroX =4
gyroY =5
gyroZ =6
magnetic =7
magneticY =8
magneticZ =9
Quaternion1 =10
Quaternion2 =11
Quaternion3 =12
Quaternion4 =13

# Initialize the Madgwick filter
madgwick = Madgwick()
# Initialize quaternion (identity quaternion)
quaternion = np.array([1.0, 0.0, 0.0, 0.0])
try:
    # Check if the serial port is open
    if ser.is_open:
        print(f"Connected to {ser.port}")
    
    while True:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        if line:
            parts= line.split()
            record = [np.nan] * 250
            #Oppurtunity dataset scales by 1000
            numbers = [np.nan if "NaN" in part else 1000 *float(part)  for part in parts]
            acc = numbers[0:3]
            gyro = numbers[3:6]
            magneto = numbers[6:9]

            # Convert to NumPy arrays (optional, but often useful)
            acc = np.array(acc)
            gyro = np.array(gyro)
            quaternion = madgwick.updateIMU(gyr= gyro, acc = acc, q= quaternion)
            numbers.extend(quaternion.tolist())
            timestamp_ms = int(time.time() * 1000)
            record[0] = timestamp_ms
            record[LOCATION: LOCATION+len(numbers)] = numbers
            print(record)
        
except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Close the serial port
    ser.close()
    print("Serial port closed.")
