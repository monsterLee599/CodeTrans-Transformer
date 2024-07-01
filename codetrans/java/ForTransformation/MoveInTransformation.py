# in for statement, ini variable; for(variable=0;;)...
# for example:
# int i; for(i=0;i<10;i++) ...
# it can be converted to:
# for(int i=0;i<10;i++) ...
from AstToTree import *
from Node import Node

def MoveInVariable(tree_root_node):
    for_list=FindForStatement(tree_root_node)
    for_list=GetForAssign(for_list)
    for_list=ForVarDecl(for_list)
    if len(for_list)==0:
        return 0
    else:
        for i in range(0,len(for_list)):
            ProcessMoveInVariable(for_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

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

def FindForStatement(tree_root_node):
    for_list=[]
    if tree_root_node.type=='for_statement':
        for_list.append(tree_root_node)
    #internal node
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindForStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    for_list.append(result[i])

    else:
        pass

    return for_list


def GetForAssign(for_list):
    new_for_list=[]
    for i in range(0,len(for_list)):
        num=0
        for child in for_list[i].children:
            if child.type=='assignment_expression':
                num=num+1
            if child.type==';':
                break
        if num==1:
            new_for_list.append(for_list[i])

    return new_for_list

# only in this pattern, we transform the for statement:
# int i; for(i=0;i<10;i++){...}
# if the variable declaration statement and for_statement are not adjacent, we do not transform it
# for example: int i=0; i=i+1; System.out.println(i); for(i=10;i<10;i++)...
# if we transform it to: i=i+1; System.out.println(i); for(int i=10;i<10;i++)... that is wrong
def ForVarDecl(for_list):
    new_for_index=[]
    for i in range(0,len(for_list)):
        for_index=for_list[i].parent.children.index(for_list[i])
        if for_index!=0 and for_list[i].parent.children[for_index-1].type=='local_variable_declaration':
            # find the variable name of local variable declaration
            local_variable_declaration=for_list[i].parent.children[for_index-1]
            # we must ensure that the local variable declaration statement declarate one variable
            num=0
            var_declarator_index=0
            for child in local_variable_declaration.children:
                if child.type=='variable_declarator':
                    num=num+1
                    var_declarator_index=local_variable_declaration.children.index(child)
            if num==1:
                var_declarator=local_variable_declaration.children[var_declarator_index]
                # we shoule make sure that the var_declarator does not assign value to variable
                is_equal=False
                for child in var_declarator.children:
                    if child.type=='=':
                        is_equal=True
                        break
                if not is_equal:
                    local_variable_name=var_declarator.children[0].text
                    # find the variable name of for statement
                    assigenment_expression=for_list[i].children[2]
                    for child in assigenment_expression.children:
                        if child.type=='identifier':
                            for_variable_name=child.text

                    if local_variable_name==for_variable_name:
                        new_for_index.append(for_list[i])

    return new_for_index

def ProcessMoveInVariable(for_node):
    for_index=for_node.parent.children.index(for_node)
    local_variable_declaration=for_node.parent.children[for_index-1]
    assignment_expression=for_node.children[2]

    for child in assignment_expression.children:
        if child.type=='=':
            equal_index=assignment_expression.children.index(child)

    for child in local_variable_declaration.children:
        if child.type=='variable_declarator':
            variable_declarator=child

    for i in range(equal_index,len(assignment_expression.children)):
        variable_declarator.addchild(assignment_expression.children[i])
        assignment_expression.children[i].parent=variable_declarator
    # remove the local variable declaration node from its parent
    for_node.parent.children.remove(local_variable_declaration)
    # replace the assignment_expression node with local variable declaration
    local_variable_declaration.parent=for_node
    for_node.children[2]=local_variable_declaration

    for i in range(3,len(for_node.children)):
        if for_node.children[i].type==';':
            for_node.children.remove(for_node.children[i])
            break


