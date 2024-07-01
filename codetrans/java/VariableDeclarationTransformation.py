# for example: int x=0;
# the converted code is:
# int x; x=0;

from AstToTree import *
from Node import Node

# this is the main function to convert the variable declaration
# param: tree_root_node: the root node of the tree generated from ast
# return: new code
def VariableDecl(tree_root_node):
    variable_decl_list=FindVariableDecl(tree_root_node)
    variable_decl_list=IsVariableAssignment(variable_decl_list)
    variable_decl_list=DelArray(variable_decl_list)
    if len(variable_decl_list)==0:
        return 0
    else:
        for i in range(0,len(variable_decl_list)):
            ProcessVariableDecl(variable_decl_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has variable declaration statement, it will return true, else it will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsVariableDecl(tree_root_node):
    if tree_root_node.type=='local_variable_declaration':
        # for example: for(int i=0;;){..}, it can not be for(int i;i=0;;){..}, so we do not consider for statement
        # in other transformation, we will use for statement
        if tree_root_node.parent.type!='for_statement':
            return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsVariableDecl(child)
            if result==True:
                return True
        return False
    else:
        return False

# return the list of variable declaration statement
# param: tree_root_node: the root node of the tree generated from ast
# return: list of variable declaration statement
def FindVariableDecl(tree_root_node):
    variable_decl_list=[]
    if  tree_root_node.type=='local_variable_declaration':
        if tree_root_node.parent.type!='for_statement':
            variable_decl_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindVariableDecl(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    variable_decl_list.append(result[i])

    else:
        pass

    return variable_decl_list

# sometimes, the variable declaration statement only declare a variable, but do not assign it with value,
# so we shoule delete the statement. for example: int a ; we delete it
# also, if the statement is: int a,b=0; we do not consider it
# param: variable_decl_list: list of variable declaration statement
# return: the new list of variable declaration statement
def IsVariableAssignment(variable_decl_list):
    variable_decl_assign_list=[]
    for i in range(0,len(variable_decl_list)):
        index=0;
        num=0
        for child in variable_decl_list[i].children:
            if child.type=='variable_declarator':
                index=variable_decl_list[i].children.index(child)
                num=num+1
        if num==1:
            for child in variable_decl_list[i].children[index].children:
                if child.type=='=':
                    variable_decl_assign_list.append(variable_decl_list[i])
                    break
    return variable_decl_assign_list

# in java, the static array can not be transformed
# for example: int x[]={1,2,3};
# but if we convert it such as:
# int []x;
# x={1,2,3}
# that is wrong, so we must delete static array
# param: variable_decl_list: the list of variable declaration statement
# return: the list of variable declaration statement with out static array
def DelArray(variable_decl_list):
    variable_del_no_array_list=[]
    for i in range(0,len(variable_decl_list)):
        index=0
        for child in variable_decl_list[i].children:
            if child.type=='variable_declarator':
                index=variable_decl_list[i].children.index(child)
                break
        array_ini=False
        for child in variable_decl_list[i].children[index].children:
            if child.type=='array_initializer':
                array_ini=True
                break
        if not array_ini:
            variable_del_no_array_list.append(variable_decl_list[i])

    return variable_del_no_array_list

# this function will process the variable declaration statement
# param: node: the node which type is local_variable_declaration
# return: None
def ProcessVariableDecl(node):
    index=0
    for child in node.children:
        if child.type=='variable_declarator':
            index=node.children.index(child)
            break

    variable_declarator=node.children[index]
    # for example: int x;
    # we create a new variable declarator node and the child node before '=' will be the child of new variable declarator
    # the other nodes can be contributed to the child of assignment expression
    new_variable_declarator=Node()
    new_variable_declarator.type='variable_declarator';
    new_variable_declarator.parent=node
    node.children[index]=new_variable_declarator
    for child in variable_declarator.children:
        if child.type=='=':
            equal_index=variable_declarator.children.index(child)
    for i in range(0,equal_index):
        variable_declarator.children[i].parent=new_variable_declarator
        new_variable_declarator.addchild(variable_declarator.children[i])

    identifier_node=Node()
    identifier_node.type='identifier'
    identifier_node.text=variable_declarator.children[0].text
    #identifier_node.parent=new_variable_declarator
    #new_variable_declarator.addchild(identifier_node);

    # for example: x=0;
    # we should ensure that int x ; and x=0; has the same parent
    # the parent of the variable declaration node
    node_parent=node.parent
    # the index of the variable declaration node
    node_index=node_parent.children.index(node)

    expression_statement=Node()
    expression_statement.type='expression_statement'
    expression_statement.parent=node_parent
    node_parent.children.insert(node_index+1,expression_statement)
    # for exapmle: int {x=0}; and the text in the curly brace belong to variable_declarator, so we can copy the variable_declarator
    variable_declarator.children=variable_declarator.children[equal_index:]
    variable_declarator.children.insert(0,identifier_node)
    identifier_node.parent=variable_declarator
    variable_declarator.type='assignment_expression'
    variable_declarator.parent=expression_statement
    expression_statement.addchild(variable_declarator)

    semicolon_node=Node()
    semicolon_node.type=';'
    semicolon_node.text=';'
    semicolon_node.parent=expression_statement
    expression_statement.addchild(semicolon_node)





