import json
import os
from subprocess import run

import redis

ACCOUNT = {'name': 'Oliver',
           'budget': 540,
           'address': 'DF89A73034FDC1BF105806847466D0D204F2F687'}

HAMSTERS = [{'id': 0, 'data':
                      {'name': 'Andalusian Ham', 'price': 150, 'amount': 4}},
            {'id': 1, 'data':
                      {'name': 'Sicilian Ham', 'price': 200, 'amount': 3}},
            {'id': 2, 'data':
                      {'name': 'Russian Ham', 'price': 50, 'amount': 3}},
            {'id': 3, 'data':
                      {'name': 'African Ham', 'price': 250, 'amount': 3}},
            {'id': 4, 'data':
                      {'name': 'Mexican Ham', 'price': 350, 'amount': 3}}]

REDIS_URL = os.environ.get('REDIS_URL', 'gtp-redis')
rds = redis.StrictRedis(host=REDIS_URL, port=6379, db=7)


def bash(command):
    run(command.split())


def run_burrow_validity():
    bash("/home/phoenix/go/src/github.com/hyperledger/burrow/bin/"
         "burrow deploy --address EDFA0114FDF6614E17168606235A794614037EDF "
         "-f alice_store_validate.yaml")


def run_burrow_integrity():
    bash("/home/phoenix/go/src/github.com/hyperledger/burrow/bin/"
         "burrow deploy --address EDFA0114FDF6614E17168606235A794614037EDF "
         "-f alice_store_integrity.yaml")


def run_burrow_store():
    bash("/home/phoenix/go/src/github.com/hyperledger/burrow/bin/"
         "burrow deploy --address EDFA0114FDF6614E17168606235A794614037EDF "
         "-f alice_store.yaml")


def read_chain_value(key, file):
    with open(file) as json_data:
        d = json.load(json_data)
        value = d[key]

    return value
