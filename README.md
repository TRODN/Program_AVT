# Program_AVT
## Assignment 1
#### source directory:

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

#### testcases directory:

  - This directory consist the testcases and its corresponding expected output.

#### run.sh:
  - This script file take python file as input and print the assignment 
    statements, loop conditions and branch conditions
  - This file first run ast2json_convert.py and then run json_ast_parser.py to 
    generate required output
     
#### To run the code :

./run.sh path_to_source_directory path_to_input_file

example:
./run.sh source testcases/testcase_1.txt
./run.sh path_to_source_directory path_to_file/input.py


## Assignment 2
#### source directory:

ast2json_convert.py
  - input : python file
  - ouput : ast of input file as json
  
  - This file take python file as input, convert python input file's ast to json
    and dumps json data in json file. (Assignment_1)

ast2cfg.py 
  - input : ast of python program as json file
  - output : generate Control Flow Graph from given ast
 
  - cfg_parse(body, count, parent, child):
    - body of program, initial index of basic block, parent(entry basic block) 
      and child(exit basic block) are given as argument.
    - This function go through each statements and form basic block of 
      consecutive statement(not contain any jump or target of jump statements).
    - If it finds if-then or if-then-else or while statements then make 
      different basic block for each brach             
    - For evaluating assignment statement, funtion calls it take help of 
      'get_value_expr' funtion from 'json_ast_parser' file(Assignment_1). 
    
#### testcases directory:

  - This directory consist the testcases and its corresponding expected output.

#### run.sh:
  - This script file take python file as input and generate CFG as 'gv' dot 
    file and 'png' file
  - This file first run ast2json_convert.py and then ast2cfg.py to 
    generate required output
     
#### To run the code :

./run.sh path_to_source_directory path_to_input_file

example:
./run.sh source testcases/testcase_1.txt
./run.sh path_to_source_directory path_to_file/input.py


## Assignment 3
#### source directory:

ast2json_convert.py
  - input : python file
  - ouput : ast of input file as json
  
  - This file take python file as input, convert python input file's ast to json
    and dumps json data in json file. (Assignment_1)

faint_variable_analysis.py

  - input : ast of python program as json file
  - output : generate updated python code after eleminating faint variables
 
  - main function:
    - loop through the python code until there are no faint variable left.
    - function_out_in:
      - helps in calculating IN of basic block as function of OUT.
    - update_code:
      - this function removes the dead code after getting 
        stable IN and OUT of basic block 
    
#### testcases directory:

  - This directory consist the testcases and its corresponding expected output.

#### run.sh:
  - This script file take python file as input and generate 
    updated python file as output
  - This file first run ast2json_convert.py and then ast2cfg.py to 
    generate required output
     
#### To run the code :

./run.sh path_to_source_directory path_to_input_file

example:
./run.sh source testcases/testcase_1.txt
./run.sh path_to_source_directory path_to_file/input.py
