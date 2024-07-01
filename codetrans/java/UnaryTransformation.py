#if the x++ or x-- appeared in the source code, we will convert it to x=x+1/x=x-1

from Node import Node
from AstToTree import *
from GetAST import *

#this method will convert the unary operator to binary operator: x++ -> x=x+1
#param:tree_root_node: the root node of the tree generated from ast
#return: the new code with binary operator
def UnaryToBinary(tree_root_node):
    result=FindUnary(tree_root_node)
    if len(result)==0:
        return 0
    else:
        for i in range(0,len(result)):
            ProcessUnary(result[i])

        code=TreeToTextJava(tree_root_node)
        return code

#if the code has unary operator, it will return True, else it will return false
#pram: tre_root_node: root node of the tree generated from ast
#return: True/False
def IsUnary(tree_root_node):
    if tree_root_node.type=='++' or tree_root_node.type=='--' :
        return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsUnary(child)
            if result==True:
                return True
        return False
    else:
        return False


#return the list of unary operator
#param: tree_root_node: the root node of the tree generated from ast
#return: list of unary operator
def FindUnary(tree_root_node):
    unary_list=[]
    if tree_root_node.type=='++' or tree_root_node.type=='--':
        unary_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindUnary(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    unary_list.append(result[i])
    else:
        pass

    return unary_list

#this function will operate the unary operator
#param: node: the node of tree which type is ++ or --
#return: None
def ProcessUnary(node):
    unary_dict={'++':'+','--':'-'}

    update_expression=node.parent
    unary_index=update_expression.children.index(node)
    value_node=update_expression.children[1-unary_index]

    assignment_expression_node=Node()
    assignment_expression_node.type='assignment_expression'
    assignment_expression_node.parent=update_expression.parent
    update_exprssion_index=update_expression.parent.children.index(update_expression)
    update_expression_parent=update_expression.parent
    update_expression_parent.children[update_exprssion_index]=assignment_expression_node

    value_node.parent=assignment_expression_node
    assignment_expression_node.addchild(value_node)

    equation_node=Node()
    equation_node.type='='
    equation_node.text='='
    equation_node.parent=assignment_expression_node
    assignment_expression_node.addchild(equation_node)

    binary_expression_node=Node()
    binary_expression_node.type='binary_expression'
    binary_expression_node.parent=assignment_expression_node
    assignment_expression_node.addchild(binary_expression_node)

    value_2_node=Node()
    value_2_node.type=value_node.type
    value_2_node.text=value_node.text
    binary_expression_node.addchild(value_2_node)
    CopySubtreeJava(value_node,value_2_node)

    binary_operator_node=Node()
    binary_operator_node.type=unary_dict[node.type]
    binary_operator_node.text=unary_dict[node.text]
    binary_operator_node.parent=binary_expression_node
    binary_expression_node.addchild(binary_operator_node)

    integer_node=Node()
    integer_node.type='decimal_integer_literal'
    integer_node.text='1'
    integer_node.parent=binary_expression_node
    binary_expression_node.addchild(integer_node)

