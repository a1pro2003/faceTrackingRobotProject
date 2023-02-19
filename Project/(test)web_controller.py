from flask import Flask, render_template, request
from pubsub import pub
import paho.mqtt.client as mqtt

app = Flask(__name__)

inde = """
<h3>Our Flask Buttons<h3/>
    <form method="post" action="/">
        <input type="submit" value="RUN" name="action1"/>
        <input type="submit" value="stop" name="action2" />
    </form>

"""

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action1'] == 'VALUE1':
            print("nice")
        elif  request.form['action2'] == 'VALUE2':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return inde
    
    return inde


@app.route("/front/")
def front():
    comm = '{"dirr":2, "sped":2, "secs":1}'
    client.publish("arduino", comm)    
    return "front"

@app.route("/stop/")
def stop():
    comm = '{"dirr":0, "sped":2, "secs":1}'
    client.publish("arduino", comm)    
    return "stop"

if __name__=="__main__":
    client = mqtt.Client('client_2353251')
    client.connect('0.0.0.0', port=1883, keepalive=60, bind_address="")
    client.loop_start()
    app.run(debug=True, host="0.0.0.0", port="3333")