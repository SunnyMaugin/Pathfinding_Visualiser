import time
import pygame
import math
from threading import Timer
from queue import PriorityQueue

WIDTH = 800                                                   # Eseciallly this is just setting up the display of our program such as demensions
WIN = pygame.display.set_mode((WIDTH, WIDTH))                 # and how big it will be
pygame.display.set_caption("A* Path Finding Algorithm                                      Made by: Sunny Maugin")

RED = (255, 0, 0)                                             # Making colour variables using RGB so we can use them later to use for the pathfinding and such
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:                                                  # Here I make a class so that we can set all our properties which we can use later
	def __init__(self, row, col, width, total_rows):         # and this creates also helps to set up the grid we want to use and how we can find each
		self.row = row                                       # node and know what colour it is supposed to be easily throughout our program
		self.col = col
		self.x = row * width                                 # NOTE: This section of code is so that later we can 'hey so if the node is white then we know
		self.y = col * width                                 # that we haven't visited this node and if it red then we have and we can move on or if its the
		self.color = WHITE                                   # orange node then its the start note and so on, this is like setting the rules
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows
                                                             # NOTE: Below here we are sort of making the rules not actually making them the colour
	def get_pos(self):                                       # With this function we get to find the current position by checking what row it is
		return self.row, self.col                            # on and then checking what colomn it is

	def is_closed(self):                                     # This function basically ticks off the nodes we already considered and looked at as RED
		return self.color == RED

	def is_open(self):                                       # This is to mark the nodes that are in the open set that we are currently checking as GREEN
		return self.color == GREEN

	def is_barrier(self):                                    # If the user highlights a block in BLACK then it means it is a barrier
		return self.color == BLACK

	def is_start(self):                                      # If the block is regognised as the start node then it will be ORANGE
		return self.color == ORANGE

	def is_end(self):                                        # End node set to PURPLE
		return self.color == TURQUOISE

	def reset(self):                                         # resets all nodes to white
		self.color = WHITE

	def make_start(self):                                    # NOTE: Here we now have to actually make all the rules and turn them into the actual colour then need to be
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):                                                                   # Actually drawing out our grid we want
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):                                                                    #This function is simply creating an outer barrier of the grid so every bloack of the edge is black
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):                                         # The H function is where we will do our first calculation and check roughly how far the node we are currently
	x1, y1 = p1                                        # are on is to the next node we are looking for which in this case is the end node
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):        # In this function we draw out the path after the algorithm to show the shortest path in PURPLE
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):                 # This function is the main algorithm that gets the g_score and f_score of each node and creates the open_set and finds the shortest path
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):                   # This functions decides how the grid should look and how big each square should be
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])                       # Here I am just creating a grid using [], width, amount of rows and coloumns
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):              # This function and the next one is actually drawing out the grid using pygame and drawing out the rows and columns
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):         # Here I m getting the current position of where our mouse just clicked in more detail we are taking
	gap = width // rows                        # whichever position we are in x and y and  dividing it by the width of each cube and in theory
	y, x = pos                                 # that should give us exactly where we are/clicked on, on the grid

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):                          # The main function that will trigger most events in our program
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:                                 # Here we are saying while 'run' is True then check if an event is happening
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:      # If the samll x button on the top right is clicked then quit the program
				run = False

			if pygame.mouse.get_pressed()[0]:                   # All events for when the left mouse button is clicked
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot                                # This just means that if the start and end node are not on the grid yet then make the
					start.make_start()                          # next two clicks on the grid the start and then the end node meaning the ORANGE and TURQUOISE blocks

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]:                 # All events for when the left mouse button is clicked
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None                                # This is the same as the other mouse button just adjusting and making sure the start and end node are always there
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:                            # Here we check whether the key SPACE has been pressed and if it has then we can start the algorithm
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_r:                         # So that we can reset the grid using the key "r"
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

#def timer_display():
#    print(time.strftime('%M:%S'))

#class RepeatTimer(Timer):
#    def run(self):
#        while not self.finished.wait(self.interval):
#           self.function(*self.args,**self.kwargs)

#timer = RepeatTimer(1, timer_display)
#timer.start()
#time.sleep(10)
#time.cancel()

main(WIN, WIDTH)