# Program_AVT
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
