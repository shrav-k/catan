import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import math
import random

WOOD = 0
GRAIN = 1
WOOL = 2
BRICK = 3
ORE = 4
DESERT = 5

class CatanException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(message)

def generate_resource_arr(size):
	total = []
	total.append(DESERT)
	for _ in range(4):
		total.append(WOOD)
		total.append(GRAIN)
		total.append(WOOL)
	for _ in range(3):
		total.append(BRICK)
		total.append(ORE)
	random.shuffle(total)

	stop = (size + 1) // 2
	resources = []
	for i in range(stop, size + 1):
		row = []
		for j in range(i):
			row.append(total.pop())
		resources.append(row)
	for i in range(size - 1, stop - 1, -1):
		row = []
		for j in range(i):
			row.append(total.pop())
		resources.append(row)
	return resources

def generate_dice_arr(resources):
	total = []
	total.append(2)
	total.append(12)
	for _ in range(2):
		for i in range(3, 7):
			total.append(i)
		for i in range(8, 12):
			total.append(i)
	random.shuffle(total)

	dice = []
	for i in range(len(resources)):
		row = []
		for j in range(len(resources[i])):
			if resources[i][j] == DESERT:
				row.append(-1)
			else:
				row.append(total.pop())
		dice.append(row)
	return dice

def generate_board(size = 5):
	if size % 2 == 0:
		raise CatanException("Illegal board size")
	resources = generate_resource_arr(size)
	dice = generate_dice_arr(resources)
	draw_board(resources, dice)

#Drawing

hexVertices = [[0, 0], 
		[math.sqrt(3) / 2, 0.5],
		[math.sqrt(3) / 2, 1.5],
		[0, 2], 
		[-math.sqrt(3) / 2, 1.5],
		[-math.sqrt(3) / 2, 0.5]]

hexCenter = [[x, y - 1] for x, y in hexVertices]

resource_colors = ["green", "yellow", "orange", "brown", "red", "khaki"]

def draw_board(resources, dice):
	size = len(resources)
	fig = plt.figure()
	grid = fig.add_subplot(111, aspect = 'equal')
	grid.set_xlim(-size, size)
	grid.set_ylim(-size, size)
	start = (-math.sqrt(3) * (len(resources) // 2) / 2, 
		1.5 * (len(resources) // 2))
	for i in range(size // 2):
		for j in range(len(resources[i])):
			x, y = start[0] + j * math.sqrt(3), start[1]
			draw_hex_at(grid, x, y, resource_colors[resources[i][j]])
			draw_label(grid, x, y, dice[i][j])
		start = (start[0] - math.sqrt(3) / 2, start[1] - 1.5)
	for i in range(size // 2, size):
		for j in range(len(resources[i])):
			x, y = start[0] + j * math.sqrt(3), start[1]
			draw_hex_at(grid, x, y, resource_colors[resources[i][j]])
			draw_label(grid, x, y, dice[i][j])
		start = (start[0] + math.sqrt(3) / 2, start[1] - 1.5)
	plt.show()

def draw_hex_at(grid, x, y, color):
	grid.add_patch(patches.Polygon([[x + a, y + b] for a, b in hexCenter], 
		faceColor = color, edgecolor = "black"))
	
def draw_label(grid, x, y, label):
	if label == -1:
		return
	grid.text(x - 0.2 - 0.15 * (label // 10), y - 0.2, str(label), fontsize = 15)

