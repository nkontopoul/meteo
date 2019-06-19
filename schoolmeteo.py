import httplib
import urllib
import time
import Adafruit_DHT as dht
import bme280
import smbus2
import Si1145 as Sensor

Sensor.Si1145_Init()


key = ""  #  API Key here
port=1
address=0x77 # pressure sensor
bus=smbus2.SMBus(port)
bme280.load_calibration_params(bus,address)
def meter():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        temp1 = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        humi, temp = dht.read_retry(dht.DHT22, 23)
   	vis=Sensor.Si1145_readVisible()
    	IR=Sensor.Si1145_readIR()
    	UVindex=Sensor.Si1145_readUV()
    	temp = '%.2f' % temp
    	humi = '%.2f' % humi
    	bme280_data=bme280.sample(bus,address)
    	secondarytemp=bme280_data.temperature
    	pressure=bme280_data.pressure
    	params = urllib.urlencode({'field1': temp, 'field2': humi ,'field3': temp1 ,'field4': pressure, 'field5': IR,'field6': vis,'field7': UVindex, 'key':key }) 
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print temp, humi, temp1, pressure, IR, vis, UVindex
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
            break
if __name__ == "__main__":
        while True:
                meter()
