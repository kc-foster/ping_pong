#! python3

import pygame, time, pongball, pongpaddle

#MACROS
WIDTH = 1200
HEIGHT = 800
LEVEL_DELAY = 20000	# 20 seconds
BLACK = (0, 0, 0)
NEWSCOREDIGITS = [100, 10]

# INIT
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])

ball = pongball.Ball()
player_1 = pongpaddle.Paddle(1)
player_2 = pongpaddle.Paddle(2)
# 1000 (1s) / 60 ticks = 16 ms per paddle command to allow paddle_ricochet() to register with key presses
pygame.key.set_repeat(16)

# INIT SCOREBOARD
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
number_surfaces = {0: "zero_surface", 1: "one_surface", 2: "two_surface", 3: "three_surface", 4: "four_surface", 5: "five_surface", 6: "six_surface", 7: "seven_surface", 8: "eight_surface", 9: "nine_surface"}
number_files = {0: "num0.xcf", 1: "num1.xcf", 2: "num2.xcf", 3: "num3.xcf", 4: "num4.xcf", 5: "num5.xcf", 6: "num6.xcf", 7: "num7.xcf", 8: "num8.xcf", 9: "num9.xcf"}
for nums in numbers:
	number_surfaces[nums] = pygame.image.load(number_files[nums]).convert()

player_1.score = 0
player_2.score = 0
done = False
while not done:
	# clock stuff
	clock.tick(60)

	# move the ball to pos
	ball.move()

	# key press detection
	event = pygame.key.get_pressed()			# FIFO
	# if either p1 or p2 hit p or close window, these happen
	if event[pygame.K_q]:
		done = True
	# if first queue, reset paddle keys, test for key presses, set triggers
	player_1.paddle1_key_down = player_1.paddle1_key_up = 0
	if event[pygame.K_s]:
		player_1.paddle1_key_down = 1
		player_1.paddle1_key_up = 0
	elif event[pygame.K_w]:
		player_1.paddle1_key_up = 1
		player_1.paddle1_key_down = 0
	player_2.paddle2_key_down = player_2.paddle2_key_up = 0
	if event[pygame.K_DOWN]:
		player_2.paddle2_key_down = 1
		player_2.paddle2_key_up = 0
	elif event[pygame.K_UP]:
		player_2.paddle2_key_up = 1
		player_2.paddle2_key_down = 0

	pygame.event.pump()
	player_1.paddle_move(player_1.paddle1_key_up, player_1.paddle1_key_down, "p1")
	player_2.paddle_move(player_2.paddle2_key_up, player_2.paddle2_key_down, "p2")

	# detect collision with top and bottom wall
	if ball.current_ball_pos[1] - 10 < 0 or ball.current_ball_pos[1] + 10 > HEIGHT:
		ball.wall_ricochet()

	# detect collision with paddle
	# and not ((ball.current_ball_pos[0] - 10) < (player_1.paddle1_pos[0]))
	# and not ((ball.current_ball_pos[0] + 10) > (player_2.paddle2_pos[0])) both before first and
	# 
	# for no lateral ricochet:
	# if the ball and paddle cross at x axis of either paddles' front x axis AND it is within the y axis of the top and bottom of the paddles', do a non-lateral ricochet.
	# so essentially if it hits the front part of the paddles', not within it or behind it.
	# for lateral ricochet: (if the ball hits the top or bottom of the paddles')
	# if within the paddles' x-axis zone, and contact is made with the paddle at the two different y-axis', do a lateral ricochet 

	# player_1
	if ((ball.current_ball_pos[0] - 10) < (player_1.paddle1_pos[0] + 10)) and not ((ball.current_ball_pos[0] + 10) < (player_1.paddle1_pos[0] + 9)) and ((ball.current_ball_pos[1] + 10) > (player_1.paddle1_pos[1] - 35)) and ((ball.current_ball_pos[1] - 10) < (player_1.paddle1_pos[1] + 35)):
		ball.paddle_ricochet("p1", player_1, 0)
	elif ((ball.current_ball_pos[0] - 10) < (player_1.paddle1_pos[0] + 10)) and ((ball.current_ball_pos[0] + 10) > (player_1.paddle1_pos[0] - 10)) and ((ball.current_ball_pos[1] + 10) > (player_1.paddle1_pos[1] - 35)) or \
		((ball.current_ball_pos[0] - 10) < (player_1.paddle1_pos[0] + 10)) and ((ball.current_ball_pos[0] + 10) > (player_1.paddle1_pos[0] - 10)) and ((ball.current_ball_pos[1] - 10) < (player_1.paddle1_pos[1] + 35)): # or ricochet off bottom
		ball.paddle_ricochet("p1", player_1, 1)

	# player_2
	if ((ball.current_ball_pos[0] + 10) > (player_2.paddle2_pos[0] - 10)) and not ((ball.current_ball_pos[0] - 10) > (player_2.paddle2_pos[0] - 9)) and ((ball.current_ball_pos[1] + 10) > (player_2.paddle2_pos[1] - 35)) and ((ball.current_ball_pos[1] - 10) < (player_2.paddle2_pos[1] + 35)):
		ball.paddle_ricochet("p2", player_2, 0)
	elif ((ball.current_ball_pos[0] + 10) > (player_2.paddle2_pos[0] - 10)) and ((ball.current_ball_pos[0] - 10) < (player_2.paddle2_pos[0] + 10)) and ((ball.current_ball_pos[1] + 10) > (player_2.paddle2_pos[1] - 35)) or \
		((ball.current_ball_pos[0] + 10) > (player_2.paddle2_pos[0] - 10)) and ((ball.current_ball_pos[0] - 10) < (player_2.paddle2_pos[0] + 10)) and ((ball.current_ball_pos[1] - 10) < (player_2.paddle2_pos[1] + 35)): # or ricochet off bottom
		ball.paddle_ricochet("p2", player_2, 1)

	# ball reset if score
	if (ball.current_ball_pos[0] + 10) > WIDTH:
		player_2.score += 1
		player_2.scoresave = player_2.score
		player_2.left_digit = player_2.scoresave // 100
		player_2.middle_digit = ((player_2.scoresave - (player_2.left_digit * 100)) // 10)
		player_2.right_digit = ((player_2.scoresave - (player_2.left_digit * 100)) % 10)
		ball = pongball.Ball()
	elif (ball.current_ball_pos[0] - 10) < 1:
		player_1.score += 1
		player_1.scoresave = player_1.score
		player_1.left_digit = player_1.scoresave // 100
		player_1.middle_digit = ((player_1.scoresave - (player_1.left_digit * 100)) // 10)
		player_1.right_digit = ((player_1.scoresave - (player_1.left_digit * 100)) % 10)
		ball = pongball.Ball()

	screen.fill(BLACK)
	# player 2 score
	screen.blit(number_surfaces[player_2.left_digit], [WIDTH / 2 - 170, 100])
	screen.blit(number_surfaces[player_2.middle_digit], [WIDTH / 2 - 135, 100])
	screen.blit(number_surfaces[player_2.right_digit], [WIDTH / 2 - 100, 100])
	# player 1 score
	screen.blit(number_surfaces[player_1.left_digit], [WIDTH / 2 + 100, 100])
	screen.blit(number_surfaces[player_1.middle_digit], [WIDTH / 2 + 135, 100])
	screen.blit(number_surfaces[player_1.right_digit], [WIDTH / 2 + 170, 100])
	# ball and paddle draw
	screen.blit(ball.ball_surface, ball.current_ball_pos)
	screen.blit(player_1.paddle_surface, player_1.paddle1_pos)
	screen.blit(player_2.paddle_surface, player_2.paddle2_pos)
	pygame.display.flip()


pygame.quit()


