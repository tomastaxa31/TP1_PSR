import argparse
import random
import time
import msvcrt
from pprint import pprint
from collections import namedtuple
from termcolor import colored
from dicio import short_words
from datetime import datetime

#  namedtuple for the test statistics
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
        if time.time() - start_time > max_time or len(inputs) >= max_inputs:
            break

        random_input = generate_random_input("word" if args.use_words else "char")
        print(f"Input: {random_input}")

        user_input = msvcrt.getch().decode('utf-8').lower()

        duration = time.time() - start_time
        if args.use_words:
            inputs.append(Input(letter_shown=len(random_input), letter_received=int(user_input), duration=duration))
        else:
            inputs.append(Input(letter_shown=random_input, letter_received=user_input, duration=duration))

        if user_input == ' ':
            break

        if args.use_words:
            print(user_input)
            print(len(random_input))
            is_correct = int(user_input) == len(random_input)
            if is_correct:
                print("You typed number", end=" ")
                print(colored(user_input, "green"))
            else:
                print("You typed number", end=" ")
                print(colored(user_input, "red"))
        else :
            is_correct = user_input == random_input
            if is_correct:
                print("You typed letter", end=" ")
                print(colored(user_input, "green"))
            else:
                print("You typed letter", end=" ")
                print(colored(user_input, "red"))

    return inputs,test_start

def calculate_test_statistics(inputs,test_start):
    if not inputs:
        print("No inputs provided.")
        return
    
    test_start = test_start
    test_end = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    total_duration = inputs[-1].duration - 0.0

    correct_count = sum(1 for i in inputs if i.letter_shown == i.letter_received)
    incorrect_count = len(inputs) - correct_count

    accuracy = correct_count / len(inputs) * 100 if inputs else 0
    average_duration = total_duration / len(inputs) if inputs else 0

    type_average_duration = sum(i.duration for i in inputs) / len(inputs) if inputs else 0
    type_hit_average_duration = sum(i.duration for i in inputs if i.letter_shown == i.letter_received) / correct_count if correct_count else 0
    type_miss_average_duration = sum(i.duration for i in inputs if i.letter_shown != i.letter_received) / incorrect_count if incorrect_count else 0

    test_stats = TestStatistics(
        test_duration=total_duration,
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

    args = parser.parse_args()

    if args.max_value is None:
        parser.error("-mv is required.")


    inputs,test_start = test(args)

    print("\nTest completed.")
    calculate_test_statistics(inputs,test_start)
