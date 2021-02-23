import psycopg2
import time

con = psycopg2.connect(database="customers", user="postgres",
                       password="12345", host="127.0.0.1", port="5432")

cur = con.cursor()

start = time.time()


print('execution time before GIN and GiST')
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT * FROM customer WHERE to_tsvector(review) @@ to_tsquery('friend');")
print((time.time() - start)*1000, 'ms')

print('execution time after GIN')
cur.execute("CREATE INDEX review_gin ON customer USING GIN  (to_tsvector('english', review));")
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT * FROM customer WHERE to_tsvector(review) @@ to_tsquery('friend');")
print((time.time() - start)*1000, 'ms')
start = time.time()


print('execution time after GiST')
cur.execute("CREATE INDEX review_gist ON customer USING GIST (to_tsvector('english', review));")
start = time.time()
cur.execute("EXPLAIN ANALYZE SELECT * FROM customer WHERE to_tsvector(review) @@ to_tsquery('friend');")
print((time.time() - start)*1000, 'ms')
start = time.time()

print('-'*10, '\n After applying indexing the performance of queries did not change\n as we can see by execution time \n')
