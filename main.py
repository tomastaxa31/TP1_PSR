import argparse
import msvcrt
import random
import time
from termcolor import colored

def wait_for_keypress():
    print("Pressione uma tecla para começar o desafio.")
    msvcrt.getch()

def generate_random_input(mode):
    if mode == "char":
        return random.choice('abcdefghijklmnopqrstuvwxyz')
    elif mode == "word":
        words = ["python", "challenge", "keyboard", "exercise"]
        return random.choice(words)
    
def test(args):
    random_input = generate_random_input("word" if args.use_words else "char")
    print("Input: {}".format(random_input))

    user_input = msvcrt.getch().decode('utf-8').lower()  # Obtém a entrada do utilizador (apenas uma tecla)

    if not args.use_words and user_input != random_input:
        print("You typed letter", end=" ")
        print (colored(user_input, "red"))
    elif not args.use_words and user_input == random_input:
        print("You typed letter", end=" ")
        print (colored(user_input, "green"))

    if args.use_words and int(user_input) == len(random_input):
        print("You typed number", end=" ")
        print (colored(user_input, "green"))
    elif args.use_words and int(user_input) != len(random_input):
        print("You typed number", end=" ")
        print (colored(user_input, "red"))

    return user_input

def main():
    parser = argparse.ArgumentParser(description="Definition of test mode")

    # Argumentos obrigatórios
    parser.add_argument("-utm", "--use_time_mode", action="store_true", help="Use time mode.")
    parser.add_argument("-mv", "--max_value", type=int, help="Max number of seconds for time mode or maximum number of inputs for number of inputs mode.")

    # Argumento opcional
    parser.add_argument("-uw", "--use_words", action="store_true", help="Use word typing mode, instead of single character typing.")

    args = parser.parse_args()

    # Verifica se os argumentos obrigatórios foram fornecidos
    if args.max_value is None:
        parser.error("-mv is required.")

    wait_for_keypress()

    start_time = time.time()
    inputs_count = 0
    #if not args.use_time_mode and inputs_count >= args.max_value:
        #break
    if args.use_time_mode:
        try:
            while time.time() - start_time < args.max_value:
                user_input = test(args)
                if user_input == ' ':
                    break  
                inputs_count += 1
        except KeyboardInterrupt:
            pass 
    else :
        try:
            while inputs_count < args.max_value:
                print("here")
                user_input = test(args)
                if user_input == ' ':
                    break
                inputs_count += 1 
        except KeyboardInterrupt:
            pass  


    print("\nTeste concluído.")
    print("Total de inputs: {}".format(inputs_count))

if __name__ == "__main__":
    main()
