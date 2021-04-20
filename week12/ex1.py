import redis
from faker import Faker
from random import randint

r = redis.Redis(
    host='redis-15153.c263.us-east-1-2.ec2.cloud.redislabs.com',
    port="15153",
    password='xe1Cwr4EUmikABZo9D9pwlNeIJ6mNMWp'
)

fake = Faker()

customers = 'Customers'

for i in range(10):
    name = fake.name()
    r.hset(customers, str(i), name)
    
print(r.hgetall(customers))

orders = 'Orders'

for i in range(1000, 1010):
    val = [str(randint(0, 9)), fake.date(), str(randint(100, 1000))]
    string = ' '.join(val)
    r.hset(orders, str(i), string)
    
print(r.hgetall(orders))
