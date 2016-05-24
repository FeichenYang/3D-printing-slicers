# First, I want to thank my parents.
# This program only gives you woodpile structures for a Prusa-i3 printer. But in any size.
# Change parameters here.
total_layer_number = 5
x_line_number = 10
y_line_number = 10
# please enter an even number, please. I ain't want any trouble.
initial_position = [70 , 79]
strand_interval = 1
# mm
extrusion_ratio = 0.008
# 0.007074 is default; bigger = more extrusion.
x_displacement = ( x_line_number - 2 ) * extrusion_ratio * strand_interval
y_displacement = ( y_line_number - 2 ) * extrusion_ratio * strand_interval
skirt_length = 300
# mm
layer_height = 0.4
print_speed = 200
# mm/min but somehow faster than expected
E = 0
E_skirt = skirt_length * extrusion_ratio
position = [0,0]
position[0] = initial_position[0]
position[1] = initial_position[1]
z = 0.400
# mm, first layer height 
# nozzle diameter: 500 microns. Syringe: 5mL standard syringe.
# this E is based on some default setting of skirt length in Cura

def x_layer():
	global E,position
	position[0] = initial_position[0]
	position[1] = initial_position[1]
	for i in range(x_line_number/2):
		print "G1 X",position[0]," Y", position[1]," E", E
		position[0] += x_line_number * strand_interval
		E += x_displacement
		print "G1 X",position[0]," Y", position[1]," E", E
		position[1] += strand_interval
		E += extrusion_ratio * strand_interval 
		print "G1 X",position[0]," Y", position[1]," E", E
		position[0] -= x_line_number
		E += x_displacement
		print "G1 X",position[0]," Y", position[1]," E", E
		if i == x_line_number/2 - 1 :
			pass
		else:
			position[1] += strand_interval
			E += extrusion_ratio * strand_interval
		i += 1
	return 0
# Prints gcode that makes the printer goes in a seris of S shapes like this: SSSSSSSSS

def y_layer():
	global E,position
	position[0] = initial_position[0]
	position[1] = initial_position[1]
	for i in range(x_line_number/2):
		print "G1 X",position[0]," Y", position[1]," E", E
		position[1] += y_line_number * strand_interval
		E += y_displacement
		print "G1 X",position[0]," Y", position[1]," E", E
		position[0] += strand_interval
		E += extrusion_ratio * strand_interval 
		print "G1 X",position[0]," Y", position[1]," E", E
		position[1] -= x_line_number
		E += y_displacement
		print "G1 X",position[0]," Y", position[1]," E", E
		if i == y_line_number/2 -1 :
			pass
		else:
			position[0] += strand_interval
			E += extrusion_ratio * strand_interval
		i += 1
	return 0
# Is this comment really neccesary?

def purge():
	global E,position
	print "G0 F9000 X64 Y64 Z", z
	print "G0 F900"
	purge_strand_number = skirt_length/20	
	position[0] = 64
	position[1] = 64
	for i in range(purge_strand_number):
		position[1] -= 20 
		E += extrusion_ratio * 20
		print "G1 X",position[0]," Y", position[1]," E", E
		position[1] += 20
		position[0] += 1
		print "G1 X",position[0]," Y", position[1]," E", E
		i += 1
	return 0

# This is the snake-shape skirt
print "M109 S200.0 \nG28 \nG21 \nG90 \nG92 E0 \nM107"
print ";SKIRT"
purge()
j = 0
for j in range(total_layer_number):
	print ";LAYER:", j+1
	E -= 1
# retraction
	print "G1 F2500 E",E
	print "G1 F", print_speed, "X", initial_position[0], " Y", initial_position[1]," Z",z
	E += 1
# Take this, retraction！
	if j %2 == 0:
		x_layer()
	else :
		y_layer()
	j += 1
	z += layer_height
	
print "M106 S255 \nM107 \nG0 F9000 X70.252 Y71.691 Z9.001 \nM104 S0 \nM140 S0 \nM84 \nG90"
