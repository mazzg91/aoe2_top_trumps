import requests
import random


#Opening text file to add scores to later
with open('top_trumps.txt', 'w+') as text_file:
    text_file.write('Top Trumps game scores!' + 2 * '\n')


#Intro and rules of the game
print('Let\'s play Top Trumps! You will draw a random card from the deck and choose a stat to play.' + '\n' + 'The deck of cards we are using is based on the game Age of Empires II. All of the cards drawn will relate to units (mainly military) in the game' + '\n' + 'You will chose a stat to play - hit points, for example - then the computer will draw a card and you will compare the hit points.' + '\n' + 'Whoever has the card with the higher amount of hit points wins the round. Best of three wins the game!' + '\n')



#Variable to select random unit ID number for calling API
random_id = random.randint(1,104)
url = 'https://age-of-empires-2-api.herokuapp.com/api/v1/unit/{}'.format(random_id)
response = requests.get(url)
card = response.json()



#Initial creating of dictionary with blank values to be added to later
stats_dict = {
    # 'Name': '',
    'Line of Sight': '',
    'Attack': '',
    'Melee Armour': '',
    'Pierce Armour': '',
    'Hit Points': '',
}



def draw_card(random_id):
    return card['name']



def create_dict(random_id):
    if 'attack' in card:
        attack = card['attack']
    else:
        attack = 0
    armour_split = card['armor'].split('/')
    stats_dict = {
        # 'Name': card['name'],
        'Line of Sight': card['line_of_sight'],
        'Attack': attack,
        'Melee Armour': armour_split[0],
        'Pierce Armour': armour_split[1],
        'Hit Points': card['hit_points'],
    }

    return str(stats_dict)


#Round 1 of 3
round = 1
print('\n' + 'Round One!')



#User draws a card first
print('You draw a card first!')
print(draw_card(random_id))
print(create_dict(random_id))



#Allowing the user to select which stat they would like to play and saving that information for later
stat_choice = input('Which stat would you like to play? ')

def setting_stat_choice(stat_choice):
    armour_split = card['armor'].split('/')
    if stat_choice == 'Line of Sight':
        chosen_stat = card['line_of_sight']
    elif stat_choice == 'Attack':
        chosen_stat = card['attack']
    elif stat_choice == 'Melee Armour':
        chosen_stat = armour_split[0]
    elif stat_choice == 'Pierce Armour':
        chosen_stat = armour_split[1]
    else:
        chosen_stat = card['hit_points']

    return int(chosen_stat)

user_result = setting_stat_choice(stat_choice)



#Resetting 'random_id' before the computer plays
random_id = random.randint(1,104)
url = 'https://age-of-empires-2-api.herokuapp.com/api/v1/unit/{}'.format(random_id)
response = requests.get(url)
card = response.json()


#Computer draws a card
print('\n')
print('Now it\' the computer\'s turn to draw a card!')
print(draw_card(random_id))
print(create_dict(random_id))


#Comparing the results
def returning_opponent_stat():
    armour_split = card['armor'].split('/')
    if stat_choice == 'Line of Sight':
        opponent_stat = card['line_of_sight']
    elif stat_choice == 'Attack':
        if 'attack' in card:
            opponent_stat = card['attack']
        else:
            opponent_stat = 0
    elif stat_choice == 'Melee Armour':
        opponent_stat = armour_split[0]
    elif stat_choice == 'Pierce Armour':
        opponent_stat = armour_split[1]
    else:
        opponent_stat = card['hit_points']

    return int(opponent_stat)

computer_result = returning_opponent_stat()



def compare_results(round):
    user_score = 0
    computer_score = 0

    if user_result > computer_result:
        user_score += 1
        print('You won this round!')
        with open('top_trumps.txt', 'a') as text_file:
            text_file.write('Round {} results: '.format(round) + '\n')
            text_file.write('    Your score: ' + str(user_score) + '\n')
            text_file.write('    Computer score: ' + str(computer_score) + '\n')
    elif user_result < computer_result:
        computer_score += 1
        print('The computer won this round!')
        with open('top_trumps.txt', 'a') as text_file:
            text_file.write('Round {} results: '.format(round) + '\n')
            text_file.write('    Your score: ' + str(user_score) + '\n')
            text_file.write('    Computer score: ' + str(computer_score) + '\n')
    else:
        print('It\'s a draw!')
        with open('top_trumps.txt', 'a') as text_file:
            text_file.write('Round {} results: '.format(round) + '\n')
            text_file.write('    Your score: ' + str(user_score) + '\n')
            text_file.write('    Computer score: ' + str(computer_score) + '\n')



compare_results(round)



#Start of Round 2
round = 2
print('\n')
print('Round 2: ')
print('This time the computer will draw first!')


#Resetting random_id again
random_id = random.randint(1,104)
url = 'https://age-of-empires-2-api.herokuapp.com/api/v1/unit/{}'.format(random_id)
response = requests.get(url)
card = response.json()


#Computer draws a card
print(draw_card(random_id))
print(create_dict(random_id))


#Computer selects a stat to play
stats_selection = ['Line of Sight', 'Attack', 'Melee Armour', 'Hit Points']
stat_choice = random.choice(stats_selection)

print('The computer chose to play: ' + stat_choice)

computer_result = setting_stat_choice(stat_choice)


#Resetting random_id again
random_id = random.randint(1,104)
url = 'https://age-of-empires-2-api.herokuapp.com/api/v1/unit/{}'.format(random_id)
response = requests.get(url)
card = response.json()

#User selects a card
print('\n')
print('Now you draw a card!')
print(draw_card(random_id))
print(create_dict(random_id))

#Result is returned, based on the stat the computer chooses
user_result = returning_opponent_stat()


#Results are compared
compare_results(round)
print('\n')


#Check to see if there is a winner after 2 rounds
with open('top_trumps.txt', 'r+') as text_file:
    winner_check = text_file.read()
    user_score_check = winner_check.count('    Your score: 1' )
    computer_score_check = winner_check.count('    Computer score: 1')
    # print(user_score_check)
    # print(computer_score_check)
    if user_score_check == 2 and computer_score_check < 2:
        print('You have won the game!')
        text_file.write('You have won the game!')
        exit()
    elif user_score_check < 2 and computer_score_check == 2:
        print('The computer has won the game!')
        text_file.write('The computer has won the game!')
        exit()
    else:
        print('Last round!')



#Start of Round 3 (if applicable)
round = 3
print('Round Three:')
print('You draw a card first!')


#User draws card and selects a stat to play
print(draw_card(random_id))
print(create_dict(random_id))

stat_choice = input('Which stat would you like to play? ')

user_result = setting_stat_choice(stat_choice)



#Resetting 'random_id' before the computer plays
random_id = 0
random_id = random.randint(1,104)
url = 'https://age-of-empires-2-api.herokuapp.com/api/v1/unit/{}'.format(random_id)
response = requests.get(url)
card = response.json()


#Computer draws a card
print('\n')
print('Now it\' the computer\'s turn to draw a card!')
print(draw_card(random_id))
print(create_dict(random_id))

computer_result = returning_opponent_stat()


#Results are compared
compare_results(round)
print('\n')


#Final result after 3 Rounds
with open('top_trumps.txt', 'r+') as text_file:
    winner_check = text_file.read()
    user_score_check = winner_check.count('    Your score: 1' )
    computer_score_check = winner_check.count('    Computer score: 1')
    # print(user_score_check)
    # print(computer_score_check)
    if user_score_check > computer_score_check:
        print('You have won the game!')
        text_file.write('\n' + 'You have won the game!')
        exit()
    elif user_score_check < computer_score_check:
        print('The computer has won the game!')
        text_file.write('\n' + 'The computer has won the game!')
        exit()
    else:
        print('It\' a draw!')
        text_file.write('\n' + 'It\' a draw!')