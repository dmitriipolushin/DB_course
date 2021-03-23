import psycopg2


con = psycopg2.connect(database="dvdrental", user="postgres",
                       password="12345", host="127.0.0.1", port="5432")

cur = con.cursor()


cur.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
print(cur.fetchall())
cur.execute("SELECT * FROM staff LIMIT 10;")
print(cur.fetchall())
