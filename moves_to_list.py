#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

def find_start_of_game(_list, substring='1. '):
    for i, s in enumerate(_list):
        if substring in s:
              return i
    return -1

def pgn_to_json(file_name):
    data = {}

    f = open(file_name, 'r')

    lines = [l.strip().decode('latin-1').encode('utf-8') for l in f.readlines() if not l.isspace()]

    game_index = find_start_of_game(lines)

    metadata = lines[:game_index]

    moves = re.sub("(\d+\.)|(\+)|(\#)|(\d-\d)|(1/2-1/2)|\{.*?\}", "", " ".join(lines[game_index:])).split()

    data["moves"] = moves

    for i in range(len(metadata)):
        metadata[i] = re.sub("\[|\]", "", metadata[i])
        data[re.findall(r"([^\s]+)", metadata[i])[0].lower()] = re.findall(r'"(.*?)"', metadata[i])[0]

    if (", " in data["white"] and "," in data["black"]):
        for color in ["white", "black"]:
                data[color + "_surname"], data[color + "_first_name"] = [i.split()[0] for i in data.get(color).split(", ")]
    elif len(data["white"].split()) > 1:
        for color in ["white", "black"]:
                data[color + "_first_name"], data[color + "_surname"] = [i.split()[0] for i in data.get(color).split(" ")]


    return json.dumps(data, sort_keys=False)

if __name__ == '__main__':

    out = open('games.json', 'a')
    out.write(pgn_to_json('test_game.pgn') + "\n")
