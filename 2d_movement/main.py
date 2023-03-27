import json
import random

def main():
    with open("2d_movement/file.jsonl", "w") as f:
        # the first handwritten one
        hand_written = {
            "input": [
                {
                    "role": "system",
                    "content": "Please note: In the following EXERCISE, it is important that you only respond with a single line in the format (x, y). Imagine you are standing in a 2D coordinate grid at (0, 0) where coordinates are represented like (x, y). You are currently facing the positive y direction."
                },
                {
                    "role": "user",
                    "content": "EXERCISE: If you take 5 steps forward, turn left, take 2 steps forward, turn left, take 1 step backward, turn left, take two steps backward, what coordinate are you at?"
                }
            ],
            "ideal": "(-4, 6)"
        }
        f.write(json.dumps(hand_written) + "\n")

        lens = ([2] * 9) + ([4] * 20) + ([6] * 20) + ([8] * 20) + ([10] * 20) + ([12] * 10)
        # lens = ([2] * 9)
        for l in lens:
            steps = []
            current = (0, 0)
            current_direction = (0, 1)

            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # idx++ to rotate right

            for _ in range(l):
                action = random.randint(1, 4)
                action_magnitude = random.randint(1, 5)
                match action:
                    case 1: # step forward
                        current = (current[0] + current_direction[0] * action_magnitude, current[1] + current_direction[1] * action_magnitude)
                        if action_magnitude == 1:
                            steps.append(f"take 1 step forward")
                        else:
                            steps.append(f"take {action_magnitude} steps forward")
                    case 2: # step backward
                        current = (current[0] - current_direction[0] * action_magnitude, current[1] - current_direction[1] * action_magnitude)
                        if action_magnitude == 1:
                            steps.append(f"take 1 step backward")
                        else:
                            steps.append(f"take {action_magnitude} steps backward")
                    case 3: # turn left
                        current_direction = directions[(directions.index(current_direction) - 1) % len(directions)]
                        steps.append(f"turn 90 degrees left")
                    case 4: # turn right
                        current_direction = directions[(directions.index(current_direction) + 1) % len(directions)]
                        steps.append(f"turn 90 degrees right")

            line = {
                "input": [
                    {
                        "role": "system",
                        "content": "Please note: In the following EXERCISE, it is important that you only respond with a single line in the format (x, y). Imagine you are standing in a 2D coordinate grid at (0, 0) where coordinates are represented like (x, y). You are currently facing the positive y direction."
                    },
                    {
                        "role": "user",
                        "content": "EXERCISE: If you " + ", then ".join(steps) + f", what coordinate are you at?"
                    }
                ],
                "ideal": str(current)
            }
            f.write(json.dumps(line) + "\n")

if __name__ == "__main__":
    main()
