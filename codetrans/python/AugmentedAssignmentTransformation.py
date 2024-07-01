from Node import Node
from AstToTree import *

# change the insreasement statement : for example : x+=1 -> x=x+1
#param : tree root node: the root node of tree generated from ast
#return : the new code that transform the augmented assignment
def AugmentedAssignment(tree_root_node):
    augment_assignment_list=FindAugmentAssignment(tree_root_node)
    if len(augment_assignment_list)==0:
        return 0
    else:
        #return augment_assignment_list
        for i in range(0,len(augment_assignment_list)):
            ProcessAugmentedAssignment(augment_assignment_list[i])

        code= TreeToTextPy(tree_root_node)
        return code



def FindAugment(node):
    if node.type=='+=' or node.type=='-=' or node.type=='*=' or node.type=='/=' or node.type=='//=' or node.type=='%=':
        return True
    else:
        if len(node.children)!=0:
            for child in node.children:
                result=FindAugment(child)
                if result==True:
                    return True
                else:
                    continue
            return False

        else:
            return False

#find the augment assignment node and return
#param: a node of the tree
#return: the list of augment assignment node
def FindAugmentAssignment(node):
    node_list=[]
    if node.type=='+=' or node.type=='-=' or node.type=='*=' or node.type=='/=' or node.type=='//=' or node.type=='%=':
        node_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindAugmentAssignment(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    node_list.append(result[i])
    else:
        pass

    return node_list

# process the subtree of augment assignment, for example: x+=1 -> x=x+1
# param: the node(type is augment assignment)
# reutrn : none
def ProcessAugmentedAssignment(node):
    operator_dict={'+=':'+','-=':'-','*=':'*','/=':'/','//=':'//','%=':'%'}

    expression_statement_node = node.parent.parent
    left_value=node.parent.children[0]
    right_value=node.parent.children[2]

    # assignment node
    assignment_node=Node()
    assignment_node.type='assignment'
    expression_statement_node.children[0]=assignment_node
    assignment_node.parent=expression_statement_node

    assignment_node.addchild(left_value)
    left_value.parent=assignment_node

    #equation node
    equation_node=Node()
    equation_node.type='='
    equation_node.text='='
    equation_node.parent=assignment_node
    assignment_node.addchild(equation_node)

    #binary operator
    binary_operator_node=Node()
    binary_operator_node.type='binary_operator'
    binary_operator_node.parent=assignment_node
    assignment_node.addchild(binary_operator_node)

    # left value 2 the text of left value = the text of left value
    # x+=1 -> x=x+1 :the first x is the left value and the next x is left value 2
    left_value_2=Node()
    left_value_2.type=left_value.type
    left_value_2.text=left_value.text
    left_value_2.parent=binary_operator_node
    binary_operator_node.addchild(left_value_2)
    CopySubtreePY(left_value,left_value_2)

    # binary operator (+ - * % / //)
    binary_operator=Node()
    binary_operator.type=operator_dict[node.type]
    binary_operator.text=operator_dict[node.text]
    binary_operator.parent=binary_operator_node
    binary_operator_node.addchild(binary_operator)

    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=binary_operator_node
    binary_operator_node.addchild(parenthesized_expression)
    left_paren=Node()
    left_paren.type='('
    left_paren.text='('
    left_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(left_paren)

    right_value.parent=parenthesized_expression
    parenthesized_expression.addchild(right_value)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)


    # reset the level
    ResetLevelPY(expression_statement_node)

