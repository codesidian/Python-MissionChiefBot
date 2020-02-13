import random
vehicles = {
# .co.uk
"fire engines": {
"Water Ladder",
"Light 4X4 Pump (L4P)",
"Rescue Pump"
},
"aerial appliance trucks": {
"Aerial Appliance"
},
"breathing apparatus support units": {
"BASU"
},

"incident command and control units": {
"ICCU"
},
# mix of uk and com vehicles
"police cars": {
# .co.uk
"Incident response vehicle (IRV)",
"Dog Support Unit (DSU)",
"Armed Response Vehicle (ARV)",
"Police helicopter", 
# .com
"Patrol car",
"SWAT Armoured Vehicle",
"K-9 Unit",
"Police Motorcycle",
"SWAT SUV"
},

"ambulance": {
"Ambulance"
},

"fire officers": {
    "Fire Officer"
},

"Misc" : {
"Aerial Appliance",
"Fire Officer",
"Rescue Support Unit (RSU)",
"Rescue Pump",
"Water Carrier",
"HazMat Unit",
"Breathing Apparatus Support Units (BASU)",
"Incident Command and Control Unit (ICCU)"
},
# .com
"firetrucks": {
"Type 1 fire engine",
"Type 2 fire engine",
"Quint",
"Rescue Engine"
},
"пожарные машины": {
"АЦ-3,0-40",
"АЦ 2,3-40",
"ПСА"
}

}

def randomint():
 return random.randint(1, 30)



