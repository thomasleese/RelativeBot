import csv
from collections import namedtuple
import random

import requests
import tweepy

from secrets import *


Item = namedtuple('Volume', ['name', 'plural', 'value'])


def read_collection(filename):
    with open(filename) as file:
        reader = csv.reader(file)
        return [
            Item(row[0].strip(), row[1].strip(), float(row[2]))
            for row in reader
        ]


def pick_a_and_b(choices):
    a = b = random.choice(choices)
    while b.value * 2 > a.value:
        a = random.choice(choices)
        b = random.choice(choices)
    return a, b


collections = {
    'volume': read_collection('volumes.csv'),
    'duration': read_collection('durations.csv'),
    'area': read_collection('areas.csv'),
}

choice = random.choice(collections.keys())
#choice = "volume"

collection = collections[choice]

if choice == "volume":
    a, b = pick_a_and_b(collection)

    message = "Approximately " + str(int((a.value / b.value))) + " " + b.plural + " fit into " + a.name + "."

if choice == "duration":
    a, b = pick_a_and_b(collection)

    if len(b.plural) == 0:
        message = b.name[0].upper() + b.name[1:] + " fits into " + a.name + " approximately " + str(int((a.value / b.value))) + " times."
    else:
        message = "Approximately " + str(int((a.value / b.value))) + " " + b.plural + " fit into " + a.name + "."

if choice == "area":
    a, b = pick_a_and_b(collection)

    message = "Approximately " + str(int((a.value / b.value))) + " " + b.plural + " fit into " + a.name + "."


print message

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.valueet_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
api.update_status(message)
