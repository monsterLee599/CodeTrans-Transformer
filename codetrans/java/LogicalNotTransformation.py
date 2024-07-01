# this transformation will add logical not operation
# for example: a<b, we can transform it to !(a>=b)
# but we do not consider && and ||, we easily consider binary operator:>,<,>=,<=,==,!=

from AstToTree import *
from Node import Node

# in this transformation, we will add logical not operator
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def LogicalNot(tree_root_node):
    operator_list=FindRelationOperator(tree_root_node)
    if len(operator_list)==0:
        return 0
    else:
        for i in range(0,len(operator_list)):
            ProcessLogicalNot(operator_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

# if the code has relation operator, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsRelationOperator(tree_root_node):
    operator_list=['>','<','>=','<=','==','!=']
    #operator_list=['>','<','>=','<=']
    if tree_root_node.type in operator_list:
        if tree_root_node.parent.type == 'binary_expression':
            return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsRelationOperator(child)
            if result==True:
                return True
        return False

    else:
        return False

# return the list of relation operator
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of relation operator
def FindRelationOperator(tree_root_node):
    operator_list = ['>', '<', '>=', '<=', '==', '!=']
    #operator_list = ['>', '<', '>=', '<=']
    node_list=[]
    if tree_root_node.type in operator_list:
        if tree_root_node.parent.type == 'binary_expression':
            node_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindRelationOperator(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    node_list.append(result[i])

    else:
        pass

    return node_list

# add logical not operator
# param: rela_node: tree node which type is relation operator
# return: none
def ProcessLogicalNot(rela_node):
    # change x==y to !(x!=y)
    # we first replace binary expression with new unary expresion which type is !
    binary_expression=rela_node.parent
    binary_expression_parent=binary_expression.parent
    binary_expression_index=binary_expression_parent.children.index(binary_expression)
    unary_expression=Node()
    unary_expression.type='unary_expression'
    unary_expression.parent=binary_expression_parent
    binary_expression_parent.children[binary_expression_index]=unary_expression

    logical_not=Node()
    logical_not.type='!'
    logical_not.text='!'
    logical_not.parent=unary_expression
    unary_expression.addchild(logical_not)

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=unary_expression
    unary_expression.addchild(parenthesized_expression)

    left_parenthesized=Node()
    left_parenthesized.type='('
    left_parenthesized.text='('
    left_parenthesized.parent=parenthesized_expression
    parenthesized_expression.addchild(left_parenthesized)

    binary_expression.parent=parenthesized_expression
    parenthesized_expression.addchild(binary_expression)

    right_parenthesized=Node()
    right_parenthesized.type=')'
    right_parenthesized.text=')'
    right_parenthesized.parent=parenthesized_expression
    parenthesized_expression.addchild(right_parenthesized)

    # change the relation operator
    if rela_node.type=='==':
        rela_node.type='!='
        rela_node.text='!='
    elif rela_node.type=='!=':
        rela_node.type='=='
        rela_node.text='=='
    elif rela_node.type=='>':
        rela_node.type='<='
        rela_node.text='<='
    elif rela_node.type=='<':
        rela_node.type='>='
        rela_node.text='>='
    elif rela_node.type=='>=':
        rela_node.type='<'
        rela_node.text='<'
    elif rela_node.type=='<=':
        rela_node.type='>'
        rela_node.text='>'