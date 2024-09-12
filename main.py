from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TIMER = None
CURRENT_CARD = {}


def words_ended():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_word, text="You have learned\nall the words\nin flash cards")
    canvas.itemconfig(card_title, text="")


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global TIMER, CURRENT_CARD
    window.after_cancel(TIMER)
    try:
        CURRENT_CARD = random.choice(to_learn)
    except IndexError:
        words_ended()
    else:
        canvas.itemconfig(card_img, image=card_front_img)
        canvas.itemconfig(card_title, text="French", fill="black")
        canvas.itemconfig(card_word, text=CURRENT_CARD["French"], fill="black")
        TIMER = window.after(3000, flip_card)


def flip_card():
    global CURRENT_CARD
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=CURRENT_CARD["English"], fill="white")


def unknown_words():
    to_learn.remove(CURRENT_CARD)
    pandas.DataFrame(to_learn).to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

TIMER = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknown_btn = Button(image=cross_img, command=next_card)
unknown_btn.grid(row=1, column=0)

check_img = PhotoImage(file="images/right.png")
known_btn = Button(image=check_img, command=unknown_words)
known_btn.grid(row=1, column=1)

next_card()

window.mainloop()
