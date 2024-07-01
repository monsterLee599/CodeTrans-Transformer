# we will convert the integer to float
from Node import *
from AstToTree import *
import parser
# we will convert the integer to float
#param: the root node of the tree generated from ast
#return: the code add long() convert
def IntToFloat(tree_root_node):
    result=FindInt(tree_root_node)
    if len(result)==0:
        return 0
    for i in range(0,len(result)):
        ProcessIntToFloat(result[i])

    code=TreeToTextPy(tree_root_node)
    return code

#if the code has integer(except for 0 and 1), it will return node.text, else, it will return false
#param: the node of the tree generated from ast
#return node.text or false
def IsInt(node):
    if node.type=='integer' :
        return node.text

    if len(node.children)!=0:
        for child in node.children:
            result=IsInt(child)
            if result!=False:
                return result
            else:
                continue
        return False

    return False

#we will return the list of integers
#param: the node of the tree generated from ast
#return list of integers
def FindInt(node):
    int_list=[]
    number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if node.type=='integer' and node.text!='0' and node.text!='1':
        is_num=True
        for i in range(0,len(node.text)):
            if node.text[i] not in number:
                is_num=False
                break
        if is_num:
            int_list.append(node)
    if len(node.children)!=0:
        for child in node.children:
            result=FindInt(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    int_list.append(result[i])

    else:
        pass

    return int_list

# this method will convert the int to float
# param: the node of the tree generated from ast
# return: None
def ProcessIntToFloat(node):
    # int -> float
    node.type='float'
    integer=node.text
    #print(integer)
    # in python2.x, integer L is ok, but not in python3.x, so we need to delete 'L'
    if 'L' in integer:
        integer=integer.replace('L','')
    if 'j' in integer:
        integer=integer.replace('j','')
    integer=float(integer)
    node.text=str(integer)