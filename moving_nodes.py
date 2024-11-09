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

hold = False

moving_node = False

while run:
	win.fill((0,0,0))
	clock.tick(60)




	mousex,mousey = pygame.mouse.get_pos()






	for i in nodes:
		for j in i.neighbours:
			for k in nodes:
				if j[0] == k.name:
					pygame.draw.line(win,(255,0,0),(i.x,i.y),(k.x,k.y),2)
					#idk abt the green circles
					pygame.draw.circle(win,(0,255,0),((i.x+k.x)//2+10,(i.y+k.y)//2+16),20)

					win.blit(font.render(str(j[1]),0,(255,255,255)),((i.x+k.x)//2,(i.y+k.y)//2))

	

	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			hold = True
			selected_nodes = []
			for a,i in enumerate(nodes):
				if i.x-20<mousex<i.x+20 and i.y-20<mousey<i.y+20:
					selected_nodes.append(a)


			for i in selected_nodes:
				print(nodes[i].name)
			#!!!!! idk if i even need to do this part at the end because i havent decided how the nodes will be inputting in the list. If they are inputted in order of position then the first node which satisfys the constraint will have the lowest number position but if it doesnt work like that thne this system will be needed so that it can find the top node
			try:
				current_lowest = nodes[selected_nodes[0]].pos
				for i in selected_nodes:
					if nodes[i].pos <= current_lowest:
						moving_node = i
				print(nodes[moving_node].name)
			except:
				print("Error")
				hold = False



		if event.type == pygame.MOUSEBUTTONUP:
			hold = False

	if hold:
		nodes[moving_node].x = mousex
		nodes[moving_node].y = mousey




	for i in nodes:
		pygame.draw.circle(win,(255,255,255),(i.x,i.y),20)
		win.blit(font.render(i.name,0,(0,0,0)),(i.x-10,i.y-16))


	pygame.display.update()

