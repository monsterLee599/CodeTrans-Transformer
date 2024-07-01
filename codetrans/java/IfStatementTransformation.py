#in this transformation, we will split te if statement
#we get the idea from <Misleading authorship attribution of source code using adversarial learning>
#ths transformation will split the if  statement will multi condition
#for example: if (x==1 || x==2){...}
#we can change the if statament -> if x==1 {...}else if(x==2){...}

#but what you should know is that the if statement can't have else if or else
#because in thiis example: if (x==1 &&y==2){..}
#the result is if (x==1){if(y==2){...}}
#if the if statement has else if or else, if(x==1 && y==2){...} else{...}
#the result will be: if (x==1){if (y==2){...}} else{...}, that is wrong
#so if the if statement can not have else if or else, and you can also change the transformation by modify the code

from AstToTree import *
from GetAST import *
from Node import Node

# this function will convert the if statement which has been described
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def IfStatement(tree_root_node):
    if_list=FindIfStatement(tree_root_node)
    if_no_comment_list=DelComment(if_list)
    if_no_else_comment_list=DelElseIf(if_no_comment_list)
    if_no_else_comment_multi_list=MultipleCondition(if_no_else_comment_list)

    if len(if_no_else_comment_multi_list)==0:
        return 0
    else:
        for i in range(0,len(if_no_else_comment_multi_list)):
            ProcessIfStatement(if_no_else_comment_multi_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has if statement, we will return true, else we will return false
# param: tree_root_node: the root node of the tree generated from ast
# return: true/false
def IsIfStatement(tree_root_node):
    if tree_root_node.type=='if_statement':
        return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsIfStatement(child)
            if result==True:
                return True
        return False

    else:
        return False

# return the list of if statement of the code
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of ast
def FindIfStatement(tree_root_node):
    if_list=[]

    if tree_root_node.type=='if_statement':
        if_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindIfStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    if_list.append(result[i])

    else:
        pass

    return if_list

# why we set this function is that in some cases, developer will add some comments
# for example, if(x==1) /*comment*/ {...}
# the solution is del the comment node in the tree, but the generated code will delete comment as well, so we must
# judge that if the if statement has comment node
def DelComment(if_list):
    if_no_comment_list=[]
    for i in range(0,len(if_list)):
        is_comment=False
        for child in if_list[i].children:
            if child.type=='comment':
                is_comment=True
                break
        if not is_comment:
            if_no_comment_list.append(if_list[i])

    return if_no_comment_list

# if the if statement has else if or else, we will delete the if statement
# param: the list of if statement
# return: the list of statement without else if / else
def DelElseIf(if_list):
    if_no_else_list=[]

    for i in range(0,len(if_list)):
        is_else=False
        for child in if_list[i].children:
            if child.type=='else':
                is_else=True
                break

        if not is_else:
            if_no_else_list.append(if_list[i])
        else:
            continue

    return if_no_else_list

# we have said that if if statement must has multiple conditions
# for example, if (x==1 && y==2), so that we can split it
# param: the list of if statement
# return: the list of if statement with multipleconditions
def MultipleCondition(if_list):
    if_multi_list=[]

    for i in range(0,len(if_list)):
        result=IsBooleanOperator(if_list[i].children[1])
        if result==True:
            if_multi_list.append(if_list[i])
        else:
            pass

    return if_multi_list

# this function will find if the code has boolean operator, if it is, we can know that it has multiple conditions
# node: the node of tree, and the node is the second child of if statement
def IsBooleanOperator(node):
    if node.type=='binary_expression' and (node.children[1].type=='&&' or node.children[1].type=='||'):
        return True
    elif node.type=='parenthesized_expression':
        result=IsBooleanOperator(node.children[1])
        if result==True:
            return True
        else:
            return False
    else:
        return False

# we will get the first boolean operator and then to split it
# for example, if((x==1 && y==2)||z==3), the first boolean operator is '||'
# so the code can be: if (x==1 && y==2){...} else if(z==3){...}
# param: node: which is the second child of if statement
# return: the first boolean operator
def GetFirstBool(node):
    if node.type=='binary_expression' and (node.children[1].type=='&&' or node.children[1].type=='||'):
        return node
    elif node.type=='parenthesized_expression':
        result=GetFirstBool(node.children[1])
        return result

# this function will process the if statement
# param: node: node type is if statement and it must has no else if / else and has multiple condition、no comment
# return: None
def ProcessIfStatement(node):
    binary_expression=GetFirstBool(node.children[1])
    binary_operator=binary_expression.children[1]
    condition_left=binary_expression.children[0]
    condition_right=binary_expression.children[2]
    if condition_left.type!='parenthesized_expression':
        condition_left=ProcessCondition(condition_left)
    if condition_right.type!='parenthesized_expression':
        condition_right=ProcessCondition(condition_right)


    # we should know that the boolean operator is && or ||
    # so, we should judge the type of boolean operator
    # if the boolean operator is '&&' : if (condition1 && condition2){...} -> if (condition1){ if (condition2) {...} }
    # if the boolean operator is '||' : if (condition1 || condition2){...} -> if (condition1){...} else if (condition2){...}
    if binary_operator.type=='&&':
        node.children[1]=condition_left
        condition_left.parent=node
        if_content=node.children[2]
        block_node=Node()
        block_node.type=='block'
        block_node.parent=node
        node.children[2]=block_node

        left_bracket=Node()
        left_bracket.type='{'
        left_bracket.text='{'
        left_bracket.parent=block_node
        block_node.addchild(left_bracket)

        new_if_statement=Node()
        new_if_statement.type='if_statement'
        new_if_statement.parent=block_node
        block_node.addchild(new_if_statement)

        right_bracket=Node()
        right_bracket.type='}'
        right_bracket.text='}'
        right_bracket.parent=block_node
        block_node.addchild(right_bracket)

        if_node=Node()
        if_node.type='if'
        if_node.text='if'
        if_node.parent=new_if_statement
        new_if_statement.addchild(if_node)

        new_if_statement.addchild(condition_right)
        condition_right.parent=new_if_statement

        new_if_statement.addchild(if_content)
        if_content.parent=new_if_statement

    # if (x==1 || y==2){...} -> if (x==1){...} else if (y==2){...}
    elif binary_operator.type=='||':
        node.children[1]=condition_left
        condition_left.parent=node

        else_node=Node()
        else_node.type='else'
        else_node.text='else'
        else_node.parent=node
        node.addchild(else_node)

        new_if_statement=Node()
        new_if_statement.type='if_statement'
        new_if_statement.parent=node
        node.addchild(new_if_statement)
        if_node=Node()
        if_node.type='if'
        if_node.text='if'
        if_node.parent=new_if_statement
        new_if_statement.addchild(if_node)
        condition_right.parent=new_if_statement
        new_if_statement.addchild(condition_right)
        if_content2=Node()
        if_content2.parent=new_if_statement
        new_if_statement.addchild(if_content2)
        CopySubtreeJava(node.children[2],if_content2)




# because in java, we must add (...),so we use this function to do it

def ProcessCondition(condition_expression):
    parenthesized_expression=Node()
    parenthesized_expression.type = 'parenthesized_expression'
    left_paren = Node()
    left_paren.type = '('
    left_paren.text = '('
    left_paren.parent = parenthesized_expression
    parenthesized_expression.addchild(left_paren)
    condition_expression.parent=parenthesized_expression
    parenthesized_expression.addchild(condition_expression)
    right_paren = Node()
    right_paren.type = ')'
    right_paren.text = ')'
    right_paren.parent = parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    return parenthesized_expression
