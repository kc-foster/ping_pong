import pygame
import time

class Paddle():
	def __init__(self, player_num):
		self.paddle_surface = pygame.image.load("paddles.bmp").convert()
		self.score = 0
		self.scoresave = 0
		self.left_digit = 0
		self.middle_digit = 0
		self.right_digit = 0
		if player_num == 1:
			self.paddle1_Rect = pygame.Rect([100, 400, 20, 70])
			self.paddle1_pos = list(self.paddle1_Rect[0:2])
			self.paddle1_key_up = 0
			self.paddle1_key_down = 0

		if player_num == 2:
			self.paddle2_Rect = pygame.Rect([1100, 400, 20, 70])
			self.paddle2_pos = list(self.paddle2_Rect[0:2])
			self.paddle2_key_up = 0
			self.paddle2_key_down = 0

	def paddle_move(self, up, down, player):
		if player == "p1" and up:
			self.paddle1_pos[1] += -5
			self.paddle1_Rect = self.paddle1_Rect.move([0, self.paddle1_pos[1]])
		elif player == "p1" and down:
			self.paddle1_pos[1] += 5
			self.paddle1_Rect = self.paddle1_Rect.move([0, self.paddle1_pos[1]])
		if player == "p2" and up:
			self.paddle2_pos[1] += -5
			self.paddle2_Rect = self.paddle2_Rect.move([0, self.paddle2_pos[1]])
		elif player == "p2" and down:
			self.paddle2_pos[1] += 5
			self.paddle2_Rect = self.paddle2_Rect.move([0, self.paddle2_pos[1]])


	def player1_keys(self):
		return self.paddle1_key_up, self.paddle1_key_down

	def player2_keys(self):
		return self.paddle2_key_up, self.paddle2_key_down
