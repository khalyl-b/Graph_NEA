#Imports
import pygame,time

#Class
class node:
	#Constructor
	def __init__(self,name,pos,x,y,neighbours):
		self.name = name
		self.pos = pos
		self.x = x
		self.y = y
		self.neighbours = neighbours



#Predefining the nodes
A = node("A",1,50,200,[["B",1],["C",2]])
B = node("B",2,150,100,[["A",1],["E",3],["H",8]])
C = node("C",3,150,300,[["A",2],["F",7],["D",6]])
D = node("D",4,250,300,[["C",6],["F",4]])
E = node("E",5,250,100,[["B",3],["F",4],["G",6]])
F = node("F",6,350,100,[["E",4],["C",7],["D",4],["G",5]])
G = node("G",7,350,300,[["E",6],["F",5]])
H = node("H",8,450,200,[["B",8]])

#Make them into a list
nodes = [A,B,C,D,E,F,G,H]

#This function finds the highest value in the matrix
def highest_algorithm(matrix):
	#The default highest value will always be 0
	highest = 0
	#It will then cycle through each value in the matrix that was passed and check if the value of the edge is higher than the highest
	for i in matrix:
		for j in i:
			#The need for the try function is that a lack of an edge between 2 nodes is represented as a '-' which is a string
			#This means u cannot do mathematical operations to it and therefore if it is encountered it will just be ignored
			try:
				if j > highest:
					#If a new highest is found then it will set that value as the new highest
					highest = j
			except:pass

	#just returns the value
	return highest

#This function gets matrix and a list of nodes and sets the edges in the matrix to the edges in the list
def graph_to_list(matrix,old_nodes):
	#Sets a new empty list to blank
	new_nodes = []
	#Cycles through all the columns and indecies in the given matrix
	for a,i in enumerate(matrix):
		#Makes a new empty list of the neighbours, these are the neighbours of the nodes
		neighbours = []
		#Cycles through all the rows and indecies in the given matrix
		for b,j in enumerate(i):
			#Makes sure that there is actually a connection between the 2 nodes
			if j != "-":
				#Adds to the list of neighbours another list containing the name of the node and its weight
				neighbours.append([old_nodes[b].name,j])
		#Adds the nodes to the new nodes and give it the neighbours
		new_nodes.append(node(old_nodes[a].name,old_nodes[a].pos,old_nodes[a].x,old_nodes[a].y,neighbours))

	return new_nodes

#Does the opposite of the previous one where it outputs a matrix when given a list
def list_to_graph(nodes):
	#Initiates the matrix
	graph = []
	#Cycles through all the columns in the list
	for i in nodes:
		#Creates a temporary column
		temp_list = []
		#Cycles through all the rows in the list
		for j in nodes:
			#Initally sets no connected between the 2 nodes
			weight_of_graph = "-"
			#Cycles through the neighbours of that node
			for k in i.neighbours:
				#If it finds that if they are neighbours it changes the weight to its weight
				if j.name == k[0]:

					weight_of_graph = k[1]

			#Appends the weight of the edge to the column whether its '-' or an actual connection
			temp_list.append(weight_of_graph)
		#Finally after the column has had all its values inputted it adds it to the matrix
		graph.append(temp_list)

	return graph

#Creates the matrix
matrix = list_to_graph(nodes)

#Initiates the pygame window
pygame.init()
#Designs the windows dimensions
win = pygame.display.set_mode((640,640))
#Sets the clock (for the fps)
clock = pygame.time.Clock()
#Sets the font for writing text on the screen
font = pygame.font.SysFont("Arial",32)
#This controls the gameloop
run = True



def prims_algorithm(highest,matrix,starting_node,nodes):


	length = len(matrix)

	fresh = []
	selected_node = []
	for i in range(0,length):
		temp_list = []
		for j in range(0,length):
			temp_list.append("-")

		fresh.append(temp_list)
		selected_node.append(False)

	no_edge = 0

	selected_node[starting_node.pos-1] = True

	while (no_edge < length - 1):


		minimum = highest+1
		a = 0
		b = 0
		for i in range(length):
			if selected_node[i]:
				for j in range(length):
					if ((not selected_node[j]) and matrix[i][j]):  
						try:
							if minimum > matrix[i][j]:
								minimum = matrix[i][j]
								a = i
								b = j
						except:pass
		fresh[a][b] = matrix[a][b]
		selected_node[b] = True
		no_edge += 1


		MST_list = graph_to_list(fresh,nodes)
		for i in MST_list:
			for j in i.neighbours:
				for k in MST_list:
					if j[0] == k.name:
						pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)
						pygame.display.update()

		time.sleep(1)

	for i in fresh:print(i)
	return fresh



display_MST = False
hold = False
#gameloop
while run:
	#resets the screen to white every time
	win.fill((255,255,255))
	#Sets the apps fps to 60 so it cycles 60 times every second at a maximum
	clock.tick(60)
	#retrieves the mouses coordinates every loop
	mousex,mousey = pygame.mouse.get_pos()

	#Cycles nodes to draw them on the screen
	for i in nodes:
		for j in i.neighbours:
			for k in nodes:
				if j[0] == k.name:
					pygame.draw.line(win,(255,0,0),(i.x,i.y),(k.x,k.y),2)
					win.blit(font.render(str(j[1]),0,(0,0,0)),((i.x+k.x)//2,(i.y+k.y)//2))
	#Checks every event happeneing on the screen
	for event in pygame.event.get():
		#If the user clicks the X then it closes the window
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			run = False
		#If the usr clicks the spacebar then it will run prims algorithm
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			highest_number = highest_algorithm(matrix)
			MST_matrix = prims_algorithm(highest_number,matrix,A,nodes)
			MST_list = graph_to_list(MST_matrix,nodes)
			#This allows the user to toggle whether they want to see the MST or not
			if display_MST:
				display_MST = False
			else:
				display_MST = True
		#If the user holds down the moursebutton then they will be able to drag the nodes around
		if event.type == pygame.MOUSEBUTTONDOWN:
			hold = True
			selected_nodes = []
			#Checks each node that it is hovering over and adds them to a list
			for a,i in enumerate(nodes):
				if i.x-20<mousex<i.x+20 and i.y-20<mousey<i.y+20:
					selected_nodes.append(a)

			# Finds the node with the lowest pos and sets that to the node that is being moved
			try:
				current_lowest = nodes[selected_nodes[0]].pos
				for i in selected_nodes:
					if nodes[i].pos <= current_lowest:
						moving_node = i			
			except:
				hold = False
		#If the user lets go of their mouse then the program will acknowledge they are no longer holding
		if event.type == pygame.MOUSEBUTTONUP:
			hold = False
		#If the user is holding down the button then the node selected will have its x and y coordinates changed to that of the users mouse
		if hold:
			nodes[moving_node].x = mousex
			nodes[moving_node].y = mousey
	#Checks to see whether the user has toggled on or toggled off the MST and acts accordingly
	if display_MST:
		for i in MST_list:
			for j in i.neighbours:
				for k in MST_list:
					if j[0] == k.name:
						pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)
	#Draws the nodes onto the screen
	for i in nodes:
		pygame.draw.circle(win,(0,0,0),(i.x,i.y),20)
		win.blit(font.render(i.name,0,(255,255,255)),(i.x-10,i.y-16))
	#Updates any changes made to the screen
	pygame.display.update()

