from Node import Node
from AstToTree import *

#split the if statement
#we get the idea from <Misleading authorship attribution of source code using adversarial learning>
#so we only split the if statement that no elif and else
#you can also change the transformer to satisfy yourself

#param : the root node of the tree generated from ast
def IfStatement(tree_root_node):
    if_list=GetIfStatement(tree_root_node)
    if_no_else_list=IfElse(if_list)
    if_multi_list=MultipleConditions(if_list)
    if_multi_no_else_list=[]
    for i in range(0,len(if_multi_list)):
        if if_multi_list[i] in if_no_else_list:
            if_multi_no_else_list.append(if_multi_list[i])
        else:
            continue

    if len(if_multi_no_else_list)==0:
        return 0

    # two condition: if x and y: if x: if y
    #                if x or y :if x : block elif y : block
    # find the first boolean operator and judge which operation
    for i in range(0,len(if_multi_no_else_list)):
        bool_operator=GetFirstBool(if_multi_no_else_list[i])
        #print(bool_operator.children[1].type)
        condition_left=bool_operator.children[0]
        condition_right=bool_operator.children[2]
        #change the condition of if statement
        if_multi_no_else_list[i].children[1]=condition_left
        condition_left.parent=if_multi_no_else_list[i]
        if bool_operator.children[1].type=='and':
            #if x and y: block -> if x : if y : block
            new_block=if_multi_no_else_list[i].children[3]
            old_block=Node()
            old_block.level=new_block.level
            old_block.type='block'
            old_block.parent=if_multi_no_else_list[i]
            if_multi_no_else_list[i].children[3]=old_block

            #if statement
            new_if_statement=Node()
            #new_if_statement.level=old_block.level
            new_if_statement.type='if_statement'
            new_if_statement.parent=old_block
            old_block.addchild(new_if_statement)

            # if identifier
            if_identifier=Node()
            #if_identifier.level=old_block.level
            if_identifier.type='if'
            if_identifier.text='if'
            if_identifier.parent=new_if_statement
            new_if_statement.addchild(if_identifier)

            #condition
            new_if_statement.addchild(condition_right)
            condition_right.parent=new_if_statement

            #: identifier
            colon_indentifier=Node()
            colon_indentifier.type=':'
            colon_indentifier.text=':'
            colon_indentifier.parent=new_if_statement
            new_if_statement.addchild(colon_indentifier)

            # new block
            new_block.parent=new_if_statement
            new_if_statement.addchild(new_block)
            # reset the level of tree
            ResetLevelPY(if_multi_no_else_list[i])

        elif bool_operator.children[1].type=='or':
            # if x or y : block -> if x : block elif y : block

            #elif clause
            elif_clause_node=Node()
            elif_clause_node.type='elif_clause'
            elif_clause_node.parent=if_multi_no_else_list[i]
            if_multi_no_else_list[i].addchild(elif_clause_node)

            # elif identifier
            elif_identifier_node=Node()
            elif_identifier_node.type='elif'
            elif_identifier_node.text='elif'
            elif_identifier_node.parent=elif_clause_node
            elif_clause_node.addchild(elif_identifier_node)

            # condition
            condition_right.parent=elif_clause_node
            elif_clause_node.addchild(condition_right)

            #: identifier
            colon_indentifier=Node()
            colon_indentifier.type=':'
            colon_indentifier.text=':'
            colon_indentifier.parent=elif_clause_node
            elif_clause_node.addchild(colon_indentifier)

            # new block
            new_block_node=Node()
            new_block_node.parent=elif_clause_node
            elif_clause_node.addchild(new_block_node)
            CopySubtreePY(if_multi_no_else_list[i].children[3],new_block_node)
            ResetLevelPY(if_multi_no_else_list[i])

    #generate and return the new code
    code=TreeToTextPy(tree_root_node)
    return code


#get the if statement
#param : root node of tree generated from ast
#return the list of if statement nodes
def GetIfStatement(tree_root_node):
    if_list=[]

    #add if statement
    if tree_root_node.type=='if_statement':
        no_comment=True
        for child in tree_root_node.children:
            if child.type=='comment' or child.type=='string':
                no_comment=False
        if no_comment:
            if_list.append(tree_root_node)
    #internal node
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=GetIfStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    if_list.append(result[i])
    # leaf node
    else:
        pass

    return if_list

#judge that if the if statement has else/elif and return the new list: no else/elif
#param: the list of if statement
#return : new list of if statement without else/elif
def IfElse(if_list):
    if_no_else_list=[]

    for i in range(0,len(if_list)):
        #if_statement
        is_else=False
        for child in if_list[i].children:
            if child.type=='else_clause' or child.type=='elif_clause':
                is_else=True
                break

        if not is_else:
            if_no_else_list.append(if_list[i])
        else:
            continue

    return if_no_else_list

#judge if the if statement has multiple conditions : or / and
#param: the list of if statements
#return: the list of if statements with multi conditions
def MultipleConditions(if_list):
    if_multi_list=[]
    for i in range(0,len(if_list)):
        condition_node=if_list[i].children[1]
        if condition_node.type=='boolean_operator':
            if_multi_list.append(if_list[i])
        elif condition_node.type=='parenthesized_expression':
            result=RecruParen(condition_node)
            if result==True:
                if_multi_list.append(if_list[i])
        else:
            continue

    return if_multi_list



# judge if the if_statement has boolean operator in the condition (((x==1)))
# param: node of the tree - child of if_statement
#return: if has boolean operator return True ; else return false
def RecruParen(node):
    if node.type=='boolean_operator':
        return True

    elif len(node.children)==0:
        return False

    elif node.type=='parenthesized_expression':
        result=RecruParen(node.children[1])
        return result
    else :
        return False


#get the type of the boolean operator ( and / or), so we can get the operation
#param : if_statement node
#return : the type of the first boolean operator
def GetFirstBool(node):
    if node.children[1].type=='boolean_operator':
        return node.children[1]
    elif node.children[1].type=='parenthesized_expression':
        first_bool=RecruFirBool(node.children[1])
        return first_bool

# get the first boolean operator
# param: node of the tree
# return : type of the boolean operator
def RecruFirBool(node):
    if node.type=='boolean_operator':
        return node

    elif node.type=='parenthesized_expression':
        return RecruFirBool(node.children[1])