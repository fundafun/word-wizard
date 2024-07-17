import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREY = (229, 224, 229)
BLACK = (0, 0, 0)
RED = (250, 53, 79)
GREEN = (81, 176, 94)
BLUE = (83, 118, 216)
PINK = (245, 110, 236)
FONT_SIZE = 36

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Wizard")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Helper function to display text
def display_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to generate letters with at least two vowels
def generate_letters():
    vowels = "AEIOU"
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    
    # Ensure at least two vowels
    letters = random.choices(vowels, k=2)
    
    # Fill the rest with random letters
    letters += random.choices(vowels + consonants, k=8)
    
    # Shuffle the list to mix vowels and consonants
    random.shuffle(letters)
    
    return letters

# Splash screen function
def splash_screen():
    screen.fill(GREY)
    display_text("Welcome to the Word Wizard!", 100, 50, RED)
    display_text("Press 'S' to start single player", 100, 150, GREEN)
    display_text("Press 'M' to start multiplayer", 100, 200, BLUE)
    display_text("Press 'Q' to quit", 100, 250, PINK)
    display_text("Points:", 100, 350, BLACK)
    display_text("3 letter word: 2 points", 100, 400, BLACK)
    display_text("4 letter word: 4 points", 100, 450, BLACK)
    display_text("5+ letter word: 6 points", 100, 500, BLACK)
    display_text("2 letter words are not allowed!", 100, 550, RED)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting = False
                    return 'single'
                if event.key == pygame.K_m:
                    waiting = False
                    return 'multi'
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Function to ask for total game time
def ask_total_time():
    screen.fill(GREY)
    display_text("Select total game time:", 100, 200, BLUE)
    display_text("Press '3' for 30 seconds", 100, 250, BLACK)
    display_text("Press '6' for 60 seconds", 100, 300, BLACK)
    display_text("Press '9' for 90 seconds", 100, 350, BLACK)
    pygame.display.flip()

    waiting = True
    total_time = 60  # Default to 60 seconds
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    total_time = 30
                    waiting = False
                elif event.key == pygame.K_6:
                    total_time = 60
                    waiting = False
                elif event.key == pygame.K_9:
                    total_time = 90
                    waiting = False
    return total_time

# Function to ask for player names in single player mode
def get_single_player_name():
    input_name = ""
    screen.fill(GREY)
    display_text("Enter Your Name: ", 100, 200, BLUE)
    pygame.display.flip()
    entering_name = True
    while entering_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    input_name += event.unicode.upper()
        screen.fill(GREY)
        display_text(f"Enter Your Name: {input_name}", 100, 200, BLUE)
        pygame.display.flip()
    return input_name

# Function to ask for player names in multiplayer mode
def get_multiplayer_names():
    player_names = ["", ""]
    for i in range(2):
        input_name = ""
        screen.fill(GREY)
        display_text(f"Enter Player {i+1} Name: ", 100, 200, BLUE)
        pygame.display.flip()
        entering_name = True
        while entering_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        player_names[i] = input_name
                        entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                    else:
                        input_name += event.unicode.upper()
            screen.fill(GREY)
            display_text(f"Enter Player {i+1} Name: {input_name}", 100, 200, BLUE)
            pygame.display.flip()
    return player_names

# Function to show the lose screen
def lose_screen(reason):
    screen.fill(GREY)
    display_text(reason, 100, 100, RED)
    display_text("You lose!", 100, 200, RED)
    display_text("Press 'R' to restart or 'Q' to quit", 100, 300, GREEN)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Function to show the penalty screen
def penalty_screen():
    screen.fill(GREY)
    display_text("You used a letter twice!", 100, 100, RED)
    display_text("5 seconds deducted!", 100, 200, RED)
    display_text("Press any key to continue", 100, 300, GREEN)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Function to calculate points based on word length
def calculate_points(word):
    if len(word) == 3:
        return 2
    elif len(word) == 4:
        return 4
    elif len(word) >= 5:
        return 6
    return 0

def load_valid_words(filepath):
    with open(filepath, 'r') as file:
        valid_words = set(word.strip().upper() for word in file.readlines())
    return valid_words

valid_words = load_valid_words('totalwords.txt')

def is_valid_word(word, valid_words):
    return word in valid_words

# Game function
# Game function
def game(mode):
    letters = generate_letters()
    words = []
    input_word = ''
    current_player = 1
    scores = [0, 0]  # Two players for multiplayer mode

    player_names = ["Player 1", "Player 2"]
    if mode == 'multi':
        player_names = get_multiplayer_names()
    elif mode == 'single':
        player_names[0] = get_single_player_name()

    # Ask for total game time
    total_time = ask_total_time()

    # Enter key handling flag
    enter_pressed = False

    start_time_player1 = time.time()
    start_time_player2 = time.time()

    running = True
    while running:
        screen.fill(GREY)
        if mode == 'single':
            if current_player == 1:
                elapsed_time_player1 = time.time() - start_time_player1
                remaining_time = max(0, total_time - elapsed_time_player1)
            else:
                elapsed_time_player2 = time.time() - start_time_player2
                remaining_time = max(0, total_time - elapsed_time_player2)
        else:
            if current_player == 1:
                elapsed_time_player1 = time.time() - start_time_player1
                remaining_time = max(0, total_time - elapsed_time_player1)
            else:
                elapsed_time_player2 = time.time() - start_time_player2
                remaining_time = max(0, total_time - elapsed_time_player2)

        if remaining_time <= 0:
            running = False

        display_text(f"Time left for {player_names[current_player - 1]}: {int(remaining_time)}", 50, 50, RED)
        display_text("Letters: " + " ".join(letters), 50, 100, GREEN)
        display_text("Input: " + input_word, 50, 150, BLUE)
        display_text(f"{player_names[current_player - 1]}'s Turn", 50, 200, PINK)

        display_text("Words: ", 50, 250, RED)
        for i, word in enumerate(words):
            display_text(word, 50, 300 + i * 30, BLUE)

        display_text(f"Score: {scores[0]}", 600, 50, BLACK)
        if mode == 'multi':
            display_text(f"{player_names[1]}'s Score: {scores[1]}", 600, 100, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not enter_pressed:
                    enter_pressed = True
                    if input_word:
                        if len(input_word) == 2:
                            lose_screen("2-letter words are not allowed!")
                            return
                        # Check if the input_word contains only the provided letters
                        if all(input_word.count(letter) <= letters.count(letter) for letter in input_word):
                            # Check if the word is valid
                            if not is_valid_word(input_word, valid_words):
                                lose_screen("Invalid word!")
                                return
                            # Check for duplicate letters
                            if any(input_word.count(letter) > letters.count(letter) for letter in input_word):
                                penalty_screen()
                                if current_player == 1:
                                    start_time_player1 += 5  # Deduct 5 seconds from the player's time
                                else:
                                    start_time_player2 += 5  # Deduct 5 seconds from the player's time
                                continue
                            words.append(input_word)
                            scores[current_player - 1] += calculate_points(input_word)
                            input_word = ''
                            if mode == 'multi':
                                current_player = 2 if current_player == 1 else 1  # Switch turn between players
                            else:
                                current_player = 1  # In single player, always player 1's turn after each input
                        else:
                            lose_screen("You used invalid letters!")
                            return
                elif event.key == pygame.K_BACKSPACE:
                    input_word = input_word[:-1]
                else:
                    input_word += event.unicode.upper()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    enter_pressed = False

    # Determine the winner or show the player's score in single player mode
    if mode == 'single':
        screen.fill(GREY)
        display_text("Time's up!", 100, 100, RED)
        display_text(f"Your score: {scores[0]}", 100, 250, GREEN)  # Display player's score
        display_text("Press 'R' to restart or 'Q' to quit", 100, 300, GREEN)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()
    else:  # multiplayer mode
        # Determine the winner
        winner = 'Draw'
        if scores[0] > scores[1]:
            winner = f'{player_names[0]} Wins'
        elif scores[1] > scores[0]:
            winner = f'{player_names[1]} Wins'

        screen.fill(GREY)
        display_text("Time's up!", 100, 100, RED)
        display_text(winner, 100, 200, BLUE)
        display_text("Press 'R' to restart or 'Q' to quit", 100, 300, GREEN)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit()


# Main loop
while True:
    mode = splash_screen()
    game(mode)
