#Python library imports
import pygame,math,sqlite3,time,pickle
from tkinter import filedialog


#Connection to the database
conn = sqlite3.connect('Resources/SaveData/SaveData.db')
#Creates a cursor for selecting items in a database
curs = conn.cursor()
#Will attempt to create a database if there isnt one already, otherwise nothing will happen
try:
	curs.execute("""CREATE TABLE Account_info (
			Username text,
			Password text
			)""")


	curs.execute("""CREATE TABLE Folder_info (
			Folder_id int,
			Name text,
			Account_id int
			)""")

	curs.execute("""CREATE TABLE Graph_info (
			Name text,
			Weighted bool,
			Directed bool,
			Graph text,
			List text,
			Account_id int,
			Folder_id int,
			Graph_id int
			)""")

except:pass

#Save the changes
conn.commit()
#Closes the connection
conn.close()

#This variable decides the theme of the app
theme = 0

#These are the possible themes that the user can select when on the app
colour1 = [(255,222,192),(49,51,56)]
colour2 = [(226,179,136),(32,38,43)]
colour3 = [(207,188,184),(85,98,102)]
colour4 = [(200,159,116),(43,45,49)]
colour5 = [(225,192,162),(35,36,40)]




#This class is for the nodes which allows them to be created
class node:
	#This is the constructor
	def __init__(self,name,pos,x,y,neighbours):
		#Name of the node
		self.name = name
		#Position of the node (row and column)
		self.pos = pos
		#x coord
		self.x = x
		#y coord
		self.y = y
		#Neighbours of the node
		self.neighbours = neighbours
	#These methods are used for encapsulation and they allow the program to only be able to access the attributes through methods
	def get(self,var):
		if var == "name":
			return self.name
		if var == "pos":
			return self.pos
		if var == "x":
			return self.x
		if var == "y":
			return self.y
		if var == "neighbours":
			return self.neighbours

	def set(self,var,val):
		if var == "name":
			self.name = val
		if var == "pos":
			self.pos = val
		if var == "x":
			self.x = val
		if var == "y":
			self.y = val
		if var == "neighbours":
			self.neighbours = val
	#This updates the coordinates of any nodes
	def update_coords(self,nodes):
		for i in nodes:
			if i.name == self.name:
				self.x = i.x
				self.y = i.y

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


#Prims algorithm
def prims_algorithm(highest,matrix,starting_node,nodes):
	#sets the number of nodes to the length of the matrix
	length = len(matrix)
	#creates a 'fresh' matrix
	fresh = []
	#No current nodes are selected
	selected_nodes = []

	starter = 0
	for a,i in enumerate(nodes):
		if i.name == starting_node.name:
			starter = a

	order = [starter]

	#This for loop just makes the fresh matrix have the value '-' for all the edges
	for i in range(0,length):
		temp_list = []
		for j in range(0,length):
			temp_list.append("-")
		fresh.append(temp_list)
		#This part means that all current nodes will be unselected at the start
		selected_nodes.append(False)

	#This variable is responsible for keeping track of which edge its currently on
	edge_count = 0
	#This adds the inital node to the selected nodes
	selected_nodes[starter] = True

	#Makes sure every node is cycled through
	while (edge_count < length - 1):

		#Sets the inital minimum weigh of the edge to 1 more than the highest
		minimum = highest+1
		#Index 1
		a = 0
		#Index 2
		b = 0
		#Cycles through all indecies of the matrix
		for i in range(length):
			#checks to see if the current node being targetted is one of the selected nodes
			if selected_nodes[i]:
				#Iterates though all the nodes again
				for j in range(length):
					#Makes sure that the node being examined is not the selected node or a node already examined
					if ((not selected_nodes[j]) and matrix[i][j]):  
						#Uses try once again because you cant use < and > when dealing with strings
						try:
							#Checks to see if the edge weight is the lowest possible
							if minimum > matrix[i][j]:
								#Sets the new lowest
								minimum = matrix[i][j]
								a = i
								b = j
						except:pass
		#Adds the weight of that edge to the fresh matrix
		fresh[a][b] = matrix[a][b]
		order.append(b)
		#adds the new node to the seleted nodes
		selected_nodes[b] = True
		#Increases the edge count so it can iterate over the next node
		edge_count += 1
	#makes a list out of the matrix when finished
	MST_list = graph_to_list(fresh,nodes)
	ordered_nodes = []
	for i in order:
		ordered_nodes.append(MST_list[i])
	return ordered_nodes


#This small functions finds parent of the node
def find(i,parent):
	while parent[i] != i:
		i = parent[i]
	return i


def kruskals_algorithm(highest,matrix,nodes):
	#Creates an array with the numbers 1 to the number of nodes
	parent = []
	for i in range(0,len(matrix)):
		parent.append(i)

	#Once again creates a fresh matrix
	fresh = []
	for i in range(0,len(matrix)):
		temp = []
		for j in range(0,len(matrix)):
			temp.append("-")
		fresh.append(temp)
 
	#Sets each varible to what its parent is
	for i in range(len(matrix)):
		parent[i] = i
 
	#The edge count once again
	edge_count = 0
	#Loops untill all edges have been analysed
	while edge_count < len(matrix):
		#minimum value is set to 1 higher than the highest
		minimum = highest+1
		#Index 1
		a = -1
		#Index 2
		b = -1
		#Cycles through the indecies of the nodes
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				#Makes sure that there is a connection
				if matrix[i][j] != '-':
					#Finds the parents of both nodes and if they are not the same and the edge weight is smaller than the minimum
					if find(i,parent) != find(j,parent) and matrix[i][j] < minimum:
						#Sets the minimum value to the current matrix position being examiend
						minimum = matrix[i][j]
						a = i
						b = j
		#Finds the parent of the 2nd node and sets the to that parent of the parent of the 1st
		parent[find(a,parent)] = find(b,parent)
		#Adds the edge to the new 'fresh' matrix
		fresh[a][b] = matrix[a][b]
		#increase count
		edge_count += 1
	#turns the matrix into a list
	for a,i in enumerate(fresh):
		for b,j in enumerate(fresh):
			if fresh[a][b] != '-':
				fresh[b][a] = fresh[a][b]
			if fresh[b][a] != '-':
				fresh[a][b] = fresh[b][a]
	kruskal_nodes = graph_to_list(fresh,nodes)
	kruskal_nodes = sorted(kruskal_nodes, key=lambda x: x.neighbours[0][1])
	return kruskal_nodes

def dijkstras_algorithm(matrix, start, end):
	#Sets the distance to each node as infinity at the start
	dist = []
	for i in range(0,len(matrix)):
		dist.append(float('inf'))
	#sets the start node distance to 0
	dist[start] = 0
	#Sets the vitied nodes all to False
	visited = []
	for i in range(0,len(matrix)):
		visited.append(False)
	#Sets the parents of all the nodes to negative meaning they have none
	parents = []
	for i in range(0,len(matrix)):
		parents.append(-1)

	#Cycles through all the nodes
	for i in range(len(matrix)):
		#sets the minimum disance and the minimum index
		min_dist = float('inf')
		min_index = -1
		#Checks each node and finds the minimum distance and smallest index it can be
		for j in range(len(dist)):
			if dist[j] < min_dist and not visited[j]:
				min_dist = dist[i]
				min_index = j

		#Shows the node has been vitited
		visited[min_index] = True
		for j in range(len(matrix)):
			try:
				#Checks to see if the node is not visitived and that the length of the node works
				#And that that distance to the node is not infinity and that it is the shortest distance possible
				if (not visited[j] and matrix[min_index][j] != 0 and dist[min_index] != float('inf') and dist[min_index] + matrix[min_index][j] < dist[j]):
					#Adds the node to the shortest distance
					dist[j] = dist[min_index] + matrix[min_index][j]
					parents[j] = min_index
			except:pass
	#Creates an empty array for the path
	path = []
	#sets the current node to the end and backtracks
	current = end
	while current != start:
		#Back trach
		path.append(current)
		current = parents[current]
	path.append(start)
	
	shortest_path = list(reversed(path))
	return shortest_path


#Initialisation of pygame
pygame.init()
#Sets the window display size
win = pygame.display.set_mode((1280,720))
#Sets the clock which is the amount of cycles the gameloop will run per second
clock = pygame.time.Clock()
#The variable which controls the gameloop
run = True
#The standard font that will be used
font = pygame.font.SysFont("Cascadia Code",32)
#A smaller font
small_font = pygame.font.SysFont("Cascadia Code",12)
#Password font
pass_font = pygame.font.Font("Resources/Media/Pass_font.ttf",32)

#images
header = pygame.image.load("Resources/Media/header.png")
subheader = pygame.image.load("Resources/Media/subheader.png")

settings_icon = pygame.image.load("Resources/Media/settings.png")
back_icon = pygame.image.load("Resources/Media/Back.png")
export_icon = pygame.image.load("Resources/Media/share.png")
delete_icon = pygame.image.load("Resources/Media/bin.png")
paste_icon = [pygame.image.load("Resources/Media/clipboard_off.png"),pygame.image.load("Resources/Media/clipboard_on.png")]


#This variable will control what the user is currently seeing
page = "login"
#Check key press variable
keys=pygame.key.get_pressed()

#Username of the user
global username
username = False
#Password of the user
global password
password = False
#The current string is whatever the user types into the keyboard
global current_string
current_string = ""
#string of the username
user_string = ""
#string of the password
pass_string = ""

#The current account that the user is on
global current_account_id
current_account_id = 0

#The current folder the user is in
current_folder = 0

#Checks to see if the text box for inputting a new folder is true
text_box_folder = False
#Checks to see if the text box for inputting a new graph is true
text_box_graph = False




#Function for typing into the program
def type(key,page):
	global current_string,username,password
	#if the key is backspace then it removes the last character from the string
	if key.key == pygame.K_BACKSPACE:
		current_string = current_string[:-1]
	#If the key is tab it moves it from username -> password -> free in that order
	elif key.key == pygame.K_TAB:
		if page == "login" or page == "signup":
			if username:
				username = False
				password = True
				current_string = pass_string
			elif password:
				username = False
				password = False
			elif not username and not password:
				username = True
				password = False
				current_string = user_string
	#Otherwise it adds it to the curent string
	else:
		current_string += event.unicode

#Hashing algorithm for storing passwords
def hashs(plaintext):

	hashed = plaintext

	return hashed

#If the user chooses to log in
def login(user,passs):
	global current_account_id
	current_account_id = 0
	found = False
	#Connection to the database
	conn = sqlite3.connect('Resources/SaveData/SaveData.db')
	#Creates a cursor for selecting items in a database
	curs = conn.cursor()
	#Fetches all the accounts
	curs.execute("SELECT * FROM Account_info")
	#Checks to see if the username and password are correct
	for a,i in enumerate(curs.fetchall()):
		if user == i[0] and hashs(passs) == i[1]:
			found = True
			current_account_id = a+1

	#Save the changes
	conn.commit()
	#Closes the connection
	conn.close()
	#reutnrs whehters its ture or not
	return found

#Signup function
def signup(user,passs):
	global current_account_id
	#No current dupes found
	dupe = False


	conn = sqlite3.connect('Resources/SaveData/SaveData.db')
	curs = conn.cursor()

	curs.execute("SELECT * FROM Account_info")
	#Gets all the accounts from the database
	data = (curs.fetchall())

	#Checks to see if there is a dupe
	for i in data:
		if user == i[0]:
			dupe = True

	#If there is not a dupe username then it will input a new username and password into the table
	if not dupe:
		curs.execute("INSERT INTO Account_info VALUES (:Username,:Password)",
			{

			'Username': user,
			'Password': hashs(passs)

			})
		curs.execute("INSERT INTO Folder_info VALUES (:Folder_id,:Name,:Account_id)",
		{
		'Folder_id':0,
		'Name':"Root",
		'Account_id':len(data)+1

		})
		current_account_id = len(data)+1


	conn.commit()
	conn.close()
	#returns whether it found a dupe or not
	return dupe

#current folder and largest folder that the usre is on
current_folder_id = 0
largest_folder_id = 0
#current id of the graph
current_graph_id = 0
#Inittaly sets the graph to not weighted
weighted = False
##Sets the right click menu to false
right_click_menu = False
#Sets the adding new nodes enu to false
add_menu = False
#The user is not holding the mouse down atm
hold = False

#The first node is currently being selected and the second isnt
first_node = True
second_node = False
#The menu for adding the weight of the edge is False
node_menu = False
#Currently there are no nodes in the graph selected and there is not matrix either
nodes = []
matrix = []
#All the algorithms are not activated
prims = False
kruskals = False
dijkstras = False
#The nodes for the algorithms are all empty
prims_nodes = []
kruskals_nodes = []
dijkstras_nodes = []
#There is nothing in the clipboard atm
clipboard = None
#No node has been right clicked on atm
current_node_right_clicked_on = None

#Gameloop
while run:
	#The clock which will dictacte the ticks
	clock.tick(60)
	#This will fill the screen with this colour and since it is at the start of the loop this indicates that it is the background
	win.fill(colour1[theme])
	#mouse x and y coords
	mousex,mousey = pygame.mouse.get_pos()

	#This will assess which page the user is currently on
	if page == "login" or page =="signup":
		#Design
		pygame.draw.rect(win,(255,255,255),(400,40,480,160))
		#This inserts the image of the header
		win.blit(header,(400,40))
		pygame.draw.rect(win,(0,0,0),(400,40,480,160),2)
		#Subheader
		win.blit(subheader,(440,180))
		#This is the usrename/password box and text setup
		win.blit(font.render("Username:",0,(255,255,255)),(480,340))
		pygame.draw.rect(win,colour2[theme],(480,380,320,50))
		win.blit(font.render("Password:",0,(255,255,255)),(480,430))
		pygame.draw.rect(win,colour2[theme],(480,470,320,50))
		#If the user wants to login it will display the login button
		if page == "login":
			pygame.draw.rect(win,colour2[theme],(570,535,130,50))
			win.blit(font.render("Login",0,(0,0,0)),(590,540))


			win.blit(font.render("Signup?",0,(0,0,0)),(575,620))
			pygame.draw.line(win,(0,0,0),(575,660),(705,660),3)
		#If the user wants to signup it shows the signup button
		elif page == "signup":
			pygame.draw.rect(win,colour2[theme],(570,535,130,50))
			win.blit(font.render("Signup",0,(0,0,0)),(575,540))


			win.blit(font.render("Login?",0,(0,0,0)),(590,620))
			pygame.draw.line(win,(0,0,0),(575,660),(705,660),3)

		#Renders the username
		win.blit(font.render(user_string,0,(0,0,0)),(480,380))
		#If the user is signing up then the password will render shown, otherwise itll be hiddne
		if page == "login":
			win.blit(pass_font.render(pass_string,0,(0,0,0)),(480,470))
		elif page == "signup":
			win.blit(font.render(pass_string,0,(0,0,0)),(480,470))
		#If the username box is selected then the uesrname will be editted
		if username:
			user_string = current_string
			pygame.draw.rect(win,(0,0,0),(475,375,330,60),5)
		#Otherwise if the password box is selected then the passowrd wil lbe editted
		elif password:
			pass_string = current_string
			pygame.draw.rect(win,(0,0,0),(475,465,330,60),5)

		#Displays the settings icon
		win.blit(settings_icon,(1100,600))

		#If the user left clicks
		if pygame.mouse.get_pressed()[0]:
			#If it is bounded withing the username box
			if mousex >= 480 and mousex <= 800 and mousey >= 380 and mousey <= 430:
				#Allows the user to enter the username
				username = True
				password = False
				current_string = user_string
			#If tit is mbonuded within the password box
			elif mousex >= 480 and mousex <= 800 and mousey >= 470 and mousey <= 520:
				#Allows the user to enter the password
				username = False
				password = True
				current_string = pass_string
			elif mousex >= 575 and mousex <= 705 and mousey >= 620 and mousey <= 660:
				#If the login/signup? button is clicked
				time.sleep(0.2)
				if page == "login":
					page = "signup"
				elif page == "signup":
					page = "login"

			elif mousex >= 570 and mousex <= 700 and mousey >= 535 and mousey <= 585:
				#If the login button is clicked
				if page == "login":
					#checks to see if the credentials are correct
					val = login(user_string,pass_string)
					#If not it will tell the user that the username or apss is wrong
					if not val:
						win.blit(font.render("User or pass incorrect",0,(255,0,0)),(480,300))
						pygame.display.update()
						time.sleep(0.3)

					#Otherwise it will send the user to the menu screen
					else:
						page = "menu"
						current_string = ""
				#If the signup button is clicked
				elif page == "signup":
					#It checks to see if a user with that username alr exists
					val = signup(user_string,pass_string)
					if val:
						win.blit(font.render("User alr exists",0,(255,0,0)),(480,300))
						pygame.display.update()
						time.sleep(0.3)

					else:
						page = "menu"
						current_string = ""
			elif mousex >= 1100 and mousex <= 1170 and mousey >= 600 and mousey <= 670:
				#if the settings button is cliecked it sends the user to the settings button
				page = "settings_login"

			else:
				#If the user clicks anywhere else then the username and password boxes are deseected
				username = False
				password = False

	elif page == "settings_login" or page == "settings_menu":
		#Draws the settings art
		win.blit(back_icon,(20,20))
		win.blit(font.render("Theme 1",0,(0,0,0)),(600,70))
		win.blit(font.render("Theme 2",0,(0,0,0)),(600,110))
		#If user clicks
		if pygame.mouse.get_pressed()[0]:
			#If they select the back button then it returns them to the place they were at
			if mousex >= 20 and mousex <= 90 and mousey >= 20 and mousey <= 90:
				if page == "settings_login":
					page = "login"
				else:
					page = "menu"
					time.sleep(0.2)
			#If they click on theme1/theme 2 it changes the colours
			if mousex >= 600 and mousex <= 720:
				if mousey >= 70 and mousey <= 100:
					theme = 0
				elif mousey >= 110 and mousey <= 150:
					theme = 1


	#
	elif page == "menu":
		#Shows the buttons on the menu
		pygame.draw.rect(win,colour2[theme],(0,0,950,100))
		pygame.draw.rect(win,(0,0,0),(0,0,950,100),2)

		pygame.draw.rect(win,colour4[theme],(950,0,330,720))
		pygame.draw.rect(win,(0,0,0),(950,0,330,720),2)

		conn = sqlite3.connect('Resources/SaveData/SaveData.db')
		curs = conn.cursor()
		curs.execute(f"SELECT * FROM Folder_info WHERE Account_id={current_account_id}")
		#Selects all the folders associated with the acocunt fom the database
		folder_list = curs.fetchall()
		largest_folder_id = folder_list[len(folder_list)-1][0]
		#Displays all the folders associated witht the account of the panel on the right hand side
		for a,i in enumerate(folder_list):
			pygame.draw.rect(win,(0,0,0),(970,20+a*45,200,40),2)
			win.blit(font.render(f"{i[1]}",0,(255,0,0)),(975,22+a*45))

		pygame.draw.rect(win,(255,0,0),(970,20+current_folder_id*45,200,40),2)

		conn.commit()
		conn.close()
		#Settings icon again
		win.blit(settings_icon,(870,20))
		#Sends the user to the settings menu
		if pygame.mouse.get_pressed()[0]:
			if mousex >= 870 and mousex <= 940 and mousey >= 20 and mousey <= 90:
				page = "settings_menu"

		#If the user clicks on a speciic folder then the current folder id wil be changed to that which they selected
		if pygame.mouse.get_pressed()[0]:
			for a,i in enumerate(folder_list):
				if mousex >= 970 and mousex <= 1170 and mousey >= 20+a*45 and mousey <= 60+a*45:
					current_folder_id = a


		conn = sqlite3.connect('Resources/SaveData/SaveData.db')
		curs = conn.cursor()
		curs.execute(f"SELECT * FROM Graph_info WHERE Folder_id={current_folder_id} AND Account_id={current_account_id}")
		#retreve all the graphs in the database that are assocaited with the user
		graph_list = curs.fetchall()
		#will set the largest graph id to the length of the previous graph
		try:
			largest_graph_id = graph_list[len(graph_list)-1][len(graph_list[len(graph_list)-1])-1]
			#If it cant then it will set it to -1 (implying that there are no graphs currently made)
		except:
			largest_graph_id = -1
		#Draws all the graphs that are currently int the folder
		for a,i in enumerate(graph_list):
			pygame.draw.rect(win,(0,0,0),(40,120+a*45,600,40),2)
			win.blit(font.render(f"{i[0]}",0,(255,0,0)),(45,122+a*45))
	
		conn.commit()
		conn.close()
		#If the user clicks anyone of the graphs that are displayed then it will take them to the canvas where they can create graphs
		if pygame.mouse.get_pressed()[0]:
			for a,i in enumerate(graph_list):
				if mousex >= 40 and mousex <= 640 and mousey >= 120+a*45 and mousey <= 160+a*45:
					#sets the current graph id to the one that has been selected
					current_graph_id = a
					#switches pages
					page = "canvas"
					#retreives the matrix and the nodes from the database of the graph that they selected and they are assigned to the matrix and nodes
					matrix = pickle.loads(graph_list[current_graph_id][3])
					nodes = pickle.loads(graph_list[current_graph_id][4])


		#Displays the buttons for a new project, new folder and importing other graphs
		pygame.draw.rect(win,(0,0,0),(20,20,230,60),2)
		win.blit(font.render("New project",0,(0,0,0)),(30,30))

		pygame.draw.rect(win,(0,0,0),(270,20,215,60),2)
		win.blit(font.render("New folder",0,(0,0,0)),(280,30))

		pygame.draw.rect(win,(0,0,0),(505,20,135,60),2)
		win.blit(font.render("Import",0,(0,0,0)),(515,30))

		#If the user hasnt decided to create a graph or create a folder
		if not text_box_folder and not text_box_graph:
			weighted = False
			current_string = ""
			if pygame.mouse.get_pressed()[0]:
				if mousex >= 20 and mousex <= 250 and mousey >= 20 and mousey <= 80:
					#onclick
					text_box_graph = True
					time.sleep(0.1)

				elif mousex >= 270 and mousex <= 485 and mousey >= 20 and mousey <= 80:
					#onclick
					text_box_folder = True
					time.sleep(0.1)

				elif mousex >= 505 and mousex <= 640 and mousey >= 20 and mousey <= 80:
					#opens windows explorere on the imports folder ands gets the user to select a file
					import_graph = filedialog.askopenfilename(initialdir="Resources/Imports",title="Select A File",filetypes=(("dat files", "*.dat"),))
					#sets to the value being imported
					opening_import = open(import_graph,"rb")
					#unloads the binary file
					graph_pieces = pickle.loads(opening_import.read())
					opening_import.close()

					conn = sqlite3.connect('Resources/SaveData/SaveData.db')
					curs = conn.cursor()
					#creates a list with all the graphs in the folder in the account
					curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id}")
					check = curs.fetchall()
					alr = False
					#Checks to see if its already in the databse
					for i in check:
						#if the names are the same
						if graph_pieces[0] == i[0]:
							#knows its already there
							alr = True
					#if it is not already there then it wil add it to the database
					if not alr:
						curs.execute("INSERT INTO Graph_info VALUES (:Name,:Weighted,:Directed,:Graph,:List,:Account_id,:Folder_id,:Graph_id)",
							{
							'Name':graph_pieces[0],
							'Weighted':graph_pieces[1],
							'Directed':graph_pieces[2],
							'Graph':graph_pieces[3],
							'List':graph_pieces[4],
							'Account_id':current_account_id,
							'Folder_id':current_folder_id,
							'Graph_id':largest_graph_id+1

							})
						#turns off the text box
						text_box_graph = False
						#increases the length of the graphs list
						current_graph_id = largest_graph_id+1
						#sets the string to nothing
						current_string = ""
					#closes the database
					conn.commit()
					conn.close()



		elif text_box_graph:
			#displays all the buttons for the text box for creating a graph
			pygame.draw.rect(win,colour4[theme],(320,200,640,320))
			pygame.draw.rect(win,(0,0,0),(320,200,640,320),2)

			#Input field for the user to input the name
			win.blit(font.render("Enter graph name:",0,(255,255,255)),(480,220))
			pygame.draw.rect(win,colour5[theme],(360,280,560,40))
			pygame.draw.rect(win,(0,0,0),(360,280,560,40),2)

			win.blit(font.render(current_string,0,(0,0,0)),(365,280))
			#Displays whether the graph is weighted or not
			if weighted:
				win.blit(font.render("Weighted",0,(0,0,0)),(550,350))
			else:
				win.blit(font.render("Not Weighted",0,(0,0,0)),(550,350))

			#Design for the weighed? button
			pygame.draw.circle(win,(0,0,0),(620,420),18,2,draw_top_left=True,draw_bottom_left=True)
			pygame.draw.circle(win,(0,0,0),(660,420),18,2,draw_top_right=True,draw_bottom_right=True)
			pygame.draw.line(win,(0,0,0),(620,420-18),(660,420-18),2)
			pygame.draw.line(win,(0,0,0),(620,420+17),(660,420+17),2)

			pygame.draw.circle(win,colour3[theme],(620,420),14,draw_top_left=True,draw_bottom_left=True)
			pygame.draw.circle(win,colour3[theme],(660,420),14,draw_top_right=True,draw_bottom_right=True)
			pygame.draw.rect(win,colour3[theme],(620,420-14,40,28))

			#Displays a green light for weighted and a red light for not weighted
			if not weighted:
				pygame.draw.circle(win,(255,0,0),(620,420),10)
			else:
				pygame.draw.circle(win,(0,255,0),(660,420),10)

			#Enter button
			pygame.draw.rect(win,(0,0,0),(580,470,120,40),2)
			win.blit(font.render("Enter",0,(0,0,0)),(590,470))

			#Checks for mouse button clicks
			if pygame.mouse.get_pressed()[0]:
				#If they click outside the box then it removes the text box
				if not(mousex >= 320 and mousex <= 960 and mousey >= 120 and mousey <= 600):
					text_box_graph = False
				#If the user clicks the weighte dbutton then it changes it from weighted to not weighted and vice versa
				elif mousex >= 620-18 and mousex <= 660+18 and mousey >= 420-18 and mousey <= 420+18:
					#if its weighted then it will change it to not weighted
					if weighted:
						weighted = False
						win.blit(font.render("Not Weighted",0,(0,0,0)),(550,350))
						#otherwise it will be weighted
					else:
						weighted = True
						win.blit(font.render("Weighted",0,(0,0,0)),(550,350))
					#this waits 0.1 which acts like a buffer so that the person does not end up spamming
					time.sleep(0.1)
					#Enter button
				elif mousex >= 580 and mousex <= 700 and mousey >= 470 and mousey <= 510:
					#Makes sure to see theres a name inputted
					if current_string != "":
						conn = sqlite3.connect('Resources/SaveData/SaveData.db')
						curs = conn.cursor()
						#Inputs it into the database
						curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id}")
						#Checks for duplicates
						check = curs.fetchall()
						#Checks to see if its already there or not
						alr = False
						for i in check:
							if current_string == i[0]:
								alr = True

						#If it is not already tehre then it will insert it into the table
						#It enters an empty from and an empty list becauase the user has just created the graph
						#The other stuff are variables which have already been defined
						if not alr:
							curs.execute("INSERT INTO Graph_info VALUES (:Name,:Weighted,:Directed,:Graph,:List,:Account_id,:Folder_id,:Graph_id)",
								{
								'Name':current_string,
								'Weighted':weighted,
								'Directed':False,
								'Graph':pickle.dumps([]),
								'List':pickle.dumps([]),
								'Account_id':current_account_id,
								'Folder_id':current_folder_id,
								'Graph_id':largest_graph_id+1

								})
							text_box_graph = False
							#Increments the latest graph by 1
							current_graph_id = largest_graph_id+1
							#empties the current string
							current_string = ""
						else:
							win.blit(font.render("Name already exists",0,(255,0,0)),(480,150))
							pygame.display.update()
							time.sleep(0.3)
						conn.commit()
						conn.close()
					else:
						win.blit(font.render("Please enter a name",0,(255,0,0)),(480,150))
						pygame.display.update()
						time.sleep(0.3)



		else:
			
			#Displays the folder popup text box and buttons
			pygame.draw.rect(win,colour4[theme],(320,240,640,240))
			pygame.draw.rect(win,(0,0,0),(320,240,640,240),2)
			#Entry field
			win.blit(font.render("Enter folder name:",0,(255,255,255)),(480,300))
			pygame.draw.rect(win,colour5[theme],(360,360,560,40))
			win.blit(font.render(current_string,0,(0,0,0)),(370,360))
			pygame.draw.rect(win,(0,0,0),(360,360,560,40),2)
			pygame.draw.rect(win,(0,0,0),(580,420,120,40),2)
			#Displays the enter button
			win.blit(font.render("Enter",0,(0,0,0)),(590,420))
			#Checks that the mouse has bene clicked
			if pygame.mouse.get_pressed()[0]:
				#Checks to see if the mouse was outside the box otherwise it deselects
				if not(mousex >= 320 and mousex <= 960 and mousey >= 240 and mousey <= 480):
					text_box_folder = False

				#If it clicks on the button
				elif mousex >= 580 and mousex <= 700 and mousey >= 420 and mousey <= 460:
					#makes sure that the box is not empty
					if current_string != "":
						#Connects to the database
						conn = sqlite3.connect('Resources/SaveData/SaveData.db')
						curs = conn.cursor()
						#retreives all the folders under the account
						curs.execute(f"SELECT * FROM Folder_info WHERE Account_id={current_account_id}")
						#sets them to a list
						check = curs.fetchall()

						#Check to see if there is a duplicate
						alr = False
						for i in check:
							if current_string == i[1]:
								alr = True
						#If there is not a duplicate it inputs it into the database under the user
						if not alr:
							curs.execute("INSERT INTO Folder_info VALUES (:Folder_id,:Name,:Account_id)",
								{
								'Folder_id':largest_folder_id+1,
								'Name':current_string,
								'Account_id':current_account_id

								})
							text_box_folder = False
							current_folder_id = largest_folder_id+1

						else:
							win.blit(font.render("Folder already exists",0,(255,0,0)),(480,150))
							pygame.display.update()
							time.sleep(0.3)
						conn.commit()
						conn.close()

					else:
						win.blit(font.render("Please enter a name",0,(255,0,0)),(480,150))
						pygame.display.update()
						time.sleep(0.3)

	#This will be all the code for the kanvas
	elif page == "canvas":
		#Whenever the game loops it will always update the matrix by using the list_to_graph module.
		#This means whenever the matrix has an algorithm applied onto it, the matrix will be updated at the start of the loop
		matrix = list_to_graph(nodes)
		#This help with any errors that occur during the process of conversion. Sometimes the graph only fills half of the matrix.
		#This algorithm makes the matrix symmetrical along the leading diagonal
		#loops through all the columns
		for a,i in enumerate(matrix):
			#loops though all the rows
			for b,j in enumerate(matrix):
				#checks to see that there is an edge in the cell currently being examined
				if matrix[a][b] != '-':
					#will set the opposite value to it
					matrix[b][a] = matrix[a][b]
				#does the opposite for its mirror
				if matrix[b][a] != '-':
					matrix[a][b] = matrix[b][a]


		#loops through all the nodes
		for i in nodes:
			#loops through all the neighbours
			for j in i.neighbours:
				#loops through all the node again
				for k in nodes:
					#If the node is connected to the other node
					if j[0] == k.name:
						#Draws the edge
						pygame.draw.line(win,(255,0,0),(i.x,i.y),(k.x,k.y),2)
						#If it is weighted then it also draws its weight
						if weighted:
							win.blit(font.render(str(j[1]),0,(255,255,255)),((i.x+k.x)//2,(i.y+k.y)//2))

		#loops through all the nodes
		for i in nodes:
			#draws the node and its name
			pygame.draw.circle(win,(255,255,255),(i.x,i.y),20)
			pygame.draw.circle(win,(0,0,0),(i.x,i.y),20,1)
			win.blit(small_font.render(i.name,0,(0,0,0)),(i.x-30,i.y-40))


		conn = sqlite3.connect('Resources/SaveData/SaveData.db')
		curs = conn.cursor()
		#gets all the graphs from the current folder
		curs.execute(f"SELECT * FROM Graph_info WHERE Folder_id={current_folder_id} AND Account_id={current_account_id}")
		graph_list = curs.fetchall()
		conn.commit()
		conn.close()

		#checks to see if this graph is weighted
		try:
			weighted = graph_list[current_graph_id][1]
		except:
			weighted = graph_list[current_graph_id-1][1]

		#draws the pannels
		pygame.draw.rect(win,colour2[theme],(0,0,950,100))
		pygame.draw.rect(win,(0,0,0),(0,0,950,100),2)
		#draws the export button
		pygame.draw.rect(win,colour4[theme],(950,0,330,720))
		pygame.draw.rect(win,(0,0,0),(950,0,330,720),2)
		win.blit(font.render(f"Export",0,(0,0,0)),(750,20))
		win.blit(export_icon,(870,20))
		#allows the user to go back
		win.blit(back_icon,(20,20))
		#sets the string version of the weighted variable to whatever it. It needs to be a tring so that it can be displayed onto the screen
		if weighted:
			weight = "True"
		else:
			weight = "False"

		#displays whether it is weighed or not
		win.blit(font.render(f"Weighted:{weight}",0,(0,0,0)),(955,10))
		#Not yet made it able to be directed so for now all the graphs will be undirected
		win.blit(font.render(f"Directed:False",0,(0,0,0)),(955,50))

		#Displays the buttons for prims kruskals and dijkstras
		pygame.draw.rect(win,(0,0,0),(955,90,200,40),1)
		win.blit(font.render(f"Prims",0,(0,0,0)),(960,90))
		#If the algorithm has been selected then it will highlight it red
		if prims:
			pygame.draw.rect(win,(255,0,0),(955,90,200,40),1)
			win.blit(font.render(f"Prims",0,(255,0,0)),(960,90))
		#same for kruskals
		pygame.draw.rect(win,(0,0,0),(955,140,200,40),1)
		win.blit(font.render(f"Kruskals",0,(0,0,0)),(960,140))
		if kruskals:
			pygame.draw.rect(win,(255,0,0),(955,140,200,40),1)
			win.blit(font.render(f"Kruskals",0,(255,0,0)),(960,140))
		#same for dijkstras
		pygame.draw.rect(win,(0,0,0),(955,190,200,40),1)
		win.blit(font.render(f"Dijkstras",0,(0,0,0)),(960,190))
		if dijkstras:
			pygame.draw.rect(win,(255,0,0),(955,190,200,40),1)
			win.blit(font.render(f"Dijkstras",0,(255,0,0)),(960,190))
		#reset button
		pygame.draw.rect(win,(0,0,0),(955,240,200,40),1)
		win.blit(font.render(f"Reset",0,(0,0,0)),(960,240))


		#checks to see if the right click menu is active
		if right_click_menu:
			#if they left click or middle click
			if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[1]:
				#if they click outside the menu area
				if not(mousex > tempx and mousey > tempy and mousex < tempx+200 and mousey < tempy+340):
					#deselects the right click menu
					right_click_menu = False
			#if they right click tho then it just changes the corrdinates of the right click menu
			elif pygame.mouse.get_pressed()[2] and mousex >= 0 and mousex <= 950 and mousey >= 100 and mousey <= 720:
				tempx,tempy=mousex,mousey
		#if the menu isnt active
		else:
			#if the user clicks in the region of the canvas
			if mousex >= 0 and mousex <= 950 and mousey >= 100 and mousey <= 720:
				#if they right click
				if pygame.mouse.get_pressed()[2]:
					#it will load the menu
					right_click_menu = True
					#check to see if any node has been clicked on at all
					current_node_right_clicked_on = None
					#cycles through all the node
					for i in nodes:
						#checks each of the nodes corrdinated and a 40x40 region around its center to check if the user has right clicked on that node
						if mousex >= i.x-20 and mousex <= i.x+20 and mousey >= i.y-20 and mousey <= i.y+20:
							#if so then it will set it to the current node right clicked on
							current_node_right_clicked_on = i
					#in addition when the user right clicks it sets tempx,temy to the coordatinated which were right clicked on. This precents it from following the mouse cursor
					tempx,tempy=mousex,mousey
			#is the user clicks on the export buttons
			elif mousex >=870 and mousex <= 940 and mousey >=20 and mousey <=90:
				if pygame.mouse.get_pressed()[0]:
					#it collects all the information of the graph from graph list
					temp_import_graph = graph_list[current_graph_id]
					#it opens a new file with the name of th graph. the file is a dat file
					export_file = open("Resources/Exports/"+graph_list[current_graph_id][0]+".dat","wb")
					#pickles the information and stores it in the bnary file
					export_file.write(pickle.dumps(temp_import_graph))
					#closes the file so its saved
					export_file.close()

						

		#if the right click menu is active
		if right_click_menu:
			#displays the copy button
			pygame.draw.rect(win,(255,255,255),(tempx,tempy,200,340))
			pygame.draw.rect(win,(180,180,180),(tempx,tempy,200,340),1)
			pygame.draw.rect(win,(0,0,0),(tempx+20,tempy+20,40,45),1)
			pygame.draw.rect(win,(255,255,255),(tempx+24,tempy+16,40,45))
			pygame.draw.rect(win,(0,0,0),(tempx+24,tempy+16,40,45),1)
			win.blit(font.render("Copy",0,(0,0,0)),(tempx+80,tempy+20))
			#displays the paste button
			pygame.draw.line(win,(180,180,180),(tempx,tempy+80),(tempx+200,tempy+80),1)
			#if something exists in the clipboard then it will display black, otherwisde it will display grey
			if clipboard != None:
				win.blit(paste_icon[1],(tempx+10,tempy+90))
				win.blit(font.render("Paste",0,(0,0,0)),(tempx+80,tempy+105))
			else:
				win.blit(paste_icon[0],(tempx+10,tempy+90))
				win.blit(font.render("Paste",0,(150,150,150)),(tempx+80,tempy+105))

			pygame.draw.line(win,(180,180,180),(tempx,tempy+170),(tempx+200,tempy+170),1)
			#Displays the add button
			pygame.draw.circle(win,(0,0,0),(tempx+42,tempy+210),25,1)
			win.blit(font.render("Add",0,(0,0,0)),(tempx+90,tempy+190))

			pygame.draw.line(win,(180,180,180),(tempx,tempy+260),(tempx+200,tempy+260),1)
			#displays the delete button but displays it grey if o node is selected but displays black if there is
			if current_node_right_clicked_on != None:
				pygame.draw.line(win,(0,0,0),(tempx+20,tempy+270),(tempx+50,tempy+320))
				pygame.draw.line(win,(0,0,0),(tempx+20,tempy+320),(tempx+50,tempy+270))
				win.blit(font.render("Delete",0,(0,0,0)),(tempx+70,tempy+280))
			else:
				pygame.draw.line(win,(150,150,150),(tempx+20,tempy+270),(tempx+50,tempy+320))
				pygame.draw.line(win,(150,150,150),(tempx+20,tempy+320),(tempx+50,tempy+270))
				win.blit(font.render("Delete",0,(150,150,150)),(tempx+70,tempy+280))
			#if the user clicks
			if pygame.mouse.get_pressed()[0]:
				#checks to see if its in the range of the right click menu
				if mousex > tempx and mousex < tempx+200:
					#checks to see if its in the range of the copy button
					if mousey > tempy and mousey < tempy+80:
						#tries to add a node to the cliboard
						try:
							clipboard = current_node_right_clicked_on
						except:pass
					#checks to see if its in the range of the paste button
					elif mousey > tempy+80 and mousey < tempy+170:
						#checks to see if there issomething in the clipboard
						if clipboard:
							#checks to see if there is already a copy of that node
							alr = False
							temp_neighbours = []
							#finds all the neighbours of the node that has been copied
							for i in clipboard.neighbours:
								temp_neighbours.append(i)
							#cycles through al lthe nodes and their neighbours to see if they share a neighbour with the node in the clipboard
							for i in nodes:
								for j in i.neighbours:
									if j[0] == clipboard.name:
										#if they do then it wil again append it to the neighbours of the copying node
										temp_neighbours.append([i.name,j[1]])

							#checks too see for  adulicate name
							for i in nodes:
								if i.name == clipboard.name + " - Copy":
									alr = True

							#adds the new copied node to the nodes list
							if not alr:
								nodes.append(node(clipboard.name + " - Copy",len(nodes)+1,clipboard.x,clipboard.y,temp_neighbours))

							#remvoves the old node from clipboard
							clipboard = None

					#checks to see if it is in the range if the add button
					elif mousey > tempy+170 and mousey < tempy+260:
						#opens the add menu but closes the right click menu
						add_menu = True
						right_click_menu = False
					#checks to see if it is in the range of the delete button
					elif mousey > tempy+260 and mousey < tempy+340:
						try:
							#deletes the node from the nodes list
							for i in nodes:
								if i.name == current_node_right_clicked_on.name:
									nodes.remove(i)
							#goes through every other nodes neighbours and deletes the connection between theme
							for i in nodes:
								for j in i.neighbours:
									if j[0] == current_node_right_clicked_on.name:
										i.neighbours.remove(j)
						except:pass
				#saves any changes made to the database that has been made
				conn = sqlite3.connect('Resources/SaveData/SaveData.db')
				curs = conn.cursor()
				curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id} AND Graph_id={current_graph_id}")
				check = curs.fetchall()

				check = check[0]
				curs.execute(f"""UPDATE Graph_info SET 
					Name = :Name,
					Weighted = :Weighted,
					Directed = :Directed,
					Graph = :Graph,
					List = :List,
					Account_id = :Account_id,
					Folder_id = :Folder_id,
					Graph_id = :Graph_id

					WHERE Account_id = {current_account_id} AND Folder_id = {current_folder_id} AND Graph_id = {current_graph_id}
					""",
					{
					'Name':check[0],
					'Weighted':check[1],
					'Directed':check[2],
					'Graph':pickle.dumps(matrix),
					'List':pickle.dumps(nodes),
					'Account_id':check[5],
					'Folder_id':check[6],
					'Graph_id':check[7],


					})


		
				conn.commit()
				conn.close()
				current_string = ""
		#if the add menu is selected
		elif add_menu:
			#displays the buttons
			pygame.draw.rect(win,colour4[theme],(320,240,640,240))
			pygame.draw.rect(win,(0,0,0),(320,240,640,240),2)
			#displays the entry field
			win.blit(font.render("Enter node name:",0,(255,255,255)),(480,300))
			pygame.draw.rect(win,colour5[theme],(360,360,560,40))
			#limits the name of the node to be 10 characters long
			current_string = current_string[:10]
			#displays the name in the entry field
			win.blit(font.render(current_string,0,(0,0,0)),(370,360))
			pygame.draw.rect(win,(0,0,0),(360,360,560,40),2)
			pygame.draw.rect(win,(0,0,0),(580,420,120,40),2)
			#enter button
			win.blit(font.render("Enter",0,(0,0,0)),(590,420))
			#if the user clicks enter
			if pygame.mouse.get_pressed()[0]:
				#checks to see if the user has clicked on the right area
				if mousex >= 580 and mousex <= 700 and mousey >= 420 and mousey <= 460:
					#makes sure the node has a name
					if current_string != "":
						#check to see if a node already has this name
						alr = False
						for i in nodes:
							if current_string == i.name:
								alr = True
						#if it doesnt
						if not alr:
							#finds the latest position of the nodes
							temp_len = len(nodes)+1
							#adds it to the nodes list
							nodes.append(node(current_string,temp_len,tempx,tempy,[]))
							#closes the menu
							add_menu = False

							conn = sqlite3.connect('Resources/SaveData/SaveData.db')
							curs = conn.cursor()
							curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id} AND Graph_id={current_graph_id}")
							check = curs.fetchall()

							check = check[0]
							#adds it to the database
							curs.execute(f"""UPDATE Graph_info SET 
								Name = :Name,
								Weighted = :Weighted,
								Directed = :Directed,
								Graph = :Graph,
								List = :List,
								Account_id = :Account_id,
								Folder_id = :Folder_id,
								Graph_id = :Graph_id

								WHERE Account_id = {current_account_id} AND Folder_id = {current_folder_id} AND Graph_id = {current_graph_id}
								""",
								{

								'Name':check[0],
								'Weighted':check[1],
								'Directed':check[2],
								'Graph':pickle.dumps(matrix),
								'List':pickle.dumps(nodes),
								'Account_id':check[5],
								'Folder_id':check[6],
								'Graph_id':check[7],


								})


	
							conn.commit()
							conn.close()
							current_string = ""


		elif node_menu:
			#if tje user is on the add node menu
			#displays the popup box
			pygame.draw.rect(win,colour4[theme],(320,240,640,240))
			pygame.draw.rect(win,(0,0,0),(320,240,640,240),2)
			#displays entry field
			win.blit(font.render("Enter edge weight:",0,(255,255,255)),(480,300))
			pygame.draw.rect(win,colour5[theme],(360,360,560,40))
			#tests to see if the string is an integer. If it isnt then it will remove the last digit
			try:
				int(current_string)
			except:
				current_string = current_string[:-1]
			#displats enter button
			win.blit(font.render(current_string,0,(0,0,0)),(370,360))
			pygame.draw.rect(win,(0,0,0),(360,360,560,40),2)
			pygame.draw.rect(win,(0,0,0),(580,420,120,40),2)
			win.blit(font.render("Enter",0,(0,0,0)),(590,420))
			#if the mouse is pressed
			if pygame.mouse.get_pressed()[0]:
				#if the user has clicked enter
				if mousex >= 580 and mousex <= 700 and mousey >= 420 and mousey <= 460:
					#if the string isnt empty
					if current_string != "":
						#closes the popup
						node_menu = False
						#it adds to the neighours list the node edge
						nodes[closest[2]].neighbours.append([nodes[second_closest[2]].name,int(current_string)])
						matrix = list_to_graph(nodes)
						#the matrix gets updated
						conn = sqlite3.connect('Resources/SaveData/SaveData.db')
						curs = conn.cursor()
						curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id} AND Graph_id={current_graph_id}")
						check = curs.fetchall()
						check = check[0]
						#updates the database
						curs.execute(f"""UPDATE Graph_info SET 
							Name = :Name,
							Weighted = :Weighted,
							Directed = :Directed,
							Graph = :Graph,
							List = :List,
							Account_id = :Account_id,
							Folder_id = :Folder_id,
							Graph_id = :Graph_id
							WHERE Account_id = {current_account_id} AND Folder_id = {current_folder_id} AND Graph_id = {current_graph_id}
							""",
							{
							'Name':check[0],
							'Weighted':check[1],
							'Directed':check[2],
							'Graph':pickle.dumps(matrix),
							'List':pickle.dumps(nodes),
							'Account_id':check[5],
							'Folder_id':check[6],
							'Graph_id':check[7],})
						conn.commit()
						conn.close()
						current_string = ""

		else:

			#checks to see if the user has clicked on any of the algorthm buttons
			if pygame.mouse.get_pressed()[0]:
				#if they click the back button then the user goes back to the menu
				if mousex >= 20 and mousex <= 90 and mousey >= 20 and mousey <= 90:
					page = "menu"
					time.sleep(0.2)
				#if the user clicks on the right sidebar
				if mousex >= 955 and mousex <= 1155:
					#checks to see if prims has been clicked
					if mousey >= 90 and mousey <= 130:
						#only enables prims
						prims = True
						kruskals = False
						dijkstras = False
					#checks to see if kruskals has been clicked
					elif mousey >= 140 and mousey <= 180:
						#only enables kruskals
						prims = False
						kruskals = True
						dijkstras = False
					#checks to see if dijkstras has been clicked
					elif mousey >= 190 and mousey <= 230:
						#only enables djikstras
						prims = False
						kruskals = False
						dijkstras = True
					#checks to see if the reset button has been clicked
					elif mousey >= 240 and mousey <= 280:
						#disables all of them and resets the nodes in the arays
						prims = False
						kruskals = False
						dijkstras = False
						prims_nodes = []
						kruskal_nodes = []
						dijkstras_nodes = []


			#if prims is active then it will display the prims edges
			if prims:
				#cycles through all the prims nodes
				for i in prims_nodes:
					#updates the coordinates so that if the user moves around the nodes these edges will also move around
					i.update_coords(nodes)
					#cycles through neighbours
					for j in i.neighbours:
						#cycles through the nodes
						for k in prims_nodes:
							#checks to see if they are neighbours
							if j[0] == k.name:
								#draws the edge
								pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)


			#if kruskal is active then it will display the kruskal edges
			if kruskals:
				#cycles through all the kruskal nodes
				for i in kruskals_nodes:
					#updates the coordinates so that if the user moves around the nodes these edges will also move around
					i.update_coords(nodes)
					#cycles through neighbours
					for j in i.neighbours:
						#cycles through the nodes
						for k in kruskals_nodes:
							#checks to see if they are neighbours
							if j[0] == k.name:
								#draws the edge
								pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)

			#if djikstras is active then izt will display the dijkstras edges
			if dijkstras:
				##cycles through all the nodes
				for i in range(0,len(dijkstras_nodes)):
					#displays the edges from the start to the end of each of the nodes
					try:
						pygame.draw.line(win, (0, 0, 255), (nodes[dijkstras_nodes[i]].x, nodes[dijkstras_nodes[i]].y), (nodes[dijkstras_nodes[i+1]].x, nodes[dijkstras_nodes[i+1]].y),2)

					except:pass

			#checks to see if shift is pressed and that there are movre than 2 nodes
			keys = pygame.key.get_pressed()
			if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and len(nodes) >=2:
				#if prims and kruskals are not selected
				if not prims and not kruskals:
					#the user can select the first node
					if first_node:
						#sets the first node to the closest as a base case
						closest = [nodes[0].x,nodes[0].y,0]
						#goes through all the node
						for a,i in enumerate(nodes):
							#checks to see if the magnitude of the distance between the nodes is smaller and if it is then it will set that as the new closest
							if ((i.x-mousex)**2+(i.y-mousey)**2)**0.5 <= ((mousex-closest[0])**2+(mousey-closest[1])**2)**0.5:
								closest = [i.x,i.y,a]

						#highlights the selected node
						pygame.draw.circle(win,(0,255,0),(nodes[closest[2]].x,nodes[closest[2]].y),20)
						pygame.draw.circle(win,(0,0,0),(nodes[closest[2]].x,nodes[closest[2]].y),20,1)
						win.blit(small_font.render(nodes[closest[2]].name,0,(0,0,0)),(nodes[closest[2]].x-30,nodes[closest[2]].y-40))
						#if the user clicks then the second node will have a chance to get selected
						if pygame.mouse.get_pressed()[0]:
							first_node = False
							second_node = True
							time.sleep(0.2)

					#if the second node neds to be chosen
					elif second_node:
						#highlights the original selected node
						pygame.draw.circle(win,(0,0,255),(nodes[closest[2]].x,nodes[closest[2]].y),20)
						pygame.draw.circle(win,(0,0,0),(nodes[closest[2]].x,nodes[closest[2]].y),20,1)
						#finds a random other node to make the second closest as a base case
						try:
							second_closest = [nodes[closest[2]+1].x,nodes[closest[2]+1].y,closest[2]+1]
						except:
							second_closest = [nodes[closest[2]-1].x,nodes[closest[2]-1].y,closest[2]-1]

						#once again cycles though all the values to find the closest value
						for a,i in enumerate(nodes):
							##checks for the magnitude to see if it is smaller
							if ((i.x-mousex)**2+(i.y-mousey)**2)**0.5 <= ((mousex-second_closest[0])**2+(mousey-second_closest[1])**2)**0.5:
								#checks to see that the node is not the same as the starting node
								if second_closest[2] != closest[2]:
									#sets it as the 2nd node
									second_closest = [i.x,i.y,a]

						#if the user clicks the mouse now
						if pygame.mouse.get_pressed()[0]:
							#resets the variables
							first_node = True
							second_node = False
							time.sleep(0.2)
							#checks to see for duplicate nodes
							alr = False
							for i in nodes[closest[2]].neighbours:
								if i[0] ==nodes[second_closest[2]].neighbours:
									alr = True
							if nodes[closest[2]].name == nodes[second_closest[2]].name:
								alr = True
							#if there are no dupes
							if not alr:
								#if dijkstras is not selected
								if not dijkstras:
									#if it isnt weighted (it isnt atm but for future development)
									if not weighted:
										nodes[closest[2]].neighbours.append([nodes[second_closest[2]].name,1])
										alr = False
										for i in nodes:
											if current_string == i.name:
												alr = True

										if not alr:

											conn = sqlite3.connect('Resources/SaveData/SaveData.db')
											curs = conn.cursor()
											#get the informaion from the graph urrently working on
											curs.execute(f"SELECT * FROM Graph_info WHERE Account_id={current_account_id} AND Folder_id={current_folder_id} AND Graph_id={current_graph_id}")
											check = curs.fetchall()

											check = check[0]
											#updates the database
											curs.execute(f"""UPDATE Graph_info SET 
												Name = :Name,
												Weighted = :Weighted,
												Directed = :Directed,
												Graph = :Graph,
												List = :List,
												Account_id = :Account_id,
												Folder_id = :Folder_id,
												Graph_id = :Graph_id

												WHERE Account_id = {current_account_id} AND Folder_id = {current_folder_id} AND Graph_id = {current_graph_id}
												""",
												{

												'Name':check[0],
												'Weighted':check[1],
												'Directed':check[2],
												'Graph':pickle.dumps(matrix),
												'List':pickle.dumps(nodes),
												'Account_id':check[5],
												'Folder_id':check[6],
												'Graph_id':check[7],


												})

		
												
											conn.commit()
											conn.close()
											current_string = ""

									else:
										#opens node menu
										node_menu = True
										current_string = ""

								else:
									#if dijkstras is active then it will run dijkstras algorithm
									dijkstras_nodes = dijkstras_algorithm(matrix,closest[2],second_closest[2])
						#highlights the 2nd closest node
						pygame.draw.circle(win,(0,255,0),(nodes[second_closest[2]].x,nodes[second_closest[2]].y),20)
						pygame.draw.circle(win,(0,0,0),(nodes[second_closest[2]].x,nodes[second_closest[2]].y),20,1)
						win.blit(small_font.render(nodes[second_closest[2]].name,0,(0,0,0)),(nodes[second_closest[2]].x-30,nodes[second_closest[2]].y-40))
				#if prims is active
				elif prims:
					#the first node is the closes node (base case)
					closest = [nodes[0].x,nodes[0].y,0]
					#itearets through all the nodes to see if any of them are closr
					for a,i in enumerate(nodes):
						if ((i.x-mousex)**2+(i.y-mousey)**2)**0.5 <= ((mousex-closest[0])**2+(mousey-closest[1])**2)**0.5:
							closest = [i.x,i.y,a]
					#highlights selected node
					pygame.draw.circle(win,(0,255,0),(nodes[closest[2]].x,nodes[closest[2]].y),20)
					pygame.draw.circle(win,(0,0,0),(nodes[closest[2]].x,nodes[closest[2]].y),20,1)
					win.blit(small_font.render(nodes[closest[2]].name,0,(0,0,0)),(nodes[closest[2]].x-30,nodes[closest[2]].y-40))
					#if the user clicks
					if pygame.mouse.get_pressed()[0]:
					#prims algorithm runs
						prims_nodes = prims_algorithm(highest_algorithm(matrix),matrix,nodes[closest[2]],nodes)
						#initially shows the user how prims algorithm actually work
						#it cycles though the node and 1 by one displys them in the order that they were added in
						for i in prims_nodes:
							for j in i.neighbours:
								for k in prims_nodes:
									if j[0] == k.name:
										pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)
										#the reason for this update is so that the user can actually see it in real time
										pygame.display.update()
										#that is also the same reason for this sleep which just pauses for 0.1 seconds
										time.sleep(0.1)
				#if kruskals is active
				elif kruskals:
					#kruskals algorithm runs
					kruskals_nodes = kruskals_algorithm(highest_algorithm(matrix),matrix,nodes)
					#cycles though all of the node
					for i in kruskals_nodes:
						for j in i.neighbours:
							for k in kruskals_nodes:
								if j[0] == k.name:
									#once again displays it in real time
									pygame.draw.line(win,(0,255,0),(i.x,i.y),(k.x,k.y),2)
									pygame.display.update()
									time.sleep(0.1)
				
								


			#otherwise the system is just rest
			else:
				first_node = True
				second_node = False



	#This checks every event currently happening in the window
	for event in pygame.event.get():
		#If the event is the big red X in the top corner being pressed or the ESCAPE key being pressed then it will close the program
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			#This just sets the variable which dictates the gameloop to false which means it will no longer run
			run = False
			#Checks to see if the user has typed anything
		if event.type == pygame.KEYDOWN:
			type(event,page)
		#checks to see if the page is canvas and the user has held down the button and the shift buttons havent been clicked
		if event.type == pygame.MOUSEBUTTONDOWN and page == "canvas" and not (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
			#acknowledges the user is holding
			hold = True
			#no nodes currently selected
			selected_nodes = []
			#all the nodes that are in the area of mouse click are put into the selected nodes array
			for a,i in enumerate(nodes):
				if i.x-20<mousex<i.x+20 and i.y-20<mousey<i.y+20:
					selected_nodes.append(a)
			
			try:
				#this cycles through all the values in the selected array and checks to see if there is anything lower.
				current_lowest = nodes[selected_nodes[0]].pos
				for i in selected_nodes:
					if nodes[i].pos <= current_lowest:
						#if it finds any lower then it will set that to the moving node
						moving_node = i
	
			except:
				#otherwise it will deselect
				hold = False


		#if the user doesnt drag then they are not holding
		if event.type == pygame.MOUSEBUTTONUP:
			hold = False
	#if they are holding then it changes the x and y corrds of thhe moving node to whatever the mouse x and y is
	if hold:
		if mousex <= 950 and mousex >= 0:
			nodes[moving_node].x = mousex
		if mousey >=100 and mousey <=720:
			nodes[moving_node].y = mousey



	#This updates any changes going on w the screen
	pygame.display.update()
