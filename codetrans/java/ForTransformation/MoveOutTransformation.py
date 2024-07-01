# in for statement, for(init;;){...}
# for example:
# for(int i=0;i<10;i++) ...
# it can be converted to:
# int i; for(i=0;i<10;i++) ...

from java.VariableDeclarationTransformation import *

# this if the main function that move out the variable declaration of for_statement
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def MoveOutVariable(tree_root_node):
    for_list=FindForStatement(tree_root_node)
    for_list=GetForDecl(for_list)
    if len(for_list)==0:
        return 0
    else:
        for i in range(0,len(for_list)):
            ProcessMoveOutVariable(for_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the source code has for statement, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsForStatement(tree_root_node):
    if tree_root_node.type=='for_statement':
        return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsForStatement(child)
            if result==True:
                return True
        return False
    else:
        return False

# return the list of for statement
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of for statement
def FindForStatement(tree_root_node):
    for_list=[]
    if tree_root_node.type=='for_statement':
        for_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindForStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    for_list.append(result[i])

    else:
        pass

    return for_list

# we will return the variable declaration in for_statement
# example: for(int i=0;;)... we will return the for_statement
# but, as for for(i=0;;)... we will not return it
# and if it declarates many variables, for example: for(int i=0,j=0;;)... we will not return it
# param: the list of for statement
# return: the list of for statement that have been selected
def GetForDecl(for_list):
    new_for_list=[]
    for i in range(0,len(for_list)):
        if for_list[i].children[2].type=='local_variable_declaration':
            result=IsVariableAssignment([for_list[i].children[2]])
            result=DelArray(result)
            if len(result)!=0:
                new_for_list.append(for_list[i])


    return new_for_list

# this function will move out the variable declaration from for statement
# we will add block out of the for statement: for(int i=0;;)... -> { int i; for(i=0;;)... }
# param: node: the node, and its type if for_statement
# return: None
def ProcessMoveOutVariable(node):
    # we first get the parent of for_statement, and the new variable declaration statement must has the same parent with for statement

    for_parent=node.parent
    for_index=for_parent.children.index(node)

    # we will create a new block and set the for_statement the child of block
    # because the for statement may be the child of compound statement
    # for example: if(x==0) for(int i=0;i<10;i++)
    # but if(x==0) int i; for(i=0;i<10;i++) is wrong ,
    # so we get the type is: if(x==0) {int i ; for(i=0;i<10;i++)}

    block=Node()
    block.type='block'
    block.parent=for_parent
    for_parent.children[for_index]=block

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=block
    block.addchild(left_brace)

    local_variable_declaration=node.children[2]

    #find the variable declarator
    index=0
    for child in local_variable_declaration.children:
        if child.type=='variable_declarator':
            index=local_variable_declaration.children.index(child)
            break

    variable_declarator=local_variable_declaration.children[index]

    new_variable_declarator=Node()
    new_variable_declarator.type='variable_declarator'
    new_variable_declarator.parent=local_variable_declaration
    local_variable_declaration.children[index]=new_variable_declarator

    for child in variable_declarator.children:
        if child.type=='=':
            equal_index=variable_declarator.children.index(child)

    for i in range(0,equal_index):
        variable_declarator.children[i].parent=new_variable_declarator
        new_variable_declarator.addchild(variable_declarator.children[i])

    identifier_node=Node()
    identifier_node.type=variable_declarator.children[0].type
    #if identifier_node.type!='identifier':
    #    print('error')
    identifier_node.text=variable_declarator.children[0].text

    variable_declarator.children=variable_declarator.children[equal_index:]
    variable_declarator.children.insert(0,identifier_node)
    identifier_node.parent=variable_declarator


    local_variable_declaration.parent=block
    block.addchild(local_variable_declaration)

    block.addchild(node)
    node.parent=block

    variable_declarator.parent=node
    node.children[2]=variable_declarator
    variable_declarator.type='assignment_expression'

    semicolon_node=Node()
    semicolon_node.type=';'
    semicolon_node.text=';'
    semicolon_node.parent=node
    node.children.insert(3,semicolon_node)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)



