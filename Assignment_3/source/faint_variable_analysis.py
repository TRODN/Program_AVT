import json
import sys
import os
import pydotplus
import networkx as nx
import matplotlib.pyplot as plt
import ast
import json_ast_parser

from graphviz import Digraph

from ast2json import ast2json

from ast2cfg import ast2cfg


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


def get_function_args(args):
  ''' Parses the arguments of function and give list of variables '''
  
  args_str = []
  for arg in args:
    args_str.extend(get_value_expr_var_kill(arg)[0])
  return args_str

def get_keyword_args(keywords):
  ''' Parses the keyword arguments of function and give list of variables '''
  
  keyword_args = []
  for keyword in keywords:
    if keyword['_type'] == "keyword": 
      keyword_args.extend(get_value_expr_var_kill(keyword['value'])[0])
    else:
      pass
  return keyword_args

def get_bool_expr(values, operator):
  ''' Parses the boolean expression and give list of variables '''
  
  bool_expr = []
  for value in values[:-1]:
    bool_expr.extend(get_value_expr_var_kill(value)[0])
  
  return bool_expr

def parse_var(body):
  ''' 
    This function parses the body of program and give list of variables.  
  '''
  
  var = []
  for stmt in body:
    
    if stmt['_type'] == "Assign":
      target = get_value_expr_var_kill(stmt['targets'][0])[0]
      value = get_value_expr_var_kill(stmt['value'])[0]
      
      if target:
        var.extend(target)
      if value:
        var.extend(value)
      
    if stmt['_type'] == "AugAssign":
      target = get_value_expr_var_kill(stmt['target'])[0]
      value = get_value_expr_var_kill(stmt['value'])[0]
      op = binary_operators[stmt['op']['_type']]
      
      var.extend(target)
      var.extend(value)
      
    elif stmt['_type'] == 'FunctionDef':
      var.extend(parse_var(stmt['body']))
   
    else:
      pass
    
  return var

def get_value_expr_var_kill(value):
  ''' 
      This is general function to parse different type of expressions 
      and give varibles list and kill list of expression
  '''
  
  var = []
  kill = []
  
  if value == None:
    pass
   
  if value['_type'] == "Constant":
    # For parsing constant" 
    pass
  
  elif value['_type'] == "Name":
    # For parsing identifiers" 
    var.extend(str(value['id']))
  
  elif value['_type'] == "Call":
    # For parsing function call like "a = range(10)"
    fun_name = get_value_expr_var_kill(value['func'])[0]
    fun_args = get_function_args(value['args'])
    key_words = get_keyword_args(value['keywords'])
    
    var.extend(fun_args)
    var.extend(key_words)

    if len(fun_args) > 0:
      kill.extend(fun_args)
    
    if len(key_words) > 0:
      kill.extend(key_words)
    
  elif value['_type'] == "BinOp":
    # For parsing binary expressions like "a = a + b * 3"
    left = get_value_expr_var_kill(value['left'])[0]
    right = get_value_expr_var_kill(value['right'])[0]
    op = binary_operators[value['op']['_type']]
    
    var.extend(left)
    var.extend(right)
     
  elif value['_type'] == "UnaryOp":
    # For parsing unary expressions like "x = -10"
    op = unary_operators[value['op']['_type']]
    operand = get_value_expr_var_kill(value['operand'])[0]
    var.extend(operand)
  
  elif value['_type'] == "BoolOp":
    # For parsing boolean expressions like "truth = a and b and c or d xor z"
    op = logical_operators[value['op']['_type']]
    var.extend(get_bool_expr(value['values'], op))
  
  elif value['_type'] == "Compare":
    # For parsing comparisons like "truth == true"
    right = get_value_expr_var_kill(value['comparators'][0])[0]
    left = get_value_expr_var_kill(value['left'])[0]
    expr = relational_operators[value['ops'][0]['_type']]
    var.extend(left)
    var.extend(right)
    
  else:
    print('for now, can not handle this type: ', value['_type'])
  
  return var, set(kill)

def function_out_in(body, out, var):
  ''' 
    This is IN funtion in terms of OUT,GEN and KILL   
  '''
  
  body.reverse()
  
  for stmt in body:
    gen = set([])
    kill = set([])
    
    if stmt['_type'] == "Assign":
      # For parsing assignment statements
      target = get_value_expr_var_kill(stmt['targets'][0])[0]
      value,kill_fun = get_value_expr_var_kill(stmt['value'])
      
      if len(kill_fun) > 0:
        kill = kill.union(kill_fun)
      
      if target:
        
        if target[0] not in out:
          kill = kill.union(set(value).intersection(var))
        
    elif stmt['_type'] == "Expr":  
      value,kill_fun = get_value_expr_var_kill(stmt['value'])
      if len(kill_fun) > 0:
        kill = kill.union(kill_fun)
      
    elif stmt['_type'] == 'FunctionDef':
      kill = kill.union(parse(stmt['body']))
      
    else:
      pass
    
    out = out.difference(kill)
    out = out.union(gen)
    
  return out

def parse_body(body):
  ''' This convert the updated basic block in string '''
  
  updated_body = ""
  for stmt in body:
    
    if stmt['_type'] == "Assign":
      # For parsing assignment statements
      target = json_ast_parser.get_value_expr(stmt['targets'][0])
      value = json_ast_parser.get_value_expr(stmt['value'])
      
      if target and value:
        updated_body += target+" = "+value + "\n"
      else:
        pass
    
    elif stmt['_type'] == "AugAssign":
      # For parsing augmented assignment statements
      target = json_ast_parser.get_value_expr(stmt['target'])
      value = json_ast_parser.get_value_expr(stmt['value'])
      op = binary_operators[stmt['op']['_type']]
      
      if target and value:
        updated_body += target+' '+op+"= "+value + "\n"
      else:
        pass
    
    elif stmt['_type'] == "Expr":
      updated_body += json_ast_parser.get_value_expr(stmt['value']) + "\n"
      
    else:
      pass    
  return updated_body[:-1]
  
def update_code(body, ins):
  ''' 
      This function parses the body and remove dead code 
      according to faint variable analysis.  
  '''
  
  i = 0
  while i < len(body):
    stmt = body[i]
    if stmt['_type'] == "Assign":
      target = json_ast_parser.get_value_expr(stmt['targets'][0])
      
      if target in ins:
        body.remove(stmt)
        continue
    i += 1
      
  return parse_body(body)
  
def generate_python_code(start, cfg, space, stop):
  ''' This fucntion generate python code from control flow graph '''
  
  code = ''
  if start == stop:
    return ''
  if start == 'exit':
    return ''
  
  if cfg.nodes[start]:
    
    if cfg.nodes[start]['label'][1:-1].find('branch') == -1: 
      stmt_list = cfg.nodes[start]['label'][1:-1].split('\n')
      stmt_list = [space+stmt for stmt in stmt_list] 
      code +=  '\n'.join(stmt_list) + '\n'
          
    else:
      cond = cfg.nodes[start]['label'][1:-2].split('[')[1]
      
      if cfg.nodes[start]['label'][1:-1].find('branchl') != -1:  
        code += space + 'while ' + cond + ' :\n'
        succ_list = list(cfg.successors(start))
        code += generate_python_code(succ_list[0], cfg, space+'  ', start)
        code += generate_python_code(succ_list[1], cfg, space, stop)
        return code  
        
      else:
        code += space + 'if ' + cond + ' :\n'
        succ_list = list(cfg.successors(start))
        code += generate_python_code(succ_list[0],cfg,space+'  ', stop)
        
        if succ_list[1] != 'exit' and len(succ_list[1]) > len(start):
          code += space + 'else:\n'
          code += generate_python_code(succ_list[1],cfg,space+'  ', stop)  
        
        return code
  
  succ_list = list(cfg.successors(start))
  if len(succ_list) == 1:
    
    if len(succ_list[0]) < len(start):
      code += generate_python_code(succ_list[0], cfg , space[:-2], stop)
    else:
      code += generate_python_code(succ_list[0], cfg , space, stop)  
  return code  


if __name__== "__main__" :

  input_file = str(sys.argv[1]).replace("\r", "")
  json_file = os.path.basename(input_file).split('.')[0] + '.json'
  json_file = os.path.join(os.path.dirname(input_file), json_file)

  cfg = ast2cfg(json_file)
  dotplus = pydotplus.graph_from_dot_data(cfg.source)
  cfg = nx.nx_pydot.from_pydot(dotplus)


  while 1:
    # This while loop runs till there is change in input python code
    
    faint_var_in_out = [] #stores the IN and OUT for each block
    nodes_list = list(cfg.nodes)
    nodes = list(cfg.nodes.data())
    
    i = 0
    var = []
    # This loops collect all varibles of code
    while i < cfg.number_of_nodes():
      if nodes[i][1]:
        if nodes[i][1]['label'][1:-1].find('branch') == -1:
          ast1 = ast2json(ast.parse(nodes[i][1]['label'][1:-1]))
          var.extend(set(parse_var(ast1['body'])))
        else:
          cond = nodes[i][1]['label'][1:-2].split('[')[1]
          var.extend([cond])
      i += 1

    var = set(var)

    i = 0
    while i < cfg.number_of_nodes():
      if nodes_list[i] == 'exit':
        faint_var_in_out.append([nodes_list[i],set([]),var])
      else:
        faint_var_in_out.append([nodes_list[i],set([]),var])
      i += 1

    # This loop calculates INs ans OUTs of basic blocks.
    while 1:
      i = 0
      flag = 0
      while i < cfg.number_of_nodes():
        
        if nodes[i][0] == 'exit' or nodes[i][0] == 'entry':
          i += 1
          continue
    
        if nodes[i][1]:
          prev = faint_var_in_out[i][2]
          prev_out = faint_var_in_out[i][1]
          succ_list = list(cfg.successors(nodes[i][0]))
          j = 0
          k = 0
          succ_ins = set([]) 
          while j < cfg.number_of_nodes():
            if nodes[j][0] in succ_list:
              if k == 0:
                k = 1
                succ_ins = faint_var_in_out[j][2]
              else:
                succ_ins = succ_ins.intersection(faint_var_in_out[j][2])
            j += 1
      
          if nodes[i][1]['label'][1:-1].find('branch') == -1:
            ast1 = ast2json(ast.parse(nodes[i][1]['label'][1:-1]))
            faint_var_in_out[i][1] = succ_ins
            faint_var_in_out[i][2] = function_out_in(ast1['body'], \
              faint_var_in_out[i][1], var)
      
          else:
            cond = nodes[i][1]['label'][1:-2].split('[')[1]
            faint_var_in_out[i][1] = succ_ins
            faint_var_in_out[i][2] = \
              faint_var_in_out[i][1].difference(set([cond]))
    
        if prev != faint_var_in_out[i][2] or \
          prev_out != faint_var_in_out[i][1]:
          flag = 1
        i += 1

      if flag == 0:
        break
    
    prev_code = generate_python_code('entry',cfg,'','') 
    i = 0
    while i < cfg.number_of_nodes():
  
      if nodes[i][0] == 'exit' or nodes[i][0] == 'entry':
        i += 1
        continue
    
      if nodes[i][1]:
    
        if nodes[i][1]['label'][1:-1].find('branch') == -1:
          ast1 = ast2json(ast.parse(nodes[i][1]['label'][1:-1]))
          new_body = update_code(ast1['body'], faint_var_in_out[i][2])
          cfg.nodes[nodes[i][0]]['label'] = '"' + new_body + '"'
        else:
          pass
      i += 1

    if prev_code == generate_python_code('entry',cfg,'',''):
      
      file_name = os.path.basename(input_file).split('.')[0] + '_output.py'
      file_name = os.path.join(os.path.dirname(input_file), file_name)
      with open(file_name, 'w') as f:
        f.write(prev_code)
        
      break

