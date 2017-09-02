#!/usr/env python
import pygame, sys, math, random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Player:
	def __init__(self, bot, x, y, State):
		self.State = State
		self.bot = bot
		self.rect = pygame.Rect((x, y, 10, 100))
		self.speed = 1
		self.direction = 0
		self.points = 0

	def update(self):
		global SCREEN_HEIGHT
		if self.bot:
			self.ai()
		if self.rect.y+self.rect.height+self.direction*self.speed < SCREEN_HEIGHT and self.rect.y+self.direction*self.speed > 0:
			self.rect = self.rect.move(0, self.direction*self.speed)

	def ai(self):
		if self.State.ball.rect.center[1] > self.rect.center[1]:
			self.direction = 1
		elif self.State.ball.rect.center[1] < self.rect.center[1]:
			self.direction = -1
		else:
			self.direction = 0

class Ball:
	def __init__(self, State):
		self.State = State
		self.rect = pygame.Rect((0, 0, 10, 10))
		self.speed = 2
		self.spawn()
	
	def update(self):
		global BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
		if self.rect.x >= SCREEN_WIDTH:
			self.State.player1.points += 1
			self.spawn()
		elif self.rect.x <= 0:
			self.State.player2.points += 1
			self.spawn()

		if self.rect.colliderect(self.State.player1):
			if self.direction >= 180:
				self.direction = 180+(360-self.direction)
			else:
				self.direction = 180-self.direction
			self.rect.x -= 1
		elif self.rect.colliderect(self.State.player2):
			if self.direction >= 180:
				self.direction = 180+(360-self.direction)
			else:
				self.direction = 180-self.direction
			self.rect.x += 1
		elif self.rect.center[1] <= 0:
			self.direction = 360-self.direction
			self.rect.y += 1
		elif self.rect.center[1] >= SCREEN_HEIGHT:
			self.direction = 360-self.direction
			self.rect.y -= 1

		self.move_delta[0] += math.cos(math.radians(self.direction))*self.speed
		self.move_delta[1] += math.sin(math.radians(self.direction))*self.speed
		x = 0
		if math.fabs(int(self.move_delta[0])) >= 1:
			x = int(self.move_delta[0])
			self.move_delta[0] -= int(self.move_delta[0])
		y = 0
		if math.fabs(int(self.move_delta[1])) >= 1:
			y = int(self.move_delta[1])
			self.move_delta[1] -= int(self.move_delta[1])
		self.rect.center = (self.rect.center[0]+x, self.rect.center[1]+y)

	def spawn(self):
		global SCREEN_WIDTH, SCREEN_HEIGHT
		self.direction = random.randrange(359)
		self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
		self.move_delta = [0, 0]

class StateMachine:
	def __init__(self):
		global BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
		pygame.init()

		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.clock  = pygame.time.Clock()

		self.menu()

		self.player1 = Player(False, SCREEN_WIDTH-20, 10, self)
		self.player2 = Player(True, 10, 10, self)
		self.ball = Ball(self)
		
		self.game()

	def menu(self):
		global BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
		self.new_game_block 	 = pygame.font.SysFont("Arial", 58).render("New game", True, WHITE, BLACK)
		self.new_game_block_rect = self.new_game_block.get_rect().move(20, 20)

		self.exit_block 	 = pygame.font.SysFont("Arial", 58).render("Exit", True, WHITE, BLACK)
		self.exit_block_rect = self.exit_block.get_rect().move(20, 80)

		self.menuLoop = True
		while self.menuLoop:
			for event in pygame.event.get(): 
				self.menu_event_handler(event)
			self.menu_loop()

	def menu_event_handler(self, event):
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if self.new_game_block_rect.collidepoint(pygame.mouse.get_pos()):
				self.menuLoop = False
			elif self.exit_block_rect.collidepoint(pygame.mouse.get_pos()):
				sys.exit()

	def menu_loop(self):
		global BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen.fill(BLACK)

		self.screen.blit(self.new_game_block, self.new_game_block_rect)
		self.screen.blit(self.exit_block, self.exit_block_rect)

		pygame.display.update()
		pygame.display.set_caption("Ping Pong FPS: "+str(int(self.clock.get_fps())))
		self.clock.tick()

	def game(self):
		while True:
			for event in pygame.event.get():
				self.game_event_handler(event)
			self.game_loop()

	def game_event_handler(self, event):
		if event.type == pygame.QUIT: 
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.player1.direction = -1
			elif event.key == pygame.K_DOWN:
				self.player1.direction = 1
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				self.player1.direction = 0

	def game_loop(self):
		global BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen.fill(BLACK)

		pygame.draw.rect(self.screen, WHITE, pygame.Rect((SCREEN_WIDTH/2-10, 0, 10, SCREEN_HEIGHT)))

		# Display player1 points
		text = pygame.font.SysFont("Arial", 55).render(str(self.player1.points), True, WHITE, BLACK)
		self.screen.blit(text, text.get_rect().move(SCREEN_WIDTH/4-20, 10))

		# Display player2 points
		text = pygame.font.SysFont("Arial", 55).render(str(self.player2.points), True, WHITE, BLACK)
		self.screen.blit(text, text.get_rect().move(SCREEN_WIDTH-SCREEN_WIDTH/4-20, 10))

		self.player1.update()
		self.player2.update()
		self.ball.update()

		pygame.draw.rect(self.screen, WHITE, self.player1)
		pygame.draw.rect(self.screen, WHITE, self.player2)
		pygame.draw.rect(self.screen, WHITE, self.ball)

		pygame.display.update()
		pygame.display.set_caption("Ping Pong FPS: "+str(int(self.clock.get_fps())))
		self.clock.tick()

if __name__ == "__main__":
	State = StateMachine()
