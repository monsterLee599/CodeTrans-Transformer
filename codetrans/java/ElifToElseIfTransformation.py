# in this transformation, we will convert the else if{} statement to else { if {} } statement
# for example:
#if ...
#else if ...
#else ...
#we will convert it to :
#if ...
#else :
#    if ...
#    else ...

from AstToTree import *
from Node import Node
from GetAST import *

#this function will convert else if statement into else { if{} }
#param: tree_root_node: the root node of the tree generated from ast
#return: the new code
def ElifToElseIf(tree_root_node):
    result=FindElif(tree_root_node)
    if len(result)==0:
        return 0
    else:
        for i in range(0,len(result)):
            ProcessElif(result[i])

        code=TreeToTextJava(tree_root_node)
        return code

#if the code has else if statement, it will convert it to else{ if{} } statement
#param: tree_root_node: the root node of the tree generated from ast
#return true/false
def IsElif(tree_root_node):
    if tree_root_node.type=='else':
        index=tree_root_node.parent.children.index(tree_root_node)
        if tree_root_node.parent.children[index + 1].type == 'if_statement' and tree_root_node.parent.type=='if_statement':
            return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsElif(child)
            if result==True:
                return True
        return False

    else:
        return False

#return the list of else if statement
#param: tree_root_node: the root node of the tree generated from ast
#return: the list of else if node
def FindElif(tree_root_node):
    elif_list=[]
    if tree_root_node.type=='else':
        index=tree_root_node.parent.children.index(tree_root_node)
        if tree_root_node.parent.children[index + 1].type == 'if_statement' and tree_root_node.parent.type=='if_statement':
            elif_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindElif(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    elif_list.append(result[i])

    else:
        pass

    return elif_list

# we will convert the else if statement to else{ if{} }
# param: the node of tree which type is else and the next node type is if_statement
#return: None
def ProcessElif(node):
    #in tree_sitter, the structure of the if statement is : if statement-> if | param | block | else | if_statement
    #so we can easily replace the if_statement with block next to else, and the if_statement can be the child of the new block
    replace_index=node.parent.children.index(node)+1
    if_statement=node.parent.children[replace_index]
    #create a new block node
    block_node=Node()
    block_node.type='block'
    block_node.parent=node.parent
    node.parent.children[replace_index]=block_node

    #create the left bracket
    left_bracket_node=Node()
    left_bracket_node.type='{'
    left_bracket_node.text='{'
    left_bracket_node.parent=block_node
    block_node.addchild(left_bracket_node)

    #now the if_statement will be the child of the block node
    block_node.addchild(if_statement)
    if_statement.parent=block_node

    #create the right bracket too
    right_bracket_node=Node()
    right_bracket_node.type='}'
    right_bracket_node.text='}'
    right_bracket_node.parent=block_node
    block_node.addchild(right_bracket_node)


