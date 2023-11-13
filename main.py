#TP1 PSR
import argparse
import msvcrt
import random
import time

def wait_for_keypress():
    print("Pressione uma tecla para começar o desafio.")
    msvcrt.getch()

def generate_random_input(mode):
    if mode == "char":
        return random.choice('abcdefghijklmnopqrstuvwxyz')
    elif mode == "word":
        words = ["python", "challenge", "keyboard", "programming", "exercise"]
        return random.choice(words)

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

    try:
        while True:
            if args.use_time_mode and time.time() - start_time > args.max_value:
                break
            elif not args.use_time_mode and inputs_count >= args.max_value:
                break

            random_input = generate_random_input("word" if args.use_words else "char")
            print("Input: {}".format(random_input))

            user_input = msvcrt.getch().decode('utf-8').lower()  # Obtém a entrada do usuário (apenas uma tecla)

            if user_input == ' ':
                break  # Interrompe o teste se o usuário pressionar a tecla "espaço"

            if not args.use_words and user_input != random_input:
                print("Letra incorreta. Tente novamente.") 

            if args.use_words and len(user_input) != len(random_input):
                print("Tamanho incorreto. Tente novamente.")
                continue

            inputs_count += 1

    except KeyboardInterrupt:
        pass  # Captura Ctrl+C para sair graciosamente em sistemas Unix-like

    print("\nTeste concluído.")
    print("Total de inputs: {}".format(inputs_count))

if __name__ == "__main__":
    main()
