from flask import Flask, render_template, Response
from camera import Camera
import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set variables for the GPIO motor pins
pinMotorAForwards = 9
pinMotorABackwards = 10
pinMotorBForwards = 8
pinMotorBBackwards = 7

# How many times to turn the pin on and off each second
Frequency = 20
# How long the pin stays on each cycle, as a percent
DutyCycleA = 60
DutyCycleB = 60  
# Settng the duty cycle to 0 means the motors will not turn
Stop = 0

# Set the GPIO Pin mode to be Output
GPIO.setup(pinMotorAForwards, GPIO.OUT)
GPIO.setup(pinMotorABackwards, GPIO.OUT)
GPIO.setup(pinMotorBForwards, GPIO.OUT)
GPIO.setup(pinMotorBBackwards, GPIO.OUT)

# Set the GPIO to software PWM at 'Frequency' Hertz
pwmMotorAForwards = GPIO.PWM(pinMotorAForwards, Frequency)
pwmMotorABackwards = GPIO.PWM(pinMotorABackwards, Frequency)
pwmMotorBForwards = GPIO.PWM(pinMotorBForwards, Frequency)
pwmMotorBBackwards = GPIO.PWM(pinMotorBBackwards, Frequency)

# Start the software PWM with a duty cycle of 0 (i.e. not moving)
pwmMotorAForwards.start(Stop)
pwmMotorABackwards.start(Stop)
pwmMotorBForwards.start(Stop)
pwmMotorBBackwards.start(Stop)
# Turn all motors off
def StopMotors():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors forwards
def Forwards():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn both motors backwards
def Backwards():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)

# Turn right
def Right():
    pwmMotorAForwards.ChangeDutyCycle(Stop)
    pwmMotorABackwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorBForwards.ChangeDutyCycle(DutyCycleB)
    pwmMotorBBackwards.ChangeDutyCycle(Stop)

# Turn left
def Left():
    pwmMotorAForwards.ChangeDutyCycle(DutyCycleA)
    pwmMotorABackwards.ChangeDutyCycle(Stop)
    pwmMotorBForwards.ChangeDutyCycle(Stop)
    pwmMotorBBackwards.ChangeDutyCycle(DutyCycleB)


app = Flask(__name__)

@app.route('/')
def index():
    message = "ahhhhhhh"
    return render_template('index.html', message=message)

@app.route("/stream/")
def stream():
	return render_template('stream.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()),
		mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    Forwards()
    time.sleep(.5)
 
    #Right()
    #time.sleep(0.5)

#    Backwards()
#    time.sleep(.5)

    StopMotors()

#    GPIO.cleanup()

    forward_message = "Moving Forward..."
    return render_template('index.html', forward_message=forward_message);

@app.route("/back/", methods=['POST'])
def move_back():
    #Moving forward code
    Backwards()
    time.sleep(.5)
    StopMotors()

#    GPIO.cleanup()

    forward_message = "Moving Backwards..."
    return render_template('index.html', forward_message=forward_message);

@app.route("/right/", methods=['POST'])
def move_right():
    #Moving forward code
    Right()
    time.sleep(.5)
    StopMotors()

#    GPIO.cleanup()

    forward_message = "Moving right..."
    return render_template('index.html', forward_message=forward_message);

@app.route("/left/", methods=['POST'])
def move_left():
    #Moving forward code
    Left()
    time.sleep(.5)
    StopMotors()

#    GPIO.cleanup()

    forward_message = "Moving left..."
    return render_template('index.html', forward_message=forward_message);





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
