import serial
import time

# Serial port settings
serialPort = '/dev/tty.usbserial-FT4YCM0W'
baudRate = 38400
logFilePath = 'AML.txt'

def logData(data):
    with open(logFilePath, 'a') as logFile:
        logFile.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {data.decode('utf-8')}")
        
def main():
    try:
        # Open the serial port
        print(f"Opening serial port {serialPort} at {baudRate} baud...")
        ser = serial.Serial(serialPort, baudRate, timeout=1)
        print("Serial port opened successfully.")
        print("Sending MONITOR command to the device...")
        ser.write(b'MONITOR\r')
        print("Waiting for device to respond...")
        time.sleep(1)
        # Main loop to read and log data
        while True:
            if ser.in_waiting > 0:
                data = ser.readline()
                logData(data)
                print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {data.decode('utf-8')}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally: 
        # Close the serial port when done
        ser.close()
        
if __name__ == "__main__":
    main()