import curses
import json
import string
import random
import os

'''
Initializing menus and others
'''
main_menu = ['Play', 'Highscores', 'Settings', 'How to play', 'Exit']
settings_menu = {'difficulty': ['easy', 'medium', 'hard'], 'screen flashing': ['OFF', 'ON'], 'word subjects': ['Animals', 'Foods', 'Brands']}
words = {'Animals':['horse', 'hippopotamus', 'crocodile'], 'Foods':['pancakes', 'lasagna', 'pizza', 'cake'], 'Brands':['peugeot', 'mercedes', 'kelloggs', 'apple']}

settings = {
    'difficulty': 1,
    'screen flashing': 0,
    'word subjects': 1
    }

high_scores = {
    '1':  ['PancakeFear', 10],
    '2':  ['rawrpie', 9],
    '3':  ['HazuHaku', 8],
    '4':  ['jan', 7],
    '5':  ['piet', 6],
    '6':  ['dirk', 5],
    '7':  ['greetje', 4],
    '8':  ['mark', 3],
    '9':  ['fleischmeister', 2],
    '10': ['computer-3', 1],
}

'''
name says it, prints the main menu to the screen. index is used to highlight selected lines
'''

def print_title_screen(screen, title='hangman'):

    y, x = screen.getmaxyx()
    title_length = 0
    for char in title:
        if char == ' ':
            title_length += 2
        elif char == 'i':
            title_length += 3
        else: title_length += 6
    title_length -= 1

    win = curses.newwin(7, title_length + 4, 1, x//2 - title_length//2)
    win.border()

    if title == 'hangman':
        win.addstr(1, 2, '#   #  ###  #   #  ###  #   #  ###  #   #')
        win.addstr(2, 2, '#   # #   # ##  # #   # ## ## #   # ##  #')
        win.addstr(3, 2, '##### ##### # # # #     # # # ##### # # #')
        win.addstr(4, 2, '#   # #   # #  ## #  ## #   # #   # #  ##')
        win.addstr(5, 2, '#   # #   # #   #  #### #   # #   # #   #')

    if title == 'settings':
        win.addstr(1, 2, ' #### ##### ##### ##### ## #   #  ###   ####')
        win.addstr(2, 2, '#     #       #     #      ##  # #   # #    ')
        win.addstr(3, 2, ' ###  ####    #     #   ## # # # #      ### ')
        win.addstr(4, 2, '    # #       #     #   ## #  ## #  ##     #')
        win.addstr(5, 2, '####  #####   #     #   ## #   #  #### #### ')

    if title == 'highscores':
        win.addstr(1, 2, '#   # ##  ###  #   #  ####  ###   ###  ####  #####  ####')
        win.addstr(2, 2, '#   #    #   # #   # #     #   # #   # #   # #     #    ')
        win.addstr(3, 2, '##### ## #     #####  ###  #     #   # # ##  ####   ### ')
        win.addstr(4, 2, '#   # ## #  ## #   #     # #   # #   # #   # #         #')
        win.addstr(5, 2, '#   # ##  ###  #   # ####   ###   ###  #   # ##### #### ')

    if title == 'how to play':
        win.addstr(1, 2, '#   #  ###  #     #  #####  ###   ####  #      ###  #   #')
        win.addstr(2, 2, '#   # #   # #     #    #   #   #  #   # #     #   #  # # ')
        win.addstr(3, 2, '##### #   # #  #  #    #   #   #  ####  #     #####   #  ')
        win.addstr(4, 2, '#   # #   # # # # #    #   #   #  #     #     #   #   #  ')
        win.addstr(5, 2, '#   #  ###   #   #     #    ###   #     ##### #   #   #  ')

    return win

def print_main_menu(screen, main_menu_idx):

    screen.clear()
    
    y, x = screen.getmaxyx()
    y += 5

    title = print_title_screen(screen, 'hangman')
    
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
    title.refresh()

'''
name says it, prints the settings menu to the screen.
this also handles setting a selected option to the option of choice.
'''
def print_settings_menu(screen, settings_menu_idx, settings_file, selected=False):
    screen.clear()
    
    y, x = screen.getmaxyx()
    y +=5

    title = print_title_screen(screen, 'settings')

    # INITIAL PRINTS, ALLWAYS THE SAME
    title_string = "Use [ENTER] to select and the [ARROW] keys to navigate"
    title_string2 = "Press [ESC] to save and return to the main menu"
    title_string3 = "Press ['R'] at any time to revert to default settings"
    y_pos = y//2 - len(settings_menu)//2 -6
    x_pos = x//2 - len(title_string)//2
    screen.addstr(y_pos, x_pos, title_string)
    y_pos = y//2 - len(settings_menu)//2 -5
    x_pos = x//2 - len(title_string2)//2
    screen.addstr(y_pos, x_pos, title_string2)
    y_pos = y//2 - len(settings_menu)//2 -4
    x_pos = x//2 - len(title_string3)//2
    screen.addstr(y_pos, x_pos, title_string3)
    screen.addstr(y_pos+2, 85, 'current settings:')

    # PRINTING THE MENU ITEMS, ITERATING OVER THEM IS FOR HIGHLIGHTING
    # THE PROPER WORDS WHEN BROWSING TROUGH THE MENU
    for key, value in settings_menu.items():
        key_to_print = key + ":"
        value_to_print = ''
        for i in range(len(value)-1):
            value_to_print += value[i] + ' | '
        value_to_print += value[-1]
        idx = list(settings_menu).index(key)
        y_pos = y//2 - len(settings_menu)//2 + idx
        x_pos = x//2 - (len(key_to_print) + len(value_to_print))//2
        highlighted = value[settings_file[key]]

        screen.addstr(y_pos, 90, highlighted)
    
        if not selected:
            if idx == settings_menu_idx:
                screen.addstr(y_pos,x_pos-4, '--> ')
                screen.attron(curses.color_pair(1))
                screen.addstr(y_pos, x_pos, key_to_print)
                screen.attroff(curses.color_pair(1))
                screen.addstr(y_pos, x_pos+len(key_to_print), ' ' + value_to_print)
                screen.addstr(y_pos, x_pos+len(' ' + key_to_print + value_to_print), ' <--')
            else:
                screen.addstr(y_pos, x_pos, key_to_print + ' ' +  value_to_print)
        
        else:
            current_setting = settings_file[list(settings_menu.keys())[settings_menu_idx]]

            start = key_to_print + ' '
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
                screen.addstr(y_pos, x_pos, key_to_print + ' ' + value_to_print)
                
    screen.refresh()
    title.refresh()

def print_High_Scores_menu(screen, i, highscore_file):
    screen.clear()

    y, x, = screen.getmaxyx()
    screen.addstr(9, x//2-len('Press [ESC] at any time to return')//2, 'Press [ESC] at any time to return')
    y += 5
    title_length = len('#   # ##  ###  #   #   ####  ###   ###  ####  #####  ####')+4
    x_main = x//2 - (title_length-4)//2

    title = print_title_screen(screen, 'highscores')

    y_table = y//2 - 6
    x_table = x_main
    table_rows = 17
    table_col = title_length-1
    table = curses.newwin(table_rows, table_col, y_table, x_table)
    table.border()

    table.addstr(4, 6, '1')
    table.addstr(4, 10, list(highscore_file.values())[0][0], curses.color_pair(i))
    table.addstr(4, 40, str(list(highscore_file.values())[0][1]), curses.color_pair(i))
    
    x_position = 10 
    for i, l in enumerate(highscore_file.values()):
        if i == 0:
            continue
        table.addstr(4+i, 6, str(i+1))
        table.addstr(4+i, x_position, l[0] + ': ')
        table.addstr(4+i, x_position + 30, str(l[1]))

    screen.refresh()
    title.refresh()
    table.refresh()


def print_game_screen(screen, left, right, hidden_word, score, lives, guesses, mistakes=0):
    screen.clear()
    left.clear()
    right.clear()
    
    y, x = screen.getmaxyx()

    title = print_title_screen(screen, 'hangman')

    ly, lx = left.getmaxyx()
    left.border()
    if mistakes < 6:
        left.addstr(2, lx//2-len('Press [SPACE] to see how to play')//2, 'Press [SPACE] to see how to play')
        left.addstr(4, lx//2-len('Press [ENTER] to guess the word')//2, 'Press [ENTER] to guess the word')
    left.addstr(ly//2, lx//2-len(hidden_word)//2, hidden_word)


    ry, rx = right.getmaxyx()
    rx = rx//2-13//2
    right.border()
    right.addstr(1, 5, f'points: {score}')
    right.addstr(1, 38, f'lives left: {lives}')
    right.addstr(3, rx, '_____________')
    right.addstr(4, rx, '\  ||     |  ')
    right.addstr(5, rx, ' \ ||        ')
    right.addstr(6, rx, '  \||        ')
    right.addstr(7, rx, '   ||        ')
    right.addstr(8, rx, '   ||        ')
    right.addstr(9, rx, '   ||        ')
    right.addstr(10,rx, '___||________')
    right.addstr(11,rx, '-------------')

    if mistakes >= 1:
        right.addstr(5, rx+10, 'O')
    if mistakes >= 2:
        right.addstr(6, rx+10, '|')
        right.addstr(7, rx+10, '|')
    if mistakes >= 3:
        right.addstr(6, rx+9, '/')
    if mistakes >= 4:
        right.addstr(6, rx+11, '\\')
    if mistakes >= 5:
        right.addstr(8, rx+9, '/')
    if mistakes >= 6:
        if lives <= 0:
            right.addstr(8, rx+11, '\\')
            left.addstr(ly//2-2, lx//2-len('You are out of guesses!')//2, 'You are out of guesses!')
            left.addstr(ly//2-1, lx//2-len('the word was:')//2, 'the word was:')
            left.addstr(ly//2+3, lx//2-len('You are out of lives!')//2, f'You are out of lives!')
            left.addstr(ly//2+3, lx//2-len('Your final score was xx!')//2, f'Your final score was {score}!')
            left.addstr(ly//2+5, lx//2-len('press [SPACE] to continue')//2, 'press [SPACE] to continue')
        else:
            right.addstr(8, rx+11, '\\')
            left.addstr(ly//2-2, lx//2-len('You are out of guesses!')//2, 'You are out of guesses!')
            left.addstr(ly//2-1, lx//2-len('the word was:')//2, 'the word was:')
            left.addstr(ly//2+3, lx//2-len('You have x lives left')//2, f'You have {lives} lives left')
            left.addstr(ly//2+5, lx//2-len('press [SPACE] to continue')//2, 'press [SPACE] to continue')

    if mistakes > 6:
        mistakes = 6
    right.addstr(13, rx, f'wrong guesses: {mistakes}')
    guessed_letters = ''
    if guesses:
        for l in set(guesses):
            guessed_letters += l + ', '
    right.addstr(14, rx, 'already guessed:')
    right.addstr(15, rx, f'{guessed_letters}')

    screen.refresh()
    title.refresh()
    left.refresh()
    right.refresh()

def create_word(screen):
    # LOOKS AT THE SETTINGS TO PICK THE CATEGORY
    with open('settings.json') as f:
        current_set = json.load(f)

    cur = current_set['word subjects']
    choice = settings_menu['word subjects'][cur]
    word_list = words[choice]
    word = random.choice(word_list)

    hidden_word = '_' * len(word)
    # RETURNS BOTH THE WORD AND THE HIDDEN VERSION OF IT (i.e. 'horse', '_____')
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
        choice = screen.getch()
        try:
            if chr(choice) in ['y', 'Y','n', 'N']:
                return chr(choice).lower()
        except ValueError:
            pass

def find_score_position(screen, score, highscore_file):
    # RETURNS THE POSITION IN THE HIGHSCORE LIST.
    i = 1
    for n, s in highscore_file.values():
        if score > s:
            return i
        i += 1

def end_game_screen(screen, score, highscore_file):
    got_highscore = False
    screen.clear()
    
    score_pos = find_score_position(screen, score, highscore_file)
    
    y, x = screen.getmaxyx()

    title = print_title_screen(screen, 'hangman')
    title.refresh()

    screen.addstr(y//2, x//2-len('Your final score was: xxx')//2, f'Your final score was: {score}')
    screen.addstr(y//2+1, x//2-len("let's see if you ended up in the highscores!")//2, "let's see if you ended up in the highscores!")
    screen.refresh()
    for i in range(5):
        screen.addstr(y//2+2, x//2-len(".....")//2+i, ".")
        curses.napms(600)
        screen.refresh()
        title.refresh()
        
    if score > highscore_file.get(10, ['NULL', 1])[1]:
        #TODO winscreen!
        screen.addstr(y//2+3, x//2-len("You made it!")//2, "You made it!")
        screen.addstr(y//2+5, x//2-len("Please enter your credentials")//2, "Please enter your credentials")
        screen.addstr(y//2+6, x//2-len("(Min: 3, Max: 15)")//2, "(Min: 3, Max: 15)")
        screen.refresh()
        title.refresh()
        screen.move(y//2+8, x//2-7)
        name = ''
        chr_amount = 0
        while True:
            key = screen.getkey()
            if key in string.ascii_letters and chr_amount < 15:
                name += key
                chr_amount += 1
            elif key in ['KEY_BACKSPACE', r'\b', r'\x7f'] or ord(key) == 8 and chr_amount > 0:
                screen.addstr(' '*15)
                screen.move(y//2+8, x//2-7)
                name = name[:len(name)-1]
                chr_amount -= 1
            screen.addstr(name)
            screen.move(y//2+8, x//2-7)
            if ord(key) == curses.KEY_ENTER or ord(key) in [10, 13]:
                if choice := sure(screen, f'Are these your credentials?: {name} [Y/N]') == 'y':
                    #highscore_file[score_pos] = [name, score]
                    #with open('highscores.json', 'w') as f:
                    #    json.dump(highscore_file, f)
                    break
                else:
                    continue
        
        screen.clear()
        screen.addstr(y//2+3, x//2-len("Saving")//2, "Saving")
        screen.refresh()
        for i in range(5):
            screen.addstr(".")
            curses.napms(200)
            screen.refresh()
        return name
    else:
        screen.addstr(y//2+3, x//2-len("Too bad, no highscore!")//2, "Too bad, no highscore!")
        curses.napms(1000)

    # highscores = [s[1] for s in highscore_file.values()]

    screen.refresh()
    title.refresh()
    curses.napms(500)
    return None


def how_to_play_menu(screen):
    screen.clear()

    y, x = screen.getmaxyx()

    title = print_title_screen(screen, 'how to play')

    screen.addstr(10, 10, "use [ARROW] keys to navigate menu's")

    screen.addstr(12, 10, "use [ENTER] to advance to the selected menu")

    screen.addstr(14, 10, "use [ESC] to return to a previous menu")

    screen.addstr(16, 10, "otherwise, prompted keys can be used to advance	")

    screen.addstr(10, 59, "||  while playing: pressing any alphabetical")
    screen.addstr(11, 59, "||  key, will input this letter as your guess.")
    screen.addstr(12, 59, "||  +1 point per right letter guessed")
    screen.addstr(13, 59, "||")
    screen.addstr(14, 59, "||  pressing [ENTER] at any time, allows you")
    screen.addstr(15, 59, "||  to enter the entire word as a guess, ")
    screen.addstr(16, 59, "||  points guessing this way are increased")
    screen.addstr(17, 59, "||")
    screen.addstr(18, 59, "||  while this pop-up window is open, press [ESC]")
    screen.addstr(19, 59, "||  at any time to cancel your guess")
    screen.addstr(20, 59, "||  or press [ENTER] again to confirm your guess")
    screen.addstr(21, 59, "||  a missed guess in this way results in a")
    screen.addstr(22, 59, "||  substraction of points")

    screen.refresh()
    title.refresh()

def input_score(screen, name, score, score_position, highscore_file):
    new_highscore_file = {}
    for place, value in highscore_file.items():
        place = int(place)
        if place < score_position:
            new_highscore_file[place] = value
        elif place == score_position:
            new_highscore_file[place] = [name, score]
        else:
            new_highscore_file[place] = highscore_file[str(place-1)]

    return new_highscore_file


'''
main function to be used in the curses wrapper
'''
def main(screen):

    # INITIALIZE COLORPAIRS, CURRENTLY NOT ALL IN USE
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # INITIALIZE WINDOWS TO BE USED LATER
    y, x = screen.getmaxyx()
    left_win = curses.newwin(y-12, (x-4)//2, 10, 2)
    right_win = curses.newwin(y-12, (x-4)//2, 10, x//2)
    popup_win = curses.newwin(7, (x-4)//2, 12, x//2-((x-4)//2)//2)

    # SEARCH FOR THE HIGHSCORES/SETTINGS FILE LOCALLY, IF NOT FOUND TAKES THE DEFAULT.
    try:
        with open('highscores.json', 'r') as f:
            highscores_file = json.load(f)
            print('Found highscores file on your system.\n')
    except FileNotFoundError:
        highscores_file = high_scores
        print('highscores file was not found!\nStandard settings were used.')

    try:
        with open('settings.json', 'r') as f:
            settings_file = json.load(f)
    except FileNotFoundError:
        settings_file = settings

    # VARIABLES TO CONTROL MENUS
    difficulty = settings_file['difficulty']
    main_menu_idx = 0
    main_menu_active = True
    settings_menu_idx = 0
    settings_menu_active = False
    selected = False
    High_Scores_menu_active = False
    curses.savetty()
    game_loop = False
    popup_active = False
    skip_keypress = False
    score_position = 11

    # START OF PROGRAM LOOP
    while True:
        # SKIP KEYPRESS IS TO IGNORE THE WAITING FOR A KEYPRESS WHEN REDIRECTED FROM ONE MENU TO ANOTHER DIRECTLY
        # WITHOUT FIRST PASSING THE MAIN MENU
        if not skip_keypress:
            print_main_menu(screen, main_menu_idx)
            key = screen.getch()
        else:
            key = -1
        # SUBSECTION: CHECKS IF TERMINAL WAS RESIZED, IF SO 'CRASHES' THE GAME
        curses.update_lines_cols()
        if curses.LINES < 30 or curses.COLS < 116:
            print('\n==================================================\n')
            print('you terminal must be at least 30*116 (line/columns)')
            print('please resize your terminal, and launch again')
            print('\n==================================================\n')
            break
        if key == curses.KEY_UP:
            main_menu_idx -= 1
            if main_menu_idx == -1:
                main_menu_idx = len(main_menu)-1
        elif key == curses.KEY_DOWN:
            main_menu_idx += 1
            if main_menu_idx == len(main_menu):
                main_menu_idx = 0
        # SELECTING THE OPTION IN MAIN MENU, SETTING THE RIGHT MENU'S ACTIVE
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if main_menu[main_menu_idx] == 'Exit':
                if choice := sure(screen, 'Are you sure you wish to Exit? [Y/N]') == 'y':
                    break
            if main_menu[main_menu_idx] == 'Settings':
                main_menu_active = False
                settings_menu_active = True
            if main_menu[main_menu_idx] == 'Highscores':
                main_menu_active = False
                High_Scores_menu_active = True
            if main_menu[main_menu_idx] == 'Play':
                lives_lib = {0:3, 1:2, 2:1}
                lives = lives_lib[difficulty]
                score = 0
                score_position = 11
                main_menu_active = False
                game_loop = True
            if main_menu[main_menu_idx] == 'How to play':
                how_to_play_menu(screen)
                k = screen.getch()
                while k != 27:
                    k = screen.getch()

# CHECK WHAT MENU IS ACTIVE GOING INTO IT'S LOOP     
        if main_menu_active:   
            skip_keypress = False 
            print_main_menu(screen, main_menu_idx)
        if High_Scores_menu_active:
            print_High_Scores_menu(screen, 2, highscores_file)
            curses.halfdelay(1)
            while High_Scores_menu_active:
                
                for i in range(2, 4):
                    print_High_Scores_menu(screen, i, highscores_file)
                    curses.delay_output(400)

                    key = screen.getch()
                    if key == 27:# ESCAPE
                        # GO BACK TO MAIN MENU
                        curses.resetty()
                        High_Scores_menu_active = False
                        main_menu_active = True
                        skip_keypress = True
                        break

        if settings_menu_active:
            skip_keypress = False
            print_settings_menu(screen, settings_menu_idx, settings_file)
            while settings_menu_active:
                key = screen.getch()
                if key == 27:# ESCAPE
                    # GO BACK TO MAIN MENU AND SAVE SETTINGS TO FILE
                    settings_menu_active = False
                    main_menu_active = True
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
                    print_settings_menu(screen, settings_menu_idx, settings_file, selected)
                    current_option = settings_file[list(settings_menu.keys())[settings_menu_idx]]
                    while selected:
                        key = screen. getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            selected = False
                            # WRITE THE USERS SETTINGS TO FILE, SO IT CAN BE READ ON ANOTHER STARTUP.
                            with open('settings.json', 'w') as f:
                                json.dump(settings_file, f)
                            difficulty = settings_file['difficulty']
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
                print_settings_menu(screen, settings_menu_idx, settings_file)
        while game_loop:
            if lives <= 0:
                name = end_game_screen(screen, score, highscores_file)
                pos = find_score_position(screen, score, highscores_file)
                highscores_file = input_score(screen, name, score, pos, highscores_file)
                High_Scores_menu_active = True
                game_loop = False
                skip_keypress = True
                continue
                
            word, hidden = create_word(screen)
            mistakes = 0
            guesses = []
            print_game_screen(screen, left_win, right_win, hidden, score, lives, guesses, mistakes)
            while word != hidden and lives > 0:
                key = screen.getch()
                if key == 27:
                    if choice := sure(screen, 'Are you sure you wish to quit? Your score will be lost. [Y/N]') == 'y':
                        main_menu_active = True
                        game_loop = False
                        lives = 3
                        break
                if key == 32:
                    how_to_play_menu(screen)
                    k = screen.getch()
                    while k != 27:
                        k = screen.getch()
                    

                if chr(key).lower() in hidden or chr(key).lower() in guesses:
                    continue
                elif chr(key) in string.ascii_letters and chr(key).lower() in word:
                    score += difficulty
                    hidden = reveal_hidden_word(screen, word, hidden, chr(key), guesses)
                    if word == hidden:
                        print_game_screen(screen, left_win, right_win, hidden, score, lives, guesses, mistakes)
                        left_win.addstr(11, 24, 'CORRECT!')
                        left_win.refresh()
                        curses.napms(500)
                        continue
                        
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    popup_active = True
                    potential_points = 0
                    for l in hidden:
                        if l not in string.ascii_letters:
                            potential_points += 1
                    pop_y, pop_x = popup_win.getmaxyx()
                    popup_win.clear()
                    popup_win.border()
                    popup_win.addstr(2, pop_x//2-len('Think you got this? Let\'s see it')//2, 'Think you got this? Let\'s see it')
                    popup_win.addstr(3, pop_x//2-len(hidden)//2, hidden)
                    popup_win.move(4, pop_x//2-len(hidden)//2)
                    l = 0
                    full_guess = ''
                    while popup_active:
                        popup_win.refresh()
                        k = -1
                        while True:
                            k = popup_win.getch()
                            if k == 27:
                                popup_active = False
                                break
                            if chr(k) in string.ascii_letters and l < len(hidden):
                                try:
                                    popup_win.addstr(chr(k))
                                    l += 1
                                    full_guess += chr(k)
                                except ValueError:
                                    pass
                            if k == curses.KEY_ENTER or k in [10, 13]:
                                popup_active = False
                                #curses.resetty()
                                hidden = reveal_hidden_word(screen, word, hidden, full_guess, guesses)
                                if hidden == word:
                                    score += potential_points*2*difficulty
                                    popup_win.clear()
                                    popup_win.border()
                                    popup_win.addstr(3, pop_x//2-len('CORRECT!')//2, 'CORRECT!')
                                else:
                                    score -= potential_points*2
                                    popup_win.clear()
                                    popup_win.border()
                                    popup_win.addstr(3, pop_x//2-len('NOPE, WRONG!')//2, 'NOPE, WRONG!')
                                popup_win.refresh()
                                curses.napms(400)
                                break

                elif chr(key) in string.ascii_letters:
                    guesses.append(chr(key))
                    hidden = reveal_hidden_word(screen, word, hidden, chr(key), guesses)
                    mistakes += 1
                    if mistakes >= 6:
                        hidden = word
                        if settings_file['screen flashing']:
                            curses.flash()
                        lives -= 1
                        print_game_screen(screen, left_win, right_win, hidden, score, lives, guesses, mistakes)
                        k = 0
                        while k != 32:
                            k = screen.getch()
                            if k == 32:
                                mistakes = 0
                                guesses = []
                                word, hidden = create_word(screen)
                                
                        
                print_game_screen(screen, left_win, right_win, hidden, score, lives, guesses, mistakes)

# AGRESSIVLY SET WINDOW SIZE FOR BEST EXPERIENCE THEN STARTS PROGRAM
os.system('mode 116,30')
curses.wrapper(main)
