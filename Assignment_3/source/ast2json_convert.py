# python script to convert python code to its ast and dump as json file
 
import json
from ast import parse
from ast2json import ast2json
import sys
import os

if(len(sys.argv) != 2):
  exit(0)

input_file = str(sys.argv[1]).replace("\r", "")
ast = ast2json(parse(open(str(input_file)).read()))

json_ast = json.dumps(ast, indent=4)

json_file = os.path.basename(input_file).split('.')[0] + '.json'
json_file = os.path.join(os.path.dirname(input_file), json_file)

with open(json_file, "w") as outfile: 
    outfile.write(json_ast)

