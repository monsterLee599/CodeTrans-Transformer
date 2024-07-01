# this transformation will create a new function and move the other to it
# for example: x=0
# it can be:
# def func1():
#    return 0
# x=func1()

from Node import Node
from AstToTree import *
from AstToTree import *

def CreateFunction(tree_root_node):
    assign_list=FindAssignment(tree_root_node)
    if len(assign_list)==0:
        return 0
    else:
        for i in range(0,len(assign_list)):
            ProcessAssign(tree_root_node,assign_list[i],'func_'+str(i))
        code=TreeToTextPy(tree_root_node)
        return code

def FindAssignment(tree_root_node):
    assign_list=[]
    if tree_root_node.type=='assignment'  and len(tree_root_node.children)==3 and (tree_root_node.children[2].type=='identifier' or tree_root_node.children[2].type=='binary_operator'):
        for child in tree_root_node.children:
            if child.type=='assignment':
                isnum=False

        identifier_list=FindIdentifier(tree_root_node)
        isassign=True
        for i in range(0,len(identifier_list)):
            if identifier_list[i].parent.type=='call' or identifier_list[i].parent.type=='attribute':
                isassign=False
        if isassign:
            assign_list.append(tree_root_node)


    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindAssignment(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    assign_list.append(result[i])
    else:
        pass

    return assign_list


def ProcessAssign(tree_root_node,assign_node,func_name):
    identifier_list=[]
    index=0
    for child in assign_node.children:
        if child.type=='=':
            index=assign_node.children.index(child)
            break

    for i in range(index+1,len(assign_node.children)):
        result=FindIdentifier(assign_node.children[i])
        for i in range(0,len(result)):
            identifier_list.append(result[i])

    func_def=Node()
    func_def.type='function_definition'
    func_def.parent=tree_root_node
    tree_root_node.addchild(func_def)

    def_node=Node()
    def_node.type='def'
    def_node.text='def'
    def_node.parent=func_def
    func_def.addchild(def_node)

    func_name_node=Node()
    func_name_node.type='identifier'
    func_name_node.text=func_name
    func_name_node.parent=func_def
    func_def.addchild(func_name_node)

    parameters=Node()
    parameters.type='parameters'
    parameters.text='parameters'
    parameters.parent=func_def
    func_def.addchild(parameters)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parameters
    parameters.addchild(left_paren)

    for i in range(0,len(identifier_list)):
        iden=Node()
        iden.type='identifier'
        iden.text=identifier_list[i].text
        iden.parent=parameters
        parameters.addchild(iden)

        if i!=len(identifier_list)-1:
            comma=Node()
            comma.type=','
            comma.text=','
            comma.parent=parameters
            parameters.addchild(comma)

    right_paren = Node()
    right_paren.type = ')'
    right_paren.text = ')'
    right_paren.parent = parameters
    parameters.addchild(right_paren)

    colon=Node()
    colon.type=':'
    colon.text=':'
    colon.parent=func_def
    func_def.addchild(colon)

    block=Node()
    block.type='block'
    block.parent=func_def
    func_def.addchild(block)

    return_statement=Node()
    return_statement.type='return_statement'
    return_statement.parent=block
    block.addchild(return_statement)

    return_node=Node()
    return_node.type='return'
    return_node.text='return'
    return_node.parent=return_statement
    return_statement.addchild(return_node)

    for i in range(index+1,len(assign_node.children)):
        assign_node.children[i].parent=return_statement
        return_statement.addchild(assign_node.children[i])

    assign_node.children=assign_node.children[:index+1]

    call_node=Node()
    call_node.type='call'
    call_node.parent=assign_node
    assign_node.addchild(call_node)

    call_func_name=Node()
    call_func_name.type='identifier'
    call_func_name.text=func_name
    call_func_name.parent=call_node
    call_node.addchild(func_name_node)

    argument_list=Node()
    argument_list.type='argument_list'
    argument_list.parent=call_node
    call_node.addchild(argument_list)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=argument_list
    argument_list.addchild(left_paren)

    for i in range(0,len(identifier_list)):
        iden = Node()
        iden.type = 'identifier'
        iden.text = identifier_list[i].text
        iden.parent = argument_list
        argument_list.addchild(iden)

        if i!=len(identifier_list)-1:
            comma = Node()
            comma.type = ','
            comma.text = ','
            comma.parent = argument_list
            argument_list.addchild(comma)

    right_paren = Node()
    right_paren.type = ')'
    right_paren.text = ')'
    right_paren.parent = argument_list
    argument_list.addchild(right_paren)

    ResetLevelPY(func_def)
    ResetLevelPY(assign_node)



def FindIdentifier(node):
    identifier_list=[]

    if node.type=='identifier' :
        identifier_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindIdentifier(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    identifier_list.append(result[i])
    else:
        pass

    return identifier_list