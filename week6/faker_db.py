import psycopg2
from faker import Faker
import random

con = psycopg2.connect(database="customers", user="postgres",
                       password="12345", host="127.0.0.1", port="5432")

cur = con.cursor()
cur.execute('''CREATE TABLE customer (
    id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    age TEXT NOT NULL,
    review TEXT
    );''')

fake = Faker()
for i in range(100000):
    print(i)
    cur.execute("INSERT INTO customer (id, name, address, age, review) VALUES ('"+ str(i)+"','"+fake.name()+"','"+fake.address()+"', '"+str(random.randint(10, 80))+"', '"+fake.text()+"')")
    con.commit()