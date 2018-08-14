import requests
from picamera import PiCamera
from time import sleep

#THE CAMERA RECORDS ONE FRAME
camera.start_preview()
for i in range(1):
sleep(0)
camera.capture('/home/pi/auto_park/picamera/car01.jpg')
camera.stop_preview()

# change this to your prod url
url = "http://project-inbarapp.nkxpp8m2v7.us-east-2.elasticbeanstalk.com/upload"
#provide image locatopm
photo = open('/home/pi/auto_park/picamera/car01.jpg', 'rb')
files = {'user_file': photo}
try:
   r = requests.post(url, files=files)
   if r.text=="1":
		print ("***")
		import RPi.GPIO as GPIO
		import time
		control = [9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15]
		servo = 22
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(servo,GPIO.OUT)
		# in servo motor,
		# 1ms pulse for 0 degree (LEFT)
		# 1.5ms pulse for 90 degree (MIDDLE)
		# 2ms pulse for 180 degree (RIGHT)
		
		# so for 50hz, one frequency is 20ms
		# duty cycle for 0 degree = (1/20)*100 = 5%
		# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
		# duty cycle for 180 degree = (2/20)*100 = 10%
		
		p=GPIO.PWM(servo,50)# 50hz frequency
		p.start(1)# starting duty cycle ( it set the servo to 0 degree )
		try:
			   while True:
				   for x in range(12):
					 p.ChangeDutyCycle(control[x])
					 time.sleep(0.5)
					 print x
					 
				   for x in range(9,0,-1):
					 p.ChangeDutyCycle(control[x])
					 time.sleep(0.5)
					 print x
				   
		except KeyboardInterrupt:
			GPIO.cleanup()
   print r.text
   


	   
finally:
   photo.close()
   
   
