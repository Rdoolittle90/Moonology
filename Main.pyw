from tkinter import *
from files import dictionary, settings as S
import ttkthemes
import random
import datetime
import os

TODAY = str(datetime.datetime.today()).split(' ')[0]


def del_old():
    print("checking for save files: ")
    for file in os.listdir('card_pulls'):
        if str(file).split(' ')[0] != TODAY:
            print(f'Old file found: {file}...', end=' ')
            os.remove(f'card_pulls/{file}')
            print('...deleted')
        else:
            print(f"{str(file).split(' ')[2]},", end='')
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


def menu():
    forget_current()
    root.title('')
    menu_frame = LabelFrame(root, padx=20, pady=20, bg=S.BG_DARK)
    menu_frame.pack(fill='both', expand=True)
    buttons_frame = LabelFrame(menu_frame, relief='sunken', bg=S.BORDER)
    buttons_frame.pack()
    button_moonology = Button(buttons_frame, width=15, text='Moonology', command=moonology_page, pady=5)
    button_moonology.grid(row=0, column=0)
    button_tarot = Button(buttons_frame, width=15, text='Tarot', command=tarot_page, pady=5)
    button_tarot.grid(row=0, column=1)
    button_exit = Button(buttons_frame, width=15, text='Exit', command=sys.exit, pady=5)
    button_exit.grid(row=0, column=2)


def moonology_page():
    forget_current()
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
                with open('files/deck.cards') as f:
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

    name_frame = LabelFrame(root, relief='sunken')
    name_frame.pack(fill='x')

    name_label = Label(name_frame, text='Enter your name:', relief='raised')
    name_label.grid(row=0, column=0, sticky='ns')

    name_input = Entry(name_frame, relief='sunken', justify='c', width=45)
    name_input.grid(row=0, column=1, sticky='ns')
    name_input.focus_set()

    nav_frame = LabelFrame(root)
    nav_frame.pack(fill='x', expand=True)
    back = Button(name_frame, text='Back', command=menu)
    back.grid(row=1, column=0, sticky='we')
    name_submit = Button(name_frame, text='Pull', command=lambda: pull_card(name_input.get()))
    name_submit.grid(row=1, column=1, sticky='we')

    card_text_frame = LabelFrame(root, relief='flat')
    card_text_label = Label(card_text_frame, text='', relief='flat')
    card_moon_label = Label(card_text_frame, text='', relief='raised')


def tarot_page():
    root.title('Tarot cards')
    card_back = PhotoImage(file=f'files/card_backing_{random.randint(0, 9)}.gif')


    def clear_cards():
        grid_slaves = card_frame.grid_slaves()
        for grid in grid_slaves:
            grid.grid_forget()

    def three_card_pull(name):
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
            details_label.config(text=dictionary.card_details[card])
        name_input.delete(0, 'end')
        cards_3 = []
        clear_cards()
        if name != '':
            try:
                with open(f'card_pulls/{TODAY + " T3 " + name.title()}', 'r') as f:
                    lines = f.readlines()
                    cards_3 = lines[0].rstrip('\n').split('|')

            except FileNotFoundError:
                while len(cards_3) != 3:
                    card = random.choice(os.listdir("Tarot_Cards"))
                    if card in cards_3:
                        continue
                    else:
                        cards_3.append(card)
                with open(f'card_pulls/{TODAY + " T3 " + name.title()}', 'w') as f:
                    f.write('|'.join(cards_3) + '\n')

            card_1_num = PhotoImage(file=f'Tarot_Cards/{cards_3[0]}')
            card_2_num = PhotoImage(file=f'Tarot_Cards/{cards_3[1]}')
            card_3_num = PhotoImage(file=f'Tarot_Cards/{cards_3[2]}')

            card_1_label = Label(card_frame, text='Past', relief='raised')
            card_1_label.grid(row=0, column=0, sticky='we')
            card_1 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_3[0], 1), bg=S.BORDER)
            card_1.image = card_back
            card_1.grid(row=1, column=0)

            card_2_label = Label(card_frame, text='Present', relief='raised')
            card_2_label.grid(row=0, column=1, sticky='we')
            card_2 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_3[1], 2), bg=S.BORDER)
            card_2.image = card_back
            card_2.grid(row=1, column=1)

            card_3_label = Label(card_frame, text='Future', relief='raised')
            card_3_label.grid(row=0, column=2, sticky='we')
            card_3 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_3[2], 3), bg=S.BORDER)
            card_3.image = card_back
            card_3.grid(row=1, column=2)

            details_label.pack(fill='both', expand=True)

    def five_card_pull(name):
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
            details_label.config(text=dictionary.card_details[card])
        name_input.delete(0, 'end')
        cards_5 = []
        clear_cards()
        if name != '':
            try:
                with open(f'card_pulls/{TODAY + " T5 " + name.title()}', 'r') as f:
                    lines = f.readlines()
                    cards_5 = lines[0].rstrip('\n').split('|')

            except FileNotFoundError:
                while len(cards_5) != 5:
                    card = random.choice(os.listdir("Tarot_Cards"))
                    if card in cards_5:
                        continue
                    else:
                        cards_5.append(card)
                with open(f'card_pulls/{TODAY + " T5 " + name.title()}', 'w') as f:
                    f.write('|'.join(cards_5) + '\n')

            card_1_num = PhotoImage(file=f'Tarot_Cards/{cards_5[0]}')
            card_2_num = PhotoImage(file=f'Tarot_Cards/{cards_5[1]}')
            card_3_num = PhotoImage(file=f'Tarot_Cards/{cards_5[2]}')
            card_4_num = PhotoImage(file=f'Tarot_Cards/{cards_5[3]}')
            card_5_num = PhotoImage(file=f'Tarot_Cards/{cards_5[4]}')

            card_1_label = Label(card_frame, text='Far Past', relief='raised')
            card_1_label.grid(row=0, column=0, sticky='we')
            card_1 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_5[0], 1),
                            bg=S.BORDER)
            card_1.image = card_back
            card_1.grid(row=1, column=0)

            card_2_label = Label(card_frame, text='Past', relief='raised')
            card_2_label.grid(row=0, column=1, sticky='we')
            card_2 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_5[1], 2),
                            bg=S.BORDER)
            card_2.image = card_back
            card_2.grid(row=1, column=1)

            card_3_label = Label(card_frame, text='Present', relief='raised')
            card_3_label.grid(row=0, column=2, sticky='we')
            card_3 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_5[2], 3),
                            bg=S.BORDER)
            card_3.image = card_back
            card_3.grid(row=1, column=2)

            card_4_label = Label(card_frame, text='Future', relief='raised')
            card_4_label.grid(row=0, column=3, sticky='we')
            card_4 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_5[3], 4),
                            bg=S.BORDER)
            card_4.image = card_back
            card_4.grid(row=1, column=3)

            card_5_label = Label(card_frame, text='Far Future', relief='raised')
            card_5_label.grid(row=0, column=4, sticky='we')
            card_5 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_5[4], 5),
                            bg=S.BORDER)
            card_5.image = card_back
            card_5.grid(row=1, column=4)

            details_label.pack(fill='both', expand=True)

    def seven_card_pull(name):
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
            details_label.config(text=dictionary.card_details[card])

        name_input.delete(0, 'end')
        cards_7 = []
        clear_cards()
        if name != '':
            try:
                with open(f'card_pulls/{TODAY + " T7 " + name.title()}', 'r') as f:
                    lines = f.readlines()
                    cards_7 = lines[0].rstrip('\n').split('|')

            except FileNotFoundError:
                while len(cards_7) != 7:
                    card = random.choice(os.listdir("Tarot_Cards"))
                    if card in cards_7:
                        continue
                    else:
                        cards_7.append(card)
                with open(f'card_pulls/{TODAY + " T7 " + name.title()}', 'w') as f:
                    f.write('|'.join(cards_7) + '\n')

            card_1_num = PhotoImage(file=f'Tarot_Cards/{cards_7[0]}')
            card_2_num = PhotoImage(file=f'Tarot_Cards/{cards_7[1]}')
            card_3_num = PhotoImage(file=f'Tarot_Cards/{cards_7[2]}')
            card_4_num = PhotoImage(file=f'Tarot_Cards/{cards_7[3]}')
            card_5_num = PhotoImage(file=f'Tarot_Cards/{cards_7[4]}')
            card_6_num = PhotoImage(file=f'Tarot_Cards/{cards_7[5]}')
            card_7_num = PhotoImage(file=f'Tarot_Cards/{cards_7[6]}')

            card_1 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[0], 1),
                            bg=S.BORDER)
            card_1.image = card_back
            card_1.grid(row=0, rowspan=2, column=0)

            card_2 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[1], 2),
                            bg=S.BORDER)
            card_2.image = card_back
            card_2.grid(row=0, column=1)

            card_3 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[2], 3),
                            bg=S.BORDER)
            card_3.image = card_back
            card_3.grid(row=1, column=1)

            card_4 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[3], 4),
                            bg=S.BORDER)
            card_4.image = card_back
            card_4.grid(row=0, rowspan=2, column=2)

            card_5 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[4], 5),
                            bg=S.BORDER)
            card_5.image = card_back
            card_5.grid(row=0, column=3)

            card_6 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[5], 6),
                            bg=S.BORDER)
            card_6.image = card_back
            card_6.grid(row=1, column=3)

            card_7 = Button(card_frame, image=card_back, relief='raised', command=lambda: card_details(cards_7[6], 7),
                            bg=S.BORDER)
            card_7.image = card_back
            card_7.grid(row=0, rowspan=2, column=4)

            details_label.pack(fill='both', expand=True)

    forget_current()
    name_outer_frame = LabelFrame(root, relief='raised', bg=S.BORDER)
    name_outer_frame.pack(fill='both', expand=True)
    name_frame = LabelFrame(name_outer_frame, relief='sunken', bg=S.BG_DARK)
    name_frame.pack()

    name_label = Label(name_frame, text='Enter your name:', relief='raised')
    name_label.grid(row=0, column=0, sticky='ns')

    name_input = Entry(name_frame, relief='sunken', justify='c', width=45)
    name_input.grid(row=0, column=1, sticky='ns')
    name_input.focus_set()

    back = Button(name_frame, text='Back', command=menu)
    back.grid(row=1, column=0, sticky='we')
    nav_frame = LabelFrame(name_frame, bg=S.BG_LIGHT)
    nav_frame.grid(row=1, column=1)
    back = Button(name_frame, text='Back', command=menu)
    back.grid(row=1, column=0, sticky='we')
    three_card = Button(nav_frame, text='3-card', command=lambda: three_card_pull(name_input.get()))
    three_card.grid(row=0, column=0, sticky='we')
    five_card = Button(nav_frame, text='5-card', command=lambda: five_card_pull(name_input.get()))
    five_card.grid(row=0, column=1, sticky='we')
    seven_card = Button(nav_frame, text='7-card', command=lambda: seven_card_pull(name_input.get()))
    seven_card.grid(row=0, column=2, sticky='we')

    card_frame = LabelFrame(root, bg=S.BG_DARK)
    card_frame.pack(padx=30)

    details_frame = LabelFrame(root, relief='sunken', bg=S.BG_DARK)
    details_frame.pack(fill='both', expand=True)
    details_label = Label(details_frame, text='Click a card for its details', relief='raised', border=5, bg=S.BG_LIGHT)


root = ttkthemes.ThemedTk(theme='black')

root.iconbitmap('files/Moon.ico')
root.overrideredirect(True)
root.config(bg=S.BG_DARK)
root.resizable(0, 0)


del_old()
menu()

root.mainloop()
