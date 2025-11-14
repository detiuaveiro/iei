from machine import Pin
import time
import dht
import network
#import ntptime
import picozero
import ujson

from umqtt.simple import MQTTClient

ssid = 'TheOffice'
password = '8006002030'
#ntptime.host = 'pt.pool.ntp.org'
#ntptime.host = 'time.ua.pt'

led = Pin("LED", Pin.OUT)

#sensor = dht.DHT11(Pin(22))
sensor = dht.DHT22(Pin(22))

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
status = wlan.ifconfig()
print('Connected to WiFi: %s' %status[0])

#led.on()
#ntptime.settime()
#print(time.localtime())
#led.off()

mqtt_host = "192.168.0.102"
mqtt_username = ""
mqtt_password = ""
mqtt_publish_topic = "deti/pico/dht11"

mqtt_client_id = "random_name_42"

mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

try:
    while True:
        time.sleep(2)
        
        led.on()
        sensor.measure()
        timestamp = time.time()
        temp = sensor.temperature()
        hum = sensor.humidity()
        print('Timestamp: %d' %timestamp)
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
        print('')
        
        mqtt_client.publish(mqtt_publish_topic, ujson.dumps({'ts':timestamp, 't':temp, 'h':hum}))
        led.off()
    
except OSError as e:
    print('Failed to read sensor.')
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()
