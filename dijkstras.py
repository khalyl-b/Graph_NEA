import pygame, time


class node:
	def __init__(self, name, pos, x, y, neighbours):
		self.name = name
		self.pos = pos
		self.x = x
		self.y = y
		self.neighbours = neighbours


A = node("A", 1, 50, 200, [["B", 1], ["C", 2]])
B = node("B", 2, 150, 100, [["A", 1], ["E", 3], ["H", 8]])
C = node("C", 3, 150, 300, [["A", 2], ["F", 7], ["D", 6]])
D = node("D", 4, 250, 300, [["C", 6], ["F", 4]])
E = node("E", 5, 250, 100, [["B", 3], ["F", 4], ["G", 6]])
F = node("F", 6, 350, 100, [["E", 4], ["C", 7], ["D", 4], ["G", 5]])
G = node("G", 7, 350, 400, [["E", 6], ["F", 5]])
H = node("H", 8, 450, 200, [["B", 8]])

nodes = [A, B, C, D, E, F, G, H]


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


def graph_to_list(matrix, old_nodes):
	new_nodes = []
	for a, i in enumerate(matrix):
		neighbours = []
		for b, j in enumerate(i):
			if j != "-":
				neighbours.append([old_nodes[b].name, j])
		new_nodes.append(node(old_nodes[a].name, old_nodes[a].pos, old_nodes[a].x,old_nodes[a].y, neighbours))
	return new_nodes


matrix = list_to_graph(nodes)

pygame.init()
win = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
font2 = pygame.font.SysFont("Arial", 12)

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

def min_distance(dist, visited):
	min_dist = float('inf')
	min_index = -1
	for v in range(len(dist)):
		if dist[v] < min_dist and not visited[v]:
			min_dist = dist[v]
			min_index = v
	return min_index

def reconstruct_path(parents, start, end):
	path = []
	current = end
	while current != start:
		path.append(current)
		current = parents[current]
	path.append(start)
	return list(reversed(path))

def dijkstra(matrix, start, end):
	num_vertices = len(matrix)
	dist = [float('inf')] * num_vertices
	dist[start] = 0
	visited = [False] * num_vertices
	parents = [-1] * num_vertices

	for _ in range(num_vertices):
		min_dist = float('inf')
		min_index = -1
		for v in range(len(dist)):
			if dist[v] < min_dist and not visited[v]:
					min_dist = dist[v]
					min_index = v

		u = min_index
		visited[u] = True
		for v in range(num_vertices):
			try:
				if (
					not visited[v]
					and matrix[u][v] != 0
					and dist[u] != float('inf')
					and dist[u] + matrix[u][v] < dist[v]
				):
					dist[v] = dist[u] + matrix[u][v]
					parents[v] = u
			except:pass
	path = []
	current = end
	while current != start:
		path.append(current)
		current = parents[current]
	path.append(start)

	shortest_path = list(reversed(path))
	return dist[end], shortest_path
path = []
hold = False

on = False

while run:
	win.fill((255,255,255))
	clock.tick(60)
	mousex,mousey = pygame.mouse.get_pos()
	for i in nodes:
		for j in i.neighbours:
			for k in nodes:
				if j[0] == k.name:
					pygame.draw.line(win, (255, 0, 0), (i.x, i.y), (k.x, k.y),2)
					pygame.draw.circle(win,(0,255,0),((i.x+k.x)//2+4,(i.y+k.y)//2+8),8)
					win.blit(font2.render(str(j[1]),0,(0,0,0)),((i.x+k.x)//2,(i.y+k.y)//2))
	if on:
		for i in range(0,len(path)):
			try:
				pygame.draw.line(win, (0, 0, 255), (nodes[path[i]].x, nodes[path[i]].y), (nodes[path[i+1]].x, nodes[path[i+1]].y),2)

			except:pass


	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			run = False

		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

			if on:
				on = False
				distance, path = 0,[]
			else:
				on = True
				distance, path = dijkstra(matrix,7,3)
			time.sleep(0.1)

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
		pygame.draw.circle(win, (0, 0, 0), (i.x, i.y), 20)
		win.blit(font.render(i.name, 0, (255, 255, 255)), (i.x - 10, i.y - 16))

	pygame.display.update()
