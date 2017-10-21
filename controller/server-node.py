import serial, time #, datetime, sys 
from xbee import XBee
    
SERIALPORT = "/dev/ttyUSB0"    # the com/serial port the XBee is connected to, the pi GPIO should always be ttyAMA0
BAUDRATE = 9600      # the baud rate we talk to the xbee

ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=60)

print ("Starting Up Tempature Monitor")

powers = ["4","3","2","1"]; # Powe LevelsM@gu!nbo2
nSeeds = 20 # Number of repetitions of the experiment
iniSeed = 1
iIntervals = [10] # Packer inter-arrival interval (ms)
name_log="teste-optical-lab-salaleandro_"
name_log+=time.strftime("%Y-%m-%d_%H:%M:%S")
file = open(name_log+".res", "w")
ACKLost=False
#PLATCMDLost=False
seedAux=iniSeed
powerAux="1"
receive_msg = 0
flag_repeat=False
cLimit=5 # muliple of time.sleep(60)

def FinishTest() :
	global flag_repeat
	global cLimit
	flag_repeat=False # Se entrou aqui eh porque ja acabou
	timer = 0
	flag = 0
	counterP=0 #initialize the counter for time waiting
	while (timer < 6) :
		ser.write("[FIN,ACK]")
		print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] FIN-ACK Sent, waiting ACK"
		timer=timer+1
		aux = ""
        #flag_repeat=True # para repetir caso no reciba nada
		#counterP=0 #initialize the counter for time waiting
		time.sleep(5)
		while True:
			#if (ser.inWaiting()>0): 
			print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] Reading serial interface"
			response = ser.read()
			print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] Serial Interface Read"
			if response == "\n" :	#Final de linea
				if aux == "[ACK]":  # Handshake finilized
					print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] CHEGOU ACK"
					#flag_repeat=False
					return # Out the while
				elif aux == "[FIN]":
					if (ser.inWaiting()>0): #Limpar o buffer. Pode ter sido recebido outra coisas! Lixo
						print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] CHEGOU FIN, Dropped Buffer: ", ser.read(ser.inWaiting())
					break #Enviar de novo FIN,ACK	
				else :				# Nesse momento somente estava se esperando o ACK				
					print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] DEU MERDA ", aux
					aux=""
					if (ser.inWaiting()>0): #Limpar o buffer. Pode ter sido recebido outra coisas! Lixo
						print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] Dropped Buffer: ", ser.read(ser.inWaiting()) 
					break # sai do while, manda de novo o FIN.ACK
			elif response != "\0" : # response = ser.read() retornou null! isso quer dizer que nao achou nada no buffer durante o tempo que ficou bloqueado o read.
				aux += response
				print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] Response: ", response 
			else :# nao tem nada no buffer
 				#time.sleep(60)
				print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] Nothing available in the buffer"
				counterP=counterP+1
				if counterP > cLimit:
					print time.strftime("%Y-%m-%d_%H:%M:%S"), "[FinishTest()] ACK did not arrive"
					#ACKLost=True # se perdeu
					return   
			#else: 
				#time.sleep(60) # Wait for 1 minute	
		time.sleep(1) # Wait for 1 second	
	
def Execution():
	global ACKLost
	#global PLATCMDLost
	global receive_msg
	global seedAux
	global powerAux
	global powers
	global iniSeed
	global nSeeds
	#global Intervals
	global flag_repeat
	global cLimit

	msg_total = 0
	aux = ""
	if ACKLost :
		print time.strftime("%Y-%m-%d_%H:%M:%S"), "[Execution()] Rescuting current state"
		initSeed = seedAux
		if flag_repeat: #Need to repeat the last test
			print "[Execution()] Uploading last state"
			if powerAux == "1":
				powers = ["1","2", "3","4"]
			elif powerAux == "2":
				powers = ["2","3","4"]
			elif powerAux == "3":
				powers = ["3","4"]
			elif powerAux == "4" :
				powers = ["4"]                     
			#ACKLost=False
		else :
			print "[Execution()] Uploading next state"
			if powerAux == "1":
				powers = ["2", "3","4"]
			elif powerAux == "2":
				powers = ["3","4"]
			elif powerAux == "3":
				powers = ["4"]
			elif powerAux == "4" :
				initSeed=initSeed+1
				powers = ["1", "2", "3","4"]                     
		ACKLost = False

	while True:
		try:
			for seed in range(iniSeed, nSeeds+1) : #repeticoes
				seedAux=seed #to save the state of the execution 
				for power in powers : # potencias
					print time.strftime("%Y-%m-%d_%H:%M:%S"), "[Execution()] Power Level has been sent"
					powerAux = power # To save the state of the execution
					ser.write(power) # Power Level (1,2,3,4)
					flag_repeat = True # para repetir caso no reciba respuesta!
					counterP = 0
					#for iInterval in iIntervals : # inter arrival interval  
					time.sleep(30) # Wait for 20 Seconds        
					while True :
						#if (ser.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
						response = ser.read()
						if response == "\n" :
							if aux == "[FIN]": # The test finilized
								FinishTest()
								aux=""
								msg_total = receive_msg
								receive_msg=0
								if ACKLost:
									print time.strftime("%Y-%m-%d_%H:%M:%S"), "[Execution()] ACKList True"
									return
								break # Out the while
							elif aux == "Starting PL" :
								print aux, " ..."
								aux = ""
							elif aux == "Starting test" :
								print aux," ..."  
								aux = ""
							else : # It is a test messages
								receive_msg=receive_msg+1
								print aux, receive_msg
								aux = ""
						  
						elif response != "\0" :
							aux += response
						else: #response=="\0"
							print time.strftime("%Y-%m-%d_%H:%M:%S"), "[Execution()] Waiting 60s for data"
							time.sleep(60) # Wait for 1 minute
							counterP=counterP+1	
							if counterP > cLimit:					
								print time.strftime("%Y-%m-%d_%H:%M:%S"), "[Execution()] Power Level was not received by the remote node", "\n", "Current State>> seed: ", seedAux,"Power: ", powerAux 	
								ACKLost=True # se perdeu
								print seedAux, powerAux, receive_msg
								receive_msg = 0
								return
					print >>file, seed, power, msg_total
					file.flush()
					print seed, power, msg_total
					#flag_repeat=False
				powers=["1", "2", "3","4"]; #reset power (needed for solving ACK problem)		
			#file.close()
			#Finished all testes 
			break #out While True
		except KeyboardInterrupt:
			exit_flag=True
			while exit_flag :
				print "Do you what to continue executing tests? [y/n]"
				responseKeyboard = raw_input()
				if responseKeyboard == "n" : 
					ACKLost = False
					exit_flag = False
					return
				elif responseKeyboard == "y":
					print "ACK does not arrive", "\n", "Current State>> seed: ", seedAux,"Power: ", powerAux 	
					ACKLost=True
					print >>file, seedAux, powerAux, receive_msg
					file.flush()
					print seedAux, powerAux, receive_msg
					receive_msg = 0
					exit_flag = False
					return
				

while True:
	Execution()
	if not ACKLost :
		break

file.close()
ser.close()
