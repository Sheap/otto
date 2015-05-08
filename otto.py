import sys
import math

Pi = 3.141592653
R = 8.3144621
numSteps = 10000
nsElements = 10
nsSteps = 10
nsLength = 1
Bore = 0.14
Stroke = 0.14
PortArea = Pi*0.01**2
Compression = 6.7
Gamma = 7.0/5.0
Alpha = Gamma/(Gamma-1)
airMolMass = 0.02897
portLength = 0.01

RotationRate = 2000 * 0.104719755
SecondsPerRadian = 1/(RotationRate)
Seconds = SecondsPerRadian * Pi/(numSteps*nsSteps)

CompressedVolume = ((Pi/4.0)*Bore**2*Stroke)/(Compression-1)
Volume = CompressedVolume
AtmosphericPressure = 101325.0
AtmosphericDensity = 1.225
Pressure = AtmosphericPressure
Density = AtmosphericDensity
Temperature = 300
Number = (Pressure*Volume)/(R*Temperature)

Theta = 0
DistanceTravelled = 0

outFile = open("output.txt", "w")
nsFile = open("ns.txt", "w")

outFile.write("Theta, Volume, Mass, Pressure, Density, Temperature\n")
Mass = Volume * Density
outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + ", " + str(Temperature) +"\n")

#Set up ICs
Position = []
VelocityField = []
PressureField = []
DensityField = []
numberField = []
numberFlow = []
MeshVolume = (PortArea * nsElements/nsLength)

for meshPoint in range(0, nsElements):
	Position.append(meshPoint/nsLength)
	VelocityField.append(0)
	PressureField.append(AtmosphericPressure)
	DensityField.append(AtmosphericDensity)
	numberField.append(PressureField[meshPoint]*MeshVolume/(R*Temperature))
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
		Density = Mass / Volume
		Temperature = Pressure * Volume/(Number * R)

		#Solve NS

		#set inner boundary conditions
		PressureField[0] = Pressure
		DensityField[0] = Density

		for meshPoint in range(0, nsElements):
			nsFile.write(str(VelocityField[meshPoint]) + " ")
		nsFile.write("\n")

		for nsStep in range(0, nsSteps):
			#calculate velocity field
			for meshPoint in range(0, nsElements - 1):
				dvdx = (VelocityField[meshPoint + 1] - VelocityField[meshPoint])/(Position[meshPoint+1] - Position[meshPoint])
				dPdx = (PressureField[meshPoint + 1] - PressureField[meshPoint])/(Position[meshPoint+1] - Position[meshPoint])
				VelocityField[meshPoint] += dPdx/DensityField[meshPoint] - VelocityField[meshPoint]*dvdx
				numberFlow[meshPoint] = VelocityField[meshPoint] * DensityField[meshPoint]/(PortArea * airMolMass) * Seconds

			#calculate pressure field
			for meshPoint in range(1, nsElements - 1):
				numberField[meshPoint] = numberField[meshPoint] + numberFlow[meshPoint] - numberFlow[meshPoint + 1]
				PressureField[meshPoint] = numberField[meshPoint] * R * Temperature/MeshVolume
				
			for meshPoint in range(0, nsElements):
				nsFile.write(str(VelocityField[meshPoint]) + " ")

			nsFile.write("\n")
		sys.exit()



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

	outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + ", " + str(Temperature) + "\n")