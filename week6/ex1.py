import psycopg2
import time

con = psycopg2.connect(database="customers", user="postgres",
                       password="12345", host="127.0.0.1", port="5432")

cur = con.cursor()

start = time.time()



cur.execute('SELECT * FROM customer LIMIT 50')
# for row in cur:
#     print(row)
print((time.time() - start)*1000, 'ms')
start = time.time()
print('\n')

cur.execute('SELECT * FROM customer LIMIT 10 OFFSET 50000')
# for row in cur:
#     print(row)
print((time.time() - start)*1000, 'ms')
start = time.time()
print('\n')

cur.execute("SELECT (name) FROM customer WHERE age='19'")
print((time.time() - start)*1000, 'ms')
start = time.time()
print('\n')

print('execution time before btree')
cur.execute("EXPLAIN ANALYZE SELECT * FROM customer WHERE age='19'")
print((time.time() - start)*1000, 'ms')
start = time.time()


print('execution time after btree')
cur.execute('CREATE INDEX age_idx ON customer (age);')
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT * FROM customer WHERE age='19';")
print((time.time() - start)*1000, 'ms')


print('execution time before hash')
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT SUBSTRING (name, 1, 1) FROM customer;")
print((time.time() - start)*1000, 'ms')

print('execution time after hash')
cur.execute('CREATE INDEX name_idx ON customer USING hash (name);')
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT SUBSTRING (name, 1, 1) FROM customer;")
print((time.time() - start)*1000, 'ms')
start = time.time()

print('-'*10, '\n After applying indexing the performance of queries becomes much beter\n as we can see by execution time \n')




    