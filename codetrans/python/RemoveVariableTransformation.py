# this transformation will remove the variable if it is never used
# for example, we declarate a variable, and the code has not use the variable, we can delete the variable
# for example:
# x=0
# return 0
# we can find that the variable x is not used, so we can delete the statement directly

from AstToTree import *
from Node import Node
from GetAST import *

# this is the main function to remove unused variable
# param: tree_root_node: the root node of the tree generate from ast
# return: the new code that has remove the unused variable
def RemoveUnusedVariable(tree_root_node):
    variable_list=FindAllIdentifier(tree_root_node)
    variable_decl_list=AssignVariable(tree_root_node)
    #print(variable_list)
    #print(variable_decl_list)
    variable_no_decl_list=VariableNoDecl(variable_list,variable_decl_list)
    variable_name_list=GetVariableNmae(variable_no_decl_list)
    unused_variable_list=[]

    for i in range(0,len(variable_decl_list)):
        if variable_decl_list[i].text not in variable_name_list:
            unused_variable_list.append(variable_decl_list[i])

    if len(unused_variable_list)==0:
        return 0
    else:
        for i in range(0,len(unused_variable_list)):
            RemoveVariable(unused_variable_list[i])

    code=TreeToTextPy(tree_root_node)
    return code


# find and return the list of all the identifiers(variables)
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of identifiers(variables)
def FindAllIdentifier(tree_root_node):
    identifier_list = []
    if tree_root_node.type == 'identifier':
        identifier_list.append(tree_root_node)

    if len(tree_root_node.children) != 0:
        for child in tree_root_node.children:
            result = FindAllIdentifier(child)
            if len(result) != 0:
                for i in range(0, len(result)):
                    identifier_list.append(result[i])

    else:
        pass

    return identifier_list

def AssignVariable(tree_root_node):
    variable_list=[]
    if tree_root_node.type=='assignment' and tree_root_node.parent.type=='expression_statement' and len(tree_root_node.parent.children)==1 and len(tree_root_node.children)==3:
        if tree_root_node.children[0].type=='identifier':
            variable_list.append(tree_root_node.children[0])

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=AssignVariable(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    variable_list.append(result[i])
    else:
        pass

    return variable_list

# this function will return the list of variables that not int the ini varaible list
# param: variable_list: all the variables
#        variable_decla_list: the list of ini variables
# return: the list of variables not in the list of ini variables
def VariableNoDecl(variable_list,variable_decl_list):
    for i in range(0,len(variable_decl_list)):
        if variable_decl_list[i] in variable_list:
            variable_list.remove(variable_decl_list[i])

    return variable_list

# return the name of variable node
# param: variable_list: the list of variable nodes
# return: all the names of the variables
def GetVariableNmae(variable_list):
    variable_name_list=[]
    for i in range(0,len(variable_list)):
        if variable_list[i].text not in variable_name_list:
            variable_name_list.append(variable_list[i].text)

    return variable_name_list

# this function will remove the varaible declaration node
# varaible_node: the variable node and its type is identifier
# return: None
def RemoveVariable(variable_node):
    expression_statement=variable_node.parent.parent
    expresison_statement_parent=expression_statement.parent
    expression_statement_index=expresison_statement_parent.children.index(expression_statement)

    pass_stmt=Node()
    pass_stmt.type='pass_statement'
    pass_stmt.parent=expresison_statement_parent
    expresison_statement_parent.children[expression_statement_index]=pass_stmt

    pass_node=Node()
    pass_node.type='pass'
    pass_node.text='pass'
    pass_node.parent=pass_stmt
    pass_stmt.addchild(pass_node)

    ResetLevelPY(pass_stmt)

