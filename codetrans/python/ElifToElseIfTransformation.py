from Node import Node
from AstToTree import *

#we will convert the elif statement to else if statement, for example:
#if ...
#elif ...
#else ...
#we will convert it to :
#if ...
#else :
#    if ...
#    else ...

#convert elif statement to else if statement
#param: the root node of the tree generated from ast
#return: the new code that convert the elif statement to else if statement
def ElifToElseIf(tree_root_node):
    result=FindElif(tree_root_node)
    if len(result)==0:
        return 0

    for i in range(0,len(result)):
        ProcessElif(result[i])

    code=TreeToTextPy(tree_root_node)
    return code


# if the code has elif statement, we will return True,else we will return False
# param: the node of tree generated from ast
# return True or false
def IsElif(node):
    if node.type=='elif_clause':
        return True

    # if the node has children
    if len(node.children)!=0:
        for child in node.children:
            result=IsElif(child)
            if result==True:
                return True
        return False
    # is the node has no children
    else:
        return False

# return the list of elif statement
# param: the node of tree generated from ast
# return: list of elif statement
def FindElif(node):
    elif_list=[]
    if node.type=='elif_clause':
        no_comment=True
        for child in node.children:
            if child.type=='comment' or child.type=='string':
                no_comment=False
                break
        if no_comment:
            elif_list.append(node)
    # if the node has children
    if len(node.children)!=0:
        for child in node.children:
            result=FindElif(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    elif_list.append(result[i])
    #if the node has no children
    else:
        pass

    return elif_list


#we will convert the elif statement in this function
#param: the node of tree generated from ast, and the type of the node is 'elif_clause'
#return: None
def ProcessElif(elif_node):
    if_statement=elif_node.parent
    elif_node_index=if_statement.children.index(elif_node)
    cand_list=if_statement.children[elif_node_index:]
    if_statement.children=if_statement.children[:elif_node_index]

    #else clause
    else_clause_node=Node()
    else_clause_node.type='else_clause'
    else_clause_node.parent=if_statement
    if_statement.addchild(else_clause_node)

    #else node
    else_node=Node()
    else_node.type='else'
    else_node.text='else'
    else_node.parent=else_clause_node
    else_clause_node.addchild(else_node)

    #colon node
    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=else_clause_node
    else_clause_node.addchild(colon_node)

    # block node
    block_node=Node()
    block_node.type='block'
    block_node.parent=else_clause_node
    else_clause_node.addchild(block_node)

    #child_if_statement
    child_if_statement_node=Node()
    child_if_statement_node.type='if_statement'
    child_if_statement_node.parent=block_node
    block_node.addchild(child_if_statement_node)

    # if node
    if_node=Node()
    if_node.type='if'
    if_node.text='if'
    if_node.parent=child_if_statement_node
    child_if_statement_node.addchild(if_node)
    #we can easil copy the statement from cand_list
    child_if_statement_node.addchild(cand_list[0].children[1])
    cand_list[0].children[1].parent=child_if_statement_node
    child_if_statement_node.addchild(cand_list[0].children[2])
    cand_list[0].children[2].parent=child_if_statement_node
    child_if_statement_node.addchild(cand_list[0].children[3])
    cand_list[0].children[3].parent=child_if_statement_node

    for i in range(1,len(cand_list)):
        child_if_statement_node.addchild(cand_list[i])
        cand_list[i].parent=child_if_statement_node
    #reset the level
    ResetLevelPY(if_statement)




