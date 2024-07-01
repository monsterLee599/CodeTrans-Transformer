# byte -> short -> int -> long
# we will transform the type of variable in declaration statement, for example, short x =0; -> int x=0;

from AstToTree import *
from Node import Node
import random
from random import choice

# in this function, we will replace the integer with higher integral type, for example: int x=0; -> long x=0;
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def IntegralTransformation(tree_root_node):
    integer_list=FindInteger(tree_root_node)
    if len(integer_list)==0:
        return 0
    else:
        for i in range(0,len(integer_list)):
            ProcessInteger(integer_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has integer and the type is byte short int, because the long type has no upper, so we will not look for it
# param: tree_root_node: the root node of tree generated from ast
# return: true/false
def IsInteger(tree_root_node):
    integral_type=['byte','short','int']

    if tree_root_node.type in integral_type:
        if tree_root_node.parent.type=='integral_type':
            if tree_root_node.parent.parent.type=='field_declaration' or tree_root_node.parent.parent.type=='local_variable_declaration':
                return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsInteger(child)
            if result==True:
                return True
        return False

    return False

# return the list of integral node
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of integral node
def FindInteger(tree_root_node):
    integer_list=[]
    integral_type=['byte','short','int']

    if tree_root_node.type in integral_type:
        if tree_root_node.parent.type=='integral_type':
            if tree_root_node.parent.parent.type=='field_declaration' or tree_root_node.parent.parent.type=='local_variable_declaration':
                integer_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindInteger(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    integer_list.append(result[i])

    else:
        pass

    return integer_list

# we will replace the integer with higher type
# param: node: the tree node type is integer
# return: None
def ProcessInteger(node):
    if node.type=='byte':
        integral_type=['short','int','long']
        new_integer=choice(integral_type)
        node.type=new_integer
        node.text=new_integer
    elif node.type=='short':
        integral_type=['int','long']
        new_integer=choice(integral_type)
        node.type=new_integer
        node.text=new_integer
    elif node.type=='int':
        node.type='long'
        node.text='long'


