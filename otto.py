import sys
import math

Pi = 3.141592653
R = 8.3144621
numSteps = 10000
nsElements = 100
nsSteps = 10000
nsLength = 1.0
Bore = 0.14
Stroke = 0.14
PortArea = Pi*(Bore/4)**2
Compression = 6.7
Gamma = 7.0/5.0
Alpha = Gamma/(Gamma-1)
airMolMass = 0.02897
portLength = 0.01

RotationRate = 1000 * 0.104719755
SecondsPerRadian = 1/(RotationRate)
Seconds = SecondsPerRadian * 4*Pi/(numSteps*nsSteps)

CompressedVolume = ((Pi/4.0)*Bore**2*Stroke)/(Compression-1)
Volume = CompressedVolume
AtmosphericPressure = 101325.0
AtmosphericDensity = 1.225
Pressure = AtmosphericPressure
Density = AtmosphericDensity
Temperature = 300
Number = (Pressure*Volume)/(R*Temperature)

nsCoeff = -Seconds/(2*AtmosphericDensity*nsLength/nsElements)

#print("dt, rho, dx")
#print(Seconds)
#print(AtmosphericDensity)
#print(nsLength/nsElements)

#print("coeff:")
#print(nsCoeff)

Theta = 0
DistanceTravelled = 0

outFile = open("output.txt", "w")

outFile.write("Theta, Volume, Mass, Pressure, Density, Temperature, Number\n")
Mass = Volume * Density
outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + ", " + str(Temperature) + ", " + str(Number) +"\n")

#Set up ICs
VelocityField = []
PressureField = [] #difference from atmospheric pressure
numberFlow = []
numberField = []
MeshVolume = (PortArea * nsLength/nsElements)
StepLength = nsLength/float(nsElements)

for meshPoint in range(0, nsElements):
	VelocityField.append(0)
	PressureField.append(0)
	numberField.append(AtmosphericPressure*MeshVolume/(R*Temperature))
	numberFlow.append(0)

for loop in range(0, numSteps):

	Theta += 4*Pi/numSteps
	DistanceTravelled = (1+math.sin(Theta-Pi/2.0))/2.0
	Mass = Volume * Density

	OldVolume = Volume
	Volume = CompressedVolume + DistanceTravelled * Stroke * Pi * (Bore/2.0)**2

	if Theta < Pi:
		#Induction
		Pressure = (Volume/OldVolume)**-Gamma * Pressure
		Density = AtmosphericDensity
		Temperature = Pressure * Volume/(Number * R)

		#Solve NS

		#set inner boundary conditions
		PressureField[0] = Pressure - AtmosphericPressure

		for nsStep in range(0, nsSteps):
			VelocityField[0] = VelocityField[1]
			VelocityField[nsElements-1] = 0

			velFile = open("vel.txt", "w")
			presFile = open("pressure.txt", "w")

			for meshPoint in range(0, nsElements):
				presFile.write(str(PressureField[meshPoint]) + " ")
				velFile.write(str(VelocityField[meshPoint]) + " ")
			presFile.write("\n")
			velFile.write("\n")

			#calculate velocity field
			#print("Pressure")
			#for meshPoint in range(0, nsElements):
				#print(PressureField[meshPoint])
			#print("")

			#print("Velocity")
			#for meshPoint in range(0, nsElements):
				#print(`meshPoint` + ", " + `VelocityField[meshPoint]`)
			#print("")

			#print("New Velocity")
			for i in range(0, nsElements-1):
				if(i == 0):
					dv = 0
					dP = PressureField[i+1]-(Pressure-AtmosphericPressure)
				else:
					dv = VelocityField[i+1]-VelocityField[i-1]
					dP = PressureField[i+1]-PressureField[i-1] 
					stop = False
					if(math.isnan(dP)):
						stop = True
						print("P, -1, +1")
						print(PressureField[i-1])
						print(PressureField[i+1])

					if(math.isnan(dv)):
						stop = True
						print("v, -1, +1")
						print(VelocityField[i-1])
						print(VelocityField[i+1])
					if(stop):
						sys.exit()


				vin = VelocityField[i]
				#print("dv, dP, vin")
				#print(`dv` + ", " + `dP` + ", " + `vin`)
				VelocityField[i] = nsCoeff*(vin*dv + dP) + vin
				#print(`i` + ", " + `VelocityField[i]`)

				if(math.isnan(VelocityField[i])):
					print("vel nan")
					print(vin)
					print(dv)
					print(dP)
					sys.exit()

			VelocityField[0] = VelocityField[1]

			for meshPoint in range(0, nsElements-1):
				if(meshPoint == 0):
					numberFlow[meshPoint] = VelocityField[meshPoint] * Density * PortArea * Seconds / airMolMass
				else:
					numberFlow[meshPoint] = 0.5 * (VelocityField[meshPoint-1] + VelocityField[meshPoint]) * Density * PortArea * Seconds / airMolMass
				#print("flow: " + str(numberFlow[meshPoint]))

			#calculate pressure field
			for meshPoint in range(0, nsElements-1):
				dndt = numberFlow[meshPoint] - numberFlow[meshPoint+1]
				numberField[meshPoint] += dndt
				#print("dndt " + str(dndt))
				if(meshPoint > 0 and meshPoint < nsElements):
					#print("dPdt " + str(dndt * R * Temperature/MeshVolume))
					PressureField[meshPoint] += dndt * R * Temperature/MeshVolume
				
			for meshPoint in range(0, nsElements):
				presFile.write(str(PressureField[meshPoint]) + " ")
				velFile.write(str(VelocityField[meshPoint]) + " ")

			presFile.write("\n")
			velFile.write("\n")

		presFile.close()
		velFile.close()

		Number -= numberFlow[0]
		if(math.isnan(Number)):
			print("nan")
			sys.exit()
		Pressure = Number*R*Temperature/Volume


	elif Theta < 2*Pi:
		#Compression
		Pressure = (Volume/OldVolume)**-Gamma * Pressure
		Temperature = Pressure * Volume/(Number * R)
		Density = Mass / Volume

	elif Theta < 3*Pi:
		#Combustion/Expansion
		Pressure = (Volume/OldVolume)**-Gamma * Pressure
		Temperature = Pressure * Volume/(Number * R)
		Density = Mass / Volume

	else:
		#Exhaust
		Pressure = (Volume/OldVolume)**-Gamma * Pressure
		Density = Mass / Volume
		Temperature = Pressure * Volume/(Number * R)

		#Put NS solver here

	outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + ", " + str(Temperature) + ", " + str(Number) +"\n")