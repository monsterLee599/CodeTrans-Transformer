from Node import Node
from AstToTree import *

def WhileToFor(ast_root_node):
    result=IsWhileStatement(ast_root_node)
    return result

def IsWhileStatement(node):
    if node.type=='while_statement':
        return True

    if len(node.children)!=0:
        for child in node.children:
            result=IsWhileStatement(child)
            if result==True:
                return True
        return  False
    else:
        return False


def FindWhileStatement(node):
    while_list=[]
    if node.type=='while_statement':
        while_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindWhileStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    while_list.append(result[i])
    else:
        pass

    return while_list

def ChangeWhileStatement(node):
    pass