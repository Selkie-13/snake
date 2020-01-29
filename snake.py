# -*- coding:Utf-8 -*-
import pygame
import sqlite3
import random

class Option:
	hovered = False
	selected = False
	def __init__(self, text, pos):
		self.text = text
		self.pos = pos
		self.set_rect()
		self.draw()
	def draw(self):
		self.set_rend()
		gameDisplay.blit(self.rend, self.rect)
	def set_rend(self):
		self.rend = menu_font.render(self.text, True, self.get_color())
	def get_color(self):
		if self.selected:
			return (255,255,255)
		if self.hovered:
			return (255, 255, 255)
		else:
			return (100, 100, 100)
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos

def optionDraw(options):
	for option in options:
			if option.rect.collidepoint(pygame.mouse.get_pos()):
				option.hovered = True
			else :
				option.hovered = False
			option.draw()

def settings(settingsValue):
	gameDisplay = pygame.display.set_mode((400,400))
	menu_font = pygame.font.SysFont("None",40)
	color_inactive = pygame.Color(150,150,150)
	color_active = pygame.Color(250,250,250)
	options = [Option(" Main Menu -",(170,300))]
	speed = [Option("x0.5",(175,100)),Option("x1",(250,100)),Option("x2",(300,100))]
	dim = [Option("20x20",(145,200)),Option("30x30",(230,200)),Option("40x40",(320,200))]	
	speedOption = [0.5,1,2]
	dimOption = [2,3,4]  
	while True:
		gameDisplay.fill((200,200,200))
		optionDraw(options)
		optionDraw(speed)
		optionDraw(dim)
		event = pygame.event.poll()

		speed[speedOption.index(settingsValue[0])].selected = True
		for i in speed[:speedOption.index(settingsValue[0])]+speed[speedOption.index(settingsValue[0])+1:]:
			i.selected=False

		dim[dimOption.index(settingsValue[1])].selected = True
		for i in dim[:dimOption.index(settingsValue[1])]+dim[dimOption.index(settingsValue[1])+1:]:
			i.selected=False

		if event.type == pygame.MOUSEBUTTONUP :
			if options[0].rect.collidepoint(event.pos):
				break
			for i in speed:
				if i.rect.collidepoint(event.pos):
					settingsValue[0] = speedOption[speed.index(i)]
			for i in dim:
				if i.rect.collidepoint(event.pos):
					settingsValue[1] = dimOption[dim.index(i)]
		gameDisplay.blit(menu_font.render("Speed : ",30,(100,100,100)), (50,100))
		gameDisplay.blit(menu_font.render("Dims : ",30,(100,100,100)), (50,200))
		pygame.display.flip()
		continue
	return(settingsValue)

def game(settingsValue):
	cp = 0
	x,y = settingsValue[1]*10,settingsValue[1]*10
	one=20
	gameDisplay = pygame.display.set_mode((x*one, y*one))
	snake = [(0,0),(0,1),(0,2)]
	head = snake[-1]
	apple = (10,10)
	direction = (0,1)
	score = 0
	speed = int(round(100/float(settingsValue[0])))
	while 0<=head[0]<x and 0<=head[1]<x and snake.count(head)&1:
		for ev in pygame.event.get(pygame.KEYDOWN):
			if ev.key == pygame.K_LEFT: direction = (-1,0)
			elif ev.key == pygame.K_RIGHT: direction = (1,0)
			elif ev.key == pygame.K_UP: direction = (0,-1)
			elif ev.key == pygame.K_DOWN: direction = (0,1)
		if head == apple :
			cp = cp + 1
			queu = 0
		else :
			queu = 1
		snake = snake[queu:]+[(head[0]+direction[0],head[1]+direction[1])]
		gameDisplay.fill(0)
		for i in snake+[apple]:
			gameDisplay.fill((0,255,0),(i[0]*one,i[1]*one,one,one))
		pygame.display.flip()
		if head == apple: 
			apple = snake[0]
		head = snake[-1]
		pygame.event.clear()
		pygame.time.wait(speed)
	return cp

def scores(score):
	gameDisplay = pygame.display.set_mode((400,400))
	myfont = pygame.font.SysFont("None",20)
	userfont = pygame.font.SysFont("monospace",20)
	options = [Option("- Save ",(55,300)),Option(" Main Menu -",(170,300))]
	color_inactive = pygame.Color(150,150,150)
	color_active = pygame.Color(250,250,250)
	color = color_inactive
	active = False
	text = ""
	input_box = pygame.Rect(70,50,120,25)
	while True:
		gameDisplay.fill(0)
		label = myfont.render("Your score : "+str(score),30,(200,200,200))
		gameDisplay.blit(label, (80,20))
		optionDraw(options)
		event = pygame.event.poll()
		if event.type == pygame.MOUSEBUTTONUP :
			if options[0].rect.collidepoint(event.pos) and len(text)>1:
				c.execute("INSERT INTO snake VALUES ('"+text+"', "+str(score)+")")
				connection.commit()
			if options[1].rect.collidepoint(event.pos):
				break
			if input_box.collidepoint(event.pos):
				active = not active
			else :
				active = False
			color = color_active if active else color_inactive
		if event.type == pygame.KEYDOWN:
			if active:
				if event.key == pygame.K_RETURN:
					text = ''
				elif event.key == pygame.K_BACKSPACE:
					text = text[:-1]
				else:
					text += event.unicode
		res = c.execute("SELECT * FROM snake ORDER BY Score DESC LIMIT 10").fetchall()
		tableStr = ""
		x,y = input_box.bottomleft
		for row in res:
			txt = str(row[0])+" -> "+str(row[1])
			x,y=gameDisplay.blit(userfont.render(txt,1,pygame.Color(250,250,250)),(x,y)).bottomleft
		txt = userfont.render(text, True, color)
		gameDisplay.blit(txt,(input_box.x+5,input_box.y+3))
		pygame.draw.rect(gameDisplay, color, input_box, 2)
		pygame.display.flip()

if __name__ == '__main__':
	pygame.init()
	connection = sqlite3.connect("snake.db")
	c = connection.cursor()	
	gameDisplay = pygame.display.set_mode((400,400))
	pygame.display.set_caption('Snake')
	menu_font = pygame.font.Font(None, 40)
	options = [Option("NEW GAME", (115, 105)),Option("OPTIONS", (130, 155)), Option("QUIT",(155,205))]
	running = True
	settingsValue = [1,2,1]
	while running:
		gameDisplay.fill((200,200,200))
		optionDraw(options)
		pygame.display.update()
		event = pygame.event.poll()
		if event.type == pygame.QUIT :
			running = False
		elif event.type == pygame.MOUSEBUTTONUP :
			if options[0].rect.collidepoint(event.pos):
				score = game(settingsValue)
				pygame.display.update()
				scores(score)
			if options[1].rect.collidepoint(event.pos):
				settingsValue = settings(settingsValue)
			if options[2].rect.collidepoint(event.pos):
				running = False

