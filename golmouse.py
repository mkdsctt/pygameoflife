#!/usr/bin/python
# third attempt at python implementation of conway's game of life
#
# a point should be given as (x,y) alternatively: (col,row)
# a point should be given as [row][col] for array

# gamefile format:
# width,height,size,numseed
# seed[0]
# ...
# seed[n-1]
import sys, pygame, math, random

from pygame.locals import *

def drawlines():
	vbars = numcols - 1
	hbars = numrows - 1
	#draw vbars
	for i in range(vbars):
		pygame.draw.line(screen,red,[(i+1)*size-1,0],[(i+1)*size-1,height])
	#draw hbars
	for i in range(hbars):
		pygame.draw.line(screen,red,[0,(i+1)*size-1],[width,(i+1)*size-1])

def clear():
	for i in range(numrows):
		for j in range(numcols):
			game[i][j] = 0

def count(i , j):
	count = 0
	if i > 0 and game[i-1][j] == 1:
		count += 1
	if j > 0 and game[i][j-1] == 1:
		count += 1
	if i < (numrows-1) and game[i+1][j] == 1:
		count += 1
	if j < (numcols-1) and game[i][j+1] == 1:
		count += 1
	if i > 0 and j > 0 and game[i-1][j-1] == 1:
		count += 1
	if i < (numrows-1) and j < (numcols-1) and game[i+1][j+1] == 1:
		count += 1
	if i > 0 and j < (numcols-1) and game[i-1][j+1] == 1:
		count += 1
	if i < (numrows-1) and j > 0 and game[i+1][j-1] == 1:
		count += 1
	return count

def printgame():
	for i in range(numrows):
		for j in range(numcols):
			sys.stdout.write(str(game[i][j]))
		sys.stdout.write('\n')

def playgame():
	newgame = []
	for i in range(numrows):
		for j in range(numcols):
			if game[i][j] == 1:
				if count(i,j) <= 1:
					newgame.append([i,j,0])
				elif count(i,j) > 3:
					newgame.append([i,j,0])
			elif game[i][j] == 0:
				if count(i,j) == 3:
					newgame.append([i,j,1])
	for change in newgame:
		game[int(change[0])][int(change[1])] = int(change[2])

def addnoise():
	for i in range(noiselevel):
		col = random.randint(0,int(numcols) - 1)
		row = random.randint(0,int(numrows) - 1)
		game[row][col] = 1 - game[row][col]

def writegame():
	seednum = 0
	for i in range(numrows):
		for j in range(numcols):
			if game[i][j] == 1:
				seednum += 1
	print str(width) + "," + str(height) + "," + str(size) + "," + str(seednum)
	newgame = []
	for i in range(numrows):
		for j in range(numcols):
			if game[i][j] == 1:
				newgame.append([i,j])
	for change in newgame:
		#game[int(change[0])][int(change[1])] = int(change[2])
		print str(change[0]) + "," + str(change[1])

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
	gamefile = open(sys.argv[1],'r')
	line = gamefile.readline().split(',')
	width, height = int(line[0]), int(line[1])
	size, numseed = int(line[2]), int(line[3])
	numrows, numcols = height/size, width/size
	interval = int(sys.argv[2])
	seeds_read = 0
	screen = pygame.display.set_mode([width,height])
	noiselevel = int((width*height)*0.001)

	#print "rows: " + str(numrows) + ",cols: " + str(numcols)

	if width % size != 0 or height % size != 0:
		sys.exit("error: size must evenly divide width and height")

	for i in range(numrows):
		game.append([])
		for j in range(numcols):
			game[i].append(0)

	#printgame()
	while seeds_read < numseed:
		line = gamefile.readline().split(',')
		#TODO CHANGE: see if this is where problem is with numbering
		game[int(line[0])][int(line[1])] = 1
		seeds_read += 1

	play = 0
	keepgoing = 1
	while keepgoing == 1:
		screen.fill(white)
		drawlines()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == K_ESCAPE:
					keepgoing = 0
					break
				elif event.key == K_SPACE:
					playgame()
				elif event.key == K_p:
					play = 1 - play
				elif event.key == K_EQUALS and interval > 60:
					interval -= 100
				elif event.key == K_MINUS and interval < 10000:
					interval += 100
				elif event.key == K_c:
					clear()
				elif event.key == K_n:
					addnoise()
				elif event.key == K_o:
					writegame()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					x, y = int(event.pos[0]), int(event.pos[1])
					col = int(math.floor((float(x)/width)*numcols))
					row = int(math.floor((float(y)/height)*numrows))
					game[row][col] = 1 - game[row][col]
		#draw game
		for i in range(numrows):
			for j in range(numcols):
				if(game[i][j] == 1):
					pygame.draw.rect(screen,black,pygame.Rect(j*size,i*size,size,size),0)
		#update screen
		pygame.display.flip()
		pygame.time.wait(41)
		if play == 1:
			playgame()
			pygame.time.wait(interval)
