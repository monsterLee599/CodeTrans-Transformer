from Node import Node
from AstToTree import *

# 1 get the comparison operator from the tree generated from the ast
# 2 if the comparison has < > >= <=
# 3 transform the code
# but we only process the operator like x<y, if x<y<z occured,we do not process it

#change the comparison operator, for example: x>y -> y<x
#para: tree_root_node: the root node of a tree generated from the ast
#return: the new code if there if no comaprison operator , we will rerurn 0
def ComparisonTransformer(tree_root_node):
    comparison_list=GetComparisonOperator(tree_root_node)
    iscomparison_list=[]
    for i in range(0,len(comparison_list)):
        retult=IsComparisonOperator(comparison_list[i])
        if retult==True:
            iscomparison_list.append(comparison_list[i])
        else:
            continue
    if len(iscomparison_list)==0:
        return 0
    # transformer
    for i in range(0,len(iscomparison_list)):
        operator_node=iscomparison_list[i].children[1]
        left_node=iscomparison_list[i].children[0]
        right_node=iscomparison_list[i].children[2]
        iscomparison_list[i].children[0]=right_node
        iscomparison_list[i].children[2]=left_node

        if operator_node.type=='<=':
            operator_node.type='>='
            operator_node.text='>='
        elif operator_node.type=='>=':
            operator_node.type='<='
            operator_node.text='<='
        elif operator_node.type=='<':
            operator_node.type='>'
            operator_node.text='>'
        elif operator_node.type=='>':
            operator_node.type='<'
            operator_node.text='<'

    code=TreeToTextPy(tree_root_node)
    return code



#get the list of comparison operator from the tree
#param: the node of a tree generated from the ast
#return : the list of comparison operator
def GetComparisonOperator(node):
    comparison_list=[]
    if node.type=='comparison_operator' and len(node.children)==3:
        comparison_list.append(node)

    #internal node
    if len(node.children)!=0:
        for child in node.children:
            result=GetComparisonOperator(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    comparison_list.append(result[i])

    else:
        pass

    return comparison_list

#if the comparison operator meets our requirements
# the root node of comparison operator
# return true of false
def IsComparisonOperator(node):
    operator_type=node.children[1].type
    if (operator_type=='>=' or operator_type=='<=' or operator_type=='>' or operator_type=='<') and len(node.children)==3:
        return True
    else:
        return False

