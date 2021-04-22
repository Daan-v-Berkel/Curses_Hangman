import curses
import json
from curses import textpad
import string
import random

'''
Initializing menus and others
'''
main_menu = ['Play', 'High Scores', 'Settings', 'Exit']
settings_menu = {'difficulty': ['easy', 'medium', 'hard'], 'screen flashing': ['ON', 'OFF'], 'word subjects': ['Animals', 'Foods', 'Brands']}
words = {'Animals':['horse', 'hippopotamus', 'crocodile'], 'Foods':['pancakes', 'lasagna', 'pizza', 'cake'], 'Brands':['peugeot', 'mercedes', 'kelloggs', 'apple']}

settings = {
    'difficulty': 1,
    'screen flashing': 0,
    'word subjects': 1
    }

high_scores = {
    1:  ['PancakeFear', 10]
    2:  ['rawrpie', 9]
    3:  ['HazuHaku', 8]
    4:  ['jan', 7]
    5:  ['piet', 6]
    6:  ['dirk', 5]
    7:  ['greetje', 4]
    8:  ['mark', 3]
    9:  ['fleichmeister', 2]
    10: ['computer-3', 1]
}

'''
name says it, prints the main menu to the screen. index is udes to highlight selected lines
'''
def print_main_menu(screen, main_menu_idx):

    screen.clear()
    
    y, x = screen.getmaxyx()
    y += 5

    x_main = x//2 - len('#   #  ###  #   #  ###  #   #  ###  #   #')//2

    win = curses.newwin(7, len('#   #  ###  #   #  ###  #   #  ###  #   #')+4, 1, x_main)
    win.border()

    win.attron(curses.color_pair(2))
    win.addstr(1, 2, '#   #  ###  #   #  ###  #   #  ###  #   #')
    win.addstr(2, 2, '#   # #   # ##  # #   # ## ## #   # ##  #')
    win.addstr(3, 2, '##### ##### # # # #     # # # ##### # # #')
    win.addstr(4, 2, '#   # #   # #  ## #  ## #   # #   # #  ##')
    win.addstr(5, 2, '#   # #   # #   #  #### #   # #   # #   #')
    win.attroff(curses.color_pair(2))
    
    for idx, word in enumerate(main_menu):
        y_pos = y//2 - len(main_menu)//2 + idx
        x_pos = x//2 - len(word)//2
        
        if idx == main_menu_idx:
            screen.addstr(y_pos,x_pos-4, '--> ')
            screen.attron(curses.color_pair(1))
            screen.addstr(y_pos, x_pos, word)
            screen.attroff(curses.color_pair(1))
            screen.addstr(y_pos, x_pos+len(word), ' <--')
        else:
            screen.addstr(y_pos, x_pos, word)
    
    screen.refresh()
    win.refresh()

'''
name says it, prints the sttings menu to the screen.
this also handles setting a selected option to the option of choice.
'''
def print_settings_menu(screen, settings_menu_idx, settings_file=None, selected=False):
    #if not settings file is found on the system, it uses standard settings.
    if not settings_file:
        settings_file = settings

    screen.clear()
    
    y, x = screen.getmaxyx()
    y +=5

    x_main = x//2 - len(' #### ##### ##### ##### ## #   #  ###   ####')//2

    win = curses.newwin(7, len(' #### ##### ##### ##### ## #   #  ###   ####')+4, 1, x_main)
    win.border()

    win.attron(curses.color_pair(2))
    win.addstr(1, 2, ' #### ##### ##### ##### ## #   #  ###   ####')
    win.addstr(2, 2, '#     #       #     #      ##  # #   # #    ')
    win.addstr(3, 2, ' ###  ####    #     #   ## # # # #      ### ')
    win.addstr(4, 2, '    # #       #     #   ## #  ## #  ##     #')
    win.addstr(5, 2, '####  #####   #     #   ## #   #  #### #### ')
    win.attroff(curses.color_pair(2))

    title_string = "Use [ENTER] to select and the [ARROW] keys to navigate"
    title_string2 = "Press [ESC] to save and return to the main menu"
    title_string3 = "Press ['R'] at any time to revert to default settings"
    y_pos = y//2 - len(settings_menu)//2 -5
    x_pos = x//2 - len(title_string)//2
    screen.addstr(y_pos, x_pos, title_string)
    y_pos = y//2 - len(settings_menu)//2 -4
    x_pos = x//2 - len(title_string2)//2
    screen.addstr(y_pos, x_pos, title_string2)
    y_pos = y//2 - len(settings_menu)//2 -3
    x_pos = x//2 - len(title_string3)//2
    screen.addstr(y_pos, x_pos, title_string3)
    
    # handles the menu when no option is selected (browsing trough)

    if not selected:
        for key, value in settings_menu.items():
            key_to_print = key + ":"
            value_to_print = ''
            for i in range(len(value)-1):
                value_to_print += value[i] + ' | '
            value_to_print += value[-1]
            idx = list(settings_menu).index(key)
            y_pos = y//2 - len(settings_menu)//2 + idx
            x_pos = x//2 - (len(key_to_print) + len(value_to_print))//2
            
            if idx == settings_menu_idx:
                screen.addstr(y_pos,x_pos-4, '--> ')
                screen.attron(curses.color_pair(1))
                screen.addstr(y_pos, x_pos, key_to_print)
                screen.attroff(curses.color_pair(1))
                screen.addstr(y_pos, x_pos+len(key_to_print), ' ' + value_to_print)
                screen.addstr(y_pos, x_pos+len(' ' + key_to_print + value_to_print), ' <--')
            else:
                screen.addstr(y_pos, x_pos, key_to_print + ' ' +  value_to_print)
    
    # handles the menu when an option is selected to change it.

    else:
        current_setting = settings_file[list(settings_menu.keys())[settings_menu_idx]]

        for key, value in settings_menu.items():
            key_to_print = key +': '
            value_to_print = ''
            for i in range(len(value)-1):
                value_to_print += value[i] + ' | '
            value_to_print += value[-1]

            idx = list(settings_menu).index(key)
            y_pos = y//2 - len(settings_menu)//2 + idx
            x_pos = x//2 - (len(key_to_print) + len(value_to_print))//2
            
            highlighted = value[settings_file[key]]
            start = key_to_print
            end = ''
            ls = list(range(current_setting))
            le = list(range(current_setting+1, len(value)))
            if ls:
                for i in ls:
                    start += value[i] + ' | '
            if le:
                for i in le:
                    if i == le[-1]:
                        end += value[i]
                    else:
                        end += value[i] + ' | '

            if idx == settings_menu_idx:
                screen.addstr(y_pos,x_pos-4, '--> ' + start)
                screen.attron(curses.color_pair(1))
                screen.addstr(y_pos, x_pos + len(start), highlighted)
                screen.attroff(curses.color_pair(1))
                if end == '':
                    screen.addstr(y_pos, x_pos+len(start + highlighted), ' <--')
                else:
                    screen.addstr(y_pos, x_pos+len(start + highlighted), ' | ' + end + ' <--')

            else:
                screen.addstr(y_pos, x_pos, key_to_print + value_to_print)
    
    screen.refresh()
    win.refresh()

def print_High_Scores_menu(screen, i):
    screen.clear()

    y, x, = screen.getmaxyx()
    y += 5
    title_length = len('#   # ##  ###  #   #   ####  ###   ###  ####  #####  ####')+4
    x_main = x//2 - title_length//2

    win = curses.newwin(7, title_length, 1, x_main)
    win.border()

    win.attron(curses.color_pair(i))
    win.addstr(1, 2, '#   # ##  ###  #   #   ####  ###   ###  ####  #####  ####')
    win.addstr(2, 2, '#   #    #   # #   #  #     #   # #   # #   # #     #    ')
    win.addstr(3, 2, '##### ## #     #####   ###  #     #   # # ##  ####   ### ')
    win.addstr(4, 2, '#   # ## #  ## #   #      # #   # #   # #   # #         #')
    win.addstr(5, 2, '#   # ##  ###  #   #  ####   ###   ###  #   # ##### #### ')
    win.attroff(curses.color_pair(i))

    y_table = y//2 - 6
    x_table = x_main
    table_rows = 17
    table_col = title_length
    table = curses.newwin(table_rows, table_col, y_table, x_table)
    table.border()

    x_pos = table_col//2 - len('|\/\/\/|')//2
    table.addstr(2, x_pos, r'|\/\/\/|', curses.color_pair(i))
    table.addstr(3, x_pos, r'|______|', curses.color_pair(i))
    table.addstr(4, table_col//2-len('PancakeFear')//2, 'PancakeFear' + ': ' + '250000')
    #TODO implement highscore.json or whatever

    screen.refresh()
    win.refresh()
    table.refresh()


def print_game_screen(screen, left, right, hidden_word, lives, guesses, mistakes=0):
    screen.clear()
    left.clear()
    right.clear()
    
    y, x = screen.getmaxyx()

    x_main = x//2 - len('#   #  ###  #   #  ###  #   #  ###  #   #')//2

    win = curses.newwin(7, len('#   #  ###  #   #  ###  #   #  ###  #   #')+4, 1, x_main)
    win.border()

    win.attron(curses.color_pair(2))
    win.addstr(1, 2, '#   #  ###  #   #  ###  #   #  ###  #   #')
    win.addstr(2, 2, '#   # #   # ##  # #   # ## ## #   # ##  #')
    win.addstr(3, 2, '##### ##### # # # #     # # # ##### # # #')
    win.addstr(4, 2, '#   # #   # #  ## #  ## #   # #   # #  ##')
    win.addstr(5, 2, '#   # #   # #   #  #### #   # #   # #   #')
    win.attroff(curses.color_pair(2))

    ly, lx = left.getmaxyx()
    left.border()
    left.addstr(ly//2, lx//2-len(hidden_word)//2, hidden_word)


    ry, rx = right.getmaxyx()
    rx = rx//2-13//2
    right.border()
    right.addstr(2, rx, '_____________')
    right.addstr(3, rx, '\  ||     |  ')
    right.addstr(4, rx, ' \ ||        ')
    right.addstr(5, rx, '  \||        ')
    right.addstr(6, rx, '   ||        ')
    right.addstr(7, rx, '   ||        ')
    right.addstr(8, rx, '   ||        ')
    right.addstr(9, rx, '___||________')
    right.addstr(10,rx, '-------------')

    if mistakes >= 1:
        right.addstr(4, rx+10, 'O')
    if mistakes >= 2:
        right.addstr(5, rx+10, '|')
        right.addstr(6, rx+10, '|')
    if mistakes >= 3:
        right.addstr(5, rx+9, '/')
    if mistakes >= 4:
        right.addstr(5, rx+11, '\\')
    if mistakes >= 5:
        right.addstr(7, rx+9, '/')
    if mistakes >= 6:
        right.addstr(7, rx+11, '\\')
        left.addstr(ly//2-3, lx//2-len('You are out of guesses!')//2, 'You are out of guesses!')
        left.addstr(ly//2-2, lx//2-len('the word was:')//2, 'the word was:')
        left.addstr(ly//2+2, lx//2-len('You have x lives left')//2, f'You have {lives} lives left')
        left.addstr(ly//2+4, lx//2-len('press [SPACE] to continue')//2, 'press [SPACE] to continue')

    if mistakes > 6:
        mistakes = 6
    right.addstr(12, rx, f'wrong guesses: {mistakes}')
    guessed_letters = ''
    if guesses:
        for l in set(guesses):
            guessed_letters += l + ', '
    right.addstr(13, rx, 'already guessed:')
    right.addstr(14, rx, f'{guessed_letters}')

    screen.refresh()
    win.refresh()
    left.refresh()
    right.refresh()

def create_word(screen):
    with open('settings.json') as f:
        current_set = json.load(f)

    cur = current_set['word subjects']
    choice = settings_menu['word subjects'][cur]
    word_list = words[choice]
    word = random.choice(word_list)

    hidden_word = ''
    for letter in word:
        hidden_word += '_'

    return word, hidden_word

def reveal_hidden_word(screen, word, hidden, guess, guesses):
    #guesses.append(guess)
    if len(guess) == 1:
        for i in range(len(word)):
                    if word[i] == guess:
                        hidden = hidden[:i] + guess + hidden[i+1:]
        return hidden

    else:
        if guess == word:
            return word
    return hidden



'''
A promt to ask the user if they are sure, made into its own function for reusability
returns a simple "y" or "n".
'''
def sure(screen, prompt):
    screen.clear()
    
    y, x = screen.getmaxyx()
    # option = 'Are you sure you wish to Exit? [Y/N]'

    y_pos = y//2
    x_pos = x//2 - len(prompt)//2

    screen.addstr(y_pos, x_pos, prompt)
    screen.refresh()
    while True:
        choice = chr(screen.getch())
        if choice in ['y', 'Y','n', 'N']:
            return choice.lower()

def test_function(screen):
    y,x = screen.getmaxyx()

    curses.halfdelay(5)
    while True:
        key = screen.getch()
        if key == curses.KEY_ENTER or key in [10, 13]:
            break
        for i in range(5):
            screen.addstr(5, 5, 'Hallo', curses.color_pair(i))
            curses.napms(250)

            #screen.refresh()

def lose_game_screen(screen, score, highscore_file):
    screen.clear()
    
    y, x = screen.getmaxyx()

    x_main = x//2 - len('#   #  ###  #   #  ###  #   #  ###  #   #')//2

    win = curses.newwin(7, len('#   #  ###  #   #  ###  #   #  ###  #   #')+4, 1, x_main)
    win.border()

    win.attron(curses.color_pair(2))
    win.addstr(1, 2, '#   #  ###  #   #  ###  #   #  ###  #   #')
    win.addstr(2, 2, '#   # #   # ##  # #   # ## ## #   # ##  #')
    win.addstr(3, 2, '##### ##### # # # #     # # # ##### # # #')
    win.addstr(4, 2, '#   # #   # #  ## #  ## #   # #   # #  ##')
    win.addstr(5, 2, '#   # #   # #   #  #### #   # #   # #   #')
    win.attroff(curses.color_pair(2))

    highscores = [s[1] for s in highscore_file.values()]

    def find_position(score, highscores, idx=9):
        if score < highscores[-1]:
            return 10
        if len(highscores) == 1 and score > highscores[-1]:
            return 0
        if score > highscores[idx]:
            highscores.pop()
            idx -= 1
            return find_position(score, highscores, idx)

    screen.refresh()
    win.refresh()

'''
main function to be used in the curses wrapper
'''
def main(screen):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

    y, x = screen.getmaxyx()
    left_win = curses.newwin(y-12, (x-4)//2, 10, 2)
    right_win = curses.newwin(y-12, (x-4)//2, 10, x//2)

    try:
        with open('highscores.json' 'r') as f:
            highscores_file = json.load(f)
    except FileNotFoundError:
        highscores_file = high_scores

    main_menu_idx = 0
    main_menu_active = True
    settings_menu_idx = 0
    settings_menu_active = False
    selected = False
    High_Scores_menu_active = False
    curses.savetty()
    game_loop = False

    while True:
        print_main_menu(screen, main_menu_idx)
        key = screen.getch()
        if key == curses.KEY_UP:
            main_menu_idx -= 1
            if main_menu_idx == -1:
                main_menu_idx = len(main_menu)-1
        elif key == curses.KEY_DOWN:
            main_menu_idx += 1
            if main_menu_idx == len(main_menu):
                main_menu_idx = 0
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if main_menu[main_menu_idx] == 'Exit':
                if choice := sure(screen, 'Are you sure you wish to Exit? [Y/N]') == 'y':
                    break
            if main_menu[main_menu_idx] == 'Settings':
                main_menu_active = False
                settings_menu_active = True
            if main_menu[main_menu_idx] == 'High Scores':
                main_menu_active = False
                High_Scores_menu_active = True
            if main_menu[main_menu_idx] == 'Play':
                lives = 3
                main_menu_active = False
                game_loop = True

# check what menu is activated and go to that loop     
        if main_menu_active:    
            print_main_menu(screen, main_menu_idx)
        if High_Scores_menu_active:
            print_High_Scores_menu(screen, 2)
            curses.halfdelay(1)
            while High_Scores_menu_active:
                key = screen.getch()
                if key == 27:# ESCAPE
                    # go back to main
                    curses.resetty()
                    High_Scores_menu_active = False
                    main_menu_active = True
                else:
                    for i in range(2, 4):
                        print_High_Scores_menu(screen, i)
                        curses.delay_output(400)
                        #curses.napms(400)

        if settings_menu_active:
            print_settings_menu(screen, settings_menu_idx)
            while settings_menu_active:
                key = screen.getch()
                if key == 27:# ESCAPE
                    # go back to main and save settings to file
                    settings_menu_active = False
                    main_menu_active = True
                    #break
                if key == curses.KEY_UP:
                    settings_menu_idx -= 1
                    if settings_menu_idx == -1:
                        settings_menu_idx = len(settings_menu)-1
                elif key == curses.KEY_DOWN:
                    settings_menu_idx += 1
                    if settings_menu_idx == len(settings_menu):
                        settings_menu_idx = 0
                elif chr(key) in ['r', 'R']:
                    if choice := sure(screen, 'Are you sure you wish to revert to default settings? [Y/N]') == 'y':
                        with open('settings.json', 'w') as f:
                            json.dump(settings, f)
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    selected = True
                    #open the settings file, if it doesnt exist yet, uses standard settings.
                    try:
                        with open('settings.json', 'r') as f:
                            settings_file = json.load(f)
                    except FileNotFoundError:
                        settings_file = settings
                    print_settings_menu(screen, settings_menu_idx, settings_file, selected)
                    current_option = settings_file[list(settings_menu.keys())[settings_menu_idx]]
                    while selected:
                        key = screen. getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            selected = False
                            #write the users settings to file, so it can be read on another startup.
                            with open('settings.json', 'w') as f:
                                json.dump(settings_file, f)
                        elif key == curses.KEY_LEFT:
                            current_option -= 1
                            if current_option < 0:
                                current_option = len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1
                            if current_option > len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1:
                                current_option = 0
                            settings_file[list(settings_menu.keys())[settings_menu_idx]] = current_option
                        elif key == curses.KEY_RIGHT:
                            current_option += 1
                            if current_option < 0:
                                current_option = len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1
                            if current_option > len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1:
                                current_option = 0
                            settings_file[list(settings_menu.keys())[settings_menu_idx]] = current_option
                        print_settings_menu(screen, settings_menu_idx, settings_file, selected)
                print_settings_menu(screen, settings_menu_idx)
        while game_loop:
            if lives <= 0:
                lose_game_screen(screen)
                while lives <= 0:
                    key = screen.getch()
                    #TODO -- lose game screen, replay/quit option
            score = 0
            word, hidden = create_word(screen)
            mistakes = 0
            guesses = []
            print_game_screen(screen, left_win, right_win, hidden, lives, guesses, mistakes)
            while word != hidden and lives > 0:
                key = screen.getch()
                #TODO -- implement how to play screen.
                if key == 27:
                    if choice := sure(screen, 'If you quit now, progress will be lost. Quit anyway? [Y/N]') == 'y':
                        main_menu_active = True
                        game_loop = False
                        break
                if chr(key).lower() in hidden or chr(key).lower() in guesses:
                    continue
                elif chr(key) in string.ascii_letters and chr(key).lower() in word:
                    score += 1
                    hidden = reveal_hidden_word(screen, word, hidden, chr(key), guesses)
                    if word == hidden:
                        if choice := sure(screen, 'FUUUUUUUUUCK YESSSSSSSSSS!! continue? [Y/N]') == 'y':
                            break
                        else:
                            game_loop = False
                            main_menu_active = True
                            break
                elif chr(key) in string.ascii_letters:
                    guesses.append(chr(key))
                    hidden = reveal_hidden_word(screen, word, hidden, chr(key), guesses)
                    mistakes += 1
                    if mistakes >= 6:
                        hidden = word
                        curses.flash()
                        lives -= 1
                        print_game_screen(screen, left_win, right_win, hidden, lives, guesses, mistakes)
                        k = 0
                        while k != 32:
                            k = screen.getch()
                            if k == 32:
                                mistakes = 0
                                guesses = []
                                word, hidden = create_word(screen)
                                
                        
                print_game_screen(screen, left_win, right_win, hidden, lives, guesses, mistakes)



curses.wrapper(main)


