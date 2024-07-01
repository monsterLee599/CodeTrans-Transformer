from Node import Node
from AstToTree import *
import random

#we will add junk code in this transformation
#we will give you a list, and you can add your junk code, but you should satisfy the code

# we have three mode:
# the random mode: we will add junk code randomly;
# head mode: we will add junk code at the start of the code;
# tail mode: we will add the junk code at the end of the code

def AddJunkCode(tree_root_node,number,mode):
    for i in range(0,number):
        identifiers_list=GetAllIdentifier(tree_root_node)
        #print(identifiers_list)
        # insert junk code randomly
        if mode==0:
            statement_list=FindAllStatement(tree_root_node)
            AddJunkRandom(statement_list,identifiers_list)
        elif mode==1:
            AddJunkHead(tree_root_node,identifiers_list)
        elif mode==2:
            AddJunkTail(tree_root_node,identifiers_list)

    code=TreeToTextPy(tree_root_node)
    return code

def FindAllStatement(tree_root_node):
    statement_list=[]
    if tree_root_node.type in python_statement:
        statement_list.append(tree_root_node)
    # if the node has children
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindAllStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    statement_list.append(result[i])
    else:
        pass

    return statement_list

#we will generate a new identifier that not in the identifier list
#param: the list of identifier
#return: the new identifier that not in the identifier list
def GenerateNewIdentifier(identifier_list):
    identifier_base='junk_identifier_'
    number=0
    while True:
        identifier=identifier_base+str(number)
        number=number+1
        if identifier not in identifier_list:
            break

    return identifier

#in this mode, we will add the junk code randomly
#param: the node of the tree generated from ast
#return :none
def AddJunkRandom(statement_list,identifiers_list):
    #make sure where to insert the junk statement
    where_to_add=random.randint(0,len(statement_list)-1)
    add_junk_code_index=random.randint(0,4)

    junk_code_node=None
    if add_junk_code_index==0:
        # generate the identifier that not in the identifier list
        junk_code_identifier=GenerateNewIdentifier(identifiers_list)
        junk_code_node=AddAssignment(junk_code_identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPassStatement()

    # we first find where to asert the junk code, then we add the junk code before the index  statement
    statement=statement_list[where_to_add]
    parent=statement.parent
    index=parent.children.index(statement)
    parent.children.insert(index,junk_code_node)
    junk_code_node.parent=parent
    ResetLevelPY(junk_code_node)

#in this mode, we will insert the junk code at the beginning of the code
#param: the root node of the tree generated form ast
#return: none
def AddJunkHead(tree_root_node,identifiers_list):
    #decide which mode
    add_junk_code_index=random.randint(0,4)
    #add_junk_code_index=0
    junk_code_node=None

    if add_junk_code_index==0:
        junk_code_identifier=GenerateNewIdentifier(identifiers_list)
        junk_code_node=AddAssignment(junk_code_identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPassStatement()

    #we add the junk code at the beginning of the code
    tree_root_node.children.insert(0,junk_code_node)
    junk_code_node.parent=tree_root_node
    #reset the level of junk code
    ResetLevelPY(junk_code_node)

#in this mode, we will inert the junk code at the end of the code
#param: the root node of tree generated from ast
#return: none
def AddJunkTail(tree_root_node,identifiers_list):
    # decide the mode of junk code
    add_junk_code_index=random.randint(0,4)
    junk_code_node=None

    if add_junk_code_index==0:
        identifier=GenerateNewIdentifier(identifiers_list)
        junk_code_node=AddAssignment(identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPassStatement()

    tree_root_node.addchild(junk_code_node)
    junk_code_node.parent=tree_root_node
    #reset the level of junk code
    ResetLevelPY(junk_code_node)

# in this function, we will get all the identifiers
def GetAllIdentifier(tree_root_node):
    identifier_list=[]
    if tree_root_node.type=='identifier':
        identifier_list.append(tree_root_node.text)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=GetAllIdentifier(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    identifier_list.append(result[i])
    else:
        pass

    return identifier_list

#we will add assignment, for example: x=0
def AddAssignment(identifier):
    expression_node=Node()
    expression_node.type='expression_statement'

    assignment_node=Node()
    assignment_node.type='assignment'
    assignment_node.parent=expression_node
    expression_node.addchild(assignment_node)

    identifier_node=Node()
    identifier_node.type='identifier'
    identifier_node.text=identifier
    identifier_node.parent=assignment_node
    assignment_node.addchild(identifier_node)

    equal_node=Node()
    equal_node.type='='
    equal_node.text='='
    equal_node.parent=assignment_node
    assignment_node.addchild(equal_node)

    integer_node=Node()
    integer_node.type='integer'
    integer_node.text=str(random.randint(0,999))
    integer_node.parent=assignment_node
    assignment_node.addchild(integer_node)

    return expression_node

# if 0 : print('hello world')
def AddIfStatement():
    if_statement_node=Node()
    if_statement_node.type='if_statement'

    if_node=Node()
    if_node.type='if'
    if_node.text='if'
    if_node.parent=if_statement_node
    if_statement_node.addchild(if_node)

    integer_node=Node()
    integer_node.type='integer'
    integer_node.text='0'
    integer_node.parent=if_statement_node
    if_statement_node.addchild(integer_node)

    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=if_statement_node
    if_statement_node.addchild(colon_node)

    block_node=Node()
    block_node.type='block'
    block_node.parent=if_statement_node
    if_statement_node.addchild(block_node)

    expression_statement_node=Node()
    expression_statement_node.type='expression_statement'
    expression_statement_node.parent=block_node
    block_node.addchild(expression_statement_node)

    call_node=Node()
    call_node.type='call'
    call_node.parent=expression_statement_node
    expression_statement_node.addchild(call_node)

    function_name_node=Node()
    function_name_node.type='identifier'
    function_name_node.text='print'
    function_name_node.parent=call_node
    call_node.addchild(function_name_node)

    argument_list_node=Node()
    argument_list_node.type='argument_list'
    argument_list_node.parent=call_node
    call_node.addchild(argument_list_node)

    left_parenthesis_node=Node()
    left_parenthesis_node.type='('
    left_parenthesis_node.text='('
    left_parenthesis_node.parent=argument_list_node
    argument_list_node.addchild(left_parenthesis_node)

    string_node=Node()
    string_node.type='string'
    string_node.text='"hello world"'
    string_node.parent=argument_list_node
    argument_list_node.addchild(string_node)

    right_parethesis_node=Node()
    right_parethesis_node.type=')'
    right_parethesis_node.text=')'
    right_parethesis_node.parent=argument_list_node
    argument_list_node.addchild(right_parethesis_node)

    return if_statement_node

#in this function, we will add for statement-> for i in range(0,10): print(i)
def AddForStatement():
    For_statement_node=Node()
    For_statement_node.type='for_statement'

    for_node=Node()
    for_node.type='for'
    for_node.text='for'
    for_node.parent=For_statement_node
    For_statement_node.addchild(for_node)

    identifier_node=Node()
    identifier_node.type='identifier'
    identifier_node.text='i'
    identifier_node.parent=For_statement_node
    For_statement_node.addchild(identifier_node)

    in_node=Node()
    in_node.type='in'
    in_node.text='in'
    in_node.parent=For_statement_node
    For_statement_node.addchild(in_node)

    call_node=Node()
    call_node.type='call'
    call_node.parent=For_statement_node
    For_statement_node.addchild(call_node)

    method_name_node=Node()
    method_name_node.type='identifier'
    method_name_node.text='range'
    method_name_node.parent=call_node
    call_node.addchild(method_name_node)

    argument_list_node=Node()
    argument_list_node.type='argument_list'
    argument_list_node.parent=call_node
    call_node.addchild(argument_list_node)

    left_parenthesis_node=Node()
    left_parenthesis_node.type='('
    left_parenthesis_node.text='('
    left_parenthesis_node.parent=argument_list_node
    argument_list_node.addchild(left_parenthesis_node)

    integer_start_node=Node()
    integer_start_node.type='integer'
    integer_start_node.text='0'
    integer_start_node.parent=argument_list_node
    argument_list_node.addchild(integer_start_node)

    comma_node=Node()
    comma_node.type=','
    comma_node.text=','
    comma_node.parent=argument_list_node
    argument_list_node.addchild(comma_node)

    integer_end_node=Node()
    integer_end_node.type='integer'
    integer_end_node.text='10'
    integer_end_node.parent=argument_list_node
    argument_list_node.addchild(integer_end_node)

    right_parenthesis_node=Node()
    right_parenthesis_node.type=')'
    right_parenthesis_node.text=')'
    right_parenthesis_node.parent=argument_list_node
    argument_list_node.addchild(right_parenthesis_node)

    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=For_statement_node
    For_statement_node.addchild(colon_node)

    block_node=Node()
    block_node.type='block'
    block_node.parent=For_statement_node
    For_statement_node.addchild(block_node)

    expression_statement = Node()
    expression_statement.type = 'expression_statement'
    expression_statement.parent = block_node
    block_node.addchild(expression_statement)

    print_call_node=Node()
    print_call_node.type='call'
    print_call_node.parent=expression_statement
    expression_statement.addchild(print_call_node)

    print_method_name_node=Node()
    print_method_name_node.type='identifier'
    print_method_name_node.text='print'
    print_method_name_node.parent=print_call_node
    print_call_node.addchild(print_method_name_node)

    print_argument_list_node=Node()
    print_argument_list_node.type='argument_list'
    print_argument_list_node.parent=print_call_node
    print_call_node.addchild(print_argument_list_node)

    print_left_parenthesis_node=Node()
    print_left_parenthesis_node.type='('
    print_left_parenthesis_node.text='('
    print_left_parenthesis_node.parent=print_argument_list_node
    print_argument_list_node.addchild(print_left_parenthesis_node)

    i_identifier_node=Node()
    i_identifier_node.type='identifier'
    i_identifier_node.text='i'
    i_identifier_node.parent=print_argument_list_node
    print_argument_list_node.addchild(i_identifier_node)

    print_right_parenthesis_node=Node()
    print_right_parenthesis_node.type=')'
    print_right_parenthesis_node.text=')'
    print_right_parenthesis_node.parent=print_argument_list_node
    print_argument_list_node.addchild(print_right_parenthesis_node)

    return For_statement_node

# in this function, we will add while junk code-> while 0 : print('hello world')
def AddWhileStatement():
    while_statement_node=Node()
    while_statement_node.type='while_statement'

    while_node=Node()
    while_node.type='while'
    while_node.text='while'
    while_node.parent=while_statement_node
    while_statement_node.addchild(while_node)

    integer_node=Node()
    integer_node.type='integer'
    integer_node.text='0'
    integer_node.parent=while_statement_node
    while_statement_node.addchild(integer_node)

    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=while_statement_node
    while_statement_node.addchild(colon_node)

    block_node=Node()
    block_node.type='block'
    block_node.parent=while_statement_node
    while_statement_node.addchild(block_node)

    expression_statement_node=Node()
    expression_statement_node.type='expression_statement'
    expression_statement_node.parent=block_node
    block_node.addchild(expression_statement_node)

    call_node=Node()
    call_node.type='call'
    call_node.parent=expression_statement_node
    expression_statement_node.addchild(call_node)

    method_name_node=Node()
    method_name_node.type='identifier'
    method_name_node.text='print'
    method_name_node.parent=call_node
    call_node.addchild(method_name_node)

    argument_list_node=Node()
    argument_list_node.type='argument_list'
    argument_list_node.parent=call_node
    call_node.addchild(argument_list_node)

    left_parenthesis_node=Node()
    left_parenthesis_node.type='('
    left_parenthesis_node.text='('
    left_parenthesis_node.parent=argument_list_node
    argument_list_node.addchild(left_parenthesis_node)

    string_node=Node()
    string_node.type='string'
    string_node.text='"hello world"'
    string_node.parent=argument_list_node
    argument_list_node.addchild(string_node)

    right_parenthesis_node=Node()
    right_parenthesis_node.type=')'
    right_parenthesis_node.text=')'
    right_parenthesis_node.parent=argument_list_node
    argument_list_node.addchild(right_parenthesis_node)

    return while_statement_node

#in this function, we will pass statement
def AddPassStatement():
    pass_statement_node=Node()
    pass_statement_node.type='pass_statement'

    pass_node=Node()
    pass_node.type='pass'
    pass_node.text='pass'
    pass_node.parent=pass_statement_node
    pass_statement_node.addchild(pass_node)

    return pass_statement_node


python_statement=[ 'for_statement', 'if_statement', 'try_statement', 'while_statement',
                   'with_statement', 'assert_statement', 'break_statement', 'continue_statement', 'delete_statement', 'exec_statement', 'expression_statement',
                  'future_import_statement', 'global_statement', 'import_from_statement', 'import_statement', 'nonlocal_statement', 'pass_statement',
                  'print_statement', 'raise_statement', 'return_statement', '_compound_statement', '_simple_statement', 'yield_statement', 'match_statement']
