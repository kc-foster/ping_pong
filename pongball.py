import pygame, pongpaddle
import random

class Ball():
	def __init__(self):
		self.ricochet_y_direction_p1 = self.ricochet_y_direction_p2 = 0
		self.last_hit = 2 												# player 2 hits first
		self.random_ball_vector_x = 1 									# start moving right
		self.random_ball_vector_y = random.uniform(-1, 1)
		self.current_ball_speed = random.uniform(3, 4)
		self.current_ball_direction = [self.random_ball_vector_x * self.current_ball_speed, self.random_ball_vector_y * self.current_ball_speed]
		self.ball_surface = pygame.image.load("white_ball.bmp").convert()
		self.current_ball_pos = [590, 390]
		self.ball_Rect = pygame.Rect([590, 390, 20, 20])

	def move(self):
		self.ball_Rect = self.ball_Rect.move(self.current_ball_direction)
		self.current_ball_pos = list(self.ball_Rect[:2])

	def paddle_ricochet(self, player, paddle, lateral):
		self.current_ball_direction[0] *= -1
		if player == "p1" and not lateral:
			self.last_hit = 1
			p1_key_up, p1_key_down = paddle.player1_keys()
			if p1_key_up == 1 and self.current_ball_direction[1] < 0: 	# moving up
				self.ricochet_y_direction_p1 = -1
			elif p1_key_down == 1 and self.current_ball_direction[1] > 0: 	# moving down
				self.ricochet_y_direction_p1 = 1 
			elif p1_key_up == 0 and self.ricochet_y_direction_p1 < 0:
				self.ricochet_y_direction_p1 = 0
			elif p1_key_down == 0 and self.ricochet_y_direction_p1 > 0:
				self.ricochet_y_direction_p1 = 0
		elif player == "p1" and lateral:
			self.last_hit = 1
			self.current_ball_direction[1] *= -1			# do a lateral ricochet
		elif player == "p2" and not lateral:
			self.last_hit = 2
			p2_key_up, p2_key_down = paddle.player2_keys()
			if p2_key_up == 1 and self.current_ball_direction[1] < 0:
				self.current_ball_direction[1] = -1
			elif p2_key_down == 1 and self.current_ball_direction[1] > 0:
				self.current_ball_direction[1] = 1
			elif p2_key_up == 0 and self.ricochet_y_direction_p2 < 0:
				self.ricochet_y_direction_p2 = 0 						# reset the paddle ricochet change to 0
			elif p2_key_down == 0 and self.ricochet_y_direction_p2 > 0:
				self.current_ball_direction[1] = 0
		elif player == "p2" and lateral:
			self.last_hit = 2
			self.current_ball_direction[1] *= -1
			
		if self.last_hit == 1:											# if player 1 hit last then change direction[1] by its ricochet_y_direction
			self.current_ball_direction[1] = self.current_ball_direction[1] + self.ricochet_y_direction_p1
		else:
			self.current_ball_direction[1] = self.current_ball_direction[1] + self.ricochet_y_direction_p2

	def wall_ricochet(self):
		self.current_ball_direction[1] *= -1
