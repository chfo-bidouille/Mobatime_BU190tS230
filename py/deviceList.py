import serial

# Open connection
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Send data
ser.write(b'Hello Serial World!\n')

# Read response
response = ser.readline()
print(response.decode('utf-8').strip())

# Close connection
ser.close()
