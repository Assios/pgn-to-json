#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import chess.pgn
import re
import sys

if len(sys.argv) > 1:
  for pgn_file in sys.argv[1:]:
    if pgn_file[-4:]==".pgn":
      pgn_file = pgn_file[:-4]

    try:
      pgn = open(pgn_file + '.pgn')
    except:
      print "No file named " + pgn_file + ".pgn"
      continue

    print "Converting " + pgn_file + ".pgn to json..."

    json_file = open(pgn_file + '.json', 'a')

    node = chess.pgn.read_game(pgn)

    while node != None:

      data =  node.headers

      try:
        if (", " in re.sub("\(.*?\)", "", data["White"]).strip() and ", " in re.sub("\(.*?\)", "", data["Black"]).strip()):
            for color in ["White", "Black"]:
                    data[color + "Surname"], data[color + "FirstName"] = [i.split()[0] for i in data.get(color).split(", ")]
        elif len(data["White"].split()) > 1:
            for color in ["White", "Black"]:
                    data[color + "FirstName"], data[color + "Surname"] = [i.split()[0] for i in data.get(color).split(" ")]
      except:
        continue

      data["moves"] = []

      while node.variations:
        next_node = node.variation(0)
        data["moves"].append(re.sub("\{.*?\}", "", node.board().san(next_node.move)))
        node = next_node
      node = chess.pgn.read_game(pgn)
      json.dump(data, json_file, encoding='latin1')
      json_file.write('\n')

    json_file.close()
else:
  print("You need to pass in at least one pgn file.")
