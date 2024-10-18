# views.py

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import paho.mqtt.client as mqtt
import json

# Global variables to store the latest received temperature and humidity data
latest_temperature = 0
latest_humidity = 0

# MQTT broker configuration
broker_address = "5.196.78.28"  # Replace with your broker's address
port = 1883  # Default MQTT port
topic = "sensor"  # Topic to subscribe to

# Callback for when a message is received from the broker
def on_message(client, userdata, msg):
    global latest_temperature, latest_humidity
    # Assuming the message is a JSON string
    try:
        data = json.loads(msg.payload.decode())
        latest_temperature = data.get('temperature', latest_temperature)
        latest_humidity = data.get('humidity', latest_humidity)
        print(f"Received message: {data} on topic {msg.topic}")
    except json.JSONDecodeError:
        print("Failed to decode JSON message")

# Callback for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)  # Subscribe to the topic
    else:
        print("Connection failed with code", rc)

# MQTT connection setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def connect_to_device(request):
    try:
        mqtt_client.connect(broker_address, port)
        mqtt_client.loop_start()  # Start the loop to listen for messages in the background
        return JsonResponse({'status': 'connected', 'message': 'Successfully connected to MQTT broker'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Home view to render HTML page for the IoT connection
def home(request):
    return render(request, "iot_connect.html")

# Function to fetch the latest temperature and humidity data
def get_latest_message(request):
    global latest_temperature, latest_humidity
    return JsonResponse({
        'status': 'success',
        'message': {
            'temperature': latest_temperature,
            'humidity': latest_humidity
        }
    })

# Function to publish a control command to the ESP8266
@csrf_exempt
def publish_control_command(request):
    if request.method == 'POST':
        command = request.POST.get('command')
        try:
            mqtt_client.publish("webapp/control", command)  # Publish command to the "webapp/control" topic
            return JsonResponse({'status': 'success', 'message': 'Command published successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def publish_form(request):
    return render(request, "publish.html")

def tracking(request):
    return render(request, "tracking.html")

def livetracking(request):
    return render(request, "livetracking.html")

def test(request):
    return render(request, "test.html")
