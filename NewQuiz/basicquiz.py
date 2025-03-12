import pygame
pygame.mixer.init()
import tkinter as tk
# Load and play background music
pygame.mixer.music.load("launch_menu.wav")  # Load the music file
pygame.mixer.music.play(-1)  # -1 makes it loop forever
correct_sound = pygame.mixer.Sound("correct!.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")
timeout_sound = pygame.mixer.Sound("timeout.wav")
complete_sound = pygame.mixer.Sound("complete.wav")
# Create main window
root = tk.Tk()
root.title("Yes/No Quiz")
root.geometry("500x300")

# Questions and responses with correct answers
questions = [
    ("Do you know my name?", "yes", "Cool!", "It's alright! My name is Omer."),
    ("Do you play games?", "no","Good to see! ", "Hopefully not in excess mate... Oh wait..."),
    ("Is history interesting?", "yes", "Awesome! History is cool! ", "I guess everyone has their own interests huh..."),
    ("Should you judge people on personality?", "yes", "This shows you are capable of doing good in the real world... ", "Looks don't define a person... "),
    ("Would you like to build apps?", "yes", "That’s the spirit! ", "Maybe you’ll find it fun one day! "),
    ("Did you enjoy this?", "yes", "Well thank you!", "Well at least I wasted your time...")
]

# Track current question, score, and high score
current_question = 0
score = 0
high_score = 0  # Track best score

timer = None
TIME_LIMIT = 10  # Time per question in seconds

# Labels
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 12, "bold"))
score_label.pack(pady=5)

high_score_label = tk.Label(root, text=f"High Score: {high_score}", font=("Arial", 10))
high_score_label.pack(pady=5)

question_label = tk.Label(root, text=questions[current_question][0], font=("Arial", 14), wraplength=350)
question_label.pack(pady=10)

response_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
response_label.pack(pady=5)

timer_label = tk.Label(root, text=f"Time left: {TIME_LIMIT}s", font=("Arial", 12), fg="blue")
timer_label.pack(pady=5)

# Function to handle Yes/No response
def respond(choice):
    global current_question, score, high_score, timer
    root.after_cancel(timer)  # Cancel the timer if user responds in time
    yes_button.config(state=tk.DISABLED)
    no_button.config(state=tk.DISABLED)
    correct_answer = questions[current_question][1]
    if choice == correct_answer:
        score += 1
        response_label.config(text=questions[current_question][2], fg="green")
        correct_sound.play()  # 🔊 Play correct sound
    else:
        response_label.config(text=questions[current_question][3], fg="red")
        wrong_sound.play()  # 🔊 Play wrong sound

    score_label.config(text=f"Score: {score}")
    root.after(1500, next_question)

# Function to update the timer
def update_timer(time_left):
    global timer
    if time_left > 0:
        timer_label.config(text=f"Time left: {time_left}s")
        timer = root.after(1000, update_timer, time_left - 1)
    else:
        response_label.config(text="Time's up! ⏳", fg="red")
        timeout_sound.play()  # 🔊 Play timeout sound
        yes_button.config(state=tk.DISABLED)
        no_button.config(state=tk.DISABLED)
        root.after(1500, next_question)

# Function to load the next question
def next_question():
    global current_question, score, high_score
    current_question += 1
    yes_button.config(state=tk.NORMAL)
    no_button.config(state=tk.NORMAL)
    if current_question < len(questions):
        question_label.config(text=questions[current_question][0])
        response_label.config(text="")
        update_timer(TIME_LIMIT)  # Start timer for new question
    else:
        pygame.mixer.music.stop()  # 🔇 Stop background music
        complete_sound.play(loops=-1) # Play complete music.
        if score > high_score:
            high_score = score
            high_score_label.config(text=f"High Score: {high_score}")
            question_label.config(text=f"Quiz Complete! 🎉\nNew High Score: {score}/{len(questions)}")
        else:
            question_label.config(text=f"Quiz Complete! 🎉\nFinal Score: {score}/{len(questions)}")
        
        response_label.config(text="")
        timer_label.config(text="")
        yes_button.pack_forget()
        no_button.pack_forget()
        restart_button.pack(pady=10)

# Function to restart the quiz
def restart_quiz():
    global current_question, score
    score = 0
    current_question = 0
    pygame.mixer.stop()  # 🔇 Stop all sounds, including victory music
    pygame.mixer.music.play(-1)  # 🎵 Restart background music
    score_label.config(text=f"Score: {score}")
    question_label.config(text=questions[current_question][0])
    response_label.config(text="")
    restart_button.pack_forget()
    yes_button.pack(pady=5)
    no_button.pack(pady=5)
    update_timer(TIME_LIMIT)

# Buttons
yes_button = tk.Button(root, text="Yes", command=lambda: respond("yes"), width=10, bg="lightgreen")
yes_button.pack(pady=5)

no_button = tk.Button(root, text="No", command=lambda: respond("no"), width=10, bg="salmon")
no_button.pack(pady=5)

restart_button = tk.Button(root, text="Restart", command=restart_quiz, width=10, bg="lightblue")
music_playing = True  # Track music state

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.pause()  # Pause music
        complete_sound.stop()
        music_button.config(text="Unmute Music")
    else:
        pygame.mixer.music.unpause()  # Resume music
        if not (current_question < len(questions)):
           complete_sound.play(-1)
        music_button.config(text="Mute Music")
    
    music_playing = not music_playing  # Toggle state

# Start first question timer
update_timer(TIME_LIMIT)

music_button = tk.Button(root, text="Pause Music", command=toggle_music, width=15, bg="lightgray")
music_button.pack(pady=5)

# Run the application
root.mainloop()
