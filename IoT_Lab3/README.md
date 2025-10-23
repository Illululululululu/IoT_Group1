# 🌤️ IoT Atmospheric Sensor Using BMP280 and ESP32

## 📘 Project Overview
This project demonstrates the development of a simple **IoT-based environmental monitoring system** using an **ESP32 microcontroller** and a **BMP280 sensor**.  
The BMP280 measures **temperature**, **pressure**, and **altitude**, while the ESP32 reads, processes, and sends the data to the cloud for real-time visualization on a dashboard.  
The primary goal is to understand how sensors communicate with microcontrollers via the **I²C protocol** and how to transmit environmental data accurately using IoT technologies.

---

## 🎯 Objectives
- Interface the **BMP280** sensor with an **ESP32** using **MicroPython**.  
- Read and analyze **temperature**, **pressure**, and **altitude** data.  
- Understand and apply the **I²C communication protocol**.  
- Program and upload scripts using **Thonny IDE**.  
- Calculate **altitude** from atmospheric pressure readings.  
- Use the **MQTT protocol** for efficient IoT data transmission.  
- Connect the ESP32 to **ThingsBoard Cloud** for real-time data visualization.  
- Demonstrate real-world applications like **weather monitoring** and **drone altitude tracking**.

---

## 🧰 Components Required
- ESP32 development board (flashed with **MicroPython**)  
- BMP280 sensor module  
- Jumper wires  
- USB cable and laptop with **Thonny IDE**  
- Active Wi-Fi connection (for IoT cloud connection)

---

## ⚙️ Circuit Connections

| ESP32 Pin | BMP280 Pin | Description |
|------------|-------------|-------------|
| 3V3 | VCC | Power supply |
| GND | GND | Ground |
| GPIO22 | SCL | I²C clock line |
| GPIO21 | SDA | I²C data line |

---

## 🧩 Wiring Diagram
![Wiring Diagram](wiring_lab3.png)  

**Example connections:**  
- `ESP32 GPIO22 → BMP280 SCL`  
- `ESP32 GPIO21 → BMP280 SDA`

---

## 🚀 Setup and Configuration

1. Flash your **ESP32** with **MicroPython firmware**.  
2. Open **Thonny IDE** and connect to your ESP32 board.  
3. Upload the `bmp280.py` driver file to your ESP32.  
4. Create a new file named `main.py` and update the configuration below:

   ```python
   # Wi-Fi Credentials
   WIFI_SSID = 'Your_WiFi_Name'
   WIFI_PASSWORD = 'Your_WiFi_Password'

   # MQTT Configuration
   MQTT_BROKER = "test.mosquitto.org"   # Public MQTT broker
   MQTT_PORT   = 1883                   # Default MQTT port
   CLIENT_ID   = b"YourClientID"
   TOPIC       = b"YourTopic"

    
---

## How It Works
1. The ESP32 initializes communication with the BMP280 sensor over the I²C protocol.
2. The BMP280 measures the barometric pressure and temperature of the environment.
3. Using these readings, it estimates altitude based on the barometric formula.
4. Random values (10–20) every 5 seconds.
5. Those datas publish to ThingsBoard dashboards via **MQTT**.

---

## MQTT

---

## ThingsBoard 


