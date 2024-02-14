import tkinter as tk
import time
from Particle import *

BOARD_SIZE_X = 100
BOARD_SIZE_Y = 50
PARTICLE_SIZE = 10
particles_board = [[None for _ in range(BOARD_SIZE_X)] for _ in range(BOARD_SIZE_Y)]

def compute_first_line_intersection(start_x, start_y, end_x, end_y):
	if end_y == start_y and end_x == start_x:
		return [start_x, start_y]
	elif start_x == end_x:
		if start_y > end_y:
			y_mod = -1
			start = end_y
			end = start_y
		else:
			y_mod = 1
			start = start_y+1
			end = end_y+1

		for y in range(start, end)[::y_mod]: 
			if particles_board[y][start_x] is not None:
				return [start_x, y - y_mod]
	elif start_y == end_y:
		if start_x > end_x:
			x_mod = -1
			start = end_x
			end = start_x
		else:
			x_mod = 1
			start = start_x+1
			end = end_x+1
		for x in range(start, end)[::x_mod]: 
			if particles_board[start_y][x] is not None:
				return [x - x_mod, start_y]
	elif abs(end_y - start_y) < abs(end_x - start_x):
		m_new = 2 * (end_y - start_y) 
		slope_error_new = m_new - (end_x - start_x) 
		x_prev = start_x
		y_prev = start_y

		if start_x > end_x:
			x_mod = -1
			start = end_x
			end = start_x
		else:
			x_mod = 1
			start = start_x+1
			end = end_x+1

		y = start_y 
		for x in range(start, end)[::x_mod]: 
			if particles_board[y][x] is not None:
				return [x_prev, y_prev]
			x_prev = x
			y_prev = y

			slope_error_new += m_new
			if (slope_error_new >= 0): 
				y = y+1
				slope_error_new -= 2 * (end_x - start_x)
		if particles_board[end_y][end_x] is not None:
			return [x_prev, y_prev]
	else:
		m_new = 2 * (end_x - start_x) 
		slope_error_new = m_new - (end_y - start_y) 
		x_prev = start_x
		y_prev = start_y

		if start_y > end_y:
			y_mod = -1
			start = end_y
			end = start_y
		else:
			y_mod = 1
			start = start_y+1
			end = end_y+1

		x = start_x 
		for y in range(start, end)[::y_mod]: 
			if particles_board[y][x] is not None:
				return [x_prev, y_prev]
			x_prev = x
			y_prev = y

			slope_error_new += m_new
			if (slope_error_new >= 0): 
				x = x+1
				slope_error_new -= 2 * (end_y - start_y)
		if particles_board[end_y][end_x] is not None:
			return [x_prev, y_prev]
	return [end_x, end_y]

def swap_parts(x0, y0, x1, y1):
	tmp = particles_board[y0][x0]
	particles_board[y0][x0] = particles_board[y1][x1]
	particles_board[y1][x1] = tmp

	if particles_board[y0][x0] is not None:
		particles_board[y0][x0].moveTo([x0, y0])
	if particles_board[y1][x1] is not None:
		particles_board[y1][x1].moveTo([x1, y1])

def fill_adj_space(particle):
	# Down
	if particles_board[particle.getYCoor()+1][particle.getXCoor()] is None or particles_board[particle.getYCoor()+1][particle.getXCoor()].getDensity() < particle.getDensity():
		swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor(), particle.getYCoor()+1)
		return
	elif particles_board[particle.getYCoor()+1][particle.getXCoor()-1] is None or particles_board[particle.getYCoor()+1][particle.getXCoor()-1].getDensity() < particle.getDensity():
		swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()-1, particle.getYCoor()+1)
		return
	elif particles_board[particle.getYCoor()+1][particle.getXCoor()+1] is None or particles_board[particle.getYCoor()+1][particle.getXCoor()+1].getDensity() < particle.getDensity():
		swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()+1, particle.getYCoor()+1)
		return
	
	# Side
	if particle.getState() == 0 or particle.getState() == 1:
		if particles_board[particle.getYCoor()][particle.getXCoor()-1] is None:
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()-1, particle.getYCoor())
			return
		elif particles_board[particle.getYCoor()][particle.getXCoor()+1] is None:
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()+1, particle.getYCoor())
			return
		elif (particles_board[particle.getYCoor()-1][particle.getXCoor()+1] is not None 
		and particles_board[particle.getYCoor()][particle.getXCoor()-1] is not None 
		and particles_board[particle.getYCoor()-1][particle.getXCoor()+1].getState() is not None
		and particles_board[particle.getYCoor()][particle.getXCoor()-1].getState() is not None
		and particles_board[particle.getYCoor()-1][particle.getXCoor()+1].getDensity() > particles_board[particle.getYCoor()][particle.getXCoor()-1].getDensity()):
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()-1, particle.getYCoor())
			return
		elif (particles_board[particle.getYCoor()-1][particle.getXCoor()-1] is not None 
		and particles_board[particle.getYCoor()][particle.getXCoor()+1] is not None 
		and particles_board[particle.getYCoor()-1][particle.getXCoor()-1].getState() is not None
		and particles_board[particle.getYCoor()][particle.getXCoor()+1].getState() is not None
		and particles_board[particle.getYCoor()-1][particle.getXCoor()-1].getDensity() > particles_board[particle.getYCoor()][particle.getXCoor()+1].getDensity()):
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()+1, particle.getYCoor())
			return
	
	# Up
	if particle.getState() == 0:
		if particles_board[particle.getYCoor()-1][particle.getXCoor()] is None or (
			particles_board[particle.getYCoor()-1][particle.getXCoor()].getState() is not None
			and particles_board[particle.getYCoor()-1][particle.getXCoor()].getDensity() > particle.getDensity()):
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor(), particle.getYCoor()-1)
			return
		elif particles_board[particle.getYCoor()-1][particle.getXCoor()-1] is None or (
			particles_board[particle.getYCoor()-1][particle.getXCoor()-1].getState() is not None
			and particles_board[particle.getYCoor()-1][particle.getXCoor()-1].getDensity() > particle.getDensity()):
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()-1, particle.getYCoor()-1)
			return
		elif particles_board[particle.getYCoor()-1][particle.getXCoor()+1] is None or (
			particles_board[particle.getYCoor()-1][particle.getXCoor()+1].getState() is not None
			and particles_board[particle.getYCoor()-1][particle.getXCoor()+1].getDensity() > particle.getDensity()):
			swap_parts(particle.getXCoor(), particle.getYCoor(), particle.getXCoor()+1, particle.getYCoor()-1)
			return

def move_particle(particle):
	new_coors = compute_first_line_intersection(particle.getXCoor(), particle.getYCoor(), particle.getNextXCoor(), particle.getNextYCoor())
	if new_coors[0] == 0 or new_coors[0] == BOARD_SIZE_X-1 or new_coors[1] == 0 or new_coors[1] == BOARD_SIZE_Y-1:
		print(particle.getXCoor(), particle.getYCoor(), particle.getNextXCoor(), particle.getNextYCoor(), new_coors[0], new_coors[1])
		print("Error 1")
		exit(1)
	
	particle.resetPrevCoors()
	particles_board[particle.getYCoor()][particle.getXCoor()] = None
	particle.moveTo(new_coors)
	particles_board[particle.getYCoor()][particle.getXCoor()] = particle

	fill_adj_space(particle)
	if particle.getXCoor() == 0 or particle.getXCoor() == BOARD_SIZE_X-1 or particle.getYCoor() == 0 or particle.getYCoor() == BOARD_SIZE_Y-1:
		print(new_coors[0], new_coors[1], particle.getXCoor(), particle.getYCoor())
		print("Error 2")
		exit(1)

def compute_frame():
	for particle in Particle.all[::-1]:
		if particles_board[particle.y+1][particle.x] is None or not (particle.prev_x == particle.x and particle.prev_y == particle.y
			and particles_board[particle.y+1][particle.x].prev_x == particles_board[particle.y+1][particle.x].x
			and particles_board[particle.y+1][particle.x].prev_y == particles_board[particle.y+1][particle.x].y
			and type(particles_board[particle.y+1][particle.x]) == type(particle)
			and type(particles_board[particle.y][particle.x+1]) == type(particle)
			and type(particles_board[particle.y][particle.x-1]) == type(particle)
			and type(particles_board[particle.y-1][particle.x]) == type(particle)):
			move_particle(particle)

def draw_frame(canvas):
	canvas.delete("all")
	for particle in Particle.all:
		canvas.create_rectangle(
			particle.getXCoor() * PARTICLE_SIZE, particle.getYCoor() * PARTICLE_SIZE, 
			(particle.getXCoor() + 1) * PARTICLE_SIZE, (particle.getYCoor() + 1) * PARTICLE_SIZE,
			fill = particle.getColour(), outline = ""
		)
	for particle in Border.all:
		canvas.create_rectangle(
			particle.getXCoor() * PARTICLE_SIZE, particle.getYCoor() * PARTICLE_SIZE, 
			(particle.getXCoor() + 1) * PARTICLE_SIZE, (particle.getYCoor() + 1) * PARTICLE_SIZE,
			fill = particle.getColour(), outline = ""
		)
	canvas.pack(fill = tk.BOTH, expand = 1)

def main():
	window = tk.Tk()
	window.geometry(f"{BOARD_SIZE_X*PARTICLE_SIZE}x{BOARD_SIZE_Y*PARTICLE_SIZE + 20}")
	canvas = tk.Canvas(window)
	
	for i in range(BOARD_SIZE_X):
		particles_board[0][i] = Border(i, 0)
		particles_board[BOARD_SIZE_Y - 1][i] = Border(i, BOARD_SIZE_Y - 1)
	
	for i in range(1, BOARD_SIZE_Y - 1):
		particles_board[i][0] = Border(0, i)
		particles_board[i][BOARD_SIZE_X - 1] = Border(BOARD_SIZE_X - 1, i)

	while True:
		if particles_board[5][int(BOARD_SIZE_X/2)+10] is None:
			particles_board[5][int(BOARD_SIZE_X/2)+10] = Sand(int(BOARD_SIZE_X/2)+10, 5)
		if particles_board[5][int(BOARD_SIZE_X/2)-10] is None:
			particles_board[5][int(BOARD_SIZE_X/2)-10] = Water(int(BOARD_SIZE_X/2)-10, 5)
		if particles_board[2][int(BOARD_SIZE_X/2)] is None:
			particles_board[2][int(BOARD_SIZE_X/2)] = Air(int(BOARD_SIZE_X/2), 2)
		if particles_board[2][10] is None:
			particles_board[2][10] = Mercury(10, 2)
		compute_frame()
		draw_frame(canvas)
		window.update()
	
if __name__ == "__main__":
	main()