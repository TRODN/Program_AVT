# Parse python program ast's json file and generate the control flow graph
 
import json
import sys
import os
from graphviz import Digraph

from json_ast_parser import get_value_expr


cfg = Digraph(comment='Control Flow Graph')

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

def cfg_parse(body, count, parent, child):
  ''' 
    This function parses the body of program and generates control flow graph.  
  '''
  
  nest_count = 0  # nest_count and count is for maintaining basic block name 
  block = []      #basic block 
  flag = 0
  for stmt in body:
    
    if stmt['_type'] == "Assign":
      # For parsing assignment statements
      target = get_value_expr(stmt['targets'][0])
      value = get_value_expr(stmt['value'])
      
      if target and value:
        block.append(target+" = "+value)
      
      else:
        pass
    
    elif stmt['_type'] == "Expr":
      value = get_value_expr(stmt['value'])
      block.append(value)
    
    elif stmt['_type'] == "AugAssign":
      # For parsing augmented assignment statements
      target = get_value_expr(stmt['target'])
      value = get_value_expr(stmt['value'])
      op = binary_operators[stmt['op']['_type']]
      
      if target and value and op:
        block.append(target+' '+op+"= "+value)
        
      else:
        pass
      
    elif stmt['_type'] == "If":
      # For parsing If statements
      if block:
        cfg.node(str(count) + '_' + str(nest_count), '\n'.join(block))
        if parent and flag == 0:
          cfg.edge(parent, str(count) + '_' + str(nest_count))
        parent = str(count) + '_' + str(nest_count)
        nest_count += 1
        block = []
       
      test_cond = get_value_expr(stmt['test'])
      
      cfg.node(str(count) + '_' + str(nest_count), \
        'branch[' + str(test_cond) + ']')
      if parent:
        if parent != str(count) + '_' + str(nest_count):
          cfg.edge(parent, str(count) + '_' + str(nest_count))
      parent = str(count) + '_' + str(nest_count)
      nest_count += 1
      
      # tmp_child will maintain node for the statement after if condition
      tmp_child = str(count) + '_' + str(nest_count)
      cfg.node(tmp_child, '\n' + str(count) + '_' + str(nest_count))
      
      cfg_parse(stmt['body'], str(count) + '_' + str(nest_count-1) + '_t', \
        parent, tmp_child)
      
      if stmt['orelse']:
        cfg_parse(stmt['orelse'], str(count) + '_' + str(nest_count-1) + '_f', \
          parent, tmp_child)
      
      else:
        cfg.edge(parent, tmp_child)
      parent = tmp_child
      
      flag = 1
    
    elif stmt['_type'] == "While":
      # For parsing while statements
      loop_cond = ""
      if block:
        loop_cond = block[-1]
        cfg.node(str(count) + '_' + str(nest_count), '\n'.join(block[:-1]))
        if parent and flag == 0:
          cfg.edge(parent, str(count) + '_' + str(nest_count))
        parent = str(count) + '_' + str(nest_count)
        nest_count += 1
        block = []
      
      test_cond = get_value_expr(stmt['test'])
      
      if loop_cond:
        cfg.node(str(count) + '_' + str(nest_count), \
          loop_cond + '\n' +'branch[' + str(test_cond) + ']')
      else:
        cfg.node(str(count) + '_' + str(nest_count), \
          'branch[' + str(test_cond) + ']')
      
      if parent:
        if parent != str(count) + '_' + str(nest_count):
          cfg.edge(parent, str(count) + '_' + str(nest_count))
      parent = str(count) + '_' + str(nest_count)
      nest_count += 1
      
      # tmp_child will maintain node for the statement after while loop
      tmp_child = str(count) + '_' + str(nest_count)
      cfg.node(tmp_child, '\n' + str(count) + '_' + str(nest_count))
      
      cfg_parse(stmt['body'], str(count) + '_' + str(nest_count) + '_t', \
        parent, parent)
      cfg.edge(parent, tmp_child)
      parent = tmp_child
      flag = 1

    else:
      pass
  
  if child == 'exit':
    if '\texit' in cfg.body:
      cfg.body.remove('\texit')
    if block:
      cfg.node(str(count) + '_' + str(nest_count), '\n'.join(block))
      if flag == 0:
        cfg.edge(parent, str(count) + '_' + str(nest_count))
      cfg.node('exit', 'exit')
      cfg.edge(str(count) + '_' + str(nest_count), 'exit')
    
    else:
      cfg.node(str(count) + '_' + str(nest_count), 'exit')
      if flag == 0:
        cfg.edge(parent, str(count) + '_' + str(nest_count))
    
    return
  
  if child:
    cfg.node(str(count) + '_' + str(nest_count), '\n'.join(block))
    if flag == 0:
      cfg.edge(parent, str(count) + '_' + str(nest_count))
    cfg.edge(str(count) + '_' + str(nest_count), child)

  return

if __name__== "__main__" :
  #Parse JSON File to CFG 
  input_file = str(sys.argv[1]).replace("\r", "")
  json_file = os.path.basename(input_file).split('.')[0] + '.json'
  json_file = os.path.join(os.path.dirname(input_file), json_file)
  with open(json_file) as f:
    data = json.load(f)
    cfg.node('entry')
    cfg.node('exit')
    cfg_parse(data['body'], 0, 'entry', 'exit')

  cfg.render(json_file + '.gv', format = 'png', view=True)

