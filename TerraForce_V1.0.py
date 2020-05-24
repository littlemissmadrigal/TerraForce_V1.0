import time
import sys
import pygame
import random

# Inventory
inventory = []

fight_metrics = {'guard': 14, 'Blue': 10, 'player': 12}

# Play game (Intro, typing speed, scenes 1 - 5 & outro)

def main():
    # Variable: Player name (collected at prompt)
    global your_name
    your_name = 'Andrea'

    # Variable: Hostility_counter (defines certain events)
    global hostility_counter

    hostility_counter = 0

    # Variable: Writing Speed (pause between character printing)
    global WRITE_SPEED
    WRITE_SPEED = '0.01'

    # Colour clothes - affects final scene choice
    global color_clothes
    color_clothes = 'grey'

    # Intro


    # Gets typing speed for game from user input
    WRITE_SPEED = set_text_speed()

    # Scene 1 - scene-setting

    # Scene 2 - if vegan, acquires gold bracelet


    # Scene 3 - gains item from desk for inventory


    # Scene 4 - very short interlude where you choose to turn left or right out of your room - determines next scene...
    x = play_scene_4()
    if x == True:
        direction = 'right'
    else:
        direction = 'left'

    text_branch = None
    enemy = None

    # Conditions for working out which Scene 5 to play, depending on hostility counter and colour of clothes
    if color_clothes == 'blue' and hostility_counter > 1:
        text_branch = 'scene5.a_dialog.txt'
        enemy = 'guard'
    elif color_clothes == 'blue':
        text_branch = 'scene5.b_dialog.txt'
        enemy = 'guard'
    if color_clothes == 'grey' and hostility_counter > 1:
        text_branch = 'scene5.c_dialog.txt'
        enemy = 'guard'
    elif color_clothes == 'grey':
        text_branch = 'scene5.d_dialog.txt'
        enemy = 'Blue'

    # Scene 5 - battle against chosen NPC
    play_scene_5(text_branch, direction, enemy)

    # Outro - end of chapter
    play_outro()


""" Scenes """
# Text, music & gameplay for Intro
def play_intro():
    background_music("IntroMusic.wav")
    intro_text = compile_scene_text('IntroText')
    time.sleep(1)
    counter = 0

    for value in intro_text:
            for ch in value:
                if ch == '*':
                    print("\n", end = "")
                elif counter < 14:
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    time.sleep(float(WRITE_SPEED)/3)
                else:
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    time.sleep(4 * float(WRITE_SPEED))
            if counter == 19:
                time.sleep(3)
            elif counter > 19:
                time.sleep(0.5)
            counter += 1

    transition(4, 1)

# Text, music & gameplay for Scene 1
def play_scene_1():
    global your_name
    global hostility_counter

    # Queueing music for Scene 1
    background_music("SpaceBackground.wav")

    # Opening text file for Scene 1 dialogue
    scene1_text = compile_scene_text('scene1_dialog')

    # Dialogue Exchange: Intro + Name
    your_name = 'TBC'
    print_from_list(scene1_text, 0, 2)
    your_name = get_name()

    # Dialogue Exchange: Does player want an explanation?
    x = print_from_list(scene1_text, 2, 1)

    # No = skip chunk of dialogue, Yes = in-depth story
    if x == False:
        print_from_list(scene1_text, 3, 1)
    else:
        print_from_list(scene1_text, 4, 3)
        x = print_from_list(scene1_text, 7, 1)
        if x == False:
            print_from_list(scene1_text, 8, 1)
        else:
            print_from_list(scene1_text, 9, 1)

    # Dialogue Exchange: Orientation for ship/rules
    print_from_list(scene1_text, 10, 2)
    int(multi_option_qu(scene1_text, 11, 3, 1))
    print_from_list(scene1_text, 18, 2)
    transition(5, 5)

# Text, music & gameplay for Scene 2
def play_scene_2():
    global your_name

    # Queueing music for Scene 2
    background_music("SpaceBackground2b.wav")

    # Opening text file for Scene 1 dialogue

    scene2_text = compile_scene_text('scene2_dialog')

    # First dialogue
    x = print_from_list(scene2_text, 0, 2)
    if x == True:
        print_from_list(scene2_text, 2, 1)
    else:
        print_from_list(scene2_text, 3, 1)
    print_from_list(scene2_text, 4, 6)
    food_choice = str(multi_option_qu(scene2_text, 9, 3, 1))
    print_from_list(scene2_text, 16, 3)
    transition(5,5)
    if food_choice == '2':
        inventory.append('gold_bracelet')

# Text, music & gameplay for Scene 3
def play_scene_3():
    global your_name
    global hostility_counter
    global color_clothes


    # Queueing music for Scene 1
    background_music("HomeRoom.wav")

    # Opening text file for Scene 1 dialogue
    scene3_text = compile_scene_text('scene3_dialog.txt')

    print_from_list(scene3_text, 0, 2)
    color_clothes = look_around(scene3_text, 3, 'gold_bracelet', inventory, 'chewing_gum', 'bifocals', 'cigarette_lighter', color_clothes, 'blue')
    transition(5, 5)
    return color_clothes

# Text, music & gameplay for Scene 4
def play_scene_4():
    global your_name
    global hostility_counter

    # Queueing music for Scene 1
    pygame.mixer.init()
    pygame.mixer.music.load("WakeUp.wav")
    pygame.mixer.music.play(loops=1)
    time.sleep(3)

    # Opening text file for Scene 1 dialogue
    scene4_text = compile_scene_text('scene4_dialog')
    print_from_list(scene4_text, 0, 2)
    time.sleep(0.5)
    x = two_answer_qu(scene4_text[2], 'right', 'left')
    if x == True:
        print_from_list(scene4_text, 3, 1)
    else:
        print_from_list(scene4_text, 4, 1)
    transition(5, 5)
    return x

# Text, music & gameplay for Scene 5 - 4 potential scenarios, depending on clothes colour and hostility counter
def play_scene_5(text_branch, direction, enemy):
    global hostility_counter
    global color_clothes
    global your_name

    background_music("SneakingInSpaceship1a.wav")
    scene5_text = compile_scene_text(text_branch)
    if direction == 'right':
        print_from_list(scene5_text, 0, 1)
    else:
        print_from_list(scene5_text, 1, 1)
    print_from_list(scene5_text, 2, 3)
    x = fight(0, enemy)
    background_music("SneakingInSpaceship1a.wav")
    if x == True:
        print_from_list(scene5_text, 5, 1)
    elif x == False:
        if 'gold_bracelet' in inventory:
            print_from_list(scene5_text, 7, 1)
        else:
            print_from_list(scene5_text, 6, 1)

    transition(5, 5)

# Text, music & outro
def play_outro():
    background_music("SpaceBackground.wav")
    print_from_string("Thank you for playing the first chapter of TerraForce.\n\nIf you enjoyed today's game, please do follow me on GitHub, and another chapter will be added at a later date.\nHave a good day!")
    transition(10, 10)


""" Other Functions - No User Input Required (Alphabetical)"""

# Loads background music and plays on loop
def background_music(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=-1)
    print("\n\n")
    time.sleep(2)
# Loads text file and appends to a list for easy recall
def compile_scene_text(file):
    name = open(file, encoding='utf-8')
    list = []

    for line in name:
        list.append(line)
    return list

# Prints from text file at specified letter-by-letter speed, converting certain characters to in-game variables, or adding conditions.
''' Key:
. or ! or : = long pause
, or ; = short pause
/ = new line
~ = present Y/N option
@ = your_name
'''
def print_from_list(list, start, rnge):
    global your_name
    name = str(your_name)

    pause = ['.', '!', ':']
    half_pause = [',', ';']


    for i in range(rnge):
        for value in list[start + i]:
            for ch in value:
                if ch == '/':
                    sys.stdout.write("\n")
                elif ch == '~':
                    sys.stdout.write(" (Y/N) ")
                    x = yes_no_qu()
                    return x
                elif ch == '@':
                    for i in range(len(name)):
                        sys.stdout.write(name[i])
                        sys.stdout.flush()
                        time.sleep(WRITE_SPEED)
                else:
                    sys.stdout.write(ch)
                    sys.stdout.flush()
                    time.sleep(WRITE_SPEED)
                if ch in pause:
                    time.sleep(5 * WRITE_SPEED)
                elif ch in half_pause:
                    time.sleep(2.5 * WRITE_SPEED)

# Prints from string at specified letter-by-letter speed, converting certain characters to in-game variables, or adding conditions.
''' Key:
. or ! or : = long pause
, or ; = short pause
/ = new line
~ = present Y/N option
@ = your_name
'''
def print_from_string(string):
    global your_name
    name = str(your_name)

    pause = ['.', '!', ':']
    half_pause = [',', ';']

    for ch in string:
        if ch == '/':
            sys.stdout.write("\n")
        elif ch == '~':
            sys.stdout.write(" (Y/N) ")
            x = yes_no_qu()
            return x
        elif ch == '@':
            for i in range(len(string)):
                sys.stdout.write(name[i])
                sys.stdout.flush()
                time.sleep(WRITE_SPEED)
        else:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(WRITE_SPEED)
        if ch in pause:
            time.sleep(5 * WRITE_SPEED)
        elif ch in half_pause:
            time.sleep(2.5 * WRITE_SPEED)

# Adds pauses and spacing for stylistic printing between scenes
def transition(x, y):
    pygame.mixer.music.fadeout(x * 1000)
    time.sleep(y)
    print("\n\n***\n\n")
    time.sleep(1)


""" Other Functions - User Input Required (Alphabetical) """

# Creates a fight scene between inputted enemy and player.
"""
Each turn consists of the following:
While both players have HP above the specified endpoint:
1. Player chooses to attack (punch or kick) or defend (shield)
2. If attacking, a random damage value is assigned from attack dictionary
3. Text prompt responds accordingly - random choice from relevant list
4. Enemy attacks (randomly chosen punch/kick, plus random damage value assigned from attack dictionary)
5. If player is shielding, enemy damage will be -1
6. Text prompt responds accordingly - random choice from relevant list
Once one player is dead, value is returned (True if player wins, False if player loses)

"""
def fight(endpoint, enemy):
    global your_name
    background_music("FightMusic.wav")
    enemy_hp = fight_metrics[enemy]
    your_hp = fight_metrics['player']

    your_attacks = {'punch': [0, 1, 1, 1, 3, 4], 'kick': [0, 0, 2, 2, 2, 4], 'shield': [0, 0]}
    enemy_attacks = {'punch': [0, 1, 1, 2, 2, 3], 'kick': [0, 1, 1, 2, 4]}
    enemy_attack_list = ['punch', 'kick']
    global your_attack_choice
    your_attack_choice = 'dunno'

    # Maximum values from attack libraries (for prompt purposes)

    your_max_punch = max(your_attacks['punch'])
    your_max_kick = max(your_attacks['kick'])
    enemy_max_punch = max(enemy_attacks['punch'])
    enemy_max_kick = max(enemy_attacks['kick'])

    time.sleep(1)

    # Battle mechanics
    while (int(enemy_hp)) > int(endpoint) and (int(your_hp)) > int(endpoint):

        # Declaring HPs to user
        print("Your HP: " + str(your_hp) + "\n" + enemy.capitalize() + "'s HP: " + str(enemy_hp))
        time.sleep(0.75)

        # Taking player input for attack
        your_attack_choice = input("\n[Pick an attack (punch/kick/shield)] ")
        your_attack_choice = your_attack_choice.lower()
        while your_attack_choice not in your_attacks:
            your_attack_choice = str(input("[Please pick a valid option (punch/kick/shield)] "))
            your_attack_choice = your_attack_choice.lower()

        # Assigning random damage value to player attack, and subtracting from enemy HP
        your_attack_value = random.choice(your_attacks[your_attack_choice])
        your_attack_value = int(your_attack_value)
        enemy_hp -= your_attack_value
        time.sleep(0.5)
        print("\n")

        # Player attack prompts
        random_you_attacks = ["(You " + your_attack_choice + " the " + enemy + " in the stomach. They flinch.",
                              "(You prepare yourself to " + your_attack_choice + " the " + enemy + ", and hit them square in the ribcage.",
                              "(You strike the " + enemy + " in the ribs. They splutter slightly.",
                              "(You flail with panic and manage to " + your_attack_choice + " the " + enemy + "."]
        max_you_attacks = [
            "(You " + your_attack_choice + " the " + enemy + " incredibly hard. They recoil with pain and shock.",
            "(You stealthily shift your centre of balance and " + your_attack_choice + " with all your strength. They howl out in pain."]
        miss_you_attacks = "(You try to " + your_attack_choice + " the " + enemy + " and miss.)"
        shield_yourself = ["(You raise your arms and huddle up into a ball, trying to protect yourself)",
                           "(You shield your face with your hands, trying to lessen the " + enemy + "'s blow)"]

        # Choosing which appropriate prompt to print
        if your_attack_choice == 'punch':
            if your_attack_value == your_max_punch:
                print_from_string(random.choice(max_you_attacks))
            elif your_attack_value == 0:
                print_from_string(miss_you_attacks)
            else:
                print_from_string(random.choice(random_you_attacks))
        elif your_attack_choice == 'kick':
            if your_attack_value == your_max_kick:
                print_from_string(random.choice(max_you_attacks))
            elif your_attack_value == 0:
                print_from_string(miss_you_attacks)
            else:
                print_from_string(random.choice(random_you_attacks))
        elif your_attack_choice == 'shield':
            print_from_string(random.choice(shield_yourself))
        if your_attack_value > 0:
            print_from_string(" You do " + str(your_attack_value) + " damage to the " + enemy + ".)")
        time.sleep(1)

        # If enemy is still alive:
        if int(enemy_hp) > int(endpoint):
            # Enemy chooses attack & attack value (subtracts from player HP)
            enemy_attack_choice = random.choice(enemy_attack_list)
            enemy_attack_value = random.choice(enemy_attacks[enemy_attack_choice])
            if your_attack_choice == 'shield':
                enemy_attack_value -= 1
            your_hp -= enemy_attack_value

            # Enemy attack prompts
            random_enemy_attacks = [
                "/(The " + enemy + " hits you with a " + enemy_attack_choice + " to the solar plexus. You bruise instantly.",
                "/(The " + enemy + " crouches, ready to " + enemy_attack_choice + ". They attack, and hit your hip bone.",
                "/(The " + enemy + " swings wildly and hits you with a " + enemy_attack_choice + ".",
                "/(You barely have time to blink before the " + enemy + " retaliates angrily."]
            max_enemy_attacks = ["/(The " + enemy + " hits you dead in the groin. You scream with agony.",
                                 "/(Before you can move out of the way, the " + enemy + " smashes you hard to the skull./You yell out in pain."]
            miss_enemy_attacks = "/(The " + enemy + " swings to hit you, and misses.)"
            hit_enemy_shield = "/(The " + enemy + " strikes at you. You shield yourself from some of the injury, but not/all of it."
            miss_enemy_shield = "/(The " + enemy + " swings at you, but you block their " + enemy_attack_choice + " successfully)."

            # Choosing which appropriate prompt to print
            if your_attack_choice == 'shield':
                if enemy_attack_value < 1:
                    print_from_string(miss_enemy_shield)
                else:
                    print_from_string(hit_enemy_shield)
            else:
                if enemy_attack_choice == 'punch':
                    if enemy_attack_value == enemy_max_punch:
                        print_from_string(random.choice(max_enemy_attacks))
                    elif enemy_attack_value == 0:
                        print_from_string(miss_enemy_attacks)
                    else:
                        print_from_string(random.choice(random_enemy_attacks))
                if enemy_attack_choice == 'kick':
                    if enemy_attack_value == enemy_max_kick:
                        print_from_string(random.choice(max_enemy_attacks))
                    elif enemy_attack_value == 0:
                        print_from_string(miss_enemy_attacks)
                    else:
                        print_from_string(random.choice(random_enemy_attacks))
            if enemy_attack_value > 0:
                print_from_string(" The " + enemy + " does " + str(enemy_attack_value) + " damage to you.)")

        time.sleep(1)
        print("\n")

    # If player wins, return True; if enemy wins, return False
    if int(enemy_hp) < int(endpoint) + 1:
        pygame.mixer.music.fadeout(3000)
        time.sleep(3)
        return True
    else:
        pygame.mixer.music.fadeout(3000)
        time.sleep(3)
        return False

# Asks for player's name and returns value
def get_name():
    global your_name
    your_name = input("")
    check_name = your_name.isalpha()
    while not check_name:
            your_name = str(input("I know the sedative has not yet entirely worn off, but I really need just your first name, please. "))
            check_name = your_name.isalpha()
    your_name = your_name.capitalize()
    return your_name

# Offers multiple options, and returns answer, modifying hostility counter accordingly
"""
Key:
Option 1: Pacifist option - removes from hostility counter
Option 2: Neutral option - no effect
Option 3: Hostile option - adds to hostility counter
"""
def multi_option_qu(text, start, number, pause):
    global hostility_counter
    questions = []

    time.sleep(pause)

    for i in range(number):
        x = int(i) + 1
        questions.append(str(x))

    for i in range(number):
        x = int(start)+int(i)+1
        print(text[x], end ="")

    choice = str(input())
    while choice not in questions:
        choice = input("Please pick a valid option. ")

    choice = int(choice)
    hostility_counter += (choice - 2)

    print_from_list(text, (start + number + choice), 1)
    return choice

# Offers 4 choices of interaction for user according to input (each can only be played once):
"""
Option 1: Text from narrative - 2 options, dependent on whether player has item1 in their itemlist - back to menu
Option 2: 3 objects presented, player can choose to add one to inventory - back to menu
Option 3: Y/N offered for a scenario - back to menu
Option 4: Text from narrative, scene ends - NO return to menu, function ended

Function returns Question 3 answer

"""
def look_around(text, start, item1, itemlist, q2ch1, q2ch2, q2ch3, qu3_variable, choice_yn):
    global hostility_counter
    questions = []
    answers = []
    time.sleep(1)

    global v
    v = None

    print("[What would you like to do now?]\n")

    for i in range(4):
        x = int(i) + 1
        questions.append(str(x))
        answers.append(text[start + i - 1])

    for i in range(len(answers)):
        print(answers[i], end="")

    choice = str(input())
    chosen_already = []

    while choice != '4':
        while choice in chosen_already:
            choice = str(input("You've already picked this option. Please pick another. "))
        while choice not in questions:
            choice = str(input("Please pick a valid option. "))

        chosen_already.append(choice)

        if choice == '1':
            if item1 not in itemlist:
                print_from_list(text, start + 3, 1)
            else:
                print_from_list(text, start + 4, 1)
            questions.remove('1')

        if choice == '2':
            print_from_list(text, start + 5, 1)
            print('\n[Which would you like to pick?]\n')
            item = str(multi_option_qu(text, start + 5, 3, 0))
            if item == '1':
                inventory.append(q2ch1)
            elif item == '2':
                inventory.append(q2ch2)
            elif item == '3':
                inventory.append(q2ch3)
            questions.remove('2')

        if choice == '3':
            f = print_from_list(text, start + 12, 1)
            if f == True:
                print_from_list(text, start + 13, 1)
                v = choice_yn
            else:
                print_from_list(text, start + 14, 1)
            questions.remove('3')

        print("\n[What would you like to do next?]\n")

        for i in range(len(answers)):
            print(answers[i], end="")

        choice = str(input())

    print_from_list(text, start + 15, 1)
    if v != None:
        qu3_variable = str(v)
        return qu3_variable
    else:
        return qu3_variable

# Sets text speed for entire game
def set_text_speed():
    speedchoices = ['0', '1', '2', '3', '4', '5']
    x = input("On a scale of 1-5, 1 being the fastest, how fast would you like your text to appear? (3 = recommended) ")
    while x not in speedchoices:
        x = input("Please enter a valid number: ")
    x = int(x)
    x *= 0.02

    time.sleep(1)
    print("\n\n***\n\n")
    time.sleep(1)

    return x

# Offers two option question, returning answer
def two_answer_qu(question, answer1, answer2):
    answer1 = str(answer1.lower())
    answer2 = str(answer2.lower())

    x = answer1[0]
    y = answer2[0]

    options = [x, y]

    print("\n" + question)

    z = input()
    z = z.lower()

    while z[0] not in options:
        z = input('Please select a valid option: ')
        z = z.lower()

    if z[0] == str(answer1[0]):
        return True
    else:
        return False

# Presents player with yes/no question, allowing input for 'yes', 'y', 'no', 'n', 'yeah', 'ye', 'nah'.
def yes_no_qu():
    answers = ['yes', 'y', 'no', 'n', 'yeah', 'ye', 'nah']
    x = input()
    x = x.lower()
    while x not in answers:
            x = input("I need a yes/no answer, please. ")
    if x[0] == 'y':
        return True
    else:
        return False


if __name__ == '__main__':
    main()