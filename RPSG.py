import random
import time

print("=== ROCK - PAPER - SCISSORS GAME (WITH HANDS) ===")

choices = ["rock", "paper", "scissors"]

hands = {
    "rock": r"""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""",

    "paper": r"""
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
""",

    "scissors": r"""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""
}

while True:
    user = input("\nEnter your choice (rock/paper/scissors): ").lower()

    if user not in choices:
        print("Invalid choice! Try again.")
        continue

    computer = random.choice(choices)

    print("\nComputer is choosing...")
    time.sleep(1)

    print("\nYou chose:")
    print(hands[user])

    print("Computer chose:")
    print(hands[computer])

    if user == computer:
        print("It's a tie!")
    elif (user == "rock" and computer == "scissors") or \
         (user == "paper" and computer == "rock") or \
         (user == "scissors" and computer == "paper"):
        print("You win! ??")
    else:
        print("You lose! ??")

    again = input("\nPlay again? (yes/no): ").lower()
    if again != "yes":
        print("Thanks for playing!")
        break
