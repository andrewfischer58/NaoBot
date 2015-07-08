import paho.mqtt.client as mqtt
import sys
import time

def on_publish(cli, userdata, mid):
  # Disconnect after our message has been sent.
  print 'Message sent'
  cli.disconnect()

def main(arg1=0, arg2=0):
# If a match is found, the name is sent to the robot
			if arg1 != -1:
				#Find name that matches the key predicted.
				print 'Face found!' 
				print "{} is Correctly Recognized with confidence {}".format(arg1, arg2)
				
				'''
				while(os.path.isfile(path + '/subject' + str(arg1) + '.' + str(count) + '.jpg') == True):
					count += 1
		
				cv2.imwrite(path + '/subject' + str(arg1) + '.' + str(count) + '.jpg',predict_image[y: y + h, x: x + w])
				'''
				
				Subject = arg1
				name  = ''
				if(Subject == 16):
					name = 'Lincoln'
				elif(Subject == 18):
					name = 'Yiran'
				elif(Subject == 20):
					name = 'Andrew'
				else:
					name = 'stranger'
					
				print ('Hello ' + name)
				
				cli = mqtt.Mosquitto("FaceResults")
				cli.connect("54.173.42.47")
				cli.on_publish = on_publish
				time.sleep(3)
				cli.publish('response',name,2)
			else:
				print 'No faces were found!' 
				cli.publish('response','Null',2)
if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])	
	