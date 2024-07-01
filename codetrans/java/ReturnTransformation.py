# this transformation will change the return statement
# if the return statement return integer, we will return a variable
# for example, return 0; -> int x=0; return x;

from Node import Node
from AstToTree import *

def ReturnTransformation(tree_root_node):
    return_list=FindReturnStatement(tree_root_node)
    return_list=FindUsefulReturn(return_list)
    if len(return_list)==0:
        return 0
    else:
        for i in range(0,len(return_list)):
            identifier='return_variable_'+str(i)
            ProcessReturnStatement(return_list[i],identifier)
        code=TreeToTextJava(tree_root_node)
        return code

def IsReturnStatement(tree_root_node):
    if tree_root_node.type=='return_statement':
        return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsReturnStatement(child)
            if result==True:
                return True
        return False
    else:
        return False

def FindReturnStatement(tree_root_node):
    return_list=[]
    if tree_root_node.type=='return_statement':
        return_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindReturnStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    return_list.append(result[i])

    else:
        pass

    return return_list

# we only accept the four return type:decimal_floating_point_literal decimal_integer_literal true false
def FindUsefulReturn(return_list):
    return_type_list=['decimal_floating_point_literal','decimal_integer_literal','false', 'true']
    accept_return_list=[]
    for i in range(0,len(return_list)):
        if return_list[i].children[1].type in return_type_list and len(return_list[i].children)==3:
            accept_return_list.append(return_list[i])

    return accept_return_list

def ProcessReturnStatement(node,variable_name):
    parent = node.parent
    index = parent.children.index(node)

    block = Node()
    block.type = 'block'
    block.parent = parent
    parent.children[index] = block

    left_brace = Node()
    left_brace.type = '{'
    left_brace.text = '{'
    left_brace.parent = block
    block.addchild(left_brace)

    local_variable_declaration=Node()
    local_variable_declaration.type='local_variable_declaration'
    local_variable_declaration.parent=block
    block.addchild(local_variable_declaration)

    if node.children[1].type=='decimal_integer_literal':
        integral_type=Node()
        integral_type.type='integral_type'
        integral_type.parent=local_variable_declaration
        local_variable_declaration.addchild(integral_type)
        int_node=Node()
        int_node.type='int'
        int_node.text='int'
        int_node.parent=integral_type
        integral_type.addchild(int_node)

    elif node.children[1].type=='decimal_floating_point_literal':
        floating_point_type=Node()
        floating_point_type.type='floating_point_type'
        floating_point_type.parent=local_variable_declaration
        local_variable_declaration.addchild(floating_point_type)
        double_node=Node()
        double_node.type='double'
        double_node.text='double'
        double_node.parent=floating_point_type
        floating_point_type.addchild(double_node)

    elif node.children[1].type=='false' or node.children[1].type=='true':
        boolean_type=Node()
        boolean_type.type='boolean_type'
        boolean_type.text='boolean'
        boolean_type.parent=local_variable_declaration
        local_variable_declaration.addchild(boolean_type)

    variable_declarator=Node()
    variable_declarator.type='variable_declarator'
    variable_declarator.parent=local_variable_declaration
    local_variable_declaration.addchild(variable_declarator)

    variable=Node()
    variable.type='identifier'
    variable.text=variable_name
    variable.parent=variable_declarator
    variable_declarator.addchild(variable)

    equal_node=Node()
    equal_node.type='='
    equal_node.text='='
    equal_node.parent=variable_declarator
    variable_declarator.addchild(equal_node)

    variable_declarator.addchild(node.children[1])
    node.children[1].parent=variable_declarator

    semicolon_node=Node()
    semicolon_node.type=';'
    semicolon_node.text=';'
    semicolon_node.parent=local_variable_declaration
    local_variable_declaration.addchild(semicolon_node)

    return_variable=Node()
    return_variable.type='identifier'
    return_variable.text=variable_name
    return_variable.parent=node
    node.children[1]=return_variable

    block.addchild(node)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)

