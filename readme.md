#Disclaimer
This project is under development, and is far from working. What's written in this readme is a combination of what is, and what is planned to be, with no clear distinction given.

#Overview
Given a set of parameters such as bore, stroke, port area, compression ratio, etc, this program produces a series of tables describing the engine power curves at various conditions.

#Input Format
TBD

#Output Format
TBD

#Physical description
##Induction
This stage is modelled on a combination of adiabatic expansion and a 1D compressible Navier-Stokes solver. The model iterates over time with the piston moving out a small amount, creating a pressure imbalance over the intake port (adiabatic expansion), which then causes a flow in from the manifold (solved via NS). Viscous effects are ignored, and an ideal gas EoS is used.

##Compression
This stage is modelled purely on adiabatic compression

##Combustion/Expansion
To be determined

##Exhaust
Essentially a reverse of the induction stage 