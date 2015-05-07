#Overview
Given a set of parameters such as bore, stroke, port area, compression ratio, etc, this program produces a series of tables describing the engine power curves at various conditions.

#Input Format
TBD

#Output Format
TBD

#Physical description
##Induction
This stage is modelled on a combination of adiabatic expansion and bernoulli's principle. The model iterates over time with the piston moving out a small amount, creating a pressure imbalance over the intake port, which then causes a flow in from the manifold.

##Compression
This stage is modelled purely on adiabatic compression

##Combustion/Expansion
To be determined

##Exhaust
Essentially a reverse of the induction stage 