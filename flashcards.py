import json
import os.path
import io
import argparse


def print_message_and_log(message, output):
    print(message)
    output.write(message + "\n")


def input_message_and_log(output):
    message = input()
    output.write(message + "\n")
    return message


def import_from_file(filename, cards_dict, output):
    if not os.path.exists(filename):
        print_message_and_log("File not found.\n", output)
        return None

    with open(filename, "r") as file:
        file_data = file.read()
        json_data = json.loads(file_data)
        for key, value in json_data.items():
            cards_dict[key] = value
        print_message_and_log(f"{len(json_data.keys())} cards have been loaded.\n", output)

    return True


def export_data_to_file(filename, cards_dict, output):
    json_data = json.dumps(cards_dict)
    with open(filename, "w") as file:
        file.write(json_data)
    print_message_and_log(f"{len(cards_dict.keys())} cards have been saved.\n", output)


cards_dict = dict()
output = io.StringIO()

parser = argparse.ArgumentParser()

parser.add_argument("--import_from")
parser.add_argument("--export_to")

try:
    args = parser.parse_args()
except:
    pass

import_filename = args.import_from
export_filename = args.export_to

if not import_filename is None:
    import_from_file(import_filename, cards_dict, output)

while True:

    print_message_and_log("Input the action (add, remove, import, export, "
                              "ask, exit, log, hardest card, reset stats):", output)


    action = input_message_and_log(output)

    if action == "exit":
        print_message_and_log("Bye bye!", output)
        if not export_filename is None:
            export_data_to_file(export_filename, cards_dict, output)
        break
    elif action == "add":
        print_message_and_log("The card:", output)
        while True:
            term = input_message_and_log(output)
            if term in cards_dict.keys():
                print_message_and_log(f"The card \"{term}\" already exists. Try again:", output)
            else:
                break
        print_message_and_log("The definition of the card:", output)

        while True:
            definition = input_message_and_log(output)
            found = False
            for value in cards_dict.values():
                if value["definition"] == definition:
                    found = True
                    print_message_and_log(f"The definition \"{definition}\" already exists. Try again:", output)
                    break
            if not found:
                break

        value = {"definition": definition, "mistakes": 0}
        cards_dict[term] = value

        print_message_and_log(f"The pair (\"{term}\":\"{definition}\") has been added.\n", output)
    elif action == "remove":
        print_message_and_log("Which card?", output)
        term = input_message_and_log(output)
        if term in cards_dict:
            cards_dict.pop(term)
            print_message_and_log("The card has been removed.\n", output)
        else:
            print_message_and_log(f"Can't remove \"{term}\": there is no such card.\n", output)
    elif action == "import":
        print_message_and_log("File name:", output)
        filename = input_message_and_log(output)
        success = import_from_file(filename, cards_dict, output)
        if not success:
            continue

    elif action == "export":
        print_message_and_log("File name:", output)
        filename = input_message_and_log(output)
        export_data_to_file(filename, cards_dict, output)

    elif action == "ask":
        print_message_and_log("How many times to ask?", output)
        n = int(input())
        list_of_cards = list(cards_dict.keys())
        num_of_card = 0
        for i in range(n):
            term = list_of_cards[num_of_card]
            print_message_and_log(f"Print the definition of \"{term}\":", output)
            answer = input()
            value = cards_dict[term]
            correct_answer = value["definition"]
            if answer == correct_answer:
                print_message_and_log("Correct!", output)
            else:
                value["mistakes"] += 1
                another_term = None
                for key, value in cards_dict.items():
                    if value["definition"] == answer:
                        another_term = key
                        break
                if another_term is None:
                    print_message_and_log(f"Wrong. The right answer is \"{correct_answer}\"", output)
                else:
                    message = f"Wrong. The right answer is \"{correct_answer}\", but your definition is correct for \"{another_term}\""
                    print_message_and_log(message, output)

            num_of_card += 1
            if num_of_card == len(list_of_cards):
                num_of_card = 0

    elif action == "hardest card":
        max_mistakes = -1
        for key, value in cards_dict.items():
            if value["mistakes"] > 0 and value["mistakes"] > max_mistakes:
                max_mistakes = value["mistakes"]
        hardest_cards = []
        for key, value in cards_dict.items():
            if value["mistakes"] == max_mistakes:
                hardest_cards.append(key)
        if len(hardest_cards) == 1:
            message = f"The hardest card is \"{hardest_cards[0]}\". " \
                      f"You have {max_mistakes} errors answering it.\n"
            print_message_and_log(message, output)
        elif len(hardest_cards) > 1:
            desc = ""
            for card in hardest_cards:
                if desc == "":
                    desc += f"{card}"
                else:
                    desc += f", {card}"
            message = f"The hardest cards are {desc}. You have 10 errors answering them.\n"
            print_message_and_log(message, output)
        else:
            message = "There are no cards with errors.\n"
            print_message_and_log(message, output)

    elif action == "reset stats":
        for key, value in cards_dict.items():
            value["mistakes"] = 0
        message = "Card statistics have been reset.\n"
        print_message_and_log(message, output)

    elif action == "log":
        print_message_and_log("File name:", output)
        filename = input()
        with open(filename, "w") as file:
            file.write(output.getvalue())
        print_message_and_log("The log has been saved.\n", output)
