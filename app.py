from flask import Flask, render_template, jsonify, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# Store received symptoms data
received_symptoms = []

# MQTT settings
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "symptoms"

# MQTT client
mqtt_client = mqtt.Client()

# Connect to the MQTT broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

# MQTT message callback
def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    received_symptoms.append(payload)
    print("Received symptoms:", payload)

# Subscribe to MQTT topic
mqtt_client.on_message = on_message
mqtt_client.subscribe(MQTT_TOPIC)

# Flask routes
@app.route('/')
def home():
    return render_template('index.html')

# Route to display received symptoms
@app.route('/received-symptoms')
def display_symptoms():
    return render_template('received_symptoms.html', symptoms=received_symptoms)

# Route to receive symptoms through MQTT
@app.route('/receive-symptoms', methods=['POST'])
def receive_symptoms():
    data = request.json

    received_symptoms.append(data)
    return jsonify({'message': 'Symptoms received successfully'})

if __name__ == '__main__':
    mqtt_client.loop_start()  # Start MQTT client loop
    app.run(debug=True,port=5001)

