source directory:

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
    
testcases directory:

  - This directory consist the testcases and its corresponding expected output.

run.sh:
  - This script file take python file as input and generate CFG as 'gv' dot 
    file and 'png' file
  - This file first run ast2json_convert.py and then ast2cfg.py to 
    generate required output
     
To run the code :

./run.sh path_to_source_directory path_to_input_file

example:
./run.sh source testcases/testcase_1.txt
./run.sh path_to_source_directory path_to_file/input.py

