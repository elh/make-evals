import json
import random

def main():
    with open("greedy_coins/file.jsonl", "w") as f:
        for _ in range(100):
            cents = random.randint(1, 400)
            quarters = cents // 25
            cents = cents % 25
            dimes = cents // 10
            cents = cents % 10
            nickels = cents // 5
            cents = cents % 5
            pennies = cents

            f.write(json.dumps({
                "input": [
                    {
                        "role": "system",
                        "content": f"Please note: In the following EXERCISE, it is important that you only respond with a single integer."
                    },
                    {
                        "role": "user",
                        "content": f"EXERCISE: What is the fewest total number of quarters, dimes, nickels, and pennies needed to sum to ${quarters * 0.25 + dimes * 0.1 + nickels * 0.05 + pennies * 0.01:.2f}?"
                    }
                ],
                "ideal": str(quarters + dimes + nickels + pennies)
            }) + "\n")

if __name__ == "__main__":
    main()
