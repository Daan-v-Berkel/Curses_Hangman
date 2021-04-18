import curses

main_menu = ['Play', 'Scoreboard', 'Settings', 'Exit']
settings_menu = {'difficulty': ['easy', 'medium', 'hard'], 'screen flashing': ['ON', 'OFF'], 'word subjects': ['Animals', 'Foods', 'Brands']}

settings = {
    'difficulty': 1,
    'screen flashing': 0,
    'word subjects': 0
    }

def print_main_menu(screen, main_menu_idx):

    screen.clear()
    
    y, x = screen.getmaxyx()

    
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

def print_settings_menu(screen, settings_menu_idx, selected=False):

    screen.clear()
    
    y, x = screen.getmaxyx()

    title_string = "Press ['Q'] to save and return to the main menu"
    title_string2 = "Use [ENTER] to select and the [ARROW] keys to navigate"
    y_pos = y//2 - len(settings_menu)//2 -4
    x_pos = x//2 - len(title_string)//2
    screen.addstr(y_pos, x_pos, title_string)
    y_pos = y//2 - len(settings_menu)//2 -3
    x_pos = x//2 - len(title_string2)//2
    screen.addstr(y_pos, x_pos, title_string2)
    
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
    
    else:
        current_setting = settings[list(settings_menu.keys())[settings_menu_idx]]

        for key, value in settings_menu.items():
            key_to_print = key +': '
            value_to_print = ''
            for i in range(len(value)-1):
                value_to_print += value[i] + ' | '
            value_to_print += value[-1]

            idx = list(settings_menu).index(key)
            y_pos = y//2 - len(settings_menu)//2 + idx
            x_pos = x//2 - (len(key_to_print) + len(value_to_print))//2
            
            highlighted = value[settings[key]]
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
                    screen.addstr(y_pos, x_pos+len(start + highlighted), '' + end + ' <--')
                else:
                    screen.addstr(y_pos, x_pos+len(start + highlighted), ' | ' + end + ' <--')

            else:
                screen.addstr(y_pos, x_pos, key_to_print + value_to_print)
    
    screen.refresh()

def sure(screen):
    screen.clear()
    
    y, x = screen.getmaxyx()
    option = 'Are you sure you wish to Exit? [Y/N]'

    y_pos = y//2
    x_pos = x//2 - len(option)//2

    screen.addstr(y_pos, x_pos, option)
    screen.refresh()
    while True:
        choice = chr(screen.getch())
        if choice in ['y', 'Y','n', 'N']:
            return choice.lower()
        

def main(screen):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    main_menu_idx = 0
    main_menu_active = True
    settings_menu_idx = 0
    settings_menu_active = False
    selected = False
    
    while True:
        print_main_menu(screen, main_menu_idx)
        key = screen.getch()
        if key == curses.KEY_UP:
            main_menu_idx -= 1
            if main_menu_idx == -1:
                main_menu_idx = len(main_menu)-1
            #print_main_menu(screen, main_menu_idx)
        elif key == curses.KEY_DOWN:
            main_menu_idx += 1
            if main_menu_idx == len(main_menu):
                main_menu_idx = 0
            #print_main_menu(screen, main_menu_idx)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if main_menu[main_menu_idx] == 'Exit':
                if choice := sure(screen) == 'y':
                    break
            if main_menu[main_menu_idx] == 'Settings':
                main_menu_active = False
                settings_menu_active = True
                
        if main_menu_active:    
            print_main_menu(screen, main_menu_idx)
        if settings_menu_active:
            print_settings_menu(screen, settings_menu_idx)
            current_option = settings[list(settings_menu.keys())[settings_menu_idx]]
            while True:
                key = screen.getch()
                if chr(key) in ['q', 'Q']:
                    settings_menu_active = False
                    main_menu_active = True
                    break
                if key == curses.KEY_UP:
                    settings_menu_idx -= 1
                    if settings_menu_idx == -1:
                        settings_menu_idx = len(settings_menu)-1
                elif key == curses.KEY_DOWN:
                    settings_menu_idx += 1
                    if settings_menu_idx == len(settings_menu):
                        settings_menu_idx = 0
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    selected = True
                    print_settings_menu(screen, settings_menu_idx, selected)
                    while selected:
                        key = screen. getch()
                        if key == curses.KEY_ENTER or key in [10, 13]:
                            selected = False
                            break
                        elif key == curses.KEY_LEFT:
                            current_option -= 1
                            if current_option < 0:
                                current_option = len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1
                            if current_option > len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1:
                                current_option = 0
                                settings[list(settings_menu.keys())[settings_menu_idx]] = current_option
                        elif key == curses.KEY_RIGHT:
                            current_option += 1
                            if current_option < 0:
                                current_option = len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1
                            if current_option > len(settings_menu[list(settings_menu.keys())[settings_menu_idx]])-1:
                                current_option = 0
                                settings[list(settings_menu.keys())[settings_menu_idx]] = current_option
                        print_settings_menu(screen, settings_menu_idx, selected)
                print_settings_menu(screen, settings_menu_idx, selected)


    #print_main_menu(screen, main_menu_idx)

    #screen.getch()

curses.wrapper(main)


