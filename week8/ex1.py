import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = psycopg2.connect(database="week8", user="postgres", password="12345", host="127.0.0.1", port="5432")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

def transaction(src_name, dest_name, value):
    cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(value, src_name))
    cur.execute('UPDATE accounts SET credit=credit+{} WHERE id={}'.format(value, dest_name))
    
def transaction_bank(src_name, dest_name, value):
    cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(value, src_name))
    cur.execute('SELECT bankname FROM accounts WHERE id={}'.format(src_name))
    bank1 = cur.fetchone()
    cur.execute('SELECT bankname FROM accounts WHERE id={}'.format(dest_name))
    bank2 = cur.fetchone()
    if bank1 != bank2:
        cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(30, src_name))
        cur.execute("UPDATE accounts SET credit=credit+{} WHERE username='{}'".format(30, bank1[0]))
    cur.execute('UPDATE accounts SET credit=credit+{} WHERE id={}'.format(value, dest_name))
    

def list_acc():
    cur.execute('SELECT * from accounts;')
    for i in cur.fetchall():
        print(i)
        
def list_ledger():
    cur.execute('SELECT * from ledger;')
    for i in cur.fetchall():
        print(i)
    
cur.execute('DROP TABLE IF EXISTS accounts;')

cur.execute('''CREATE TABLE accounts (
                id serial PRIMARY KEY,
                username varchar(50),
                credit int
                );''')


cur.execute('''INSERT INTO accounts(username, credit)
                VALUES ('Dima', 1000)''')

cur.execute('''INSERT INTO accounts(username, credit)
                VALUES ('Vlad', 1000);''')


cur.execute('''INSERT INTO accounts(username, credit)
                VALUES ('Anton', 1000);''')

print('--------\n','task1 part1\n', '--------\n')
cur.execute('BEGIN')
cur.execute('SAVEPOINT T1')
transaction(1, 3, 500)
list_acc()
print('\n')
transaction(2, 1, 700)
list_acc()
print('\n')
transaction(2, 3, 100)
list_acc()
print('\n')
cur.execute('ROLLBACK TO T1;')
list_acc()


cur.execute('ALTER TABLE accounts ADD COLUMN bankname VARCHAR;')
cur.execute('''INSERT INTO accounts(username, credit, bankname)
                VALUES ('Tinkoff', 1000, 'Tinkoff');''')
cur.execute('''INSERT INTO accounts(username, credit, bankname)
                VALUES ('SberBank', 1000, 'SberBank');''')
cur.execute("UPDATE accounts SET bankname='Tinkoff' WHERE id={};".format(2))
cur.execute("UPDATE accounts SET bankname='SberBank' WHERE id={};".format(1))
cur.execute("UPDATE accounts SET bankname='SberBank' WHERE id={};".format(3))


print('--------\n','task1 part2\n', '--------\n')
list_acc()
print('\n')

cur.execute('BEGIN')
cur.execute('SAVEPOINT T1')
transaction_bank(1, 3, 500)
list_acc()
print('\n')
transaction_bank(2, 1, 700)
list_acc()
print('\n')
transaction_bank(2, 3, 100)
list_acc()
print('\n')
cur.execute('ROLLBACK TO T1;')
list_acc()


print('--------\n','task2\n', '--------\n')

cur.execute('DROP TABLE IF EXISTS ledger;')

cur.execute('''CREATE TABLE ledger (
                id serial PRIMARY KEY,
                source INT,
                dest INT,
                fee INT,
                amount VARCHAR(50)
                );''')


def transaction2(src_name, dest_name, value):
    cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(value, src_name))
    cur.execute('''INSERT INTO ledger(source, dest, fee, amount)
                VALUES ({}, {}, {}, {});'''.format(src_name, dest_name, 0, value))
    cur.execute('UPDATE accounts SET credit=credit+{} WHERE id={}'.format(value, dest_name))
    
def transaction_bank2(src_name, dest_name, value):
    cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(value, src_name))
    cur.execute('SELECT bankname FROM accounts WHERE id={}'.format(src_name))
    bank1 = cur.fetchone()
    cur.execute('SELECT bankname FROM accounts WHERE id={}'.format(dest_name))
    bank2 = cur.fetchone()
    if bank1 != bank2:
        cur.execute('UPDATE accounts SET credit=credit-{} WHERE id={}'.format(30, src_name))
        cur.execute("UPDATE accounts SET credit=credit+{} WHERE username='{}'".format(30, bank1[0]))
    cur.execute('UPDATE accounts SET credit=credit+{} WHERE id={}'.format(value, dest_name))
    cur.execute('''INSERT INTO ledger(source, dest, fee, amount)
            VALUES ({}, {}, {}, {});'''.format(src_name, dest_name, 30, value))
    
print('\nfor task 1.1\n')
cur.execute('BEGIN')
cur.execute('SAVEPOINT T1')
transaction2(1, 3, 500)
transaction2(2, 1, 700)
transaction2(2, 3, 100)
list_ledger()
cur.execute('ROLLBACK TO T1;')

print('\nfor task 1.2\n')

cur.execute('BEGIN')
cur.execute('SAVEPOINT T1')
transaction_bank2(1, 3, 500)
transaction_bank2(2, 1, 700)
transaction_bank2(2, 3, 100)
list_ledger()
cur.execute('ROLLBACK TO T1;')
