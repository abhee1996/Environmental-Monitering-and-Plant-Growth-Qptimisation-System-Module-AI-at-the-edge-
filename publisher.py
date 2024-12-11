import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import os

broker = "192.168.0.32"#"192.168.6.67"  # Replace with your Mosquitto broker's IP address
topic = "sensor/temperature"
topic2 = "sensor/LightResistor"

GPIO.setmode(GPIO.BOARD)  
resistorPin = 7          # Pin number connected to the photoresistor (physical numbering)


client = mqtt.Client()
try:
    print("Connecting to broker...")
    client.connect(broker, 1883, 60)
    print("Connected to broker.")
    
    while True:
        #temp_output = os.popen("vcgencmd measure_temp").readline()
        #temp = temp_output.replace("temp=", "").strip()
        GPIO.setup(resistorPin, GPIO.OUT)  # Set the pin as output mode
        GPIO.output(resistorPin, GPIO.LOW)  # Set the pin to low (grounded)
        time.sleep(0.1)                     # Wait for 0.1 seconds to ensure the capacitor is fully discharged

        
        GPIO.setup(resistorPin, GPIO.IN)    # Set the pin back to input mode
        currentTime = time.time()           # Record the current time
        diff = 0                            # Initialize the time difference variable
        while GPIO.input(resistorPin) == GPIO.LOW:  # Wait until the pin state changes to HIGH
            diff = time.time() - currentTime        # Calculate the elapsed time
        lit=diff*1000
        print(diff * 1000)              # Print the elapsed time in milliseconds
        time.sleep(1)                   # Wait 1 second before taking the next measurement
        
        print(f"Publishing: {lit} to topic {topic2}")
        print(f"Publishing: {lit} to topic {topic2}")

        result = client.publish(topic2, lit)  

        # Check publish status
        status = result[0]
        if status == 0:
            print(f"Successfully sent: {lit}")
        else:
            print(f"Failed to send message to topic {topic2}")

        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")
finally:
    client.disconnect()