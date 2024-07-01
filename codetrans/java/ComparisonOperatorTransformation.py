#this transformation wll convert the comparison operator
#for example: x>=y -> y<=x

from Node import Node
from AstToTree import *
from GetAST import *

# this function will convert the comparison operator
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code with opposite comparison operator
def ComparisonTransformation(tree_root_node):
    result=FindComparisonOperator(tree_root_node)
    if len(result)==0:
        return 0
    else:
        for i in range(0,len(result)):
            ProcessComparison(result[i])
        code=TreeToTextJava(tree_root_node)
        return code

# if the code has comparison operator, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsComparisonOperator(tree_root_node):
    if tree_root_node.type=='>' or tree_root_node.type=='<' or tree_root_node.type=='>=' or tree_root_node.type=='<=':
        if tree_root_node.parent.type == 'binary_expression':
            return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsComparisonOperator(child)
            if result==True:
                return True

        return False
    else:
        return False

#return the list of comparison operator
#param: tree_root_node: the root node of the tree generated from ast
#return: list of comparison operator
def FindComparisonOperator(tree_root_node):
    comparison_list=[]
    if tree_root_node.type=='>' or tree_root_node.type=='<' or tree_root_node.type=='>=' or tree_root_node.type=='<=':
        if tree_root_node.parent.type=='binary_expression':
            comparison_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindComparisonOperator(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    comparison_list.append(result[i])

    else:
        pass

    return comparison_list

# this function will process the comparison operator
# param: the node of tre which type if comparison operator
# return: None
def ProcessComparison(node):

    if node.type=='>':
        node.type='<'
        node.text='<'
    elif node.type=='<':
        node.type='>'
        node.text='>'
    elif node.type=='>=':
        node.type='<='
        node.text='<='
    elif node.type=='<=':
        node.type='>='
        node.text='>='

    #for exapmle : left_value binary_operator right_value
    #we will convert it and get : right_value binary_operator right_value

    binary_expression_node=node.parent
    operator_index=binary_expression_node.children.index(node)
    left_value=binary_expression_node.children[0:operator_index]
    right_value=binary_expression_node.children[operator_index+1:]

    binary_expression_node.children=[]

    for i in range(0,len(right_value)):
        binary_expression_node.addchild(right_value[i])

    binary_expression_node.addchild(node)

    for i in range(0,len(left_value)):
        binary_expression_node.addchild(left_value[i])



