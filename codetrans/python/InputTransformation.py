# we will transform the 'input' to 'input_raw' in python

from AstToTree import *
from GetAST import *
from Node import Node

# this is the main function to convert input method to raw_input
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def InputToRawInput(tree_root_node):
    input_list=FindInput(tree_root_node)
    if len(input_list)==0:
        return 0
    else:
        for i in range(0,len(input_list)):
            input_list[i].text='raw_input'

        code=TreeToTextPy(tree_root_node)
        return code

# if the code has print, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true or false
def IsInput(tree_root_node):
    if tree_root_node.type=='identifier' and tree_root_node.text=='input':
        return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsInput(child)
            if result==True:
                return True
        return False
    else:
        return False

# return the list of print node
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of print node
def FindInput(tree_root_node):
    input_list=[]
    if tree_root_node.type=='identifier' and tree_root_node.text=='input':
        input_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindInput(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    input_list.append(result[i])
    else:
        pass

    return input_list

