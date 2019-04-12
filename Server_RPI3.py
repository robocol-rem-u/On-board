import socket
from gpiozero import LED
import serial
import threading
import time









# Variables globales de telemetria

HOST_INTERFAZ = '192.168.0.100'
PORT_INTERFAZ = 7080

global latitude, longitude, azimuth, lineal_speed, steering_speed
global L0_speed, L1_speed, L2_speed, R0_speed, R1_speed, R2_speed
global L0_current, L1_current, L2_current, R0_current, R1_current, R2_current
global rover_temp, bat0, bat1, bat2, bat3
global joint0, joint1, joint2, joint3, joint4, joint5, joint6

latitude = longitude = azimuth = lineal_speed = steering_speed = 0
L0_speed = L1_speed = L2_speed = R0_speed = R1_speed = R2_speed = 0
L0_current = L1_current = L2_current = R0_current = R1_current = R2_current = 0
rover_temp = bat0 = bat1 = bat2 = bat3 = 0
joint0 = joint1 = joint2 = joint3 = joint4 = joint5 = joint6 = 0

# Envio a la interfaz de todos los datos de telemetria
def ThreadEnviarAInterfaz():

	global latitude, longitude, azimuth, lineal_speed, steering_speed
	global L0_speed, L1_speed, L2_speed, R0_speed, R1_speed, R2_speed
	global L0_current, L1_current, L2_current, R0_current, R1_current, R2_current
	global rover_temp, bat0, bat1, bat2, bat3
	global joint0, joint1, joint2, joint3, joint4, joint5, joint6

	while True:
		try:
			
			mensaje = "%.10f\n%.10f\n%.3f\n%.3f\n%.3f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.0f\n%.2f\n%.2f\n%.2f\n%.2f\n%.2f\n%.1f\n%.1f\n%.1f\n%.1f\n%.1f\n%.1f\n%.1f"%(latitude, longitude, azimuth, lineal_speed, steering_speed, L0_speed, L1_speed, L2_speed, R0_speed, R1_speed, R2_speed, L0_current, L1_current, L2_current, R0_current, R1_current, R2_current, rover_temp, bat0, bat1, bat2, bat3, joint0, joint1, joint2, joint3, joint4, joint5, joint6)
			socket_interfaz = socket.socket()
			socket_interfaz.connect((HOST_INTERFAZ, PORT_INTERFAZ))
			socket_interfaz.send((mensaje).encode())
		except:
			pass
		socket_interfaz.close()

	time.sleep(100E-3)

threading.Thread(target=ThreadEnviarAInterfaz).start()









# Socket para control del Rover y MUX
s = socket.socket()
host = '192.168.0.101'
port = 7070
s.bind((host, port))
s.listen(5)

# Conexion serial a la FPGA
ser = serial.Serial(port='/dev/serial0', baudrate = 115200)

# Pin de MUX en la FPGA
pinMUX = LED(26)


# Recepcion de datos de la base a la Rpi y reenvio a la FPGA, manejo del MUX
while True:
	c, addr = s.accept()
	rcv = c.recv(512).decode()

	if rcv == "C+RF":
		pinMUX.off()
	elif rcv == "C+WIFI":
		pinMUX.on()
	else:
		ser.write(rcv.encode())

	c.close()




#### FPGA COM ####


def StartServerFPGA():

	global L0_speed, L1_speed, L2_speed, R0_speed, R1_speed, R2_speed
	global L0_current, L1_current, L2_current, R0_current, R1_current, R2_current
	global joint0, joint1, joint2, joint3, joint4, joint5, joint6


	line = ""

	while(True):
		try:
			received = ser.read().decode()
			line += received

			if received == "!" or received == "#":


				signo = 1 if received=="!" else -1
				numero = signo * int(line[1:5])
				codigo = line[0]

				if codigo == 'A':
					L0_current = numero
				elif codigo == 'B':
					L1_current = numero
				elif codigo == 'C':
					L2_current = numero
				elif codigo == 'D':
					R0_current = numero
				elif codigo == 'E':
					R1_current = numero
				elif codigo == 'F':
					R2_current = numero
				elif codigo == 'G':
					joint0 = numero
				elif codigo == 'H':
					joint1 = numero
				elif codigo == 'I':
					joint2 = numero
				elif codigo == 'J':
					joint3 = numero
				elif codigo == 'K':
					joint4 = numero
				elif codigo == 'L':
					joint5 = numero
				elif codigo == 'M':
					joint6 = numero
				elif codigo == 'N':
					L0_speed = numero
				elif codigo == 'O':
					L1_speed = numero
				elif codigo == 'P':
					L2_speed = numero
				elif codigo == 'Q':
					R0_speed = numero
				elif codigo == 'R':
					R1_speed = numero
				elif codigo == 'S':
					R2_speed = numero

				line = ""


		except:
			line=""
threading.Thread(target=StartServerFPGA).start()

#### ARDUINO COM ####

serArduino = serial.Serial(port='/dev/serialArduino', baudrate = 115200)

def StartServerArduino():

	global latitude, longitude
	global bat0, bat1, bat2, bat3


	line = ""

	while(True):
		try:
			received = serArduino.read().decode()
			line += received

			if received == '\n':

				numero = float(line[1:])
				codigo = line[0]

				if codigo == 'A':
					latitude = numero
				elif codigo == 'B':
					longitude = numero
				elif codigo == 'C':
					bat0 = numero
				elif codigo == 'D':
					bat1 = numero
				elif codigo == 'E':
					bat2 = numero
				elif codigo == 'F':
					bat3 = numero



				line = ""
		except:
			line=""
threading.Thread(target=StartServerArduino).start()



