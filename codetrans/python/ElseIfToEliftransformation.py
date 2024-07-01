from Node import Node
from AstToTree import *

# we will convert else if statement to elif statement
#for example:
# if ...
# else:
#     if ...
#     else: ...
#we can convert it into :
# if ...
# elif ...
# else ...

def ElseIfToElif(tree_root_node):
    if_list=FindElseIf(tree_root_node)
    if len(if_list)==0:
        return  0
    else:
        for i in range(0,len(if_list)):
            ProcessElseIf(if_list[i])
        code=TreeToTextPy(tree_root_node)
        return code

def IsElseIf(node):
    if node.type=='if_statement':
        if node.parent.type=='block':
            if_statement_index=node.parent.children.index(node)
            #print(if_statement_index)
            #print(node.parent.parent.type)

            if len(node.parent.children)==1 and  if_statement_index==0 and node.parent.parent.type=='else_clause' and node.parent.parent.parent.type=='if_statement':
               return True

    if len(node.children)!=0:
        for child in node.children:
            result=IsElseIf(child)
            if result==True:
                return True
        return False
    else:
        return False

def FindElseIf(node):
    if_list=[]
    if node.type=='if_statement':
        if node.parent.type == 'block':
            if_statement_index = node.parent.children.index(node)
            # print(if_statement_index)
            # print(node.parent.parent.type)

            if len(node.parent.children) == 1 and if_statement_index == 0 and node.parent.parent.type == 'else_clause' and len(node.parent.parent.children)==3 and node.parent.parent.parent.type == 'if_statement':
                if_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindElseIf(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    if_list.append(result[i])
    else:
        pass

    return if_list


def ProcessElseIf(node):
    if_statement=node.parent.parent.parent
    else_clause_index=if_statement.children.index(node.parent.parent)

    elif_clause=Node()
    elif_clause.type='elif_clause'
    elif_clause.parent=if_statement
    if_statement.children[else_clause_index]=elif_clause

    elif_node=Node()
    elif_node.type='elif'
    elif_node.text='elif'
    elif_node.parent=elif_clause
    elif_clause.addchild(elif_node)

    if_chi=False
    for i in range(1,len(node.children)):
        if node.type=='elif_clause' or node.type=='else_clause':
            if_chi=True
        if if_chi==False:
            node.children[i].parent=elif_clause
            elif_clause.addchild(node.children[i])
        else:
            node.children[i].parent=if_statement
            if_statement.addchild(node.children[i])

    ResetLevelPY(if_statement)
