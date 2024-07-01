#in this function, we will convert the argumented operator into arithmetic operator
#for example, x+=1 -> x=x+1
from Node import Node
from AstToTree import *
from GetAST import *


#this method will convert argumented assignment to normal assignment: x+=1 -> x=x+1
#param: tree_root_node : the root node of the tree generated from the ast
#return: the new code
def ArgumentedAssinment(tree_root_node):
    result=FindArgument(tree_root_node)
    if len(result)==0:
        return 0
    else:
        for i in range(0,len(result)):
            ProcessArgument(result[i])

        code=TreeToTextJava(tree_root_node)
        return code


#if the code has argumented assignment, it will return true, else, it will return false
#param: the root node of the tree generated from ast
#return: true/false
def IsArgument(tree_root_node):
    if tree_root_node.type in ['+=','-=','*=','/=','%=']:
        return True
    elif len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsArgument(child)
            if result==True:
                return True
        return False
    else:
        return False



#return the list of argumented assignment
#param: the root node of the tree generated from ast
#return: list of arumented assignment
def FindArgument(tree_root_node):
    argument_list=[]
    if tree_root_node.type in ['+=','-=','*=','/=','%=']:
        argument_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindArgument(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    argument_list.append(result[i])
    else:
        pass

    return argument_list

#it will process the argumented asignment
#node
#return: None
def ProcessArgument(node):
    operator_dict = {'+=': '+', '-=': '-', '*=': '*', '/=': '/', '%=': '%'}

    left_value=node.parent.children[0]
    operator=node.parent.children[1]
    right_value=node.parent.children[2]
    assignment_expression=node.parent

    assignment_expression.children=[]

    assignment_expression.addchild(left_value)
    left_value.parent=assignment_expression

    equation_node=Node()
    equation_node.type='='
    equation_node.text='='
    equation_node.parent=assignment_expression
    assignment_expression.addchild(equation_node)

    binary_expression_node=Node()
    binary_expression_node.type='binary_expression'
    binary_expression_node.parent=assignment_expression
    assignment_expression.addchild(binary_expression_node)

    left_value_2=Node()
    left_value_2.type=left_value.type
    left_value_2.text=left_value.text
    left_value_2.parent=binary_expression_node
    binary_expression_node.addchild(left_value_2)
    CopySubtreeJava(left_value,left_value_2)

    binary_operator_node=Node()
    binary_operator_node.type=operator_dict[node.type]
    binary_operator_node.text=operator_dict[node.text]
    binary_operator_node.parent=binary_expression_node
    binary_expression_node.addchild(binary_operator_node)

    right_value.parent=binary_expression_node
    binary_expression_node.addchild(right_value)







