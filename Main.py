from flask import Flask, render_template, request
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
broker = 'broker.emqx.io'
port = 1883
topic = 'topicName/spaceIot'

client_id = 'test'
username = 'emqx'
password = ''

def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.connect(broker, port)
    return client

def send_data(client, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send {msg} to topic {topic}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        client = connect_mqtt()
        client.loop_start()
        button_value = request.form['btn']
        send_data(client, button_value)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5001)
