import psycopg2
import time


"""Run this file to see the time performance of queries and my summary
"""

con = psycopg2.connect(database="dvdrental", user="postgres",
                       password="12345", host="127.0.0.1", port="5432")

cur = con.cursor()

start = time.time()

print('--------------\n','B-tree','--------------\n')

print('--------------\n','Query1\n','--------------\n')

sql_query1 = '''select *, (select count(*) from rental r2, payment p2 where
r2.rental_id = p2.rental_id and p2.amount<p.amount) as
count_smaller_pay from rental r, payment p where r.rental_id=p.rental_id;'''

cur.execute(cur.mogrify('explain analyze ' + sql_query1))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')

cur.execute('CREATE INDEX idx_payments_amount_id ON payment (amount, rental_id);')

cur.execute(cur.mogrify('explain analyze ' + sql_query1))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')

print('--------------\n','Query2\n','--------------\n')

sql_query2 = '''SELECT r1.staff_id, p1.payment_date
FROM rental r1, payment p1
WHERE r1.rental_id = p1.rental_id AND
NOT EXISTS (SELECT 1 FROM rental r2, customer c WHERE r2.customer_id =
c.customer_id and active = 1 and r2.last_update > r1.last_update);'''

cur.execute(cur.mogrify('explain analyze ' + sql_query2))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')

cur.execute('CREATE INDEX idx_rental_update_id ON rental USING btree(rental_id, last_update);')


cur.execute(cur.mogrify('explain analyze ' + sql_query2))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')


print('--------------\n','Query3\n','--------------\n')

sql_query3 = '''select f1.release_year, max(f2.rating), (select max(phone) from
address) as max_phone from film f1, film f2 where f1.length > 120 and
f1.rental_duration>f2.rental_duration group by f1.release_year;'''

cur.execute(cur.mogrify('explain analyze ' + sql_query3))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')

cur.execute('CREATE INDEX idx_film_length_duration ON film (length, rental_duration);')

cur.execute(cur.mogrify('explain analyze ' + sql_query3))
analyze_fetched = cur.fetchall()
for i in analyze_fetched:
    print(i)

print('\n\n')

