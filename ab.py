import BulletsHolder
import ChickenHolder
from sources import *


##############################################################################################################

def check_collision(obj1_mask, obj1_pos, obj2_mask, obj2_pos):
    pos1 = [(point[0] + obj1_pos[0], point[1] + obj1_pos[1]) for point in obj1_mask]
    pos2 = [(point[0] + obj2_pos[0], point[1] + obj2_pos[1]) for point in obj2_mask]
    for point1 in pos1:
        for point2 in pos2:
            if point2 == point1:
                return True
    return False

def dist(pos1,pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class Node:
    def __init__(self, player, enemies: ChickenHolder.ChicksHolder, bulls: BulletsHolder.BulletsHolder, move):
        self.player = player.copy_object()
        self.enemies = enemies.copy_object()
        self.bulls = bulls.copy_object()
        self.move = move
        self.is_terminal = False
    
    # def __gt__(self, other):
    #     return len(self) > len(other)
    #
    # def __lt__(self, other):
    #     return len(self) < len(other)
    
    def check_collision_egg_n_player(self) -> bool:
        for egg in self.bulls.bullets:
            if check_collision(self.player.mask.outline(), (self.player.x, self.player.y), egg.mask.outline(),
                               (egg.x, egg.y)):
                return True
        return False
    
    def check_collision_chick_n_laser(self) -> bool:
        for laser in self.bulls.lasers:
            for chick in self.enemies.chicks:
                if check_collision(laser.mask.outline(), (laser.x, laser.y), chick.mask.outline(), (chick.x, chick.y)):
                    return True
        return False
    
    def generate_children(self):
        children = []
        for new_position, direction in [((-8, 0), '<'),((8, 0), '>')]:#,((0, -12),'↑'), ((0, 12),'↓')]:  # Adjacent squares ,
            # Get node position
            node_position = (self.player.x + new_position[0], self.player.y + new_position[1])
            # Make sure within range
            if node_position[0] > WIDTH - 1 or node_position[0] < 1 or node_position[1] > HEIGHT - 1 or node_position[
                1] < 1:
                continue
            
            # move elements
            self.enemies.move(self.bulls)
            self.bulls.move_all()
            
            # check player collisions
            if self.check_collision_egg_n_player():
                self.is_terminal = True
            
            self.player.x += new_position[0]
            # useless
            # self.player.y+=node_position[1]
            
            # Create new node
            new_node = Node(self.player, self.enemies, self.bulls, direction)
            # Append
            children.append(new_node)
        return children
    
    def evaluation_function(self):
        if self.check_collision_egg_n_player():
            return -float('inf')
        elif self.check_collision_chick_n_laser():
            return float('inf')
        else:
            centre_player = (self.player.x + self.player.image.get_width(), self.player.y)
            distances =[]
            for enemy in self.enemies.chicks:
                distances.append(dist(centre_player, (enemy.x , enemy.y)))
            try:
                minvalue = min(distances)
            except ValueError:
                minvalue = 1
        return 1/minvalue

def alphabeta(node: Node, depth, a, b, maximizingPlayer):
    if depth == 0 or node.is_terminal:  # or node is terminal_node:
        return (node.evaluation_function(), node)
    if maximizingPlayer:
        value = -float('inf')
        best_node = node
        # if collide with egg then return value -inf, node
        for child in node.generate_children():
            alphares, alphanode = alphabeta(child, depth - 1, a, b, False)
            # value = max(value, alphares)
            if alphares > value:
                value = alphares
                best_node = child
            if value >= b:
                break  # (* b cutoff *)
            if value > a:
                a = value
        return (value, best_node)
    else:
        worst_node = node
        value = float('inf')
        # if collide with laser then return value +inf, node
        for child in node.generate_children():
            alphares, alphanode = alphabeta(child, depth - 1, a, b, True)
            # value = min(value, alphares)
            if alphares<value:
                value=alphares
                worst_node = child
            if value <= a:
                break  # (* a cutoff *)
            if value < b:
                b = value
        return (value, worst_node)



def expectiminimax(node: Node, depth, maximizingPlayer):
        if depth == 0 or node.is_terminal:  # or node is terminal_node:
            return (node.evaluation_function(), node)
        if maximizingPlayer:
            
            res_arr_of_nodes = [expectiminimax(child, depth - 1, False) for child in node.generate_children()]
            alphares, alphanode = max(res_arr_of_nodes,key=lambda x:x[0],default=node)
                # [(value,node),(value,node),(value,node),]
            return (alphares/len(res_arr_of_nodes), alphanode)
        else:
            res_arr_of_nodes = [expectiminimax(child, depth - 1, True) for child in node.generate_children()]
            alphares, alphanode = min(res_arr_of_nodes,key=lambda x:x[0],default=node)
                # [(value,node),(value,node),(value,node),]
            return (alphares/len(res_arr_of_nodes), alphanode)
