import argparse
import random
import time
import msvcrt
from pprint import pprint
from collections import namedtuple
from termcolor import colored
from dicio import short_words
from datetime import datetime
import pygame

#Iniialize pygame
pygame.init()
pygame.mixer.init()

correct_sound = pygame.mixer.Sound ("correct.wav")
incorrect_sound = pygame.mixer.Sound ("incorrect.wav")

# namedtuple for the test statistics
Input = namedtuple('Input', ['letter_shown', 'letter_received', 'duration'])

TestStatistics = namedtuple('TestStatistics', [
    'test_duration',
    'test_start',
    'test_end',
    'number_of_types',
    'number_of_hits',
    'accuracy',
    'type_average_duration',
    'type_hit_average_duration',
    'type_miss_average_duration',
    'inputs'
])

def wait_for_keypress():
    print("Pressione uma tecla para começar o desafio.")
    msvcrt.getch()

def generate_random_input(mode):
    if mode == "char":
        return random.choice('abcdefghijklmnopqrstuvwxyz')
    elif mode == "word":
        words = short_words
        return random.choice(words)

def test(args):
    wait_for_keypress()
    test_start = datetime.now().strftime("%a %b %d %H:%M:%S %Y")

    inputs = []
    start_time = time.time()
    max_time = args.max_value if args.use_time_mode else float('inf')
    max_inputs = args.max_value if not args.use_time_mode else float('inf')

    while True:
        if not args.unlimited:
            if time.time() - start_time > max_time or len(inputs) >= max_inputs:
                break

        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b' ':
                print("Test stopped by user.")
                break

        random_input = generate_random_input("word" if args.use_words else "char")
        print(f"Input: {random_input}")

        user_input = None

        while user_input is None and time.time() - start_time <= max_time:
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode('utf-8').lower()

        if user_input == " ":
            break

        if user_input is None:
            break

        duration = time.time() - start_time
        if args.use_words:
            try:
                inputs.append(Input(letter_shown=len(random_input), letter_received=int(user_input), duration=duration))
            except ValueError:
                print("Invalid input. Please enter a number.", end=" ")
        else:
            inputs.append(Input(letter_shown=random_input, letter_received=user_input, duration=duration))

        if args.use_words:
            try:
                is_correct = int(user_input) == len(random_input)
                if is_correct:
                    print("You typed number", end=" ")
                    print(colored(user_input, "green"))
                    if args.use_sound:
                        correct_sound.play()
                        time.sleep(1)
                else:
                    print("You typed number", end=" ")
                    print(colored(user_input, "red"))
                    if args.use_sound:
                        incorrect_sound.play()
                        time.sleep(1)
            except ValueError:
                print(" ")
        else:
            is_correct = user_input == random_input
            if is_correct:
                print("You typed letter", end=" ")
                print(colored(user_input, "green"))
                if args.use_sound:
                    correct_sound.play()
                    time.sleep(1)
            else:
                print("You typed letter", end=" ")
                print(colored(user_input, "red"))
                if args.use_sound:
                    incorrect_sound.play()
                    time.sleep(1)

    return inputs, test_start

def calculate_test_statistics(args,inputs, test_start):
    inputs2 = inputs.copy()
    
    if not inputs:
        print("No inputs provided.")
        return
    
    for i in range(1, len(inputs)):
        modified_duration = inputs[i].duration - inputs[i - 1].duration
        inputs2[i] = inputs2[i]._replace(duration=modified_duration)

    inputs = inputs2.copy()
    test_start = test_start
    test_end = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    test_start_datetime = datetime.strptime(test_start, "%a %b %d %H:%M:%S %Y")
    test_end_datetime = datetime.strptime(test_end, "%a %b %d %H:%M:%S %Y")
    if args.use_time_mode:
        total_duration = test_end_datetime - test_start_datetime
        total_duration = total_duration.seconds
    else:
        total_duration = 0
        for i in range(0, len(inputs)):
            total_duration += inputs[i].duration
        total_duration = total_duration

    correct_count = sum(1 for i in inputs if i.letter_shown == i.letter_received)
    incorrect_count = len(inputs) - correct_count

    accuracy = correct_count / len(inputs) * 100 if inputs else 0
    #average_duration = total_duration / len(inputs) if inputs else 0

    type_average_duration = sum(i.duration for i in inputs) / len(inputs) if inputs else 0
    type_hit_average_duration = sum(i.duration for i in inputs if i.letter_shown == i.letter_received) / correct_count if correct_count else 0
    type_miss_average_duration = sum(i.duration for i in inputs if i.letter_shown != i.letter_received) / incorrect_count if incorrect_count else 0

    test_stats = TestStatistics(
        test_duration=float(total_duration),
        test_start=test_start,
        test_end=test_end,
        number_of_types=len(inputs),
        number_of_hits=correct_count,
        accuracy=accuracy,
        type_average_duration=type_average_duration,
        type_hit_average_duration=type_hit_average_duration,
        type_miss_average_duration=type_miss_average_duration,
        inputs=inputs
    )

    pprint(test_stats._asdict())  # Use pprint to print the dictionary in a more readable format

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PSR Typing Test")

    parser.add_argument("-utm", "--use_time_mode", action="store_true", help="Use time mode.")
    parser.add_argument("-mv", "--max_value", type=int, help="Max number of seconds for time mode or maximum number of inputs for the number of inputs mode.")
    parser.add_argument("-uw", "--use_words", action="store_true", help="Use word typing mode, instead of single character typing.")
    parser.add_argument("-unlimited", "--unlimited", action="store_true", help="Run the test indefinitely.")
    parser.add_argument("-us", "--use_sound",type=float, help="Use sound on correct and incorrect answers.")

    args = parser.parse_args()

    if args.use_sound :
        if args.use_sound < 0.1 or args.use_sound > 1:
            parser.error("Value of use sound should be between 0 and 1")

    if args.unlimited and args.use_time_mode:
        parser.error("-unlimited and -utm are mutually exclusive.")

    if args.unlimited and args.max_value:
        parser.error("-unlimited and -mv are mutually exclusive.")

    if not args.unlimited and args.max_value is None:
        parser.error("-mv is required unless -unlimited is specified.")

    if args.use_sound:
        correct_sound.set_volume(args.use_sound)
        incorrect_sound.set_volume(args.use_sound)
    inputs, test_start = test(args)
    while inputs == []:
        print("\nTest incomplete. If you want to restart press Y, if not, press any other key")
        choice = msvcrt.getch().decode('utf-8').lower()
        if choice == "y":
            inputs, test_start = test(args)
        else:
            break

    if inputs == []:
        print("\nTest incomplete.")
    else:
        print("\nTest complete.")
    calculate_test_statistics(args, inputs, test_start)
