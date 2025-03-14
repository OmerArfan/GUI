import tkinter as tk
import random
import pygame
root = tk.Tk()
pygame.mixer.init()
root.title("Math Quiz!")
pygame.mixer.music.load("launch_menu.wav")  # Load the music file
pygame.mixer.music.play(-1)  # -1 makes it loop forever
correct_sound = pygame.mixer.Sound("correct!.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")
timeout_sound = pygame.mixer.Sound("timeout.wav")
time_left = 10  
timer_id = None  
score = 0  # Track correct answers
difficulty = 1  # Start at Level 1
launch_file = True
current_audio = {"file": None}
def is_specific_audio_playing(filename):
    """Check if the given audio file is playing."""
    return pygame.mixer.music.get_busy() and current_audio["file"] == filename
# to generate a question
def generate_question():
    global VALUE1, VALUE2, correct_answer, score, operation, time_left, timer_id, difficulty, launch_file
    check_button.config(state=tk.NORMAL)
    if score == 0: 
        difficulty = 1 #to make sure the difficulty is reset as score is reset
    difficulty = 1 + (score // 5)
    # Increase difficulty every 5 correct answers
    if score == 0 and not launch_file: # to play soundtrack if lost 
     pygame.mixer.music.stop()
     pygame.mixer.music.load("launch_menu.wav")    
     pygame.mixer.music.play(-1)  # -1 makes it loop forever
    if score == 10:
     pygame.mixer.music.stop()
     pygame.mixer.music.load("green_menu.wav")    
     pygame.mixer.music.play(-1)  # -1 makes it loop forever
     launch_file = False
    if score == 30:
     pygame.mixer.music.stop()
     pygame.mixer.music.load("grinding_menu.wav")    
     pygame.mixer.music.play(-1)  # -1 makes it loop forever
    if score == 50:
     pygame.mixer.music.stop()
     pygame.mixer.music.load("ultra_grinding_menu.wav")    
     pygame.mixer.music.play(-1)  # -1 makes it loop forever
    # Randomly select an operation
    operation = random.choice(["+", "-", "*", "/"])

    # Adjust number ranges based on difficulty
    if operation == "+":
        VALUE1 = random.randint(1, 10 * difficulty)
        VALUE2 = random.randint(1, 10 * difficulty)
        correct_answer = VALUE1 + VALUE2
    elif operation == "-":
        VALUE1 = random.randint(5 * difficulty, 10 * difficulty)  # Ensure non-negative result
        VALUE2 = random.randint(1, VALUE1)
        correct_answer = VALUE1 - VALUE2
    elif operation == "*":
        VALUE1 = random.randint(2, 5 * difficulty)
        VALUE2 = random.randint(2, 5 * difficulty)
        correct_answer = VALUE1 * VALUE2
    elif operation == "/":
        VALUE2 = random.randint(2, 5 + difficulty)  # Avoid division by zero
        correct_answer = random.randint(2, 5 + difficulty)
        VALUE1 = VALUE2 * correct_answer  # Ensures whole number division

    # Update the label with the new question
    label.config(text=f"What is {VALUE1} {operation} {VALUE2}? (Level {difficulty})")
    entry.delete(0, tk.END)  # Clear entry box
    output_label.config(text="")  # Clear previous result
    time_left = 10  # Reset timer
    timer_label.config(text=f"Time left: {time_left} sec")

    if timer_id:  # Cancel existing timer
        root.after_cancel(timer_id)

    countdown()  # Start countdown again


def check_input():
    global time_left, score, difficulty

    if time_left > 0:  # Only check if time remains
        user_input = entry.get().strip()
        try:
            user_input = int(user_input)  # Convert to integer
            if user_input == correct_answer:
                score += 1  # Increase score if correct
                output_label.config(text=f"Correct! Score: {score}", fg="green")
                check_button.config(state=tk.DISABLED)
                correct_sound.play()
            else:
                score = 0  # Reset score if wrong
                check_button.config(state=tk.DISABLED)
                output_label.config(text=f"Wrong! Correct: {correct_answer}. Score Reset!", fg="red")
                wrong_sound.play()
            root.after(1000, generate_question)  # Wait 1 sec then new question
        except ValueError:
            output_label.config(text="Invalid input! Enter a whole number.", fg="orange")
#way to update the timer

def countdown():
    global time_left, timer_id, score
    if timer_id:
        root.after_cancel(timer_id)  # Cancel previous countdown
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time left: {time_left} seconds")
        timer_id = root.after(1000, countdown)  # Store timer reference
    else:
        score = 0 # reset score if time out
        output_label.config(text=f"Time’s up! Correct: {correct_answer}. Score reset!", fg="red")
        timeout_sound.play()
        check_button.config(state=tk.DISABLED)
        root.after(1000, generate_question)  #to generate new question

#User Interface
label = tk.Label(root, text="What is ? + ?", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

output_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
output_label.pack(pady=5)

timer_label = tk.Label(root, text=f"Time left: {time_left} seconds", font=("Arial", 12), fg="black")
timer_label.pack(pady=5)

check_button = tk.Button(root, text="Check Answer", command=check_input)
check_button.pack(pady=5)

# Start the game
generate_question()  # First question

root.mainloop()
