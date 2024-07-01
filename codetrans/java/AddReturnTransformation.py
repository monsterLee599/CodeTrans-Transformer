# will will add return statement at the end of the code
# in java, only in the void function, we can add return statement -> return ;

from AstToTree import *
from Node import Node
from GetAST import *
# this is the main function of the add return statement transformation
# param: tree_root_node: the root node of the tree generated from ast
# return: new code
def AddReturn(tree_root_node):
    method_list=FindMethod(tree_root_node)
    method_list=MethodKeyVoid(method_list)
    if len(method_list)==0:
        return 0
    else:
        for i in range(0,len(method_list)):
            ProcessMehtodReturn(method_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

# this method will find and return all the method declaration
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of method declaration
def FindMethod(tree_root_node):
    method_list=[]
    if tree_root_node.type=='method_declaration':
        method_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindMethod(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    method_list.append(result[i])

    return method_list

# if the method type is 'void', we can add 'return ;', so we only use the method which type is 'void'
# param: method_list: the list of method declaration
# return: the new list of method declaration
def MethodKeyVoid(method_list):
    new_method_list=[]
    for i in range(0,len(method_list)):
        for child in method_list[i].children:
            if child.type=='void_type' and method_list[i].children[len(method_list[i].children)-1].type=='block':
                new_method_list.append(method_list[i])
                break
    return new_method_list

# this method will add 'return ;' at the end of the source code
# param: method_node: the node which type is method_declaration
# return: None
def ProcessMehtodReturn(method_node):

    block=method_node.children[len(method_node.children)-1]
    #print(block.type)
    return_statement=Node()
    return_statement.type='return_statement'
    return_statement.parent=block
    block.children.insert((len(block.children)-1),return_statement)

    return_node=Node()
    return_node.type='return'
    return_node.text='return'
    return_node.parent=return_statement
    return_statement.addchild(return_node)

    semicolon=Node()
    semicolon.type=';'
    semicolon.text=';'
    semicolon.parent=return_statement
    return_statement.addchild(semicolon)