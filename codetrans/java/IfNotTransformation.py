# this function will transform the if statement
# for example:
# if (x>=0){
#     block1
# }
# else{
#     block2
# }
# we can transform it to:
# if(!(x>=0)){
#     block2
# }
# else{
# block1
# }

from AstToTree import *
from GetAST import *
from Node import Node

# this is the main function that transform the code
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def IfNotTransformation(tree_root_node):
    if_list=FindIfAndElseStatement(tree_root_node)
    if_list=DelComment(if_list)
    if len(if_list)==0:
        return 0
    else:
        for i in range(0,len(if_list)):
            ProcessIfNot(if_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has if statement, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsIfAndElseStatement(tree_root_node):
    if tree_root_node.type=='if_statement':
        for child in tree_root_node.children:
            if child.type=='else':
                return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsIfAndElseStatement(child)
            if result==True:
                return True
        return False

    else:
        return False

# return the list of if statement
# param: tree_root_node: the root node of the tree generated from ast
# return: list of if statement
def FindIfAndElseStatement(tree_root_node):
    if_list = []
    if tree_root_node.type == 'if_statement':
        for child in tree_root_node.children:
            if child.type=='else':
                if_list.append(tree_root_node)
                break

    if len(tree_root_node.children) != 0:
        for child in tree_root_node.children:
            result = FindIfAndElseStatement(child)
            if len(result) != 0:
                for i in range(0, len(result)):
                    if_list.append(result[i])

    else:
        pass
    return if_list

# return the list of if statement that has no comment
# param: if_list: the list of if statement
# return: new list of if statement
def DelComment(if_list):
    if_no_comment_list=[]
    for i in range(0,len(if_list)):
        is_comment=False
        for child in if_list[i].children:
            if child.type=='comment':
                is_comment=True
                break
        if not is_comment:
            if_no_comment_list.append(if_list[i])

    return if_no_comment_list

# process the if statement
# param: the tree node which type is if_statement
# return: none
def ProcessIfNot(if_statement_node):
    condition=if_statement_node.children[1]

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=if_statement_node
    if_statement_node.children[1]=parenthesized_expression

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(left_paren)

    unary_expression=Node()
    unary_expression.type='unary_expression'
    unary_expression.parent=parenthesized_expression
    parenthesized_expression.addchild(unary_expression)

    logical_not=Node()
    logical_not.type='!'
    logical_not.text='!'
    logical_not.parent=unary_expression
    unary_expression.addchild(logical_not)

    condition.parent=unary_expression
    unary_expression.addchild(condition)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    if_content=if_statement_node.children[2]
    else_content=if_statement_node.children[4]

    if_statement_node.children[2]=else_content
    if_statement_node.children[4]=if_content

