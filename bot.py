import csv
from collections import namedtuple
import random

import requests
import tweepy

from secrets import *


Volume = namedtuple('Volume', ['name', 'plural', 'ml'])
Duration = namedtuple('Duration', ['name', 'plural', 's'])
Area = namedtuple('Area', ['name', 'plural', 'm3'])


def read_collection(filename, klass):
    with open(filename) as file:
        reader = csv.reader(file)
        return [
            klass(row[0].strip(), row[1].strip(), float(row[2]))
            for row in reader
        ]


def pick_a_and_b(choices, picker):
    a = b = random.choice(choices)
    while picker(b) * 2 > picker(a):
        a = random.choice(choices)
        b = random.choice(choices)
    return a, b


collections = {
    'volume': read_collection('volumes.csv', Volume),
    'duration': read_collection('durations.csv', Duration),
    'area': read_collection('areas.csv', Area),
}

choice = random.choice(collections.keys())
choice = "volume"

collection = collections[choice]

if choice == "volume":
    a, b = pick_a_and_b(collection, lambda volume: volume.ml)

    message = "Approximately " + str(int((a.ml / b.ml))) + " " + b.plural + " fit into " + a.name + "."

if choice == "duration":
    a, b = pick_a_and_b(collection, lambda duration: duration.s)

    if len(b.plural) == 0:
        message = b.name[0].upper() + b.name[1:] + " fits into " + a.name + " approximately " + str(int((a.s / b.s))) + " times."
    else:
        message = "Approximately " + str(int((a.s / b.s))) + " " + b.plural + " fit into " + a.name + "."

if choice == "area":
    a, b = pick_a_and_b(collection, lambda duration: duration.m3)

    message = "Approximately " + str(int((a.m3 / b.m3))) + " " + b.plural + " fit into " + a.name + "."


print message

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
api.update_status(message)
