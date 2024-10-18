from django.http import JsonResponse
from django.shortcuts import render
import paho.mqtt.client as mqtt
from django.views.decorators.csrf import csrf_exempt

# Home view to render HTML page for the IoT connection
def home(request):
    return render(request, "iot_connect.html")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("esp8266/data")  # Subscribe to ESP8266 data topic
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    # You can store the message in a session or send it to the frontend as needed

# MQTT setup and connection API
def connect_to_device(request):
    broker_address = "5.196.78.28"  # Replace with your broker's address
    port = 1883  # Default MQTT port
    client = mqtt.Client(client_id="WebAppClient", protocol=mqtt.MQTTv311)  # Set client ID and MQTT version

    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        # Connect to the MQTT broker
        client.connect(broker_address, port)
        client.loop_start()  # Start the loop to handle network traffic

        return JsonResponse({'status': 'connected', 'message': 'Successfully connected to MQTT broker'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Function to publish a message to the ESP8266 control topic
@csrf_exempt
def publish_control_command(request):
    if request.method == 'POST':
        command = request.POST.get('command') 
        print(command)# Get the command from the request
        broker_address =  "5.196.78.28" # Replace with your broker's address
        port = 1883  # Default MQTT port
        client = mqtt.Client(client_id="WebAppClient", protocol=mqtt.MQTTv311)
        try:
            # Connect and publish
            client.connect(broker_address, port)
            client.publish("webapp/control", command)  # Publish command to ESP8266 control topic
            client.disconnect()
            return JsonResponse({'status': 'success', 'message': 'Command published successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def publish_form(request):
    return render(request,"publish.html")