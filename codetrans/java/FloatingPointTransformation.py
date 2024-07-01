# this transformation will transform the floating point type
# in java, it can be float or double
# forther more, we can also convert the integer type to floating type
# so, it can be byte -> short -> int -> long -> float -> double

from Node import Node
from AstToTree import *
from random import choice

# in this transformation, we will replace the integer type with upper integer type or floating point type and replace float with double
# param: tree_root_node: the root node of the tree generated from ast
# return: new code
def FloatingTransformation(tree_root_node):
    floating_point_list=FindFloating(tree_root_node)
    if len(floating_point_list)==0:
        return 0
    else:
        for i in range(0,len(floating_point_list)):
            ProcessFloating(floating_point_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has int type or floating point type, it will return True, else it will return false
# param: tree_root_node: the root node of tree generated from ast
# return: true/false
def IsFloating(tree_root_node):
    integral_type=['byte','short','int','long']
    floating_type=['float']

    if tree_root_node.type in integral_type or tree_root_node.type in floating_type:
        if tree_root_node.parent.type=='integral_type' or tree_root_node.parent.type=='floating_point_type':
            if tree_root_node.parent.parent.type=='field_declaration' or tree_root_node.parent.parent.type=='local_variable_declaration':
                return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsFloating(child)
            if result==True:
                return True
        return False

    else:
        return False

# return the list of int type and floating point type
# param: tree_root_node: root node of the tree generated from ast
# return: the list of int type / floating point type
def FindFloating(tree_root_node):
    float_list=[]
    integral_type=['byte','short','int','long']
    floating_type=['float']

    if tree_root_node.type in integral_type or tree_root_node.type in floating_type:
    #if tree_root_node.type in integral_type:
    #if tree_root_node.type in integral_type or tree_root_node.type in floating_type:
        if tree_root_node.parent.type=='integral_type' or tree_root_node.parent.type=='floating_point_type':
        #if tree_root_node.parent.type=='integral_type':
            if tree_root_node.parent.parent.type=='field_declaration' or tree_root_node.parent.parent.type=='local_variable_declaration':
                float_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindFloating(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    float_list.append(result[i])

    else:
        pass

    return float_list

# we will replace integer with higher type or replace integer type with floating point type
# node: the node which type is integer_type or floating_point_type
# return: None
def ProcessFloating(node):
    if node.type=='byte':
        replace_type=['short','int','long','float','double']
        replace=choice(replace_type)
        node.type=replace
        node.text=replace
        if replace in ['float','double']:
            node.parent.type='floating_point_type'
    elif node.type=='short':
        replace_type=['int','long','float','double']
        replace=choice(replace_type)
        node.type=replace
        node.text=replace
        if replace in ['float','double']:
            node.parent.type='floating_point_type'
    elif node.type=='int':
        replace_type=['long','float','double']
        replace=choice(replace_type)
        node.type=replace
        node.text=replace
        if replace in ['float','double']:
            node.parent.type='floating_point_type'
    elif node.type=='long':
        replacea_type=['float','double']
        replace=choice(replacea_type)
        node.type=replace
        node.text=replace
        if replace in ['float','double']:
            node.parent.type='floating_point_type'
    elif node.type=='float':
        node.type='double'
        node.text='double'

