import time

import pygame
def get_score():
    return score
def set_score(scoree):
    global score
    score=scoree
def inc_score(scoree):
    global score
    score+=scoree

score=0
WIDTH = 500
HEIGHT = 400
FPS = 60
точність_побудови_маршруту=40 #...1 одиниця це найточніший пошук але менше 10 це просто слайдшоу
depth_recurtion = 3
FONT=20
size_of_chick = 30
SPACE_IMG = pygame.transform.scale(pygame.image.load('imgs/Nebula Blue.png'), (WIDTH, HEIGHT))
SHIP_IMG = pygame.transform.scale(pygame.image.load('imgs/player.png'), (30, 30))
BLUE_CHICK_IMG = pygame.transform.scale(pygame.image.load('imgs/blue.png'), (size_of_chick, size_of_chick))
YELLOW_CHICK_IMG = pygame.transform.scale(pygame.image.load('imgs/yellow.png'), (size_of_chick, size_of_chick))
RED_CHICK_IMG = pygame.transform.scale(pygame.image.load('imgs/red.png'), (size_of_chick, size_of_chick))
EGG_IMG = pygame.transform.scale(pygame.image.load('imgs/egg.png'), (10, 10))
LASER_IMG = pygame.transform.scale(pygame.image.load('imgs/laser.png'), (10, 50))

start_time=time.time()


def snext(method):
    
    if method == 'star':
        return 'dfs'
    elif method == 'dfs':
        return 'bfs'
    elif method == 'bfs':
        return 'ucs'
    elif method == 'ucs':
        return 'star'


serach_method = 'star'
def write_to_csv(iswin, time, score, alg):
    import csv
    with open('res.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow([iswin, time, score, alg])
        
# def expectiminіmax(node, depth, a, b, maximizingPlayer):
#     if depth == 0 or node.is_terminal:  # or node is terminal_node:
#         return (node.evaluation_function(), node)
#     if maximizingPlayer:
#         value = -float('inf')
#         best_node = node
#         # if collide with egg then return value -inf, node
#         for child in node.generate_children():
#             alphares, alphanode = expectiminіmax(child, depth - 1, a, b, True)
#             # value = max(value, alphares)
#             if alphares > value:
#                 value = alphares
#                 best_node = child
#             if value >= b:
#                 break  # (* b cutoff *)
#             if value > a:
#                 a = value
#         return (value, best_node)
#     else:
#         worst_node = node
#         value = float('inf')
#         # if collide with laser then return value +inf, node
#         for child in node.generate_children():
#             alphares, alphanode = expectiminіmax(child, depth - 1, a, b, False)
#             # value = min(value, alphares)
#             if alphares<value:
#                 value=alphares
#                 worst_node = child
#             if value <= a:
#                 break  # (* a cutoff *)
#             if value < b:
#                 b = value
#         return (value, worst_node)

