import pygame,time



class node:
	def __init__(self,name,pos,x,y,neighbours):
		self.name = name
		self.pos = pos
		self.x = x
		self.y = y
		self.neighbours = neighbours




A = node("A",1,50,200,[["B",1],["C",2]])
B = node("B",2,150,100,[["A",1],["E",3],["H",8]])
C = node("C",3,150,300,[["A",2],["F",7],["D",6]])
D = node("D",4,250,300,[["C",6],["F",4]])
E = node("E",5,250,100,[["B",3],["F",4],["G",6]])
F = node("F",6,350,100,[["E",4],["C",7],["D",4],["G",5]])
G = node("G",7,350,300,[["E",6],["F",5]])
H = node("H",8,450,200,[["B",8]])


nodes = [A,B,C,D,E,F,G,H]

def list_to_graph(nodes):
	graph = []
	for i in nodes:
		temp_list = []
		for j in nodes:
			length = "-"
			for k in i.neighbours:
				if j.name == k[0]:

					length = k[1]


			temp_list.append(length)
		graph.append(temp_list)

	return graph

def graph_to_list(matrix,old_nodes):

	new_nodes = []
	for a,i in enumerate(matrix):
		neighbours = []
		for b,j in enumerate(i):
			if j != "-":
				neighbours.append([old_nodes[b].name,j])
		new_nodes.append(node(old_nodes[a].name,old_nodes[a].pos,old_nodes[a].x,old_nodes[a].y,neighbours))

	return new_nodes



matrix = list_to_graph(nodes)


pygame.init()
win = pygame.display.set_mode((640,640))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",32)

run = True

def highest_algorithm(graph):
	highest = 0
	for i in graph:
		for j in i:
			try:
				if j > highest:
					highest = j
			except:pass

	return highest

parent = [i for i in range(len(matrix))]



def find(i):
	while parent[i] != i:
		i = parent[i]
	return i


def kruskals_algorithm(highest,matrix,nodes):
	
	fresh = [ ['-'] * 8 for _ in range(8)]
	mincost = 0 # Cost of min MST
 
	# Initialize sets of disjoint sets
	for i in range(len(matrix)):
		parent[i] = i
 
	# Include minimum weight edges one by one 
	edge_count = 0
	while edge_count < len(matrix):
		min = highest+1
		a = -1
		b = -1
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				if matrix[i][j] != '-':
					if find(i) != find(j) and matrix[i][j] < min:
						min = matrix[i][j]
						a = i
						b = j
		parent[find(a)] = find(b)
		
		fresh[a][b] = matrix[a][b]
		edge_count += 1
	
		kruskal_nodes = graph_to_list(fresh,nodes)

	for i in kruskal_nodes:
		for j in i.neighbours:
			for k in kruskal_nodes:
				if j[0] == k.name:
					pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)
					pygame.display.update()
					time.sleep(0.2)
	for i in fresh:print(i)
	time.sleep(1)

hold = False



while run:
	win.fill((255,255,255))
	mousex,mousey = pygame.mouse.get_pos()
	clock.tick(60)




	for i in nodes:
		for j in i.neighbours:
			for k in nodes:
				if j[0] == k.name:
					pygame.draw.line(win,(255,0,0),(i.x,i.y),(k.x,k.y),2)
					win.blit(font.render(str(j[1]),0,(0,0,0)),((i.x+k.x)//2,(i.y+k.y)//2))




	



	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			run = False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			kruskals_algorithm(highest_algorithm(matrix),matrix,nodes)

		if event.type == pygame.MOUSEBUTTONDOWN:
			hold = True
			selected_nodes = []
			for a,i in enumerate(nodes):
				if i.x-20<mousex<i.x+20 and i.y-20<mousey<i.y+20:
					selected_nodes.append(a)


			try:
				current_lowest = nodes[selected_nodes[0]].pos
				for i in selected_nodes:
					if nodes[i].pos <= current_lowest:
						moving_node = i
						
			except:
				hold = False



		if event.type == pygame.MOUSEBUTTONUP:
			hold = False

		if hold:
			nodes[moving_node].x = mousex
			nodes[moving_node].y = mousey
			

	
	for i in nodes:
		pygame.draw.circle(win,(0,0,0),(i.x,i.y),20)
		win.blit(font.render(i.name,0,(255,255,255)),(i.x-10,i.y-16))


	pygame.display.update()

