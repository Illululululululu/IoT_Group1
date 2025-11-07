\# Lab 4: MQTT Communication with BMP280 Sensor

\#\# 📘 Project Overview  
This project demonstrates the development of a simple \*\*IoT-based environmental monitoring system\*\* using an \*\*ESP32 microcontroller\*\* and a \*\*BMP280 sensor\*\*.    
The BMP280 measures \*\*temperature\*\*, \*\*pressure\*\*, and \*\*altitude\*\*, while the ESP32 reads, processes, and transmits these data to an \*\*MQTT broker\*\* for remote monitoring.    
The objective is to understand how to interface sensors using the \*\*I²C protocol\*\* and send sensor data to an IoT platform using \*\*MQTT communication\*\*.

\---

\#\# 🎯 Objectives  
\- Interface the \*\*BMP280 sensor\*\* with an \*\*ESP32\*\* using \*\*MicroPython\*\*.    
\- Read and analyze \*\*temperature\*\*, \*\*pressure\*\*, and \*\*altitude\*\* data.    
\- Understand and apply the \*\*I²C communication protocol\*\*.    
\- Program and upload scripts using \*\*Thonny IDE\*\*.    
\- Convert pressure readings into \*\*altitude\*\* values.    
\- Use the \*\*MQTT protocol\*\* for efficient IoT data transfer.    
\- Connect the ESP32 to a \*\*public MQTT broker (test.mosquitto.org)\*\* for real-time data transmission.    
\- Demonstrate real-world applications such as \*\*weather monitoring\*\* and \*\*altitude tracking\*\*.

\---

\#\# 🧰 Components Required  
| No. | Component | Quantity | Description |  
|:---:|:-----------|:----------:|:-------------|  
| 1 | ESP32 | 1 | Microcontroller with built-in Wi-Fi |  
| 2 | BMP280 Sensor | 1 | Measures temperature, pressure, and altitude |  
| 3 | Breadboard | 1 | For prototyping connections |  
| 4 | Jumper Wires | Some | For I²C wiring |  
| 5 | USB Cable | 1 | For ESP32 connection to PC |  
| 6 | Laptop/PC | 1 | Running \*\*Thonny IDE\*\* with MicroPython support |

\---

\#\# ⚙️ Circuit Connections

| ESP32 Pin | BMP280 Pin | Description |  
|------------|-------------|-------------|  
| 3V3 | VCC | Power supply |  
| GND | GND | Ground connection |  
| GPIO22 | SCL | I²C Clock Line |  
| GPIO21 | SDA | I²C Data Line |

\---

\#\# 🧩 Wiring Diagram  
\!\[Wiring Diagram\](wiring\_lab4.png)

\*\*Example connection details:\*\*  
\- \`ESP32 GPIO22 → BMP280 SCL\`    
\- \`ESP32 GPIO21 → BMP280 SDA\`    
\- \`3.3V → VCC\`    
\- \`GND → GND\`

\---

\#\# 🚀 Setup and Configuration

1\. \*\*Flash MicroPython\*\* onto your ESP32 using the latest firmware.    
2\. Open \*\*Thonny IDE\*\* and select your ESP32 board under the interpreter settings.    
3\. Upload the \`bmp280.py\` driver file to your ESP32 device.    
4\. Create a new file named \`main.py\` and paste the full code provided below.    
5\. Update your \*\*Wi-Fi credentials\*\* and \*\*MQTT topic\*\* if needed.  

\---

\#\#\# 🧠 Wi-Fi and MQTT Configuration

| Setting | Value |  
|:--------|:-------|  
| \*\*Wi-Fi SSID\*\* | \`Robotic WIFI\` |  
| \*\*Wi-Fi Password\*\* | \`rbtWIFI@2025\` |  
| \*\*MQTT Broker\*\* | \`test.mosquitto.org\` |  
| \*\*MQTT Port\*\* | \`1883\` |  
| \*\*Client ID\*\* | \`esp32\_bmp280\_1\` |  
| \*\*Topic\*\* | \`/aupp/esp32/visal\` |

\---

\#\# 💻 Source Code

\`\`\`python  
import network, time  
from umqtt.simple import MQTTClient  
from machine import Pin, I2C  
from bmp280 import BMP280

\# \==== WiFi & MQTT Config \====  
SSID \= "Robotic WIFI"  
PASSWORD \= "rbtWIFI@2025"

BROKER \= "test.mosquitto.org"  
PORT \= 1883  
CLIENT\_ID \= b"esp32\_bmp280\_1"  
TOPIC \= b"/aupp/esp32/visal"  
KEEPALIVE \= 30

\# \==== Connect to WiFi \====  
def wifi\_connect():  
    wlan \= network.WLAN(network.STA\_IF)  
    wlan.active(True)  
    if not wlan.isconnected():  
        print("Connecting to WiFi...")  
        wlan.connect(SSID, PASSWORD)  
        t0 \= time.ticks\_ms()  
        while not wlan.isconnected():  
            if time.ticks\_diff(time.ticks\_ms(), t0) \> 20000:  
                raise RuntimeError("Wi-Fi connect timeout")  
            time.sleep(0.3)  
    print("WiFi OK:", wlan.ifconfig())  
    return wlan

\# \==== MQTT Client \====  
def make\_client():  
    return MQTTClient(client\_id=CLIENT\_ID, server=BROKER, port=PORT, keepalive=KEEPALIVE)

def connect\_mqtt(client):  
    time.sleep(0.5)  
    client.connect()  
    print("MQTT connected")

\# \==== BMP280 Setup \====  
def setup\_bmp280():  
    i2c \= I2C(0, scl=Pin(22), sda=Pin(21))  
    bmp \= BMP280(i2c, addr=0x76)  
    return bmp

\# \==== Main Loop \====  
def main():  
    wifi\_connect()  
    client \= make\_client()  
    bmp \= setup\_bmp280()

    while True:  
        try:  
            connect\_mqtt(client)  
            while True:  
                temperature \= bmp.temperature  
                pressure \= bmp.pressure / 100  \# Convert Pa → hPa  
                altitude \= bmp.altitude

                msg \= '{{"temperature": {:.2f}, "pressure": {:.2f}, "altitude": {:.2f}}}'.format(  
                    temperature, pressure, altitude  
                )

                client.publish(TOPIC, msg)  
                print("Sent:", msg)  
                time.sleep(5)

        except OSError as e:  
            print("MQTT error:", e)  
            try:  
                client.close()  
            except:  
                pass  
            print("Retrying MQTT in 3s...")  
            time.sleep(3)

main()

\# \==== How It Works \====  
"""  
1️⃣ The ESP32 powers on and initializes a connection to the configured Wi-Fi network using the SSID and password.

2️⃣ The BMP280 sensor communicates with the ESP32 through the I²C protocol, where:  
   \- SDA (Data) connects to GPIO21  
   \- SCL (Clock) connects to GPIO22

3️⃣ The ESP32 continuously reads the following environmental parameters from the BMP280:  
   \- Temperature (°C)  
   \- Pressure (hPa)  
   \- Altitude (m)

4️⃣ The sensor readings are formatted into a JSON message such as:  
   {"temperature": 28.34, "pressure": 1007.15, "altitude": 24.12}

5️⃣ The ESP32 connects to the public MQTT broker at test.mosquitto.org and publishes the JSON message every 5 seconds to the topic /aupp/esp32/visal.

6️⃣ Any MQTT client (e.g., MQTT Explorer, HiveMQ Web Client, or Node-RED) subscribed to the topic will receive the real-time data.

7️⃣ The loop continues indefinitely, and in case of an error (e.g., Wi-Fi drop or MQTT disconnection), the system automatically retries after 3 seconds.  
"""

