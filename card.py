from random import randint
import sys
import sqlite3


class Bank:

    def __init__(self):
        self.cardnumber = str(400000) + str(randint(0, 999999999)).rjust(9, "0") + str(randint(0, 9)).rjust(1, "0")
        self.pin = str(randint(0000, 9999))
        while len(self.pin) != 4:
            self.pin = '0' + self.pin
        self.balance = 0

def Luhn(x):
    last_number = int(x[-1])
    step1 = x[:-1]
    step1_listed = list(i for i in step1)
    step2 = []
    for index, i in enumerate(step1_listed):
        i = int(i)
        if (index - 1) % 2 != 0:
            i *= 2
            step2.append(i)
        else:
            i = i
            step2.append(i)
    step3 = []
    for i in step2:
        i = int(i)
        if i > 9:
            step3.append(i - 9)
        else:
            step3.append(i)
    sum = 0
    for i in step3:
        sum += i
    sum += last_number
    if sum % 10 == 0:
        return True
    else:
        return False

def login_prompt():
    print('''
1. Create an account
2. Log into account
0. Exit
        ''')
def logged_prompt():
    print('''
    1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit
            ''')

def get_len():
    cur.execute('SELECT * FROM card')
    return len(cur.fetchall()) + 1

accounts = {}


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


#Create table

# cur.execute('DROP table card')
# conn.commit()
try:
    cur.execute('CREATE TABLE card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
except sqlite3.OperationalError:
    print(sqlite3.OperationalError)
conn.commit()

while True:
    login_prompt()
    user_input = input()
    if user_input == '1':
        account = Bank()
        while True:
            account = Bank()
            if Luhn(account.cardnumber) == True:
                cur.execute(f'INSERT INTO card(id, number, pin, balance) VALUES({get_len()}, {account.cardnumber}, {account.pin}, {account.balance});')
                conn.commit()
                cur.execute('SELECT * FROM card')
                # print(cur.fetchall())
                print(f'''
Your card has been created
Your card number:
{account.cardnumber}
Your card PIN:
{account.pin}
''')
                break
        else:
            continue
        # print(accounts)
    if user_input == '2':
        card_number = str(input('Enter your card number:'))
        pin = str(input('Enter your PIN:'))
        cur.execute(f'SELECT * from card WHERE number={card_number} AND pin={pin};')
        if len(cur.fetchall()) > 0:
            print('You have successfully logged in!')
            while True:
                logged_prompt()
                user_input = input()
                if user_input == '1':
                    cur.execute(f'SELECT balance FROM card WHERE number={card_number} AND pin={pin};')
                    print(f"Balance: {cur.fetchall()[0][0]}")
                if user_input == '2':
                    income = int(input('Enter income:'))
                    cur.execute(f'SELECT balance FROM card WHERE number={card_number} AND pin={pin};')
                    cur.execute(f'UPDATE card SET balance = {int(cur.fetchall()[0][0]) + income} WHERE number={card_number} AND pin={pin};')
                    conn.commit()
                    print('Income was added!')

                if user_input == '3':
                    print('Transfer')
                    transferTo = input('Enter card number:')
                    if Luhn(transferTo) != True:
                        print('Probably you made a mistake in the card number. Please try again!')
                        transferTo = input('Enter card number:')
                    else:
                        cur.execute(f'SELECT * from card WHERE number={transferTo};')
                        if len(cur.fetchall()) == 0:
                            print('Such a card does not exist.')
                        else:
                            transferAmount = int(input('Enter how much money you want to transfer'))
                            cur.execute(f'SELECT balance FROM card WHERE number={card_number} AND pin={pin};')
                            if cur.fetchall()[0][0] < transferAmount:
                                print('Not enough money!')
                            else:
                                cur.execute(f'SELECT balance FROM card WHERE number={card_number} AND pin={pin};')

                                cur.execute(f'UPDATE card SET balance = {int(cur.fetchall()[0][0]) - transferAmount} WHERE number={card_number} AND pin={pin};')
                                cur.execute(f'SELECT balance FROM card WHERE number={transferTo};')
                                cur.execute(f'UPDATE card SET balance = {int(cur.fetchall()[0][0]) + transferAmount} WHERE number={transferTo};')
                                conn.commit()
                                print('Success!')
                if user_input == '4':
                    cur.execute(f'DELETE FROM card WHERE number={card_number};')
                    conn.commit()
                    print('The account has been closed!')
                    break

                if user_input == '5':
                    print('You have successfully logged out!')
                    break
                if user_input == '0':
                    print('Bye!')
                    sys.exit()
        else:
            print('Wrong card number or PIN!')
    if user_input == '0':
        print('Bye!')
        sys.exit()
