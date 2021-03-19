source directory:

ast2json_convert.py
  - input : python file
  - ouput : ast of input file as json
  
  - This file take python file as input, convert python input file's ast to json
    and dumps json data in json file.

json_ast_parser.py 
  - input : ast of python program as json file
  - output : print the assignment statements, branch conditions and 
    loop conditions from json data of ast
 
  - parse(body):
    - The body of input python file is passed to a funtion "parse(body)", which 
      go through the json data and check for assignment statement, 
      branch conditions and loop conditions and append in appropriate list.
    - The function also check recursively for nested blocks of branch statements
      and loop statements till it reach inner most block.
      
  - get_value_expr(value):
    - This is most common used function. It is generic function to parse 
      different type of expressions, function calls, etc.
  
  - There are other function which support above two function in completing 
    their tasks  
  
  - Finally after compeletion of parse(body) function, json_ast_parser prints 
    the required output.         

testcases directory:

  - This directory consist the testcases and its corresponding expected output.


run.sh:
  - This script file take python file as input and print the assignment 
    statements, loop conditions and branch conditions
  - This file first run ast2json_convert.py and then run json_ast_parser.py to 
    generate required output
     
To run the code :

./run.sh path_to_source_directory path_to_input_file

example:
./run.sh source testcases/testcase_1.txt
./run.sh path_to_source_directory path_to_file/input.py

