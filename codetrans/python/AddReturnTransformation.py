from  Node import *
from AstToTree import *
# we will add a return statement at the end of each method/function if there is no return

#add a return statement : return 0
#param: tree_root_node: the root node of the tree generated from ast
#return: the new code with return statement
def AddReturn(tree_root_node):
    function_list=FindFunction(tree_root_node)
    add_return_list=[]
    for i in range(0,len(function_list)):
        result=IsAddReturn(function_list[i])
        if result==True:
            add_return_list.append(function_list[i])
        else:
            continue
    if len(add_return_list)==0:
        return 0
    for i in range(0,len(add_return_list)):
        ProcessFunctionReturn(add_return_list[i])

    code=TreeToTextPy(tree_root_node)
    return code


# if the code has function definition, we will return true, else we will return false
# param: node of the tree generated from ast
# the code has function -> true, the code doesn't have function -> false
def IsFunction(node):
    if node.type=='function_definition':
        return True

    if len(node.children)!=0:
        for child in node.children:
            result=IsFunction(child)
            if result==True:
                return True
        return False
    else:
        return False

def FindFunction(node):
    function_list=[]
    if node.type=='function_definition':
        function_list.append(node)
    if len(node.children)!=0:
        for child in node.children:
            result=FindFunction(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    function_list.append(result[i])
    else:
        pass

    return function_list

def IsAddReturn(function_node):
# we assume that the block statement at the end of function definition ast
    block_node=function_node.children[len(function_node.children)-1]
    #if block_node.type=='block':
        #return True
    #else:
        #return False
    #if the last child of block node is not return statement, we will add return 0
    if len(block_node.children)>=1 and block_node.children[len(block_node.children)-1].type=='return_statement':
        return False
    else:
        return True

#add return statement at the end of the function: add return 0
def ProcessFunctionReturn(function_node):
    block_node=function_node.children[len(function_node.children)-1]
    # add the return statement-> return 0
    return_statement_node=Node()
    return_statement_node.type='return_statement'
    return_statement_node.parent=block_node
    block_node.addchild(return_statement_node)

    #return
    return_node=Node()
    return_node.type='return'
    return_node.text='return'
    return_node.parent=return_statement_node
    return_statement_node.addchild(return_node)

    integer_node=Node()
    integer_node.type='integer'
    integer_node.text='0'
    integer_node.parent=return_statement_node
    return_statement_node.addchild(integer_node)
    # reset the level
    ResetLevelPY(function_node)
