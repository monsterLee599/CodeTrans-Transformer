# this method will add junk code and the code will not run
# if you want add other junk code, you can also them, but you should add new code

from AstToTree import *
from Node import Node
import random

# we have three model:
# random mode: we will add junk code randomly
# head mode: we will add junk code at the beginning of the source code
# tail mode: we will add junk code at the end of the source code

# add junk code
# param: tree_root_node: the root node of the tree generated from ast
#        number: the number of junk code you want to add
#        mode: you shoule select the mode

def AddJunkCode(tree_root_node,number,mode):
    for i in range(0,number):

        identifier_list=GetAllIdentifiers(tree_root_node)

        if mode==0:
            statement_list=FindAllStatement(tree_root_node)
            AddJunkRandom(statement_list,identifier_list)
            #code=TreeToTextJava(tree_root_node)
            #print(code)
        elif mode==1:
            AddJunkHead(tree_root_node,identifier_list)
        elif mode==2:
            AddJunkTail(tree_root_node,identifier_list)
        else:
            print('-- please input 0/1/2 --')

    code=TreeToTextJava(tree_root_node)
    return code

def FindAllStatement(tree_root_node):
    statement_list=[]
    if ('_statement' in tree_root_node.type or tree_root_node.type=='}')  and tree_root_node.parent.type=='block':
        statement_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindAllStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    statement_list.append(result[i])
    else:
        pass

    return statement_list

def GetAllIdentifiers(tree_root_node):
    identifier_list=[]
    if tree_root_node.type=='identifier':
        identifier_list.append(tree_root_node.text)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=GetAllIdentifiers(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    identifier_list.append(result[i])
    else:
        pass
    return identifier_list

def GenerateNewIdentifier(identifier_list):
    identifier_base='junk_identifier_'
    number=0
    while True:
        identifier=identifier_base+str(number)
        number=number+1
        if identifier not in identifier_list:
            break

    return identifier

def AddJunkRandom(statement_list,identifier_list):
    where_to_add= random.randint(0,len(statement_list)-1)
    add_junk_code_index=random.randint(0,4)

    junk_code_node=None

    if add_junk_code_index==0:
        junk_code_node_identifier=GenerateNewIdentifier(identifier_list)
        junk_code_node=AddLocalVariable(junk_code_node_identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPass()

    statement=statement_list[where_to_add]
    parent=statement.parent
    index=parent.children.index(statement)
    parent.children.insert(index,junk_code_node)
    junk_code_node.parent=parent


def AddJunkHead(tree_root_node,identifier_list):
    add_junk_code_index=random.randint(0,4)
    junk_code_node=None
    add_block_index=Node

    for child in tree_root_node.children:
        if child.type=='class_declaration':
            class_body=child.children[-1]
            for child in class_body.children:
                if child.type=='method_declaration':
                    add_block_index=child.children[-1]

    if add_junk_code_index==0:
        junk_code_identifier=GenerateNewIdentifier(identifier_list)
        junk_code_node=AddLocalVariable(junk_code_identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPass()

    add_block_index.children.insert(1,junk_code_node)
    junk_code_node.parent=add_block_index


def AddJunkTail(tree_root_node,identifier_list):
    add_junk_code_index = random.randint(0, 4)
    junk_code_node = None
    add_block_index = Node

    for child in tree_root_node.children:
        if child.type == 'class_declaration':
            class_body = child.children[-1]
            for child in class_body.children:
                if child.type == 'method_declaration':
                    add_block_index = child.children[-1]

    if add_junk_code_index==0:
        identifier=GenerateNewIdentifier(identifier_list)
        junk_code_node=AddLocalVariable(identifier)
    elif add_junk_code_index==1:
        junk_code_node=AddIfStatement()
    elif add_junk_code_index==2:
        junk_code_node=AddForStatement()
    elif add_junk_code_index==3:
        junk_code_node=AddWhileStatement()
    elif add_junk_code_index==4:
        junk_code_node=AddPass()

    add_block_index.children.insert(len(add_block_index.children)-1,junk_code_node)
    junk_code_node.parent=add_block_index


# add an local variable
def AddLocalVariable(identifier):


    local_variable_declaration=Node()
    local_variable_declaration.type='local_variable_declaration'

    integral_type=Node()

    integral_type.type='integer_type'
    integral_type.parent=local_variable_declaration
    local_variable_declaration.addchild(integral_type)

    # byte short int long
    int_type=Node()
    int_type_cho=random.choice(['byte','short','int','long'])
    int_type.type=int_type_cho
    int_type.text=int_type_cho
    int_type.parent=integral_type
    integral_type.addchild(int_type)

    variable_declarator=Node()
    variable_declarator.type='variable_declarator'
    variable_declarator.parent=local_variable_declaration
    local_variable_declaration.addchild(variable_declarator)

    identifier_node=Node()
    identifier_node.type='identifier'
    identifier_node.text=identifier
    identifier_node.parent=variable_declarator
    variable_declarator.addchild(identifier_node)

    equal_node=Node()
    equal_node.type='='
    equal_node.text='='
    equal_node.parent=variable_declarator
    variable_declarator.addchild(equal_node)

    decimal_integer_literal=Node()
    decimal_integer_literal.type='decimal_integer_literal'
    decimal_integer_literal.text=str(random.randint(0,999))
    decimal_integer_literal.parent=variable_declarator
    variable_declarator.addchild(decimal_integer_literal)

    semicolon_node = Node()
    semicolon_node.type = ';'
    semicolon_node.text = ';'
    semicolon_node.parent=local_variable_declaration
    local_variable_declaration.addchild(semicolon_node)

    return local_variable_declaration

# add system.out.println("hello world!");
def SystemPrint():

    expression_statement=Node()
    expression_statement.type='expression_statement'

    method_invocation=Node()
    method_invocation.type='method_invocation'
    method_invocation.parent=expression_statement
    expression_statement.addchild(method_invocation)

    field_access=Node()
    field_access.type='field_access'
    field_access.parent=method_invocation
    method_invocation.addchild(field_access)

    identifier1=Node()
    identifier1.type='identifier'
    identifier1.text='System'
    identifier1.parent=field_access
    field_access.addchild(identifier1)

    point_1=Node()
    point_1.type='.'
    point_1.text='.'
    point_1.parent=field_access
    field_access.addchild(point_1)

    identifier2=Node()
    identifier2.type='identifier'
    identifier2.text='out'
    identifier2.parent=field_access
    field_access.addchild(identifier2)

    point_2=Node()
    point_2.type='.'
    point_2.text='.'
    point_2.parent=method_invocation
    method_invocation.addchild(point_2)

    identifier3=Node()
    identifier3.type='identifier'
    identifier3.text='println'
    identifier3.parent=method_invocation
    method_invocation.addchild(identifier3)

    argument_list=Node()
    argument_list.type='argument_list'
    argument_list.parent=method_invocation
    method_invocation.addchild(argument_list)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=argument_list
    argument_list.addchild(left_paren)

    string_literal=Node()
    string_literal.type='string_literal'
    string_literal.text='"hello world"'
    string_literal.parent=argument_list
    argument_list.addchild(string_literal)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=argument_list
    argument_list.addchild(right_paren)

    semicolon_node = Node()
    semicolon_node.type = ';'
    semicolon_node.text = ';'
    semicolon_node.parent=expression_statement
    expression_statement.addchild(semicolon_node)

    return expression_statement

# add if(0>1){ system.out.println("hello world"); }
def AddIfStatement():
    if_statement=Node()
    if_statement.type='if_statement'

    if_node=Node()
    if_node.type='if'
    if_node.text='if'
    if_node.parent=if_statement
    if_statement.addchild(if_node)

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=if_statement
    if_statement.addchild(parenthesized_expression)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(left_paren)

    binary_expression=Node()
    binary_expression.type='binary_expression'
    binary_expression.parent=parenthesized_expression
    parenthesized_expression.addchild(binary_expression)

    left_value=Node()
    left_value.type='decimal_integer_literal'
    left_value.text='0'
    left_value.parent=binary_expression
    binary_expression.addchild(left_value)

    operator=Node()
    operator.type='>'
    operator.text='>'
    operator.parent=binary_expression
    binary_expression.addchild(operator)

    right_value=Node()
    right_value.type='decimal_integer_literal'
    right_value.text='1'
    right_value.parent=binary_expression
    binary_expression.addchild(right_value)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    block=Node()
    block.type='block'
    block.parent=if_statement
    if_statement.addchild(block)

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=block
    block.addchild(left_brace)

    expression_statement=SystemPrint()

    expression_statement.parent=block
    block.addchild(expression_statement)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)

    return if_statement


# add for statement
# example: for(int i=0;i<10;i++){ System.out.println("hello world"); }
def AddForStatement():
    for_statement=Node()
    for_statement.type='for_statement'

    for_node=Node()
    for_node.type='for'
    for_node.text='for'
    for_node.parent=for_statement
    for_statement.addchild(for_node)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=for_statement
    for_statement.addchild(left_paren)

    local_variable_declaration=AddLocalVariable('i')
    local_variable_declaration.parent=for_statement
    for_statement.addchild(local_variable_declaration)

    binary_expression=Node()
    binary_expression.type='binary_expression'
    binary_expression.parent=for_statement
    for_statement.addchild(binary_expression)

    identifier_1=Node()
    identifier_1.type='identifier'
    identifier_1.text='i'
    identifier_1.parent=binary_expression
    binary_expression.addchild(identifier_1)

    operator=Node()
    operator.type='<'
    operator.text='<'
    operator.parent=binary_expression
    binary_expression.addchild(operator)

    decimal_integer_literal=Node()
    decimal_integer_literal.type='decimal_integer_literal'
    decimal_integer_literal.text='1000'
    decimal_integer_literal.parent=binary_expression
    binary_expression.addchild(decimal_integer_literal)

    semicolon_node = Node()
    semicolon_node.type = ';'
    semicolon_node.text = ';'
    semicolon_node.parent=for_statement
    for_statement.addchild(semicolon_node)

    update_expression=Node()
    update_expression.type='update_expression'
    update_expression.parent=for_statement
    for_statement.addchild(update_expression)

    identifier_2=Node()
    identifier_2.type='identifier'
    identifier_2.text='i'
    identifier_2.parent=update_expression
    update_expression.addchild(identifier_2)

    unary_node=Node()
    unary_node.type='++'
    unary_node.text='++'
    unary_node.parent=update_expression
    update_expression.addchild(unary_node)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=for_statement
    for_statement.addchild(right_paren)

    block=Node()
    block.type='block'
    block.parent=for_statement
    for_statement.addchild(block)

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=block
    block.addchild(left_brace)

    expression_statement=SystemPrint()
    expression_statement.parent=block
    block.addchild(expression_statement)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)

    return for_statement

# add while(0>1){ System.out.println("hello world!"); }
def AddWhileStatement():

    while_statement=Node()
    while_statement.type='while_statement'

    while_node=Node()
    while_node.type='while'
    while_node.text='while'
    while_node.parent=while_statement
    while_statement.addchild(while_node)

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=while_statement
    while_statement.addchild(parenthesized_expression)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(left_paren)

    binary_expression=Node()
    binary_expression.type='binary_expression'
    binary_expression.parent=parenthesized_expression
    parenthesized_expression.addchild(binary_expression)

    left_value=Node()
    left_value.type='decimal_integer_literal'
    left_value.text='0'
    left_value.parent=binary_expression
    binary_expression.addchild(left_value)

    operator=Node()
    operator.type='>'
    operator.text='>'
    operator.parent=binary_expression
    binary_expression.addchild(operator)

    right_value=Node()
    right_value.type='decimal_integer_literal'
    right_value.text='1'
    right_value.parent=binary_expression
    binary_expression.addchild(right_value)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    block=Node()
    block.type='block'
    block.parent=while_statement
    while_statement.addchild(block)

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=block
    block.addchild(left_brace)

    expression_statement=SystemPrint()
    expression_statement.parent=block
    block.addchild(expression_statement)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)

    return while_statement

# addd pass
def AddPass():
    semicolon = Node()
    semicolon.type=';'
    semicolon.text=';'

    return semicolon











