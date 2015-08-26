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

###1D inviscid, compressible NS (aka 1D compressible euler equation):

d(rho)/dt + d(rho.u)/dx = 0
d(rho.u)/dt + d(rho.u^2+p)/dx = 0

These equations are (will be) solved via a Riemann solver to give density and velocity fields for the next timestep

Calculate dP/dt via ideal gas equation based on movement of gas (i.e. calculate net change of n in a cell, then recalculate P = nRt/V)

##Compression
This stage is modelled purely on adiabatic compression

##Combustion/Expansion
To be determined

##Exhaust
Essentially a reverse of the induction stage 