import json

def remove_duplicatas(seq, idfun=None): 
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def shunting_yard_parser(tokens):
    output = []
    stack = []
    left_parenthesis = '('
    right_parenthesis = ')'
    precedence = {}
    with open('./indexed/config.json') as f: 
        d = json.load(f)
        precedence = d['precedence_table']

    for token in tokens:
        if token not in precedence:
            output.append(token)

        elif token is left_parenthesis:
            stack.append(token) 

        elif token is right_parenthesis:
            operator = stack.pop()
            while operator != '(':
                output.append(operator)
                operator = stack.pop()

        elif token in precedence:
            if(stack):
                old_operator = stack[-1]
                while(precedence[old_operator] > precedence[token]):
                    output.append(stack.pop())
                    if(stack):
                        old_operator = stack[-1]
            stack.append(token)

    while(stack):
        output.append(stack.pop())

    return output