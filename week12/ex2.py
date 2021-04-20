import redis
from faker import Faker
from random import randint

def dict_to_redis_hset(r, hkey, dict_to_store):
    return all([r.hset(hkey, k, v) for k, v in dict_to_store.items()])


fake = Faker()


r = redis.Redis(
    host='redis-15153.c263.us-east-1-2.ec2.cloud.redislabs.com',
    port="15153",
    password='xe1Cwr4EUmikABZo9D9pwlNeIJ6mNMWp'
)

for i in range(10):
    data = {
        'login': fake.first_name(),
        'name': fake.name(),
        'followers': randint(1, 100),
        'following': randint(1, 100),
        'posts': ''
    }
    dict_to_redis_hset(r, str(i) + ' user', data)

# We can access the info about user by searching like:
#   'id_of_user user'
# The post consist a time and the user key in this format
# When we create a new post, we create new hash field with key 'number_of_post post'
# And then insert in the dict of user number_of_post in field posts


for i in range(10):
    data = {
        'time': fake.date(),
        'user': str(randint(0, 10)) + ' user',
    }
    dict_to_redis_hset(r, str(i) + ' post', data)
    
    
    
    