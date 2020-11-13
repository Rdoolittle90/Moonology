from tkinter import ttk as tk
from tkinter import PhotoImage
from files import tarot_card_definitions
import ttkthemes
import random
import datetime
import os


TODAY = str(datetime.datetime.today()).split(' ')[0]


def del_old():
    print("checking for save files: ")
    for file in os.listdir('card_pulls'):
        if str(file).split(' ')[0] != TODAY:
            print(f'Old file found: {file}...', end='.')
            os.remove(f'card_pulls/{file}')
            print('...deleted')
        else:
            print(f"{str(file).split(' ')[2]},", end=' ')
    print(TODAY)


def forget_current():
    pack_slaves = root.pack_slaves()
    grid_slaves = root.grid_slaves()
    place_slaves = root.place_slaves()

    for pack in pack_slaves:
        pack.pack_forget()
    for grid in grid_slaves:
        grid.grid_forget()
    for place in place_slaves:
        place.place_forget()


def app_title():
    def move_window(event):
        root.geometry(f'+{event.x_root}+{event.y_root}')

    core_frame = tk.Frame(root, relief='ridge', border=0)
    core_frame.pack(fill='x', expand=True)

    handle_frame = tk.Frame(core_frame, relief='raised')  # recreates the top bar
    handle_frame.pack(fill='x', expand=True)

    app_logo = PhotoImage(file='files/app_images/earth_moon_64x64.png')
    app_logo = app_logo.zoom(8)  # resize the image
    app_logo = app_logo.subsample(30)  # resample the image

    handle_frame_logo = tk.Label(handle_frame, relief='raised', image=app_logo)
    handle_frame_logo.image = app_logo
    handle_frame_logo.pack(side='left', fill='y')

    app_title = tk.Label(handle_frame, text=" Fortune_teller ")
    app_title.pack(side='left', padx=2)

    close_button = tk.Button(handle_frame, text='X', command=root.destroy)  # creates a button for the top bar to exit
    close_button.pack(side='right')

    handle_frame.bind('<B1-Motion>', move_window)
    # handle_frame_logo.bind('<B1-Motion>', move_window)
    app_title.bind('<B1-Motion>', move_window)


def menu():
    forget_current()
    app_title()
    root.title('')
    menu_frame = tk.Frame(root)
    menu_frame.pack(fill='both', expand=True, padx=5, pady=5)

    bg_holder = tk.Frame(menu_frame)
    bg_holder.place(anchor='c', relx=.5, rely=.5)

    background_image = PhotoImage(file='files/app_images/bg.png')
    bg_image = tk.Label(bg_holder, image=background_image)
    bg_image.image = background_image
    bg_image.pack()

    buttons_frame = tk.Frame(menu_frame, relief='sunken')
    buttons_frame.pack(padx=20, pady=75)

    button_moonology = tk.Button(buttons_frame, width=15, text='Moonology', command=moonology_page)
    button_moonology.grid(row=0, column=0)

    button_tarot = tk.Button(buttons_frame, width=15, text='Tarot', command=tarot_page)
    button_tarot.grid(row=1, column=0)


def moonology_page():
    forget_current()
    app_title()
    root.title('Moonology Oracle')

    def key_press_enter(event):
        pull_card(name_input.get())

    root.bind('<Return>', key_press_enter)

    def pull_card(name):
        name_input.delete(0, 'end')
        if name != '':
            try:
                with open(f'card_pulls/{TODAY + " M " + name.title()}', 'r') as f:
                    lines = f.readlines()
                    card_text = lines[0].split('|')[0]
                    card_moon = lines[0].split('|')[1].rstrip('\n')

                card_text_label.config(text=card_text)
                card_moon_label.config(text=card_moon)
                card_text_frame.pack(fill='both', expand=True)
                card_moon_label.pack(fill='both', expand=True)
                card_text_label.pack(fill='both', expand=True)
                return card_text, card_moon

            except FileNotFoundError:
                with open('files/moonology_card_definitions.txt') as f:
                    lines = f.readlines()

                with open(f'card_pulls/{TODAY + " M " + name.title()}', 'w') as f:
                    card_number = random.randint(0, 43)
                    card_text = lines[card_number].split('|')[0]
                    card_moon = lines[card_number].split('|')[1].rstrip('\n')
                    f.write(lines[card_number])

                card_text_label.config(text=card_text)
                card_moon_label.config(text=card_moon)
                card_text_frame.pack(fill='both', expand=True)
                card_moon_label.pack(fill='both', expand=True)
                card_text_label.pack(fill='both', expand=True)
                return card_text, card_moon
        else:
            pass

    name_frame = tk.Frame(root)
    name_frame.pack(fill='x')

    name_label = tk.Label(name_frame, text='Enter your name:')
    name_label.grid(row=0, column=0, sticky='ns')

    name_input = tk.Entry(name_frame, justify='c', width=45)
    name_input.grid(row=0, column=1, sticky='ns')
    name_input.focus_set()

    nav_frame = tk.Frame(root)
    nav_frame.pack(fill='x', expand=True)
    back = tk.Button(name_frame, text='Back', command=menu)
    back.grid(row=1, column=0, sticky='we')
    name_submit = tk.Button(name_frame, text='Pull', command=lambda: pull_card(name_input.get()))
    name_submit.grid(row=1, column=1, sticky='we')

    card_text_frame = tk.Frame(root)
    card_text_label = tk.Label(card_text_frame, text='')
    card_moon_label = tk.Label(card_text_frame, text='')


def tarot_page():
    root.title('Tarot cards')
    card_back = PhotoImage(file=f'files/card_backings/card_backing_{random.randint(0, 9)}.gif')


    def clear_cards():
        grid_slaves = card_frame.grid_slaves()
        for grid in grid_slaves:
            grid.grid_forget()

    def three_card_pull(name, question):
        details_label.config(text='Click a card for its details')

        def card_details(card, slot):
            if slot == 1:
                card_1.config(image=card_1_num)
                card_1.image = card_1_num
            if slot == 2:
                card_2.config(image=card_2_num)
                card_2.image = card_2_num
            if slot == 3:
                card_3.config(image=card_3_num)
                card_3.image = card_3_num
            details_label.config(text=tarot_card_definitions.card_details[card])
        cards_3 = []
        clear_cards()
        if question != '':
            if name != '':
                try:
                    with open(f'card_pulls/{TODAY + " T3 " + name.title()}', 'r') as f:
                        lines = f.readlines()
                        cards_3 = lines[0].rstrip('\n').split('|')
                    with open(f'files/questions.txt', 'a') as qu:
                        qu.write(f'{name_input.get()}\t{TODAY}\t{question_input.get()}\n')

                except FileNotFoundError:
                    while len(cards_3) != 3:
                        card = random.choice(os.listdir("files/Tarot_Cards"))
                        if card in cards_3:
                            continue
                        else:
                            cards_3.append(card)
                    with open(f'card_pulls/{TODAY + " T3 " + name.title()}', 'w') as f:
                        f.write('|'.join(cards_3) + '\n')

                name_input.delete(0, 'end')
                question_input.delete(0, 'end')
                card_1_num = PhotoImage(file=f'files/Tarot_Cards/{cards_3[0]}')
                card_2_num = PhotoImage(file=f'files/Tarot_Cards/{cards_3[1]}')
                card_3_num = PhotoImage(file=f'files/Tarot_Cards/{cards_3[2]}')

                card_1_label = tk.Label(card_frame, text='Past')
                card_1_label.grid(row=0, column=0, sticky='we')
                card_1 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_3[0], 1))
                card_1.image = card_back
                card_1.grid(row=1, column=0)

                card_2_label = tk.Label(card_frame, text='Present')
                card_2_label.grid(row=0, column=1, sticky='we')
                card_2 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_3[1], 2))
                card_2.image = card_back
                card_2.grid(row=1, column=1)

                card_3_label = tk.Label(card_frame, text='Future')
                card_3_label.grid(row=0, column=2, sticky='we')
                card_3 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_3[2], 3))
                card_3.image = card_back
                card_3.grid(row=1, column=2)

                details_label.pack(fill='both', expand=True)

    def five_card_pull(name, question):
        details_label.config(text='Click a card for its details')

        def card_details(card, slot):
            if slot == 1:
                card_1.config(image=card_1_num)
                card_1.image = card_1_num
            if slot == 2:
                card_2.config(image=card_2_num)
                card_2.image = card_2_num
            if slot == 3:
                card_3.config(image=card_3_num)
                card_3.image = card_3_num
            if slot == 4:
                card_4.config(image=card_4_num)
                card_4.image = card_4_num
            if slot == 5:
                card_5.config(image=card_5_num)
                card_5.image = card_5_num
            details_label.config(text=tarot_card_definitions.card_details[card])

        cards_5 = []
        clear_cards()
        if question != '':
            if name != '':
                try:
                    with open(f'card_pulls/{TODAY + " T5 " + name.title()}', 'r') as f:
                        lines = f.readlines()
                        cards_5 = lines[0].rstrip('\n').split('|')
                    with open(f'files/questions.txt', 'a') as qu:
                        qu.write(f'{name_input.get()}\t{TODAY}\t{question_input.get()}\n')

                except FileNotFoundError:
                    while len(cards_5) != 5:
                        card = random.choice(os.listdir("files/Tarot_Cards"))
                        if card in cards_5:
                            continue
                        else:
                            cards_5.append(card)
                    with open(f'card_pulls/{TODAY + " T5 " + name.title()}', 'w') as f:
                        f.write('|'.join(cards_5) + '\n')
                    with open(f'files/questions.txt', 'a') as qu:
                        qu.write(f'{name_input.get()}\t{TODAY}\t{question_input.get()}\n')

                name_input.delete(0, 'end')
                question_input.delete(0, 'end')
                card_1_num = PhotoImage(file=f'files/Tarot_Cards/{cards_5[0]}')
                card_2_num = PhotoImage(file=f'files/Tarot_Cards/{cards_5[1]}')
                card_3_num = PhotoImage(file=f'files/Tarot_Cards/{cards_5[2]}')
                card_4_num = PhotoImage(file=f'files/Tarot_Cards/{cards_5[3]}')
                photo_image = PhotoImage(file=f'files/Tarot_Cards/{cards_5[4]}')
                card_5_num = photo_image

                card_1_label = tk.Label(card_frame, text='Far Past')
                card_1_label.grid(row=0, column=0, sticky='we')
                card_1 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_5[0], 1))
                card_1.image = card_back
                card_1.grid(row=1, column=0)

                card_2_label = tk.Label(card_frame, text='Past')
                card_2_label.grid(row=0, column=1, sticky='we')
                card_2 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_5[1], 2))
                card_2.image = card_back
                card_2.grid(row=1, column=1)

                card_3_label = tk.Label(card_frame, text='Present')
                card_3_label.grid(row=0, column=2, sticky='we')
                card_3 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_5[2], 3))
                card_3.image = card_back
                card_3.grid(row=1, column=2)

                card_4_label = tk.Label(card_frame, text='Future')
                card_4_label.grid(row=0, column=3, sticky='we')
                card_4 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_5[3], 4))
                card_4.image = card_back
                card_4.grid(row=1, column=3)

                card_5_label = tk.Label(card_frame, text='Far Future')
                card_5_label.grid(row=0, column=4, sticky='we')
                card_5 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_5[4], 5))
                card_5.image = card_back
                card_5.grid(row=1, column=4)

                details_label.pack(fill='both', expand=True)

    def seven_card_pull(name, question):
        details_label.config(text='Click a card for its details')

        def card_details(card, slot):
            if slot == 1:
                card_1.config(image=card_1_num)
                card_1.image = card_1_num
            if slot == 2:
                card_2.config(image=card_2_num)
                card_2.image = card_2_num
            if slot == 3:
                card_3.config(image=card_3_num)
                card_3.image = card_3_num
            if slot == 4:
                card_4.config(image=card_4_num)
                card_4.image = card_4_num
            if slot == 5:
                card_5.config(image=card_5_num)
                card_5.image = card_5_num
            if slot == 6:
                card_6.config(image=card_6_num)
                card_6.image = card_6_num
            if slot == 7:
                card_7.config(image=card_7_num)
                card_7.image = card_7_num
            details_label.config(text=tarot_card_definitions.card_details[card])

        cards_7 = []
        clear_cards()
        if question != '':
            if name != '':
                try:
                    with open(f'card_pulls/{TODAY + " T7 " + name.title()}', 'r') as f:
                        lines = f.readlines()
                        cards_7 = lines[0].rstrip('\n').split('|')
                    with open(f'files/questions.txt', 'a') as qu:
                        qu.write(f'{name_input.get()}\t{TODAY}\t{question_input.get()}\n')

                except FileNotFoundError:
                    while len(cards_7) != 7:
                        card = random.choice(os.listdir("files/Tarot_Cards"))
                        if card in cards_7:
                            continue
                        else:
                            cards_7.append(card)
                    with open(f'card_pulls/{TODAY + " T7 " + name.title()}', 'w') as f:
                        f.write('|'.join(cards_7) + '\n')
                    with open(f'files/questions.txt', 'a') as qu:
                        qu.write(f'{name_input.get()}\t{TODAY}\t{question_input.get()}\n')

                name_input.delete(0, 'end')
                question_input.delete(0, 'end')
                card_1_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[0]}')
                card_2_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[1]}')
                card_3_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[2]}')
                card_4_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[3]}')
                card_5_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[4]}')
                card_6_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[5]}')
                card_7_num = PhotoImage(file=f'files/Tarot_Cards/{cards_7[6]}')

                card_1 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[0], 1))
                card_1.image = card_back
                card_1.grid(row=0, rowspan=2, column=0)

                card_2 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[1], 2))
                card_2.image = card_back
                card_2.grid(row=0, column=1)

                card_3 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[2], 3))
                card_3.image = card_back
                card_3.grid(row=1, column=1)

                card_4 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[3], 4))
                card_4.image = card_back
                card_4.grid(row=0, rowspan=2, column=2)

                card_5 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[4], 5))
                card_5.image = card_back
                card_5.grid(row=0, column=3)

                card_6 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[5], 6))
                card_6.image = card_back
                card_6.grid(row=1, column=3)

                card_7 = tk.Button(card_frame, image=card_back, command=lambda: card_details(cards_7[6], 7))
                card_7.image = card_back
                card_7.grid(row=0, rowspan=2, column=4)

                details_label.pack(fill='both', expand=True)

    forget_current()
    app_title()

    name_outer_frame = tk.Frame(root)
    name_outer_frame.pack(fill='both', expand=True, padx=5, pady=5)
    name_frame = tk.Frame(name_outer_frame)
    name_frame.pack()

    name_label = tk.Label(name_frame, text='Enter your name:')
    name_label.grid(row=0, column=0, sticky='ns')

    name_input = tk.Entry(name_frame, justify='c', width=45)
    name_input.grid(row=0, column=1, sticky='ns')
    name_input.focus_set()

    question_label = tk.Label(name_frame, text='What is your question?')
    question_label.grid(row=1, column=0, sticky='ns')

    question_input = tk.Entry(name_frame, justify='c', width=45)
    question_input.grid(row=1, column=1, sticky='ns')
    question_input.focus_set()

    back = tk.Button(name_frame, text='Back', command=menu)
    back.grid(row=2, column=0, sticky='we')
    nav_frame = tk.Frame(name_frame)
    nav_frame.grid(row=2, column=1)
    back = tk.Button(name_frame, text='Back', command=menu)
    back.grid(row=2, column=0, sticky='we')
    three_card = tk.Button(nav_frame, text='3-card', command=lambda: three_card_pull(name_input.get(), question_input.get()))
    three_card.grid(row=0, column=0, sticky='we')
    five_card = tk.Button(nav_frame, text='5-card', command=lambda: five_card_pull(name_input.get(), question_input.get()))
    five_card.grid(row=0, column=1, sticky='we')
    seven_card = tk.Button(nav_frame, text='7-card', command=lambda: seven_card_pull(name_input.get(), question_input.get()))
    seven_card.grid(row=0, column=2, sticky='we')

    card_frame = tk.Frame(root)
    card_frame.pack(padx=30)

    details_frame = tk.Frame(root)
    details_frame.pack(fill='both', expand=True)
    details_label = tk.Label(details_frame, text='Click a card for its details', border=5)


root = ttkthemes.ThemedTk(theme='black')

root.iconbitmap('files/app_images/Moon.ico')
root.overrideredirect(True)
root.config(bg='#3e3e3e')
root.resizable(0, 0)


del_old()
menu()

root.mainloop()
