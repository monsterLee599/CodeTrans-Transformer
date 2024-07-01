# this transformation will add logical not operation
# for example: a<b, we can transform it to not(a>=b)
# but we do not consider 'and' and 'or', we easily consider binary operator:>,<,>=,<=,==,!=

from Node import Node
from AstToTree import *
from GetAST import *

def LogicalNot(tree_root_node):
    operator_list=FindComparisonOperator(tree_root_node)
    if len(operator_list)==0:
        return 0
    else:
        for i in range(0,len(operator_list)):
            ProcessLogicalNot(operator_list[i])
        code=TreeToTextPy(tree_root_node)
        return code


def IsComparisonOperator(tree_root_node):

    operator_list=['>','<','>=','<=','==','!=']

    if tree_root_node.type in operator_list:
        if tree_root_node.parent.type =='comparison_operator' and len(tree_root_node.parent.children)==3:
            return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsComparisonOperator(child)
            if result==True:
                return True
        return False

    else:
        return False

def FindComparisonOperator(tree_root_node):
    #operator_list = ['>', '<', '>=', '<=']
    operator_list = ['>', '<', '>=', '<=', '==', '!=']
    node_list=[]
    if tree_root_node.type in operator_list:
        if tree_root_node.parent.type == 'comparison_operator' and len(tree_root_node.parent.children)==3:
            node_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindComparisonOperator(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    node_list.append(result[i])

    else:
        pass

    return node_list

def ProcessLogicalNot(operator_node):
    comparison_operator=operator_node.parent
    comparison_operator_parent=comparison_operator.parent
    comparison_operator_index=comparison_operator_parent.children.index(comparison_operator)

    not_operator=Node()
    not_operator.type='not_operator'
    not_operator.parent=comparison_operator_parent
    comparison_operator_parent.children[comparison_operator_index]=not_operator

    logical_not=Node()
    logical_not.type='not'
    logical_not.text='not'
    logical_not.parent=not_operator
    not_operator.addchild(logical_not)

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=not_operator
    not_operator.addchild(parenthesized_expression)

    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(left_paren)

    comparison_operator.parent=parenthesized_expression
    parenthesized_expression.addchild(comparison_operator)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    # we will change the comparison operator

    if operator_node.type=='==':
        operator_node.type='!='
        operator_node.text='!='
    elif operator_node.type=='!=':
        operator_node.type='=='
        operator_node.text='=='
    elif operator_node.type=='>':
        operator_node.type='<='
        operator_node.text='<='
    elif operator_node.type=='<':
        operator_node.type='>='
        operator_node.text='>='
    elif operator_node.type=='>=':
        operator_node.type='<'
        operator_node.text='<'
    elif operator_node.type=='<=':
        operator_node.type='<='
        operator_node.text='<='




