#!/usr/env python
import random, pygame, sys, time

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Slot Machine")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)

def draw_num(font, x, y, val):
	num_font = pygame.font.SysFont("Arial", font)
	num = num_font.render(str(val), True, RED, BLACK)
	screen.blit(num, num.get_rect().move(x, y))
	return num.get_rect().move(x, y)

menuLoop = True

while menuLoop:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if start_game_rect.collidepoint(pygame.mouse.get_pos()):
				menuLoop = False
			elif exit_game_rect.collidepoint(pygame.mouse.get_pos()):
				sys.exit()

	screen.fill(WHITE)

	start_game_rect = draw_num(80, 40, 40, "Start game")
	exit_game_rect = draw_num(80, 40, 150, "Exit game")

	pygame.display.update()

value = [0, 0, 0]
money = 1000
bet = 0
game_played = 0
mixing = False

start_mixing = 0
last_mix = 0

mixing_val = [False, False, False]

def go_mixing():
	global mixing, money, start_mixing, last_mix, mixing_val
	mixing = True
	money -= bet
	start_mixing = time.time()
	last_mix = time.time()
	mixing_val = [True, True, True]

def mix():
	global value, game_played, money
	game_played += 1
	if value[0] == value[1] and value[1] == value[2]:
		money += bet*10
	elif value[0] == value[1] or value[1] == value[2]:
		money += bet*2

while True:
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and not mixing:
				go_mixing()
			elif event.key == pygame.K_KP_PLUS:
				if money > bet:
					bet += 10
			elif event.key == pygame.K_KP_MINUS:
				if bet > 0:
					bet -= 10
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if plus_bet_rect.collidepoint(pygame.mouse.get_pos()):
				if money > bet:
					bet += 10
			elif minus_bet_rect.collidepoint(pygame.mouse.get_pos()):
				if bet > 0:
					bet -= 10
			elif pygame.Rect((700, 10, 30, 200)).collidepoint(pygame.mouse.get_pos()) and not mixing:
				if money < bet:
					bet = money
				go_mixing()

	screen.fill(WHITE)

	if mixing and time.time()-last_mix >= 0.003:
		if time.time()-start_mixing >= random.random()*3:
			if mixing_val[0]:
				mixing_val[0] = False
			elif mixing_val[1]:
				mixing_val[1] = False
			elif mixing_val[2]:
				mixing_val[2] = False
			else:
				mixing = False
				mix()
		else:
			for i in range(3):
				if mixing_val[i]:
					if value[i] == 9:
						value[i] = 0
					else:
						value[i] += 1
			if not mixing:
				last_mix = time.time()

	draw_num(320, 30,  10, value[0])
	draw_num(320, 250, 10, value[1])
	draw_num(320, 470, 10, value[2])

	draw_num(85, 130,      380, int(money/10000))
	draw_num(85, 130+55,   380, int((money-int(money/10000)*10000)/1000))
	draw_num(85, 130+55*2, 380, int((money-int(money/1000)*1000)/100))
	draw_num(85, 130+55*3, 380, int((money-int(money/100)*100)/10))
	draw_num(85, 130+55*4, 380, money-int(money/10)*10)
	draw_num(29,  30,       380, "Money:")

	draw_num(85, 130,      480, int(bet/10000))
	draw_num(85, 130+55,   480, int((bet-int(bet/10000)*10000)/1000))
	draw_num(85, 130+55*2, 480, int((bet-int(bet/1000)*1000)/100))
	draw_num(85, 130+55*3, 480, int((bet-int(bet/100)*100)/10))
	draw_num(85, 130+55*4, 480, bet-int(bet/10)*10)
	draw_num(29,  30,       480, "Bet:")

	plus_bet_rect  = draw_num(30, 130+55*5, 480, " + ")
	minus_bet_rect = draw_num(30, 130+55*5, 520, " - ")	

	draw_num(115, 570, 425, int(game_played/10))
	draw_num(115, 650, 425, game_played-int(game_played/10)*10)
	draw_num(35,  540, 380, "Game played:")

	if mixing:
		pygame.draw.rect(screen, BLACK, pygame.Rect((700, 160, 30, 200)))
	else:
		pygame.draw.rect(screen, BLACK, pygame.Rect((700, 10, 30, 200)))

	pygame.display.update()
