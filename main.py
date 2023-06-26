import keyboard
import random
import json
from prettytable import PrettyTable

from recorder import ActionRecorder
from replayer import ActionReplayer


def display_menu():
    table = PrettyTable()
    table.field_names = ["Choice", "Action"]
    table.add_row(["1", "Record actions"])
    table.add_row(["2", "Replay actions"])
    table.add_row(["3", "Exit"])
    print(table)


def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            print("Press Ctrl+R to start recording...")
            keyboard.wait("ctrl+r")
            print("Recording actions...")
            recorder = ActionRecorder()
            actions = recorder.record_actions()
            print("Actions recorded.")
            filename = input("Enter the filename to save the actions as JSON: ")
            recorder.save_actions_to_json(filename)
            print(f"Actions saved to {filename}.")
        elif choice == '2':
            print("Press Ctrl+P to start replaying...")
            keyboard.wait("ctrl+p")
            filenames = input("Enter the filenames separated by commas: ").split(",")
            actions = []
            for filename in filenames:
                with open(filename.strip(), 'r') as file:
                    actions.extend(json.load(file))
            # random.shuffle(actions)
            print("Replaying actions...")
            replayer = ActionReplayer(actions)
            replayer.replay_actions()
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    main()


