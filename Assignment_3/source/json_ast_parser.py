# Parse python program ast's json file and print assignment statements, loop conditions and branch conditions 

import json
import sys
import os

#For converting comparison operators' names to its equivalent python operators
relational_operators = {
             'Eq' : '==',
             'NotEq' : '!=',
             'Lt' : '<',
             'Gt' : '>',
             'LtE' : '<=',
             'GtE' : '>=',
             'In' : 'in'
}

#For converting binary operators' names to its equivalent python operators
binary_operators = {
             'Add' : '+',
             'Sub' : '-',
             'Mult' : '*',
             'Div' : '/',
             'FloorDiv' : '//',
             'Mod' : '%',
             'Pow' : '**',
             'BitAnd' : '&',
             'BitOr' : '|',
             'BitXor' : '^',
             'LShift' : '<<',
             'RShift' : '>>'                  
}

#For converting unary operators' names to its equivalent python operators
unary_operators = {
             'UAdd' : '+',
             'USub' : '-',
             'Invert' : '~',
             'Not' : 'not '
}

#For converting logical operators' names to its equivalent python operators
logical_operators = {
             'Or' : 'or',
             'And' : 'and'
}

#For Storing Assignment Statements
assignment_stmts = []
#For Storing Branch Conditions
branch_conds = []
#For Storing Loop Conditions
loop_conds = []

def get_elts_list(elts):
  ''' This function parses list of elements of list,set,tuple,etc as string '''
  
  if len(elts) == 0:
    return ''
  lst_elems = ''
  for value in elts:
    lst_elems += get_value_expr(value) + ','
  return lst_elems[:-1]

def get_dict(value):
  ''' 
      This function parses the dictionary, which is initialized with some key 
      value pair, as a string
  '''
  
  dictionary = '{'
  for k, v in zip(value['keys'], value['values']):
    dictionary += get_value_expr(k) + ' : ' + get_value_expr(v) + ', '
  return dictionary[:-2] + '}'

def get_lst_slice(value):
  ''' This function parses slicing value of list '''

  if value['slice']['_type'] == "Slice":    
    # For slicing such as "a = list[1:10:2]"
    lst_name = get_value_expr(value['value'])
    lower = get_value_expr(value['slice']['lower'])
    upper = get_value_expr(value['slice']['upper'])
    step = get_value_expr(value['slice']['step'])
    lst_name += '[' + lower + ':' + upper + (':' + step if step else '') + ']'
    return lst_name
  
  elif value['slice']['_type'] == "Index":
    # For slicing such as "a = list[2]"
    lst_name = get_value_expr(value['value'])
    index_value = get_value_expr(value['slice']['value'])
    return lst_name + '[' + index_value + ']'
  
  else:
    pass

def get_function_args(args):
  ''' This function parses the arguments of function '''
  
  args_str = ""
  for arg in args:
    args_str += get_value_expr(arg) + ','
  return args_str[:-1]


def get_keyword_args(keywords):
  ''' This function parses the keyword arguments of function '''
  
  keyword_args = ""
  for keyword in keywords:
    if keyword['_type'] == "keyword": 
      keyword_args += keyword['arg'] + '=' \
        + get_value_expr(keyword['value']) + ","
    else:
      pass
  return keyword_args[:-1]

def get_ifs(ifs):
  ''' This function parses all the if condition of list comprehension '''
  
  ifs_str = '' 
  for each_if in ifs:
    if_cond = get_value_expr(each_if)
    ifs_str += 'if ' + if_cond + ' '
  
  return ifs_str 

def get_list_comprehension(generator, expression):
  ''' This function parses list comprehension '''

  if generator['_type'] == "comprehension":
    # For parsing list comprehension
    ifs = get_ifs(generator['ifs'])
    iterator = get_value_expr(generator['iter'])
    return '[' + expression + ' for '+ expression + ' in ' + iterator \
      + ' ' + ifs + ']'
  else:
    print('for now, can not handle this type: ', value['_type'])
    return ''

def get_bool_expr(values, operator):
  ''' This function parses the boolean expression as string '''
  
  bool_expr = ''
  for value in values[:-1]:
    bool_expr += get_value_expr(value) + ' ' + operator + ' '
  
  return '(' + bool_expr + get_value_expr(values[-1]) + ')'


def get_value_expr(value):
  ''' This is general function to parse different type of expressions '''
  
  if value == None:
    return ''
   
  if value['_type'] == "Constant":
    # For parsing constant" 
    return str(value['value'] if not isinstance(value['value'],str) \
      else '\''+ value['value'] + '\'')
  
  elif value['_type'] == "Name":
    # For parsing identifiers" 
    return str(value['id'])
  
  elif value['_type'] == "Call":
    # For parsing function call like "a = range(10)"
    fun_name = get_value_expr(value['func'])
    fun_args = get_function_args(value['args'])
    key_words = get_keyword_args(value['keywords'])
    return fun_name + '(' + fun_args + (',' \
      + key_words if key_words else '') + ')'
  
  elif value['_type'] == "List":
    # For parsing Lists like "lst = [1,2,,4.5,'abc']"
    list_elems = get_elts_list(value['elts'])
    return '[' + list_elems + ']'
  
  elif value['_type'] == "Tuple":
    # For parsing Tuples like "tup = (1,2,7)"
    tuple_elems = get_elts_list(value['elts'])
    return '(' + tuple_elems + ')'
    
  elif value['_type'] == "Set":
    # For parsing Sets like "st = {1,3,4,6,7,3,0}"
    set_elems = get_elts_list(value['elts'])
    return '{' + set_elems + '}'
  
  elif value['_type'] == "Subscript":
    # For parsing Subscript value like "a=[1:15:3]"
    lst_slice = get_lst_slice(value)
    return lst_slice
  
  elif value['_type'] == "Dict":
    # For parsing Dictionaries like "dct = {'and':'&', 'or': '|'}"
    dictionary = get_dict(value)
    return dictionary
  
  elif value['_type'] == "BinOp":
    # For parsing binary expressions like "a = a + b * 3"
    left = get_value_expr(value['left'])
    right = get_value_expr(value['right'])
    op = binary_operators[value['op']['_type']]
    return '(' + left + ' ' + op + ' ' + right + ')'
     
  elif value['_type'] == "UnaryOp":
    # For parsing unary expressions like "x = -10"
    op = unary_operators[value['op']['_type']]
    operand = get_value_expr(value['operand'])
    return op+operand
  
  elif value['_type'] == "BoolOp":
    # For parsing boolean expressions like "truth = a and b and c or d xor z"
    op = logical_operators[value['op']['_type']]
    return get_bool_expr(value['values'], op)
  
  elif value['_type'] == "Compare":
    # For parsing comparisons like "truth == true"
    right = get_value_expr(value['comparators'][0])
    left = get_value_expr(value['left'])
    expr = relational_operators[value['ops'][0]['_type']]
    return left+ ' ' + expr + ' ' +right
  
  elif value['_type'] == "IfExp":
    # For parsing "if expression" like "print(a) if truth else print(b)"
    test_cond = get_value_expr(value['test'])
    body = get_value_expr(value['body'])
    else_body = get_value_expr(value['orelse'])
    return '(' + body + ' if ' + test_cond + ' ' + else_body + ')'
  
  elif value['_type'] == "Attribute":
    # For parsing attributes like "list.index('apple')"
    return str(get_value_expr(value['value'])) + '.' + value['attr']
  
  elif value['_type'] == "ListComp":
    # For parsing list comprehension
    expression = get_value_expr(value['elt'])
    generator = get_list_comprehension(value['generators'][0], expression)
    return generator
    
  else:
    print('for now, can not handle this type: ', value['_type'])
    return ''
    
def parse(body):
  ''' 
    This function parses the body of program, function, loops, conditions,etc.  
  '''
  
  for stmt in body:
    
    if stmt['_type'] == "Assign":
      # For parsing assignment statements
      target = get_value_expr(stmt['targets'][0])
      value = get_value_expr(stmt['value'])
      
      if target and value:
        assignment_stmts.append(target+" = "+value)
      
      else:
        pass
    
    if stmt['_type'] == "AugAssign":
      # For parsing augmented assignment statements
      target = get_value_expr(stmt['target'])
      value = get_value_expr(stmt['value'])
      op = binary_operators[stmt['op']['_type']]
      
      if target and value and op:
        assignment_stmts.append(target+' '+op+"= "+value)
      
      else:
        pass
      
    elif stmt['_type'] == "If":
      # For parsing If statements 
      test_cond = get_value_expr(stmt['test'])
      branch_conds.append(test_cond)
      parse(stmt['body'])
      parse(stmt['orelse'])
    
    elif stmt['_type'] == 'For':
      # For parsing For statements
      target = get_value_expr(stmt['target'])
      iterator = get_value_expr(stmt['iter'])
      loop_conds.append(target + ' in ' + iterator)
      parse(stmt['body'])
       
    elif stmt['_type'] == 'While':
      # For parsing While statements
      test_cond = get_value_expr(stmt['test'])
      loop_conds.append(test_cond)
      parse(stmt['body'])
   
    elif stmt['_type'] == 'FunctionDef':
      # For parsing Function body
      parse(stmt['body'])
   
    elif stmt['_type'] == "With":
      # For parsing body of with statement
      parse(stmt['body'])
   
    else:
      # It will parse the body of statements which are not in above cases
      if 'body' in stmt:
        parse(stmt['body'])

if __name__== "__main__" :
  #Parse JSON File
  input_file = str(sys.argv[1]).replace("\r", "")
  json_file = os.path.basename(input_file).split('.')[0] + '.json'
  json_file = os.path.join(os.path.dirname(input_file), json_file)
  with open(json_file) as f:
    data = json.load(f)
    parse(data['body'])

  #Print Assignment Statements  
  print("\nAssignment statements:\n" if assignment_stmts \
    else '\nNo assignment statements in python code\n')
  for stmt in assignment_stmts:
    print(stmt)

  #Print Branch Conditions
  print("\nBranch Conditions:\n" if branch_conds \
    else '\nNo branch conditions in python code\n')
  for cond in branch_conds:        
    print(cond)

  #Print Loop Conditions
  print("\nLoop Conditions:\n" if loop_conds \
    else '\nNo loop conditions in python code\n')
  for cond in loop_conds:
    print(cond)  

