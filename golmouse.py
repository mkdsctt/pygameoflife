#!/usr/bin/python
# python implementation of conway's game of life
#
# a point should be given as (x,y) alternatively: (col,row)
# a point should be given as [row][col] for array
import sys, pygame, math, random

from pygame.locals import *

""" draw the cell grid """
def drawlines():
	#draw vbars -- use numcols - 1 since 4 cols are separated by 3 lines
	for i in range(numcols - 1):
		pygame.draw.line(screen,red,[(i+1)*size-1,0],[(i+1)*size-1,height])
		
	#draw hbars -- use numrows - 1 since 3 lines separate 4 rows
	for i in range(numrows - 1):
		pygame.draw.line(screen,red,[0,(i+1)*size-1],[width,(i+1)*size-1])

""" clear the game board of all live cells """
def clear():
	for i in range(numrows):
		# for each row
		for j in range(numcols):
			# for each colum
			game[i][j] = 0

""" determine whether a given cell location is valid and is inhabited"""
def alive(theGame, i, j):
	# check row validity
	if(i < 0 or i >= numrows):
		return 0
		
	# check col validity
	if(j < 0 or j >= numcols):
		return 0
	
	# if we are here the row, col is valid, return the value of the cell
	return theGame[i][j]

""" determine how many of the 8 neighbors of (i,j) are 'alive' """
def count(i , j):
	# the coordinates we should check
	coords = [ (i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1) ]
	
	count = 0
	for c in coords:
		if alive(game,c[0],c[1]):
			count += 1

	return count

""" print out the game , for internal use -- not for writing game file """
def printgame():
	for i in range(numrows):
		# loop over each row
		for j in range(numcols):
			# loop over each col
			# write out the cell status/value
			sys.stdout.write(str(game[i][j]))
		# add a newline at the end of a row
		sys.stdout.write('\n')
		
""" play one generation of the game """
def playgame():
	# track changes to make in next step, so that we dont interfere
	diff = []
	
	for i in range(numrows):
		# for each row
		for j in range(numcols):
			# for each col
			if alive(game,i,j):
				# if the cell is living, see if we need to kill it
				if count(i,j) <= 1:
					# if the cell is too low we die (str in numbers)
					diff.append([i,j,0])
				elif count(i,j) > 3:
					# if the count is too high the cell starves
					diff.append([i,j,0])
			else:
				# if a cell is unoccupied, see if we should fill it
				if count(i,j) == 3:
					# population conditions for spawning a new cell
					diff.append([i,j,1])
	# update the game to reflect our changes
	for change in diff:
		game[int(change[0])][int(change[1])] = int(change[2])

""" add noise randomly to the picture """
def addnoise():
	# noiselevel is the number of cells we should affect
	for i in range(noiselevel):
		# get a randomly chosen row, col
		col = random.randint(0,int(numcols) - 1)
		row = random.randint(0,int(numrows) - 1)
		
		# invert its live-ness
		invertCell(row,col)
		
""" get the population count -- the number of 'live' cells """
def population():
	count = 0
	for i in range(numrows):
		# for each row
		for j in range(numcols):
			# for each col
			if alive(game,i,j):
				# count the cell if it is alive
				count += 1
	return count

""" write out the game description to std out """
def writegame():
	print str(width) + "," + str(height) + "," + str(size) + "," + str(population())
	newgame = []
	for i in range(numrows):
		# for each row
		for j in range(numcols):
			# for each column in the row (i.e. for each cell)
			if alive(game,i,j):
				# if the cell is alive, record it
				newgame.append([i,j])
	for change in newgame:
		# for each live cell recorded
		# print out the coordinates to std out can be loaded later
		print str(change[0]) + "," + str(change[1])

""" initialize the game board to all empty cells """
def initGame(theGame):
	for i in range(numrows):
		# for each row we need
		# get an empty list for the cells
		theGame.append([])
		for j in range(numcols):
			# for each column we need append a zero (blank) to the row
			theGame[i].append(0)

""" load the game board from a game file """
def loadGame(theGame, theFile):
	global width
	global height
	global size
	global numseed
	global numrows
	global numcols
	global screen
	
	gamefile = open(theFile,'r')
	line = gamefile.readline().split(',')
	width, height = int(line[0]), int(line[1])
	size, numseed = int(line[2]), int(line[3])
	numrows, numcols = height/size, width/size
	screen = pygame.display.set_mode([width,height])
	initGame(theGame)
	
	seeds_read = 0
	while seeds_read < numseed:
		line = gamefile.readline().split(',')
		theGame[int(line[0])][int(line[1])] = 1
		seeds_read += 1
		
	updateDisplay(screen)

""" draw the game, draw each cell """
def drawGame():
	#draw game
	for i in range(numrows):
		# for each row
		for j in range(numcols):
			# for each col (i.e. for each cell)
			if alive(game,i,j):
				# if the cell is alive
				# fill in the cell location with a black rectangle
				pygame.draw.rect(screen,black,pygame.Rect(j*size,i*size,size,size),0)

""" get the row, col of the cell under the screen coords x, y """
def getCellCoords( x, y ):
	return y / size, x / size

""" invert the value of a cell -- keep track of last one inverted """
def invertCell( x, y):
	game[x][y] = 1 - game[x][y]

""" handle the keyboard / mouse events """
def handleEvents():
	global play 
	global keepgoing
	global interval

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == K_ESCAPE:
				keepgoing = 0
				break
			elif event.key == K_SPACE:
				# space - advance the simulation one step / generation
				playgame()
				updateDisplay(screen)
			elif event.key == K_p:
				# p - 'play' the game -- one generation per interval
				play = 1 - play
			elif event.key == K_EQUALS and interval > 60:
				# = - increase the play speed (by reducing interval)
				interval -= 100
			elif event.key == K_MINUS and interval < 10000:
				# - - decrease the play speed (by increasing interval)
				interval += 100
			elif event.key == K_c:
				# c - clear the game screen
				clear()
			elif event.key == K_n:
				# n - add noise to the grid
				addnoise()
			elif event.key == K_o:
				# w - write out game description to stdout
				writegame()
			elif event.key == K_r:
				# r - reload the game from file
				clear()
				loadGame(game,sys.argv[1])
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				# toggle cells on left mouse button click
				target = getCellCoords(int(event.pos[0]),int(event.pos[1]))
				invertCell(target[0],target[1])
		elif event.type == pygame.MOUSEMOTION:
			if pygame.mouse.get_pressed()[0]:
				# if we have a LMB press, enable cells
				target = getCellCoords(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
				game[target[0]][target[1]] = 1
			elif pygame.mouse.get_pressed()[2]:
				# if we have a RMB press, disable cells
				target = getCellCoords(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
				game[target[0]][target[1]] = 0

def updateDisplay(screen):
	# update the display
	screen.fill(white)
	drawlines()
	drawGame()
	pygame.display.flip()

""" main method """
if __name__ == "__main__":
	if len(sys.argv) != 3:
		sys.exit("usage: " + sys.argv[0] + " gamefile interval")

	pygame.init()

	#define colors
	white = 	255,	255,	255
	red =		255,	0,		0
	green =		0,		255,	0
	blue =		0,		0,		255
	black = 	0,		0,		0

	game = []
	numrows, numcols = 0, 0
	
	loadGame(game,sys.argv[1])	
	interval = int(sys.argv[2])
	
	noiselevel = int((width*height)*0.001)
	
	if width % size != 0 or height % size != 0:
		sys.exit("error: size must evenly divide width and height")
	
	play = 0
	keepgoing = 1
	while keepgoing:
		handleEvents()
		
		# if we are playing, step one generation
		if play:
			# update a generation
			playgame()
			updateDisplay(screen)
			
		pygame.time.wait(interval)
		
