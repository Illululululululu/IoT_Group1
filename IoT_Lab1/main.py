import network, time, urequests, json
from machine import Pin, reset
import dht

# ---------- USER CONFIG ----------
WIFI_SSID     = "QualityWIFI"
WIFI_PASSWORD = "12964246"

BOT_TOKEN     = "8314612108:AAHiF8LN4gQGacy1CtMl28ORjDalBw5ScCI"   # <-- put your token here
ALLOWED_CHAT_IDS = {-4961594574}           # auto-learn first user/group

RELAY_PIN = 2
RELAY_ACTIVE_LOW = False
POLL_TIMEOUT_S = 25
DEBUG = True

DHT_PIN = 4   # GPIO4 for DHT22
# ---------------------------------

API = "https://api.telegram.org/bot" + BOT_TOKEN
relay = Pin(RELAY_PIN, Pin.OUT)
sensor = dht.DHT22(Pin(DHT_PIN))

def _urlencode(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, int):
            v = str(v)
        s = str(v)
        s = s.replace("%", "%25").replace(" ", "%20").replace("\n", "%0A")
        s = s.replace("&", "%26").replace("?", "%3F").replace("=", "%3D")
        parts.append(str(k) + "=" + s)
    return "&".join(parts)

def log(*args):
    if DEBUG:
        print(*args)

# ---- relay control ----
def relay_on():  relay.value(0 if RELAY_ACTIVE_LOW else 1)
def relay_off(): relay.value(1 if RELAY_ACTIVE_LOW else 0)
def relay_is_on(): return (relay.value() == 0) if RELAY_ACTIVE_LOW else (relay.value() == 1)

# ---- Wi-Fi ----
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        t0 = time.time()
        while not wlan.isconnected():
            if time.time() - t0 > 25:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.25)
    print("Wi-Fi OK:", wlan.ifconfig())
    return wlan

# ---- Telegram API ----
def send_message(chat_id, text):
    try:
        url = API + "/sendMessage?" + _urlencode({"chat_id": chat_id, "text": text})
        r = urequests.get(url)
        _ = r.text
        r.close()
        log("send_message OK to", chat_id)
    except Exception as e:
        print("send_message error:", e)

def get_updates(offset=None, timeout=POLL_TIMEOUT_S):
    qs = {"timeout": timeout}
    if offset is not None:
        qs["offset"] = offset
    url = API + "/getUpdates?" + _urlencode(qs)
    try:
        r = urequests.get(url)
        data = r.json()
        r.close()
        if not data.get("ok"):
            print("getUpdates not ok:", data)
            return []
        return data.get("result", [])
    except Exception as e:
        print("get_updates error:", e)
        return []

# ---- handle commands ----
def handle_cmd(chat_id, text, T=None, H=None):
    t = (text or "").strip().lower()
    if t in ("/on", "on"):
        relay_on()
        send_message(chat_id, "Relay: ON")
    elif t in ("/off", "off"):
        relay_off()
        send_message(chat_id, "Relay: OFF")
    elif t in ("/status", "status"):
        msg = "Relay is {}\n".format("ON" if relay_is_on() else "OFF")
        if T is not None and H is not None:
            msg += "Temperature: {:.2f}°C\nHumidity: {:.2f}%".format(T, H)
        send_message(chat_id, msg)
    elif t in ("/whoami", "whoami"):
        send_message(chat_id, "Your chat id is: {}".format(chat_id))
    elif t in ("/start", "/help", "help"):
        send_message(chat_id, "Commands:\n/on\n/off\n/status\n/whoami")
    else:
        send_message(chat_id, "Unknown. Try /on, /off, /status, /whoami")

# ---- main loop ----
def main():
    connect_wifi()
    relay_off()

    last_id = None
    old = get_updates(timeout=1)
    if old:
        last_id = old[-1]["update_id"]

    print("Bot running. Waiting for commands…")
    global ALLOWED_CHAT_IDS

    alerting = False
    auto_off_sent = False

    while True:
        # --- ensure Wi-Fi connected ---
        wlan = network.WLAN(network.STA_IF)
        if not wlan.isconnected():
            print("⚠️ Wi-Fi not connected. Waiting for reconnection...")
            try:
                connect_wifi()
            except Exception as e:
                print("Wi-Fi reconnect failed:", e)
                time.sleep(5)
                continue   # Skip this cycle entirely until Wi-Fi is back

        # --- read sensor safely ---
        try:
            sensor.measure()
            T = sensor.temperature()
            H = sensor.humidity()
            log("Sensor: {:.2f}°C, {:.2f}%".format(T, H))
        except OSError:
            print("DHT read error, skipping cycle")
            time.sleep(5)
            continue

        # --- handle telegram updates ---
        updates = get_updates(offset=(last_id + 1) if last_id is not None else None)
        for u in updates:
            last_id = u["update_id"]
            msg = u.get("message") or u.get("edited_message")
            if not msg:
                continue
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            log("From", chat_id, ":", text)

            if not ALLOWED_CHAT_IDS:
                ALLOWED_CHAT_IDS = {chat_id}
                log("Learned ALLOWED_CHAT_IDS =", ALLOWED_CHAT_IDS)
                send_message(chat_id, "Authorized. You can now control the relay.")

            if chat_id not in ALLOWED_CHAT_IDS:
                send_message(chat_id, "Not authorized.")
                continue

            handle_cmd(chat_id, text, T, H)

        # --- task 4 behavior ---
        if ALLOWED_CHAT_IDS:
            chat_id = next(iter(ALLOWED_CHAT_IDS))  # pick one group/user
            if T >= 30 and not relay_is_on():
                send_message(chat_id, "⚠️ ALERT: Temp {:.2f}°C ≥ 30, Relay is OFF!".format(T))
                alerting = True
                auto_off_sent = False
            elif relay_is_on():
                alerting = False
                if T < 30:
                    relay_off()
                    if not auto_off_sent:
                        send_message(chat_id, "✅ Temp dropped < 30°C. Relay auto-OFF.")
                        auto_off_sent = True
            else:
                alerting = False

        time.sleep(5)

try:
    main()
except Exception as e:
    print("Fatal error:", e)
    time.sleep(5)
    reset()

