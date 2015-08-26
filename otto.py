import sys
import math

Pi = 3.141592653
R = 8.3144621
dt = 0.00000000001
nsElements = 5
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
timeToRotate = 2*Pi * RotationRate

CompressedVolume = ((Pi/4.0)*Bore**2*Stroke)/(Compression-1)
Volume = CompressedVolume
AtmosphericPressure = 101325.0
AtmosphericDensity = 1.225
Pressure = AtmosphericPressure
Density = AtmosphericDensity
Temperature = 300
Number = (Pressure*Volume)/(R*Temperature)

nsCoeff = dt/(2*nsLength/nsElements)

Theta = 0
DistanceTravelled = 0

outFile = open("output.txt", "w")

outFile.write("Theta, Volume, Mass, Pressure, Density, Temperature, Number\n")

Mass = Volume * Density
outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + ", " + str(Temperature) + ", " + str(Number) +"\n")

#Set up ICs
VelocityField = []
PressureField = []
DensityField = []
numberFlow = []
numberField = []
MeshVolume = (PortArea * nsLength/nsElements)
StepLength = nsLength/float(nsElements)

for meshPoint in range(0, nsElements):
	VelocityField.append(0)
	PressureField.append(0)
	DensityField.append(Density)
	numberField.append(AtmosphericPressure*MeshVolume/(R*Temperature))
	numberFlow.append(0)

timeElapsed = 0
i = 0
velFile = open("vel.txt", "w")
presFile = open("pressure.txt", "w")
while timeElapsed < timeToRotate:
	i += 1
	timeElapsed += dt
	Theta += dt*RotationRate
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

		VelocityField[0] = VelocityField[1]
		VelocityField[nsElements-1] = 0

		NewVelField = []
		NewDensField = []

		#inner boundary condition
		jin = DensityField[0]*VelocityField[0]
		jinm1 = 0
		jinp1 = DensityField[1]*VelocityField[1]
		rhoin = DensityField[0]
		Pinm1 = Pressure - AtmosphericPressure
		uinm1 = 0
		Pinp1 = PressureField[1]
		uinp1 = VelocityField[1]

		rhoip1n = nsCoeff*(jinm1-jinp1) + rhoin
		jip1n = nsCoeff*((jinm1*uinm1+Pinm1) - (jinp1*uinp1+Pinp1)) + jin

		# print("------------------------------")
		# print("rho")
		# print(rhoin)
		# print("drho")
		# print(nsCoeff * (jinm1-jinp1))
		# print("j")
		# print(jin)
		# print("dj")
		# print(nsCoeff*((jinm1*uinm1+Pinm1) - (jinp1*uinp1+Pinp1)))
		# print("based on")
		# print(nsCoeff, jinm1, uinm1, Pinm1, jinp1, uinp1, Pinp1)

		NewDensField.append(rhoip1n)
		NewVelField.append(jip1n/rhoip1n)

		#internal points
		for n in range(1, nsElements-1):
			jin = DensityField[n]*VelocityField[n]
			jinm1 = DensityField[n-1]*VelocityField[n-1]
			jinp1 = DensityField[n+1]*VelocityField[n+1]
			rhoin = DensityField[n]
			Pinm1 = PressureField[n-1]
			uinm1 = VelocityField[n-1]
			Pinp1 = PressureField[n+1]
			uinp1 = VelocityField[n+1]

			rhoip1n = nsCoeff*(jinm1-jinp1) + rhoin
			jip1n = nsCoeff*((jinm1*uinm1+Pinm1) - (jinp1*uinp1+Pinp1)) + jin

			# print("------------------------------")
			# print("rho")
			# print(rhoin)
			# print("drho")
			# print(nsCoeff * (jinm1-jinp1))
			# print("j")
			# print(jin)
			# print("dj")
			# print(nsCoeff*((jinm1*uinm1+Pinm1) - (jinp1*uinp1+Pinp1)))
			# print("based on")
			# print(nsCoeff, jinm1, uinm1, Pinm1, jinp1, uinp1, Pinp1)

			NewDensField.append(rhoip1n)
			NewVelField.append(jip1n/rhoip1n)

		#outer boundary condition
		NewVelField.append(0)
		NewDensField.append(AtmosphericDensity)

		#update velocity and density via euler equations
		VelocityField = NewVelField
		DensityField = NewDensField

		#update pressure and number fields
		#inner boundary (into cylinder)
		Number += Density*VelocityField[0]*PortArea/airMolMass
		Pressure = Number*R*Temperature/Volume
		for n in range(0, nsElements):
			numberFlow[n] = DensityField[n]*VelocityField[n]*PortArea/airMolMass

		# print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
		# for n in range(0, nsElements):
		# 	print(numberFlow[n])
			
		for n in range(0, nsElements-1):
			numberField[n] += (numberFlow[n]-numberFlow[n+1])
			PressureField[n] = numberField[n]*R*300/MeshVolume - AtmosphericPressure
			
		for meshPoint in range(0, nsElements):
			presFile.write(str(PressureField[meshPoint]) + " ")
			velFile.write(str(VelocityField[meshPoint]) + " ")
		presFile.write("\n")
		velFile.write("\n")

		# print("===================================")
		# for n in range(0, nsElements):
		# 	print(VelocityField[n], DensityField[n], PressureField[n], numberField[n])

		# try:
		# 	input("press enter")
		# except SyntaxError:
		# 	pass

		for n in range(0, nsElements-1):
			if numberField[n] < 0:
				print("cell has lost more than it had, restart with smaller timestep")
				print(i, n)
				outFile.close()
				presFile.close()
				velFile.close()
				sys.exit()

	elif Theta < 2*Pi:
		presFile.close()
		velFile.close()
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