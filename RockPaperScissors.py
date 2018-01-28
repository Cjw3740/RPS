
from random import randint


#memory format: memory[lastmove][lastoutcome][nextmove]
memory = [[[0 for nextmove in range(3)] for outcome in range(3)] for lastmove in range(3)]
mem_map = {"rock":0,"paper":1,"scissors":2,"win":0,"lose":1,"tie":2}
beats = {"rock":"paper","paper":"scissors","scissors":"rock"}
last_moves = ["rock","paper"]			#the last move, and the one before it
last_outcomes = ["win","lose"]			#the last outcome and the one before it
outcome_tracker = {"win":0,"lose":0,"tie":0}
total_rounds = 0
strategy_list = ["random","smart"]


def find_max(next_move_list):  #returns the players most likley move
	translate = {0:"rock",1:"paper",2:"scissors"}
	pos_list = [i for i, j in enumerate(next_move_list) if j == max(next_move_list)] #finds the position of any values that are equal to the max value in the list
	return translate[pos_list[randint(0,len(pos_list)-1)]] #if more than 1 possible answer,pick one at random


def log_outcome(player_move,outcome):
	global total_rounds
	global last_outcomes
	global last_moves
	outcome_tracker[outcome] += 1
	total_rounds += 1
	lastMove = mem_map[last_moves[0]]
	lastOutcome = mem_map[last_outcomes[0]]
	nextMove = mem_map[player_move]
	memory[lastMove][lastOutcome][nextMove] +=1 #updates the memory
	last_moves[0],last_moves[1]=player_move,last_moves[0]
	last_outcomes[0],last_outcomes[1]=outcome,last_outcomes[0]


#outcome from perspective of human player
def rps(player_move,ai_move):
	move_dict = {"rock":{"rock":"tie","paper":"lose","scissors":"win"},"paper":{"rock":"win","paper":"tie","scissors":"lose"},"scissors":{"rock":"lose","paper":"win","scissors":"tie"}}
	outcome = move_dict[player_move][ai_move]
	log_outcome(player_move,outcome)
	return outcome


def choose_move(strategy):
	if strategy == "random":
		return ["rock","paper","scissors"][randint(0,2)]
	elif strategy == "smart":
		global mem_map
		global beats
		lastMoveIndx = mem_map[last_moves[0]]
		lastOutcomeIndx = mem_map[last_outcomes[0]]
		return beats[find_max(memory[lastMoveIndx][lastOutcomeIndx])]




#MAIN GAME LOOP
while True:
	strategy = input("what strategy would you like me to use: random or smart   ").lower()
	if strategy == "exit":
		break
	elif strategy not in strategy_list:
		print("Invalid selection. Try again")
	else:
		print("I will use the {} strategy".format(strategy))
	
		player_move = ""
		while True:
			ai_move = choose_move(strategy)
			player_move = input("I have chosen a move. Type rock, paper, or scissors  ").lower()
			if player_move == "exit":
				break
			elif player_move not in ["rock","paper","scissors"]:
				print("Invalid selection. Try again")
			else:
				result = rps(player_move,ai_move)
				if result == "tie":
					print("I chose {}. You chose {}. We {}!".format(ai_move,player_move,result))
				else:
					print("I chose {}. You chose {}. You {}!".format(ai_move,player_move,result))
				print("total rounds played: {}".format(total_rounds))
				print("Wins: {}, Loses: {}, Ties: {}\n".format(outcome_tracker["win"],outcome_tracker["lose"],outcome_tracker["tie"]))






	
