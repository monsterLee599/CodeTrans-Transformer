# this function will transform the else{ if(...) } to else if{ ... }
# what we should know is that the block of else must only has an if statement
# for example:
# else {
# if(x==0){
# x=1;
# }
# }
# and we do not consider other condition

from AstToTree import *
from Node import Node
from GetAST import *

def ElseIftoElif(tree_root_node):
    if_list=FindIfAndElseStatement(tree_root_node)
    if_list=DelComment(if_list)
    if_list=IsElseIf(if_list)

    if len(if_list)==0:
        return 0
    else:
        for i in range(0,len(if_list)):
            ProcessElseIf(if_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

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

def IsElseIf(if_list):
    new_if_list=[]
    for i in range(0,len(if_list)):
        if if_list[i].children[len(if_list[i].children)-1].type=='block':
            block=if_list[i].children[len(if_list[i].children)-1]
            if len(block.children)==3 and block.children[1].type=='if_statement':
                new_if_list.append(if_list[i])

    return new_if_list

def ProcessElseIf(if_statement_node):
    block=if_statement_node.children[len(if_statement_node.children)-1]
    if_statement=block.children[1]
    if_statement.parent=if_statement_node
    if_statement_node.children[len(if_statement_node.children)-1]=if_statement
