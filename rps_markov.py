import numpy as np
import matplotlib.pyplot as plt
from random import choice, randint, random

POSSIBLE_MOVES: list[str] = ['rock', 'paper', 'scissors'];
SHORTCUTS: dict[str, str] = {'r': 'rock', 'p': 'paper', 's': 'scissors'}


WINNING_MOVES: dict[str, str] = {'rock':'paper', 'paper':'scissors', 'scissors':'rock'}


learning_rate = 0.02
exploration_rate = 0.2

transition_matrix: dict[str, dict[str, float]] = {}

def initialize_transition_matrix()->None:
    for source in POSSIBLE_MOVES:
        transition_matrix[source] = {}
        for target in POSSIBLE_MOVES:
            transition_matrix[source][target] = 1/3


def update_transition_matrix(previous_move, current_move)->None:
    for move in POSSIBLE_MOVES:
        if move == current_move:
            transition_matrix[previous_move][move] += learning_rate * (1 - transition_matrix[previous_move][move])
        else:
            transition_matrix[previous_move][move] -= learning_rate * transition_matrix[previous_move][move]

    normalize(previous_move)


def normalize(source: str) -> None:
    total = sum(transition_matrix[source].values())
    if total > 0:
        for move in POSSIBLE_MOVES:
            transition_matrix[source][move] /= total

def fight(player_move: str, ai_move: str) -> int:
    if(player_move == ai_move):
        return 0
    elif(WINNING_MOVES[player_move] == ai_move):
        return -1
    else:
        return 1
    

def make_ai_move(previous_move: str, first_round: bool) -> str:
    if first_round or random() < exploration_rate:
        return choice(POSSIBLE_MOVES)
    predicted_player_move = max(transition_matrix[previous_move], key=transition_matrix[previous_move].get)

    return WINNING_MOVES[predicted_player_move]


def start()->None:
    initialize_transition_matrix()
    print('Welcome to Markov Rock Paper Scissors!')
    print('You are playing by typing fullname of valid moves or first letter.\n')
    mode = input("► Choose mode: 'manual' (m) or 'auto' (a): ").lower()

    if mode == 'a' or mode == 'auto':
        num_iterations = int(input("► Enter number of auto-play points: "))
        auto_play(num_iterations)
        return
    elif mode == 'm' or mode == 'manual':
        play()

def play()->None:
    max_points = int(input('► How many points are we playing for? '))
    previous_move = None

    player_points = 0
    ai_points = 0
    score_history = []


    while player_points < max_points and ai_points < max_points:
        user_input = input("Choose: ►'rock' (r), ►'paper' (p), or ►'scissors' (s), ►'quit' (q): ").lower()

        if user_input in SHORTCUTS:
            player_move = SHORTCUTS[user_input]
        elif user_input in POSSIBLE_MOVES:
            player_move = user_input
        elif user_input == 'quit' or user_input == 'q':
            return 
        else:
            print("Invalid move! Try again.")
            continue

        first_round = previous_move is None
        ai_move = make_ai_move(previous_move, first_round)

        print(f"You chose: {player_move} vs AI chose: {ai_move}")
        result = fight(player_move, ai_move)
        if result == 1:
            print("► You win (+1)")
            player_points += 1
            ai_points -= 1
        elif result == -1:
            print("► AI wins (-1)")
            ai_points += 1
            player_points -= 1
        else:
            print("► It is a draw (0)")
        
        score_history.append(abs(player_points))

        print(f"► Score: You ({player_points})  ({ai_points}) AI\n")

        if player_points >= max_points:
            print("🎉 Congratulations! You won the game! 🎉")
            break
        elif ai_points >= max_points:
            print("💀 AI has won.... Try again! 💀")
            break

        previous_move = player_move

        if previous_move is not None:
            update_transition_matrix(previous_move, player_move)


    print("Game over!")
    plot_score_history(score_history)


def auto_play(target_score):
    previous_move = None
    player_points = 0
    ai_points = 0
    score_history = []
    rounds = 0

    while player_points < target_score and ai_points < target_score:
        rounds += 1
        player_move = choice(POSSIBLE_MOVES)
        first_round = previous_move is None
        ai_move = make_ai_move(previous_move, first_round)

        result = fight(player_move, ai_move)
        if result == 1:
            player_points += 1
        elif result == -1:
            ai_points += 1

        score_history.append(abs(player_points))
        previous_move = player_move

        if previous_move:
            update_transition_matrix(previous_move, player_move)

        if rounds % 100 == 0:
            print(f"Round {rounds} - AI: {ai_points} | Player AI: {player_points}")

    print(f"Auto-play finished in {rounds} rounds! Final Score: AI ({ai_points}) vs Player AI ({player_points})")
    plot_score_ai_history(score_history)




def plot_score_history(score_history):
    plt.plot(score_history, linestyle='-', color='b', label="Player's Absolute Score")
    plt.xlabel("Game Round")
    plt.ylabel("Absolute Score")
    plt.title("Player's Score History")
    plt.savefig("player_score_history.png")
    plt.show()

def plot_score_ai_history(score_history):
    plt.plot(score_history, linestyle='-', color='r', label="Player AI's Absolute Score")
    plt.xlabel("Game Round")
    plt.ylabel("Absolute Score")
    plt.title("Player AI's Score History")
    plt.savefig("ai_score_history.png")
    plt.show()


if __name__ == '__main__':
    start()















