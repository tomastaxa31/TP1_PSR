# Sound effects

import pygame
import time

#Iniialize pygame
pygame.init()
pygame.mixer.init()

# sound files and their paths from my pc (necessary to change the destination folder in ypour pc)
correct_sound = pygame.mixer.Sound ("/home/achiau/Downloads/tp1_psr_soundeffects/correct.wav")
incorrect_sound = pygame.mixer.Sound ("/home/achiau/Downloads/tp1_psr_soundeffects/incorret.wav")

def play_sound(is_correct):
	if is_correct:
		correct_sound.play()
	else:
		incorrect_sound.play()
		
### Typing test code ....

#Example usage:
user_input = "a"
correct_character = "a"
is_correct = user_input ==correct_character


#Play the corresponding sound
play_sound(is_correct)

#Allow some time fro sound to play (adjust as nedeed)
time.sleep(1) 
