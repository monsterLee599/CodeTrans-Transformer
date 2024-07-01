from AstToTree import *
from Node import Node

#True->1; False-> 0
#param: tree_root_node: the root node of tree generated from ast
#return : code: new code that True->1 false->0
#          jud: is the code has true or false
def BoolToInt(tree_root_node):
    jud=operate(tree_root_node)
    for child in tree_root_node.children:
        result=recruoperate(child)
        if result==True:
            jud=True
        else:
            continue
    return TreeToTextPy(tree_root_node),jud

# change node type and text
# param: the node of tree
# return : true or false
def operate(node):
    if node.type=='true':
        node.type='integer'
        node.text='1'
        return True
    elif node.type=='false':
        node.type='integer'
        node.text='0'
        return True
    else:
        return False


# recrute the operate
# param: tree node
# return: true or false
def recruoperate(node):

    jud=False
    #internal_node
    if len(node.children)!=0:
        retuls=operate(node)
        if retuls==True:
           jud=True
        for child in node.children:
            result=recruoperate(child)
            if result==True:
                jud=True
            else:
                continue
    #leaf node
    else:
        jud=operate(node)

    return jud