import sys
import pygame
import string
import queue
from math import *
from heapq import *
import time
import copy
#-----------------------function for get boxes and goals--------------------------------------#
def checkBoxsGoals(temp_matrix):
    boxs = []
    goals = []
    x = 0
    y = 0
    for row in temp_matrix:
        for i in row:
            if (i == '$' or i == '*'): boxs.append((x,y))
            if (i == '.' or i == '*'): goals.append((x,y))
            x+=1
        y+=1
        x = 0
    return boxs, goals
#-----------------------function for get player----------------------------------------------#
def get_character(matrix):
    x = 0
    y = 0
    for row in matrix:
        for i in row:
            if (i=='@' or i == '+'):
                return (x,y)
            x+=1
        y+=1
        x=0
    print("Khong tim thay character")
    return []
#----------------------function for check end state------------------------------------------#
def isCompleted(boxs,goals):
    for b in boxs:
        if (b not in goals): return False
    return True
#-----------------------------------------------------------------------#
def get_content(x,y,matrix):
    return matrix[y][x]
#-----------------------------------------------------------------------#
U = (0, -1) #up
D = (0, 1)  #down
L = (-1, 0) #left
R = (1, 0)  #right
direction = [U,D,L,R]
#-------------------function for check deadlock when player moves up-------------------------#
#  #  ##   #   ##  :  $$  #$  #$   $$  $#   $#
# #$  $$   $#  $$  :  $$  #$   $#  $$  $#  #$
#  |   |   |   |   :   |   |   |   |   |    |
#-----------------------------------------------------------------------#
def is_Deadlock_up(next_next_nodex, next_next_nodey, matrix): #x , y-1
  node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
  if node == "#":
    node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
    if node == "#":
      return True
    elif node == "$":
      node = get_content(next_next_nodex - 1, next_next_nodey - 1, matrix) #up_left
      if node == "#":
        return True
    else:
      node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
      if node == "#":
        return True
      elif node == "$":
        node = get_content(next_next_nodex + 1, next_next_nodey - 1, matrix) #up_right
        if node == "#":
          return True
  elif node == "$":
    node = get_content(next_next_nodex - 1, next_next_nodey - 1, matrix) #up_left
    if node == "#" or node == "$":
      node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
      if node == "#" or node == "$":
        return True
      else:
        node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
        if node == "#":
          return True
    else:
      node = get_content(next_next_nodex + 1, next_next_nodey - 1, matrix)#up_right
      if node == "#" or node == "$":
        node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
        if node == "#" or node == "$":
          return True
        else:
          node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
          if node == "#":
            return True
  return False
#-------------------function for check deadlock when player moves down-----------------------#
#  |   | :  |   |   :   |   |   |  :  |   |    |
# #$  $$ :  $#  $$  :  $$  #$   $# :  $$  $#  #$
#  #  ## :  #   ##  :  $$  #$  #$  :  $$  $#   $#
#-----------------------------------------------------------------------#
def is_Deadlock_down(next_next_nodex, next_next_nodey, matrix): #x, y + 1
  node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
  if node == "#":
    node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
    if node == "#":
      return True
    elif node == "$":
      node = get_content(next_next_nodex - 1, next_next_nodey + 1, matrix) #down_left
      if node == "#":
        return True
    else:
      node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
      if node == "#":
        return True
      elif node == "$":
        node = get_content(next_next_nodex + 1, next_next_nodey + 1, matrix) #down_right
        if node == "#":
          return True
  elif node == "$":
    node = get_content(next_next_nodex - 1, next_next_nodey + 1, matrix) #down_left
    if node == "#" or node == "$":
      node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
      if node == "#" or node == "$":
        return True
      else:
        node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
        if node == "#":
          return True
    else:
      node = get_content(next_next_nodex + 1, next_next_nodey + 1, matrix)#down_right
      if node == "#" or node == "$":
        node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
        if node == "#" or node == "$":
          return True
        else:
          node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
          if node == "#":
            return True
  return False
#-------------------function for check deadlock when player moves left-----------------------#
#                                       #                #
# #$ <- #$ <-   #    #$    $$ <- $$ <- $$ <- $$    ##    $$ <-
#  #    #$     #$ <- #$ <- $$    ##    #     $$ <- $$ <-  #
#-----------------------------------------------------------------------#
def is_Deadlock_left(next_next_nodex, next_next_nodey, matrix): #x-1,y
  node = get_content(next_next_nodex - 1, next_next_nodey, matrix) #left
  if node == "#":
    node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
    if node == "#":
      return True
    elif node == "$":
      node = get_content(next_next_nodex - 1, next_next_nodey + 1, matrix) #left_down
      if node == "#":
        return True
    else:
      node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
      if node == "#":
        return True
      elif node == "$":
        node = get_content(next_next_nodex - 1, next_next_nodey - 1, matrix) #left_up
        if node == "#":
          return True
  elif node == "$": #left
    node = get_content(next_next_nodex - 1, next_next_nodey + 1, matrix) #left_down
    if node == "#" or node == "$":
      node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
      if node == "#" or node == "$":
        return True
      else:
        node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
        if node == "#":
          return True
    else:
      node = get_content(next_next_nodex - 1, next_next_nodey - 1, matrix)#left_up
      if node == "#" or node == "$":
        node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
        if node == "#" or node == "$":
          return True
        else:
          node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
          if node == "#":
            return True
  return False
#-------------------function for check deadlock when player moves right-----------------------#
#                                   #                 #
# ->$# ->$#    #    $#  ->$$ ->$$ ->$$    $$   ##  ->$$
#   #    $#  ->$# ->$#    $$   ##    #  ->$$ ->$$    #
#-----------------------------------------------------------------------#
def is_Deadlock_right(next_next_nodex, next_next_nodey, matrix): #x + 1,y
  node = get_content(next_next_nodex + 1, next_next_nodey, matrix) #right
  if node == "#":
    node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
    if node == "#":
      return True
    elif node == "$":
      node = get_content(next_next_nodex + 1, next_next_nodey + 1, matrix) #right_down
      if node == "#":
        return True
    else:
      node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
      if node == "#":
        return True
      elif node == "$":
        node = get_content(next_next_nodex + 1, next_next_nodey - 1, matrix) #right_up
        if node == "#":
          return True
  elif node == "$":
    node = get_content(next_next_nodex + 1, next_next_nodey + 1, matrix) #right_down
    if node == "#" or node == "$":
      node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
      if node == "#" or node == "$":
        return True
      else:
        node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
        if node == "#":
          return True
    else:
      node = get_content(next_next_nodex + 1, next_next_nodey - 1, matrix)#right_up
      if node == "#" or node == "$":
        node = get_content(next_next_nodex, next_next_nodey - 1, matrix) #up
        if node == "#" or node == "$":
          return True
        else:
          node = get_content(next_next_nodex, next_next_nodey + 1, matrix) #down
          if node == "#":
            return True
  return False
#-----------------------------Blind search: BFS------------------------------------------#
def search_BFS(matrix):
    start = time.perf_counter()
    visited = []
    queue = [(matrix,[])] # Queue chứa (ma trận, danh sách người đi)
    visited.append(matrix)
    repeated_nodes = 0
    while len(queue) > 0:
        currentPos = queue.pop(0) # dequeue
        boxs, goals = checkBoxsGoals(currentPos[0])

        if isCompleted(boxs,goals):
            end = time.perf_counter()
            return currentPos[1], len(visited), len(visited) - len(queue), repeated_nodes, end - start
    
        for d in direction:
            temp_matrix = copy.deepcopy(currentPos[0]) #matrix of current state
            moves = copy.deepcopy(currentPos[1])
            (x,y) = get_character(currentPos[0])
            (new_x,new_y) = (x + d[0],y+d[1]) # new pos
            cur_obj = get_content(x,y,temp_matrix)
            next_obj = get_content(new_x,new_y,temp_matrix) # object which character will meet in next direction
            if next_obj == '#': # gap wall
                continue
            elif next_obj == ' ' or next_obj == '.':
                if cur_obj == '+':
                    temp_matrix[y][x] = '.'
                else:
                    temp_matrix[y][x] = ' '
                if next_obj == ' ':
                    temp_matrix[new_y][new_x] = '@'
                elif next_obj == '.':
                    temp_matrix[new_y][new_x] = '+'
                #add more later
            else: # box in next direction
                next_next_obj = get_content(new_x+d[0],new_y+d[1],temp_matrix)
                if (next_next_obj == '#' or next_next_obj == '$' or next_next_obj == '*'):
                    continue
                if next_next_obj == '.':
                  temp_matrix[(new_y+d[1])][(new_x+d[0])] = '*'
                elif d == U:
                  if is_Deadlock_up(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                elif d == D:
                  if is_Deadlock_down(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                elif d == L:
                  if is_Deadlock_left(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                else:
                  if is_Deadlock_right(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                    # can push box
                    # xet vi tri tiep theo cua box
                if next_next_obj == ' ': #
                   temp_matrix[(new_y+d[1])][(new_x+d[0])] = '$'
                
                    # xet vi tri tiep theo cua character
                if next_obj == '*':
                   temp_matrix[new_y][new_x] = '+'
                else:
                   temp_matrix[new_y][new_x] = '@'

                    # xet vi tri cu cua character
                if cur_obj == '+':
                   temp_matrix[y][x] = '.'
                else:
                   temp_matrix[y][x] = ' '
            # end action
            if temp_matrix not in visited:
                moves.append(d)
                visited.append(temp_matrix)                
                queue.append((temp_matrix, moves)) #enqueue
            else:
                repeated_nodes += 1
            #end for
    # end while
    #if fail
    end = time.perf_counter()
    return [], len(visited), len(visited), repeated_nodes, end - start
#-----------------------------------------------------------------------#
def heuristic(a,b):
    sum = 0
    for i in a:
        for j in b:
            manhantan = abs(i[0]-j[0])+abs(i[1]-j[1])
            sum += manhantan
    return sum
#----------------------------Heuristic: A*-------------------------------------------#
def search_Astar(matrix):
    start = time.perf_counter()
    node_repeated = 0
    visited = []
    boxs,goals = checkBoxsGoals(matrix)
    prior_queue = [(heuristic(boxs,goals),matrix,[])] # moi element chua [heuristic,map]
    visited.append(matrix)
    while (len(prior_queue) > 0):
        currentPos = heappop(prior_queue)
        boxs,goals = checkBoxsGoals(currentPos[1])
        if (isCompleted(boxs,goals)):
            total_node = len(visited)
            node_visited = len(visited)-len(prior_queue)
            end = time.perf_counter()
            return currentPos[2], total_node, node_visited, node_repeated, end - start

        for d in direction:
            temp_matrix = copy.deepcopy(currentPos[1]) #matrix of current state
            moves = copy.deepcopy(currentPos[2])
            (x,y) = get_character(currentPos[1])
            (new_x,new_y) = (x + d[0],y+d[1]) # new pos
            cur_obj = get_content(x,y,temp_matrix)
            next_obj = get_content(new_x,new_y,temp_matrix) # object which character will meet in next direction
            if (next_obj == '#'): # gap wall
                continue
            elif (next_obj== ' ' or next_obj == '.'):
                if (cur_obj == '+'):
                    temp_matrix[y][x] = '.'
                elif (cur_obj == '@'):
                    temp_matrix[y][x] = ' '
                if(next_obj == ' '):
                    temp_matrix[new_y][new_x] = '@'
                elif (next_obj == '.'):
                    temp_matrix[new_y][new_x] = '+'
                #add more later
            else: # box in next direction
                next_next_obj = get_content(new_x+d[0],new_y+d[1],temp_matrix)
                if (next_next_obj == '#' or next_next_obj == '$' or next_next_obj == '*'):
                    continue
                if next_next_obj == '.':
                  temp_matrix[(new_y+d[1])][(new_x+d[0])] = '*'
                elif d == U:
                  if is_Deadlock_up(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                elif d == D:
                  if is_Deadlock_down(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                elif d == L:
                  if is_Deadlock_left(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                else:
                  if is_Deadlock_right(new_x+d[0],new_y+d[1],temp_matrix):
                    continue
                # can push box
                # xet vi tri tiep theo cua box
                if (next_next_obj == ' '): #
                    temp_matrix[(new_y+d[1])][(new_x+d[0])] = '$'

                # xet vi tri tiep theo cua character
                if (next_obj == '*'):
                    temp_matrix[new_y][new_x] = '+'
                else:
                    temp_matrix[new_y][new_x] = '@'

                    # xet vi tri cu cua character
                if (cur_obj == '+'):
                    temp_matrix[y][x] = '.'
                else:
                    temp_matrix[y][x] = ' '

            # end action
           
            if (temp_matrix not in visited):
                moves.append(d)
                boxs,goals = checkBoxsGoals(temp_matrix)
                visited.append(temp_matrix)
                heappush(prior_queue,(len(moves)+heuristic(boxs,goals),temp_matrix,moves))
            else:
                node_repeated +=1
    end = time.perf_counter()
    #if fail
    return [], total_node, node_visited, node_repeated, end - start
#---------------------------------Object for printing demo--------------------------------------#
class game:

    def is_valid_value(self,char): #check key from input file
        if ( char == ' ' or #floor
            char == '#' or #wall
            char == '@' or #worker on floor
            char == '.' or #dock
            char == '*' or #box on dock
            char == '$' or #box
            char == '+' ): #worker on dock
            return True
        else:
            return False

    def __init__(self,matrix):
        self.matrix = matrix

    def load_size(self): #size of windows
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    def get_matrix(self): 
        return self.matrix

    def get_content(self,x,y):
        return self.matrix[y][x]

    def set_content(self,x,y,content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print ("ERROR: Value '"+content+"' to be added is not valid")

    def worker(self): #get location of player
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+': # worker on floor or worker on dock
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self,x,y): #check can move
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y) not in ['#','*','$']

    def next(self,x,y): #get value in next move
        return self.get_content(self.worker()[0]+x,self.worker()[1]+y)

    def can_push(self,x,y): #check push box
        return (self.next(x,y) in ['*','$'] and self.next(x+x,y+y) in [' ','.'])

    def is_completed(self): #check all of "$" => "*"
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self,x,y,a,b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x,y)
        future_box = self.get_content(x+a,y+b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x+a,y+b,'$')
            self.set_content(x,y,'.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x+a,y+b,'*')
            self.set_content(x,y,'.')

    def move(self,x,y):
        if self.can_move(x,y):
            current = self.worker()
            future = self.next(x,y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '@' and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],' ')
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0]+x,current[1]+y,'@')
                self.set_content(current[0],current[1],'.')
            elif current[2] == '+' and future == '.':
                self.set_content(current[0]+x,current[1]+y,'+')
                self.set_content(current[0],current[1],'.')
        elif self.can_push(x,y):
            current = self.worker()
            future = self.next(x,y)
            future_box = self.next(x+x,y+y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],' ')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@')
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'@') # + => @
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0]+x,current[1]+y,x,y)
                self.set_content(current[0],current[1],'.')
                self.set_content(current[0]+x,current[1]+y,'+')
#--------------------------------function for print game-------------------------------------#
def print_game(matrix, screen, background, floor, wall, worker, docker, box_docked, box, worker_docked):
        screen.fill(background)
        x = 0
        y = 0
        for row in matrix:
           for char in row:
                if char == ' ': #floor
                    screen.blit(floor,(x,y))
                elif char == '#': #wall
                    screen.blit(wall,(x,y))
                elif char == '@': #worker on floor
                    screen.blit(worker,(x,y))
                elif char == '.': #dock
                    screen.blit(docker,(x,y))
                elif char == '*': #box on dock
                    screen.blit(box_docked,(x,y))
                elif char == '$': #box
                    screen.blit(box,(x,y))
                elif char == '+': #worker on dock
                    screen.blit(worker_docked,(x,y))
                x = x + 32
           x = 0
           y = y + 32
#-----------------------------------------------------------------------#
def move_string(moves):
  movesssss = ""
  for i in moves: 
    if i[0] == -1 and i[1] == 0:
      movesssss += "l"
    elif i[0] == 1 and i[1] == 0:
      movesssss += "r"
    elif i[0] == 0 and i[1] == -1:
      movesssss += "u"
    else:
      movesssss += "d"
    movesssss += " "
  return movesssss
#-------------------------format of result print in command----------------------------------#
def format_string(moves, all_nodes, visited_nodes, repeated_nodes, time_run, level):
    stringcopy = level
    stringcopy += "\nMoves (" + str(len(moves)) + "): " + moves + "\n"
    stringcopy += "Number of states have been reached: " + str(all_nodes) + "\n"
    stringcopy += "Number of states have been visited: " + str(visited_nodes) + "\n"
    stringcopy += "Number of duplicated states: " + str(repeated_nodes) + "\n"
    stringcopy += "Time for searching: " + str(time_run) + " seconds\n"
    stringcopy += "*****************************************************\n"
    return stringcopy
#-----------------------------------------------------------------------#
def choose_Option():
  print("Chon loai demo")
  option = -1
  while option != 1 and option != 2:
    print("Nhap 1 de chon Blind search, nhap 2 de chon Heuristic: ")
    option = int(input())
  option = -1
  while option != 1 and option != 2:
    print("Nhap 1 de demo file mini-test, nhap 2 de demo file micro-test ")
    option = int(input())
  fileread = "./mini-test.txt"
  if option == 2:
    fileread = "./micro-test.txt"
  level = -1
  while level < 1 or level > 40:
    print("Chon level thuc hien: ")
    level = int(input())
  return option, level, fileread
#-----------------------------------------------------------------------#
def read(file,level):
    f = open(file,'rt')
    level_found = 0
    matrix = []
    for line in f:
        temp = []
        if (line.strip() == ("Level "+str(level))):
            level_found = 1
            continue
        if (level_found == 1):
            if (line.strip() == ''): break
            else:
                for c in line:
                    if (c == '\n'): break
                    else: temp.append(c)
                matrix.append(temp)
    f.close()
    return matrix
#-----------------------------------------------------------------------#
def run_game():
  #-------------load image----------#
  wall = pygame.image.load('images/wall.png')
  floor = pygame.image.load('images/floor.png')
  box = pygame.image.load('images/box.png')
  box_docked = pygame.image.load('images/box_docked.png')
  worker = pygame.image.load('images/worker.png')
  worker_docked = pygame.image.load('images/worker_dock.png')
  docker = pygame.image.load('images/dock.png')
  background = 255, 226, 191 #background color

  pygame.init()

  while True:
    #input demo
    option, level, fileread = choose_Option()
    #elements for printing terminal
    moves, all_nodes, visited_nodes, repeated_nodes, time_run = [], 0, 0, 0, 0
    matrix = read(fileread, level)

    print("Solving level " + str(level) + "..........")
    if option == 1:
      moves, all_nodes, visited_nodes, repeated_nodes, time_run = search_BFS(matrix)
    else:
      moves, all_nodes, visited_nodes, repeated_nodes, time_run = search_Astar(matrix)
    
    print(format_string(move_string(moves), all_nodes, visited_nodes, repeated_nodes, time_run, "Llevel " + str(level)))
    
    sokoban = game(matrix) #create game
    size = sokoban.load_size() #load size
    screen = pygame.display.set_mode(size)
    pygame.display.init()

    print_game(sokoban.get_matrix(),screen, background, floor, wall, worker, docker, box_docked, box, worker_docked)
    pygame.display.update()
    time.sleep(0.5)

    for i in moves:
          pygame.event.pump()
          sokoban.move(i[0],i[1])
          print_game(sokoban.get_matrix(),screen, background, floor, wall, worker, docker, box_docked, box, worker_docked)
          pygame.display.update()
          if (sokoban.is_completed()): 
            time.sleep(0.5)
          else: time.sleep(0.3)
    pygame.display.flip ()
    pygame.quit()

    a = -1
    print("Tiep tuc demo?")
    print("Chon 1 de tiep tuc, chon 2 de dung: ")
    while a != 1 and a != 2:
      a = int(input())
    if a == 2: break
  print("Demo thanh cong")
#-----------------------------------------------------------------------#
run_game()