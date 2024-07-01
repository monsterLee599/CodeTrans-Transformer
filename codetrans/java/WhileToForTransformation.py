# this transforamtion will transform while statement to for statement

from AstToTree import *
from Node import Node

def WhileToFor(tree_root_node):
    while_list=FindWhileStatement(tree_root_node)
    if len(while_list)==0:
        return 0
    else:
        for i in range(0,len(while_list)):
            ProcessWhile(while_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

def IsWhileStatement(tree_root_node):
    if tree_root_node.type=='while_statement':
        return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsWhileStatement(child)
            if result==True:
                return True
        return False

    else:
        return False

def FindWhileStatement(tree_root_node):
    while_list=[]
    if tree_root_node.type=='while_statement':
        while_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindWhileStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    while_list.append(result[i])

    else:
        pass

    return while_list

def ProcessWhile(while_node):
    # create the for statement and repalce the while statement while for statement
    for_statement=Node()
    for_statement.type='for_statement'

    while_parent=while_node.parent
    while_index=while_parent.children.index(while_node)

    while_parent.children[while_index]=for_statement
    for_statement.parent=while_parent

    # move the child of while statement to for statement
    for_node = Node()
    for_node.type = 'for'
    for_node.text = 'for'
    for_node.parent = for_statement
    for_statement.addchild(for_node)

    iscondition=False

    for i in range(1,len(while_node.children)):
        if while_node.children[i].type=='parenthesized_expression' and iscondition==False:
            left_parenthesized = Node()
            left_parenthesized.type = '('
            left_parenthesized.text = '('
            left_parenthesized.parent = for_statement
            for_statement.addchild(left_parenthesized)

            semicolon_1 = Node()
            semicolon_1.type = ';'
            semicolon_1.text = ';'
            semicolon_1.parent = for_statement
            for_statement.addchild(semicolon_1)

            for j in range(1,len(while_node.children[i].children)-1):
                for_statement.addchild(while_node.children[i].children[j])
                while_node.children[i].children[j].parent=for_statement

            semicolon_2 = Node()
            semicolon_2.type = ';'
            semicolon_2.text = ';'
            semicolon_2.parent = for_statement
            for_statement.addchild(semicolon_2)

            right_parenthesized = Node()
            right_parenthesized.type = ')'
            right_parenthesized.text = ')'
            right_parenthesized.parent = for_statement
            for_statement.addchild(right_parenthesized)

            iscondition=True

        else:
            while_node.children[i].parent=for_statement
            for_statement.addchild(while_node.children[i])



