
import pygame
from math import *  #can limit this to just the functions you need when you're closer to being done
import datetime
import json
from random import randint,choice

from random import randint,triangular, choice

pygame.init()

screen_size_x,screen_size_y  = 1600, 1000
screen = pygame.display.set_mode((screen_size_x,screen_size_y))

#setting up text options (needs to be cleaned up, some use msg_obj some use font)
pygame.font.init()  #must call this
msg_obj = pygame.font.SysFont('New Times Roman', 30) #msg object to render, font and size
font = pygame.font.Font(None,30)

#defining rgb colors for easy reference
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
light_blue = (0,255,255)
purple = (255,0,255)
yellow = (255,255,0)
orange = (255,128,0)

player_move = ""
ai_move = ""
outcome_rulling = ""
#from player's perspective
num_wins = 0
num_losses = 0
num_ties = 0
#win_percent = 0
#lose_percent = 0
#tie_percent = 0

rounds_played = 0

memory = [[[0 for nextmove in range(3)] for outcome in range(3)] for lastmove in range(3)]   #memory[lastMove][lastOutcome][nextMove]
mem_maping = {"rock":0,"paper":1,"scissors":2,"win":0,"lose":1,"tie":2}
beats = {"rock":"paper","paper":"scissors","scissors":"rock"} #what beats what

two_moves_ago = ""
last_outcome = ""
one_move_ago = ""
this_outcome = ""



def save_memory():
	global memory
	with open('RPS Memory.txt','w') as outfile:
		json.dump(memory, outfile)
		outfile.close

#need to add backup settings to use if no save fileis found
def load_memory():
	global memory
	with open('RPS Memory.txt','r') as infile:
		memory = json.load(infile)
		infile.close



def update_memory(p_move,wlt):
	global two_moves_ago
	global one_move_ago
	global last_outcome
	global this_outcome
	global memory
	
	two_moves_ago = one_move_ago
	one_move_ago = p_move
	last_outcome = this_outcome
	this_outcome = wlt
	
	if rounds_played>1:
		memory[mem_maping[two_moves_ago]][mem_maping[last_outcome]][mem_maping[one_move_ago]] += 1

def ai_chose_next_move():
	if rounds_played < 2:
		return choice(["rock","paper","scissors"])
	else:
		next_move_set = memory[mem_maping[one_move_ago]][mem_maping[last_outcome]]
		max_val = max(next_move_set)
		max_indicies = []
		for i,n in enumerate(next_move_set):
			if n == max_val:
				max_indicies.append(i)
		your_next_move = ["rock","paper","scissors"][choice(max_indicies)]
		my_next_move = beats[your_next_move]
		#print("Your next move: ",your_next_move)
		#print("My next move: ",my_next_move)
		return my_next_move
	
	

print("Setting up custom events")
"""custom events to be handled by the event handler"""
CUSTOMEVENT = pygame.USEREVENT +1 #needs category attribute at a minimum
rock = pygame.event.Event(CUSTOMEVENT, selection = 'rock')
paper = pygame.event.Event(CUSTOMEVENT, selection = 'paper')
scissors = pygame.event.Event(CUSTOMEVENT, selection = 'scissors')



"""found the following function online. Don't remember where"""
def inside_polygon(x,y,points):
	"""return True if (x,y) is inside polygon defined by points"""
	n = len(points)
	inside = False
	p1x,p1y = points[0]
	for i in range(1,n+1):
		p2x,p2y = points[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x, p1y = p2x,p2y
	return inside


class button_rec_do():
	def __init__(self,loc,size,color,text,default_state,do_on_press):
		self.do_on_press = do_on_press
		self.loc = loc
		self.dx,self.dy = size
		self.x1 = loc[0]
		self.y1 = loc[1]
		self.x2 = self.x1 + size[0]
		self.y2 = self.y1 +size[1]
		self.points = (self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2)
		self.color = color
		self.pressed = default_state
		self.text = text

	def draw(self):
		#Being pressed or unpressed is just for appearance. clicking the button does not automatically toggle the state
		if self.pressed:
			self.boarder = 0
			self.text_bgcolor = self.color
			txt = msg_obj.render(self.text,True, black, self.text_bgcolor)
		else:
			self.boarder = 1
			self.text_bgcolor = black
			txt = msg_obj.render(self.text,True, self.color, self.text_bgcolor)
			
		self.txt_loc = (self.x1 + self.dx/2 - font.size(self.text)[0]/2,self.y1 + self.dy/2 - font.size(self.text)[1]/2)
		
		pygame.draw.rect(screen,black, pygame.Rect((self.x1,self.y1,self.dx,self.dy)))
		pygame.draw.rect(screen,self.color, pygame.Rect((self.x1,self.y1,self.dx,self.dy)),self.boarder)
		screen.blit(txt,self.txt_loc)
	
	def do(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.event.post(self.do_on_press)

class text_label():
	def __init__(self,pos,size,text,color):
		self.x1,self.y1 = pos
		self.dx,self.dy = size
		self.x2 = self.x1 + self.dx
		self.y2 = self.y1 + self.dy
		self.points = ((self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2))
		self.text = text
		self.color = color
	
	def draw(self):
		pygame.draw.rect(screen,black, pygame.Rect((self.x1,self.y1,self.dx,self.dy)))
		pygame.draw.rect(screen,self.color, pygame.Rect((self.x1,self.y1,self.dx,self.dy)),1)
		self.txt_loc = (self.x1 + self.dx/2 - font.size(self.text)[0]/2,self.y1 + self.dy/2 - font.size(self.text)[1]/2)
		txt = msg_obj.render(self.text,True, self.color, black)
		screen.blit(txt,self.txt_loc)
		
	def do(self,event):
		pass




class score_board():
	def __init__(self,pos,cell_size,name,color,player_T):
		self.x1,self.y1 = pos
		self.dx,self.dy = cell_size[0]*4,cell_size[1]*3
		self.cell_x,self.cell_y = cell_size
		self.x2 = self.x1 + self.dx
		self.y2 = self.y1 + self.dy
		self.points = ((self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2))
		self.name = name
		self.txt_space_x,self.txt_space_y = 15,15
		self.color = color
		self.player_T = player_T #true if player, false if AI
		self.wins = 0
		self.losses = 0
		self.ties = 0
		
		
	def draw(self):
		pygame.draw.rect(screen,black, pygame.Rect((self.x1,self.y1,self.dx,self.dy)))
		for row in range(4):
			pygame.draw.line(screen,self.color,(self.x1,self.y1+row*self.cell_y),(self.x2,self.y1+row*self.cell_y),1) 
		for col in range(5):
			pygame.draw.line(screen,self.color,(self.x1+col*self.cell_x,self.y1),(self.x1+col*self.cell_x,self.y2),1)
		

		
		for i,title in enumerate([self.name,"Wins","Losses","Ties"]): #need to make this just center the text
			txt = msg_obj.render(title,True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+i*self.cell_x,self.y1+self.txt_space_y))
		
		txt = msg_obj.render("Num",True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x,self.y1+self.txt_space_y+self.cell_y))
		
		txt = msg_obj.render("%",True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x,self.y1+self.txt_space_y+2*self.cell_y))
		
		
	def update_scores(self):
		self.draw()
		
		
		txt = msg_obj.render(str(num_wins*self.player_T+num_losses*(not self.player_T)),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+self.cell_y))
		txt = msg_obj.render(str(num_losses*self.player_T+num_wins*(not self.player_T)),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
		txt = msg_obj.render(str(num_ties),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
		
		txt = msg_obj.render(str(round(100*(num_wins*self.player_T+num_losses*(not self.player_T))/rounds_played,0)),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
		txt = msg_obj.render(str(round(100*(num_losses*self.player_T+num_wins*(not self.player_T))/rounds_played,0)),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
		txt = msg_obj.render(str(round(100*num_ties/rounds_played,0)),True, self.color, black)
		screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
		
		
		
		
		
		
		"""
		if self.player_T:
			txt = msg_obj.render(str(num_wins),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			txt = msg_obj.render(str(num_losses),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			txt = msg_obj.render(str(num_ties),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			
			txt = msg_obj.render(str(round(100*num_wins/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
			txt = msg_obj.render(str(round(100*num_losses/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
			txt = msg_obj.render(str(round(100*num_ties/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
		
		else:
			txt = msg_obj.render(str(num_losses),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			txt = msg_obj.render(str(num_wins),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			txt = msg_obj.render(str(num_ties),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+self.cell_y))
			
			txt = msg_obj.render(str(round(100*num_losses/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
			txt = msg_obj.render(str(round(100*num_wins/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+2*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
			txt = msg_obj.render(str(round(100*num_ties/rounds_played,0)),True, self.color, black)
			screen.blit(txt,(self.x1+self.txt_space_x+3*self.cell_x,self.y1+self.txt_space_y+2*self.cell_y))
		"""
		
	
	def do(self):
		pass



class button_img_do():
	def __init__(self,loc,img,do_on_press):
		self.do_on_press = do_on_press
		self.loc = self.x1,self.y1 = loc
		self.img = img
		self.image = pygame.image.load(self.img)
		self.dx,self.dy = self.image.get_size()
		self.x2,self.y2 = ((self.x1+self.dx),(self.y1+self.dy))
		self.points = ((self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2))
		
	def draw(self):
		screen.blit(self.image,self.loc)
		
	def do(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.event.post(self.do_on_press)



class img_label():
	def __init__(self,loc,img):
		self.loc = self.x1,self.y1 = loc
		self.image = pygame.image.load(img)
		self.dx,self.dy = self.image.get_size()
		self.x2,self.y2 = ((self.x1+self.dx),(self.y1+self.dy))
		self.points = ((self.x1,self.y1),(self.x2,self.y1),(self.x2,self.y2),(self.x1,self.y2))
	def draw(self):
		screen.blit(self.image,self.loc)


def linear_move(obj,final_pos,num_steps,speed):
	Dx = final_pos[0]-obj.x1
	Dy = final_pos[1] - obj.y1
	dx = round(Dx/num_steps,0)
	dy = round(Dy/num_steps,0)
	for i in range(num_steps):
		pygame.draw.rect(screen,black, pygame.Rect((obj.x1,obj.y1,obj.dx,obj.dy)),0) #blacks out old img
		obj.x1 += dx
		obj.y1 += dy
		obj.loc = obj.x1,obj.y1
		obj.dx,obj.dy = obj.image.get_size()
		obj.x2,obj.y2 = ((obj.x1+obj.dx),(obj.y1+obj.dy))
		obj.points = ((obj.x1,obj.y1),(obj.x2,obj.y1),(obj.x2,obj.y2),(obj.x1,obj.y2))
		obj.draw()
		pygame.display.flip()
		clock.tick(speed)
		
def dual_linear_move(obj1,obj2,final_pos1,final_pos2,num_steps,speed):
	Dx1 = final_pos1[0]-obj1.x1
	Dy1 = final_pos1[1] - obj1.y1
	dx1 = round(Dx1/num_steps,0)
	dy1 = round(Dy1/num_steps,0)
	
	Dx2 = final_pos2[0]-obj2.x1
	Dy2 = final_pos2[1] - obj2.y1
	dx2 = round(Dx2/num_steps,0)
	dy2 = round(Dy2/num_steps,0)
	
	for i in range(num_steps):
		pygame.draw.rect(screen,black, pygame.Rect((obj1.x1,obj1.y1,obj1.dx,obj1.dy)),0) #blacks out old img
		pygame.draw.rect(screen,black, pygame.Rect((obj2.x1,obj2.y1,obj2.dx,obj2.dy)),0) #blacks out old img
		
		#moving object1
		obj1.x1 += dx1
		obj1.y1 += dy1
		obj1.loc = obj1.x1,obj1.y1
		obj1.dx,obj1.dy = obj1.image.get_size()
		obj1.x2,obj1.y2 = ((obj1.x1+obj1.dx),(obj1.y1+obj1.dy))
		obj1.points = ((obj1.x1,obj1.y1),(obj1.x2,obj1.y1),(obj1.x2,obj1.y2),(obj1.x1,obj1.y2))
		obj1.draw()
		
		#moving object2
		obj2.x1 += dx2
		obj2.y1 += dy2
		obj2.loc = obj2.x1,obj2.y1
		obj2.dx,obj2.dy = obj2.image.get_size()
		obj2.x2,obj2.y2 = ((obj2.x1+obj2.dx),(obj2.y1+obj2.dy))
		obj2.points = ((obj2.x1,obj2.y1),(obj2.x2,obj2.y1),(obj2.x2,obj2.y2),(obj2.x1,obj2.y2))
		obj2.draw()
		
		pygame.display.flip()
		clock.tick(speed)



#outcome from perspective of human player
def rps(p_m,a_m):
	move_dict = {"rock":{"rock":"tie","paper":"lose","scissors":"win"},"paper":{"rock":"win","paper":"tie","scissors":"lose"},"scissors":{"rock":"lose","paper":"win","scissors":"tie"}}
	return move_dict[p_m][a_m]







rock_button = button_img_do((screen_size_x-300,50),"rock.png",rock)
rock_button.text = "rock"
paper_button = button_img_do((screen_size_x-300,350),"paper.png",paper)
paper_button.text = "paper"
scissors_button = button_img_do((screen_size_x-300,650),"scissors.png",scissors)
scissors_button.text = "scissors"

player_score_board = score_board((550,800),(100,50),"Player",light_blue,True)
ai_score_board = score_board((550,50),(100,50),"AI",light_blue,False)



#outcome = text_label((650,100),(200,100),"Outcome",yellow)

rock_ai = img_label((50,50),"rock.png")
rock_ai.text = "rock"
paper_ai = img_label((50,350),"paper.png")
paper_ai.text = "paper"
scissors_ai = img_label((50,650),"scissors.png")
scissors_ai.text = "scissors"


RPS_buttons = [rock_button,paper_button,scissors_button]


win_pic = img_label((75,75),"win.png")

next_move_prediction = text_label((0,0),(200,50),"next move",light_blue)


def event_handler(event):
	global num_wins
	global num_losses
	global num_ties
	global rounds_played
	global ai_move_chosen
	if event.type == pygame.MOUSEBUTTONDOWN:
		mouse_pos_x,mouse_pos_y = pygame.mouse.get_pos()
		for obj in RPS_buttons:
			if inside_polygon(mouse_pos_x, mouse_pos_y,obj.points):
				obj.do(event)
	for play in [rock,paper,scissors]:
		if event == play:
			for button in [rock_button,paper_button,scissors_button]:
				if play == button.do_on_press:
					
					#ai_move = choice(["rock","paper","scissors"]) #this should be moved so that it's choice has already been made before you make yours
					
					
					
					
					for ai_icon in [rock_ai,paper_ai,scissors_ai]:
						if ai_icon.text == ai_move:
							ai_target_icon = ai_icon
					
					
					rslt = rps(button.text,ai_move)
					
					update_memory(button.text,rslt)
					save_memory()
					
					button_original_pos = button.x1,button.y1
					ai_icon_original_pos = ai_target_icon.x1,ai_target_icon.y1
					
					dual_linear_move(button,ai_target_icon,(round(screen_size_x/2),350),(round(screen_size_x/2)-ai_target_icon.dx,350),100,150)
					

					num_wins += rslt=="win"
					num_losses += rslt=="lose"
					num_ties += rslt=="tie"
					rounds_played +=1
					player_score_board.update_scores()
					ai_score_board.update_scores()
					
					
					clock.tick(5)
					
					dual_linear_move(button,ai_target_icon,button_original_pos,ai_icon_original_pos,100,150)
					pygame.event.clear() #prevents random button clicks durring animation from ending up in the event queue
					ai_move_chosen = False
					
					




"""SETUP"""
"""runs once before main loop"""
#serial_comm_start()

load_memory()

clock = pygame.time.Clock()

rock_button.draw()
paper_button.draw()
scissors_button.draw()

rock_ai.draw()
paper_ai.draw()
scissors_ai.draw()



player_score_board.draw()
ai_score_board.draw()

ai_move_chosen = False

#outcome.draw()

"""MAIN PROGRAM LOOP"""
running = True
while running:
	
	if not ai_move_chosen:
		ai_move = ai_chose_next_move()
		ai_move_chosen = True

	
	for event in pygame.event.get():

		
		if event.type == pygame.QUIT:
			running = False
			
		else:
			event_handler(event)


	pygame.display.flip()	
	clock.tick(60)
