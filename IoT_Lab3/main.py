from machine import Pin, I2C
from bmp280 import BMP280
import network, time, json
from umqtt.simple import MQTTClient

# --- Wi-Fi Config ---
SSID = "Robotic WIFI"
PASS = "rbtWIFI@2025"

# --- ThingsBoard MQTT Config ---
TB_HOST = "mqtt.thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = b"x44taP26HT3TBYZpEpqZ"   # Replace with your actual token
TOPIC = b"v1/devices/me/telemetry"

# --- Initialize I2C & BMP280 Sensor ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c, addr=0x76)

# --- Connect Wi-Fi ---
w = network.WLAN(network.STA_IF)
w.active(True)
if not w.isconnected():
    print("Connecting to Wi-Fi...")
    w.connect(SSID, PASS)
    t = time.ticks_ms()
    while not w.isconnected():
        if time.ticks_diff(time.ticks_ms(), t) > 15000:
            raise RuntimeError("Wi-Fi connection timeout!")
        time.sleep(0.5)
print("Wi-Fi connected:", w.ifconfig())

# --- Connect to ThingsBoard MQTT ---
c = MQTTClient(client_id=b"esp32-tb",
               server=TB_HOST,
               port=TB_PORT,
               user=TB_TOKEN,
               password=b"",
               keepalive=30,
               ssl=False)

c.connect()
print("Connected to ThingsBoard Cloud")

# --- Main Loop: Read sensor + publish ---
while True:
    # Read BMP280 data
    temp = round(bmp.temperature, 2)
    press = round(bmp.pressure / 100, 2)   # Convert Pa → hPa
    alt = round(bmp.altitude, 2)

    # Prepare JSON payload
    payload = {
        "temperature": temp,
        "pressure": press,
        "altitude": alt
    }

    msg = json.dumps(payload).encode("utf-8")

    # Publish to ThingsBoard
    print("Publishing:", msg)
    try:
        c.publish(TOPIC, msg)
    except Exception as e:
        print("Publish failed:", e)
        try:
            c.connect()
            print("Reconnected to MQTT")
        except:
            print("Reconnection failed")
    
    time.sleep(5)
