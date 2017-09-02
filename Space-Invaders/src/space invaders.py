#!/usr/env python
import random, pygame, sys, os

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 780

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

def menu_start():
	if not os.path.exists("scores"):
		open("scores", "w+").write("0, 1")
	background = pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "menu_background.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
	while True:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if new_game_block_rect.collidepoint(pygame.mouse.get_pos()):
					game_start()
				elif exit_block_rect.collidepoint(pygame.mouse.get_pos()):
					sys.exit()

		screen.blit(background, (0, 0))

		new_game_block = pygame.font.SysFont("Arial", 60).render("New game", True, (255, 255, 255), (0, 0, 0))
		new_game_block_rect = new_game_block.get_rect().move(20, 20)
		screen.blit(new_game_block, new_game_block_rect)

		exit_block = pygame.font.SysFont("Arial", 60).render("Exit", True, (255, 255, 255), (0, 0, 0))
		exit_block_rect = exit_block.get_rect().move(20, 90)
		screen.blit(exit_block, exit_block_rect)

		file_data = open("scores", "r").read().split(", ")
		max_scores_block = pygame.font.SysFont("Arial", 60).render("Max score: "+file_data[0]+" Max level: "+file_data[1], True, (255, 255, 255), (0, 0, 0))
		max_scores_block_rect = max_scores_block.get_rect().move(20, 200)
		screen.blit(max_scores_block, max_scores_block_rect)

		pygame.display.update()
		pygame.display.set_caption("Ping Pong FPS: "+str(int(clock.get_fps())))
		clock.tick()

class Player:
	def __init__(self):
		self.img = pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "player.png")), (60, 30))
		self.rect = self.img.get_rect().move(SCREEN_WIDTH/2, SCREEN_HEIGHT-40)
		self.health = 3
		self.points = 0
		self.speed = 19
		self.bullet = None

	def render(self, screen):
		screen.blit(player.img, player.rect)

class Bullet:
	def __init__(self, x, y):
		self.rect = pygame.Rect((x, y, 7, 25))
		self.speed = -14
		self.sound_fire = pygame.mixer.Sound(os.path.join("data", "sounds", "fire.wav"))
		self.sound_fire.play(loops=0)

	def update(self):
		global player, ufo
		self.rect.y += self.speed
		if self.rect.y <= 0:
			player.bullet = None
		if ufo.is_alive() and self.rect.colliderect(pygame.Rect((ufo.x, ufo.y, 80, 40))):
			ufo.kill()
			player.bullet = None
			player.points += 2
		for y in range(len(enemy_group.matrix)):
			for x in range(len(enemy_group.matrix[y])):
				if enemy_group.matrix[y][x] is not None and self.rect.colliderect(pygame.Rect((enemy_group.x_start+x*60, enemy_group.y_start+y*60, 40, 40))):
					enemy_group.matrix[y][x] = None
					player.bullet = None
					if y == 0:
						player.points += 3
					elif y == 1 or y == 2:
						player.points += 2
					elif y == 3 or y == 4:
						player.points += 1

	def render(self, screen):
		pygame.draw.rect(screen, (0, 180, 0), self.rect)

class Enemy_Bullet(Bullet):
	def __init__(self, x, y, id):
		Bullet.__init__(self, x, y)
		self.speed = 6
		self.id = id

	def update(self):
		global player
		self.rect.y += self.speed
		if self.rect.y >= SCREEN_HEIGHT:
			enemy_group.bullets[self.id] = None
		if self.rect.colliderect(player.rect):
			player.health -= 1
			if player.health == 0:
				game_over()
			enemy_group.bullets[self.id] = None

class UFO:
	def __init__(self):
		self.img = pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy4.png")), (80, 40))
		self.alive = False
		self.x = 0; self.y = 0

	def is_alive(self):
		return self.alive

	def spawn(self):
		self.x = -80
		self.y = 0
		self.alive = True

	def kill(self):
		self.alive = False

	def update(self):
		global SCREEN_WIDTH
		if self.is_alive():
			self.x += 2
			if self.x == SCREEN_WIDTH:
				self.kill()

	def render(self, screen):
		screen.blit(self.img, pygame.Rect((self.x, self.y, 50, 50)))

class Block:
	def __init__(self):
		pass

class Enemy_Group:
	def __init__(self, x, y):
		self.img = [
			[pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy1_1.png")), (40, 40)),
			 pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy1_2.png")), (40, 40))],
			[pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy2_1.png")), (40, 40)),
			 pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy2_2.png")), (40, 40))],
			[pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy3_1.png")), (40, 40)),
			 pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "enemy3_2.png")), (40, 40))],
		]
		self.x_start = x
		self.y_start = y
		self.matrix = [
			[3 for i in range(11)],
			[2 for i in range(11)], [2 for i in range(11)],
			[1 for i in range(11)], [1 for i in range(11)],
		]
		self.state = False
		self.move_left = True
		self.bullets = []

	def update(self):
		if self.y_start+50*11 >= SCREEN_WIDTH:
			game_over()
			return
		need_next_level = True
		for y in self.matrix:
			for x in y:
				if x is not None:
					need_next_level = False
		if need_next_level:
			next_level()
		for i in range(11):
			if self.matrix[0][i] is not None:
				if random.random() <= 0.03:
					none_bull_flag = False
					for j in range(len(self.bullets)):
						if self.bullets[j] is None: 
							self.bullets[j] = Enemy_Bullet(self.x_start+i*60-25, self.y_start+40, j)
							none_bull_flag = True
					if not none_bull_flag:
						self.bullets.append(Enemy_Bullet(self.x_start+i*60-25, self.y_start+40, len(self.bullets)))
		if self.move_left:
			if self.x_start+11*60 < SCREEN_WIDTH:
				self.x_start += 15
			else:
				self.y_start += 15
				self.move_left = False
		else:
			if self.x_start > 0:
				self.x_start -= 15
			else:
				self.y_start += 15
				self.move_left = True
		self.state = not self.state

	def render(self, screen):
		for y in range(len(self.matrix)):
			for x in range(len(self.matrix[y])):
				if self.matrix[y][x] is not None:
					i = self.matrix[y][x]
					dx = self.x_start+x*60
					dy = self.y_start+y*60
					screen.blit(self.img[i-1][self.state], pygame.Rect((dx, dy, 50, 50)))

def game_over():
	global game_over_flag
	file_data = open("scores", "r").read().split(", ")
	file_new_data = []

	if player.points > int(file_data[0]):
		file_new_data.append(str(player.points))
	else:
		file_new_data.append(file_data[0])

	if level > int(file_data[1]):
		file_new_data.append(str(level))
	else:
		file_new_data.append(file_data[1])

	open("scores", "w").write(file_new_data[0]+", "+file_new_data[1])
	game_over_flag = True

def next_level():
	global level, enemy_group, player
	level += 1
	player.health += 1
	enemy_group = Enemy_Group(0, 0)
	need_next_level = False

def game_start():
	global player, enemy_group, game_over_flag, level, ufo
	gameLoop = True

	player = Player()
	enemy_group = Enemy_Group(0, 5)
	game_over_flag = False
	ufo = UFO()

	level = 1

	time_tick = 0

	background = pygame.transform.scale(pygame.image.load(os.path.join("data", "imgs", "game_background.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))

	while gameLoop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == pygame.KEYDOWN and not game_over_flag:
				if event.key == pygame.K_LEFT:
					if player.rect.x - 2 > 0: 
						player.rect.x -= player.speed
				elif event.key == pygame.K_RIGHT:
					if player.rect.x + 2 < SCREEN_WIDTH: 
						player.rect.x += player.speed
				elif event.key == pygame.K_SPACE:
					if player.bullet is None:
						player.bullet = Bullet(player.rect.center[0], player.rect.y)
			elif event.type == pygame.KEYDOWN and game_over_flag:
				if event.key == pygame.K_ESCAPE:
					gameLoop = False
					continue

		screen.blit(background, (0, 0))

		if player.bullet is not None:
			player.bullet.render(screen)
			player.bullet.update()

		player.render(screen)

		if time_tick >= 400/level:
			enemy_group.update()
			time_tick = 0

		enemy_group.render(screen)

		if ufo.is_alive():
			ufo.update()
			ufo.render(screen)
		else:
			if random.random() <= 0.001:
				ufo.spawn()

		for b in enemy_group.bullets:
			if b is not None:
				b.update()
				b.render(screen)

		score = pygame.font.SysFont("Arial", 40).render(str(player.points), True, (255, 255, 255), (0, 0, 0))
		screen.blit(score, score.get_rect().move(10, 5))

		hp = pygame.font.SysFont("Arial", 40).render(str(player.health), True, (255, 255, 255), (0, 0, 0))
		screen.blit(hp, hp.get_rect().move(SCREEN_WIDTH-30, 5))

		lvl = pygame.font.SysFont("Arial", 40).render(str(level), True, (255, 255, 255), (0, 0, 0))
		screen.blit(hp, hp.get_rect().move(SCREEN_WIDTH-30, 5))

		if game_over_flag:
			game_over_text = pygame.font.SysFont("Arial", 80).render("""Game Over (press ESC)""", True, (255, 255, 255), (0, 0, 0))
			screen.blit(game_over_text, game_over_text.get_rect().move(SCREEN_WIDTH/2-game_over_text.get_rect().width/2, SCREEN_HEIGHT/2-game_over_text.get_rect().height/2))

		pygame.display.set_caption("Space Invaders. FPS: "+str(int(clock.get_time())))
		pygame.display.update()
		clock.tick()
		time_tick += clock.get_time()

if __name__ == "__main__":
	menu_start()
