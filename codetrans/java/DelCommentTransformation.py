#this transformation will delete comments in the source code

from Node import Node
from AstToTree import *

#this method will delete the comments
#para: tree_root_node: the root node of the tree generated from ast
#return: the nwe code without comments
def Del_Java_Comment(tree_root_node):
    result=FindComment(tree_root_node)

    if len(result)==0:
        return 0

    if len(result)!=0:
        for i in range(0,len(result)):
            ProcessComment(result[i])

    return TreeToTextJava(tree_root_node)

#if source code has comment, it will return true, else it will return false
#para: tree_root_node: root node of the tree generated from ast
#return: true/false
def IsComment(tree_root_node):
    if tree_root_node.type=='comment':
        return True

    #if tree root node has children
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsComment(child)
            if result==True:
                return True
        return False
   # if tree root node has not children
    else:
        return False

#return the list of comment nodes
#para: tree_root_node: root node of the tree generated from ast
#return : list of comment nodes
def FindComment(tree_root_node):
    comment_list=[]
    if tree_root_node.type=='comment':
        comment_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindComment(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    comment_list.append(result[i])
    else:
        pass

    return comment_list

#delete comment node
#param: the node which type is comment
#return: None
def ProcessComment(node):
    #remove the comment node directly
    node.parent.children.remove(node)
