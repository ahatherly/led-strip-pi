from flask import Flask, render_template, url_for, send_from_directory
import subprocess, time

application = Flask(__name__)
patterns = None
thread = None

@application.route("/")
def index():
    return render_template('index.html')

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@application.route("/start/<pattern>")
def start(pattern):
    stop()
    subprocess.call(["/home/pi/led-strip-pi/led.sh", "start", pattern])
    return "Activated!"

@application.route("/off")
def off():
    subprocess.call(["/home/pi/led-strip-pi/led.sh", "stop"])
    return "All off!"

def stop():
    subprocess.call(["/home/pi/led-strip-pi/led.sh", "stop"])
    time.sleep(0.5)

@application.route("/rgb/<r>/<g>/<b>")
def rgb(r, g, b):
    stop()
    subprocess.call(["/home/pi/led-strip-pi/led.sh", "start", r, g, b])
    return "Activated!"

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=true)

