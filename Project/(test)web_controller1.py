from flask import Flask, render_template, request
from pubsub import pub
import paho.mqtt.client as mqtt

app = Flask(__name__)

inde = """
<style>
.button1 {
  position: absolute;
  left: 60px;
  top: 60px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
.button2 {
  position: absolute;
  left: 60px;
  top: 100px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
.button3 {
  position: absolute;
  left: 100px;
  top: 80px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
.button4 {
  position: absolute;
  left: 20px;
  top: 80px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
.button0 {
  position: absolute;
  left: 140px;
  top: 80px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}
</style>
<h3>Our Flask Buttons<h3/>
    <form method="post" action="/">
        <input class="button1" type="submit" value="F" name="action1"/>
        <input class="button2" type="submit" value="B" name="action2" />
        <input class="button3" type="submit" value="R" name="action3" />
        <input class="button4" type="submit" value="L" name="action4" />
        <input class="button0" type="submit" value="S" name="action0" />
    </form>

"""

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action1') == 'F':
            comm = '{"dirr":1, "sped":2, "secs":1}'
            client.publish("arduino", comm)
            
        elif request.form.get('action2') == 'B':
            comm = '{"dirr":2, "sped":2, "secs":1}'
            client.publish("arduino", comm)
            
        elif request.form.get('action3') == 'R':
            comm = '{"dirr":3, "sped":2, "secs":1}'
            client.publish("arduino", comm)
            
        elif request.form.get('action4') == 'L':
            comm = '{"dirr":4, "sped":2, "secs":1}'
            client.publish("arduino", comm)
            
        elif request.form.get('action0') == 'S':
            comm = '{"dirr":0, "sped":2, "secs":1}'
            client.publish("arduino", comm)
            
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
    app.run(debug=True, host="0.0.0.0", port="4333")