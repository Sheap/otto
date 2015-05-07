import math

Pi = 3.141592653
R = 8.3144621
numSteps = 10000
Bore = 0.14
Stroke = 0.14
PortArea = Pi*0.01**2
Compression = 6.7
Gamma = 7.0/5.0
Alpha = Gamma/(Gamma-1)
airMolMass = 0.02897

RotationRate = 2000 * 0.104719755
SecondsPerRadian = 1/(RotationRate)
Seconds = SecondsPerRadian * Pi/numSteps
print("Seconds")
print(Seconds)

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

outFile.write("Theta, Volume, Mass, Pressure, Density\n")
Mass = Volume * Density
outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + "\n")

for loop in range(0, numSteps):

	#Induction
	Theta += Pi/numSteps
	DistanceTravelled = (1+math.sin(Theta-Pi/2.0))/2.0

	Mass = Volume * Density

	OldVolume = Volume
	Volume = CompressedVolume + DistanceTravelled * Stroke * Pi * (Bore/2.0)**2
	Pressure = (Volume/OldVolume)**-Gamma * Pressure
	Density = Mass / Volume
	Temperature = Pressure * Volume/(Number * R)

	if(2*Alpha*(AtmosphericPressure/AtmosphericDensity-Pressure/Density) > 0):
		FlowVelocity = math.sqrt(2*Alpha*(AtmosphericPressure/AtmosphericDensity-Pressure/Density))
	else:
		FlowVelocity = 0

	MassRate = FlowVelocity * PortArea * Density
	dNum = MassRate / airMolMass

	Mass = Mass + MassRate * Seconds
	Number = Number + dNum * Seconds

	Density = Mass / Volume

	Pressure = Number*R*Temperature/Volume

	#Compression

	#Combustion/Expansion

	#Exhaust

	outFile.write(str(Theta) + ", " + str(Volume) + ", " + str(Mass) + ", " + str(Pressure) + ", " + str(Density) + "\n")