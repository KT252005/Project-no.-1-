import paho.mqtt.client as mqtt

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        # Subscribe to a topic after successful connection
        client.subscribe("your/topic")
    else:
        print("Connection failed with code", rc)

# Callback when a message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

# MQTT setup and connection
def connect_to_mqtt():
    broker_address = "5.196.78.28"  # Replace with your broker's address
    port = 1883  # Default MQTT port
    client = mqtt.Client(client_id="Client_ID", protocol=mqtt.MQTTv311)  # Set client ID and MQTT version

    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    try:
        client.connect(broker_address, port)
        client.loop_start()  # Start a background network loop
        print("Connecting to MQTT broker...")
    except Exception as e:
        print("Failed to connect to MQTT broker:", str(e))


