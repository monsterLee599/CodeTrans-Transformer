from Node import Node
from AstToTree import *

# change the insreasement statement : for example : x+=1 -> x=x+1
# tree root node: the root node of the tree generate from ast
# return : new code
def BinaryOperator(tree_root_node):
    result=FindBinaryOperator(tree_root_node)
    return result

#if the code has binary operator, we will return true, else we will return false
#node: a node of the tree generated from the ast
#return : true/false
def IsBinaryOperator(node):
    if node.type=='+' or node.type=='-' or node.type=='*' or node.type=='/' or node.type=='//' or node.type=='%':
        return True
    else:
        if len(node.children)!=0:
            for child in node.children:
                result=IsBinaryOperator(child)
                if result==True:
                    return True
                else:
                    continue
            return False

        else:
            return False

#return the list of binary operator
#param: the node of the tree generated from ast
#return: the list of binary operator
def FindBinaryOperator(node):
    binary_list=[]
    if node.type=='+' or node.type=='-' or node.type=='*' or node.type=='/' or node.type=='//' or node.type=='%':
        binary_list.append(node)

    if(len(node.children))!=0:
        for child in node.children:
            result=FindBinaryOperator(child)
            if len(result)!=0:
                for i  in range(0,len(result)):
                    binary_list.append(result[i])

    else:
        pass

    return binary_list

#we will process the code that satisfy our need
def ProcessBinaryOperator(node):
    if len(node.parent.parent.children)==3:
        pass

def RecruParentheses(node):
    if node.parent.type=='parenthesized_expression':
        result=RecruParentheses(node.parent)
        return result

    else:
        return node.parent
