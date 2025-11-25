# README – Lab 5: Mobile App DC Motor Control with Grafana Dashboard

## I. Overview
This project implements a complete IoT actuation system where an **ESP32** controls a **DC motor** through a web server, and a **mobile app (MIT App Inventor)** is used to send commands over Wi-Fi.  
All motor actions (forward, backward, stop, and speed changes) are logged to **InfluxDB** and visualized on a **Grafana** dashboard.

The system integrates:
- ESP32 (MicroPython)
- L298N motor driver
- MIT App Inventor mobile app
- InfluxDB (logging)
- Grafana (visualization)

## II. Features
- ✔️ Control DC motor direction (Forward / Backward / Stop)  
- ✔️ Adjust speed using PWM (0–100%)  
- ✔️ HTTP REST endpoints exposed by the ESP32  
- ✔️ Mobile app sends commands to ESP32 via Wi-Fi  
- ✔️ Every motor action logged to InfluxDB  
- ✔️ Grafana dashboard shows speed, direction, and event timeline  
- ✔️ Auto-reconnect Wi-Fi logic  

## III. System Architecture
1. **Mobile App → ESP32 Web Server**  
   - App sends HTTP requests like:  
     - `/forward?speed=70`  
     - `/backward?speed=40`  
     - `/stop`  
     - `/speed?value=75`

2. **ESP32 → Motor (via L298N)**  
   - ENA pin controls speed (PWM)  
   - IN1 & IN2 control direction  

3. **ESP32 → InfluxDB**  
   - Sends JSON logs:  
     ```json
     {
       "timestamp": "2025-01-01T12:00:00Z",
       "action": "forward",
       "speed": 70
     }
     ```

4. **Grafana Dashboard**  
   - Plots motor speed over time  
   - Shows latest command and event logs  

## IV. Hardware Used
- ESP32 Dev Board (MicroPython)
- L298N Motor Driver
- DC Motor
- External power supply (7–12V)
- Jumper wires & breadboard
- Android phone (MIT App Inventor)
- InfluxDB (local or cloud)
- Grafana (local or cloud)

## V. ESP32 API Endpoints
| Endpoint                | Description |
| |
| `/forward?speed=NN`     | Motor rotates forward at NN% speed |
| `/backward?speed=NN`    | Motor rotates backward at NN% speed |
| `/stop`                 | Stops the motor |
| `/speed?value=NN`       | Changes speed without changing direction |


