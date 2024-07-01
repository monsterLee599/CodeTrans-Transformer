# this transformation will remove the variable if it is never used
# for example, we declarate a variable, and the code has not use the variable, we can delete the variable
# for example: public int hello(){
#                  int x=0;
#                  return 0 ;
#              }
# we delete the variable x
# but if the type is like: int x; x=0;
# we do not delete x, even if the x do not be used

from AstToTree import *
from Node import Node
from GetAST import *

# this is the main function to remove unused variable
# param: tree_root_node: the root node of the tree generate from ast
# return: the new code that has remove the unused variable
def RemoveUnusedVariable(tree_root_node):
    variable_list=FindAllIdentifier(tree_root_node)
    variable_decl_list=FindVariableDeclaration(tree_root_node)
    variable_no_decl_list=VariableNoDeclaration(variable_list,variable_decl_list)
    variable_name_list=GetVariableNmae(variable_no_decl_list)
    unused_variable_list=[]
    # print(variable_name_list)
    for i in range(0,len(variable_decl_list)):
        #print(variable_decl_list[i].text)
        if variable_decl_list[i].text not in variable_name_list:
            unused_variable_list.append(variable_decl_list[i])


    if len(unused_variable_list)==0:
        return 0
    else:
        for i in range(0,len(unused_variable_list)):
            RemoveVariableDeclaration(unused_variable_list[i])

        code=TreeToTextJava(tree_root_node)
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

# this function will return the variables belong to variable declaration
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of init variables
def FindVariableDeclaration(tree_root_node):
    variable_declarated_list = []
    if tree_root_node.type == 'local_variable_declaration':
        num_declarator = 0
        declarator_index = 0
        for child in tree_root_node.children:
            if child.type == 'variable_declarator':
                num_declarator = num_declarator + 1
                declarator_index = tree_root_node.children.index(child)

        if num_declarator >= 2:
            pass
        else:
            for child in tree_root_node.children[declarator_index].children:
                if child.type == 'identifier':
                    variable_declarated_list.append(child)
                elif child.type == '=':
                    break

    if len(tree_root_node.children) != 0:
        for child in tree_root_node.children:
            result = FindVariableDeclaration(child)
            if len(result) != 0:
                for i in range(0, len(result)):
                    variable_declarated_list.append(result[i])
    else:
        pass

    return variable_declarated_list

# this function will return the list of variables that not int the ini varaible list
# param: variable_list: all the variables
#        variable_decla_list: the list of ini variables
# return: the list of variables not in the list of ini variables
def VariableNoDeclaration(variable_list, variable_decla_list):
    for i in range(0, len(variable_decla_list)):
        if variable_decla_list[i] in variable_list:
            variable_list.remove(variable_decla_list[i])

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
def RemoveVariableDeclaration(variable_node):
    # get the local variable declaration statement
    local_variable_declaration=variable_node.parent.parent
    # we get the parent of the local variable declaration statement and so we can remove the statement
    parent=local_variable_declaration.parent
    local_variable_declaration_index=parent.children.index(local_variable_declaration)
    parent.children.remove(local_variable_declaration)