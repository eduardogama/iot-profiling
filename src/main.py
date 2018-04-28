from xbee import XBee, ZigBee


SERIALPORT = "/dev/ttyUSB0"    # the com/serial port the XBee is connected to, the pi GPIO should always be ttyAMA0
BAUDRATE = 9600      # the baud rate we talk to the xbee

ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=60)


class Profile:
	def __init__(self):
		self.name = ""
		self.devices = []		

def switch(x):
	return {
		'new' : 1,
		'send_message': 2,
	
	} [x]

if __name__ == '__main__':

	profiles = []
	
	print("teste")
	print(switch('new'))
	
	while True:
		
		#wating_connection
		
		
		#send_message
		break
