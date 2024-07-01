from AstToTree import *
from Node import Node

#1->True; 0->False
#param: tree_root_node: the root node of the tree generated from ast
#return code: the new code that 1->True 0->False
#        jud: if the code has 1 or 0
def IntToBool(tree_root_node):
    jud=operate(tree_root_node)
    for child in tree_root_node.children:
        result=recruoperate(child)
        if result==True:
            jud=result
        else:
            continue
    code=TreeToTextPy(tree_root_node)
    return code,jud


#change node type to true or false
#param: node of tree
#return: true: if the node type is integer and text is 0/1; false: if the node type is not integer
def operate(node):
    if node.type=='integer' and node.text=='1':
        node.type='true'
        node.text='True'
        return True

    elif node.type=='integer' and node.text=='0':
        node.type='false'
        node.text='False'
        return True

    else:
        return False


#recrute the operate
#param : tree node
#return :jud: if the node or its child has 1/0 return true else return false
def recruoperate(node):
    jud=False

    #internal node
    if len(node.children)!=0:
        result=operate(node)
        if result==True:
            jud=result
        for child in node.children:
            result=recruoperate(child)
            if result==True:
                jud=result
            else:
                continue

    #leaf node
    else:
       jud=operate(node)

    return jud