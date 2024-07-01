from Node import Node
from AstToTree import *

# rewrite the for statement into while statement

#param: tree_root_node: the root node of the tree generated from ast
#return : new code that we have rewrite the fofr statement
def ForToWhile(tree_root_node):
    result=FindForStatementS(tree_root_node)
    if len(result)==0:
        return 0

    for i in range(0,len(result)):
        ChangeForStatement(result[i],i)

    code=TreeToTextPy(tree_root_node)
    return code


# find that if the code has for statement : if has we return True, else we return false
# param: a node of the tree generated from the ast, it will be root node
# return: if the code has for statement
def IsForStatement(node):
    if node.type=='for_statement':
        return True
    if len(node.children)!=0:
        for child in node.children:
            result=IsForStatement(child)
            #print(result)
            if result==True:
                #print('find true')
                return True

        return False
    else:
        return False

# find the if_node from the code
# parm: the node of tree generate from ast
# return: a list of for node
def FindForStatement(node):
    for_list=[]
    if node.type=='for_statement' :
        for_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindForStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    for_list.append(result[i])

    else:
        pass

    return for_list

#find the for statement that satisfies us ,such as for i in range(start,end,step): block .
#para: node of the tree generated from ast
#return the list of the for statement
def IsForStatementS(node):
    if node.type == 'for_statement':
        no_commet = True
        for child in node.children:
            if child.type == 'comment' or child.type == 'string':
                no_commet = False
                break
        if len(node.children) >= 6:
            if node.children[3].type == 'call':
                if node.children[3].children[0].text == 'range' and no_commet:
                    return True

    if len(node.children)!=0:
        for child in node.children:
            result=IsForStatementS(child)
            #print(result)
            if result==True:
                #print('find true')
                return True

        return False
    else:
        return False


def FindForStatementS(node):
    for_list=[]
    if node.type=='for_statement':
        no_commet=True
        for child in node.children:
            if child.type=='comment' or child.type=='string':
                no_commet=False
                break
        if len(node.children)>=6:
            if node.children[3].type=='call':
                if node.children[3].children[0].text=='range' and no_commet:
                    for_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindForStatementS(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    for_list.append(result[i])

    else:
        pass

    return for_list


# rewrite the for statement to while statement
# for example: for i in range(0,12): block -> i=0 while(i<12): block+i=i+1 ...
# what we should know is that the continue statement
# param: node of the tree generated from ast
# return : none
def ChangeForStatement(node,n):
    node_index=node.parent.children.index(node)
    var=node.children[1].text
    #for python: range(start,end,step)
    start_node=None
    end_node=None
    step_node=None
    # for example: for i in range(5): block
    if len(node.children[3].children[1].children) == 3:
        start_node = Node()
        start_node.type = 'integer'
        start_node.text = '0'
        end_node=node.children[3].children[1].children[1]
        step_node=Node()
        step_node.type='integer'
        step_node.text='1'
    elif len(node.children[3].children[1].children) == 5:
        start_node=node.children[3].children[1].children[1]
        end_node=node.children[3].children[1].children[3]
        step_node=Node()
        step_node=Node()
        step_node.type='integer'
        step_node.text='1'
    else:
        start_node=node.children[3].children[1].children[1]
        end_node=node.children[3].children[1].children[3]
        step_node=node.children[3].children[1].children[5]

    #the first statement that assign the start node, for example: x=0
    expression_statement_node_1=Node()
    expression_statement_node_1.type='expression_statement'
    expression_statement_node_1.parent=node.parent
    node.parent.children[node_index]=expression_statement_node_1

    # i=start_node
    assigement_node_1=Node()
    assigement_node_1.type='assignment'
    assigement_node_1.parent=expression_statement_node_1
    expression_statement_node_1.addchild(assigement_node_1)

    # i node, for example: i=0
    i_node=Node()
    i_node.type='identifier'
    i_node.text=var
    i_node.parent=assigement_node_1
    assigement_node_1.addchild(i_node)

    # equation node
    equation_node_1=Node()
    equation_node_1.type='='
    equation_node_1.text='='
    equation_node_1.parent=assigement_node_1
    assigement_node_1.addchild(equation_node_1)

    start_node.parent=assigement_node_1
    assigement_node_1.addchild(start_node)

    # while statement
    while_statement_node=Node()
    while_statement_node.type='while_statement'
    while_statement_node.parent=node.parent
    node.parent.children.insert(node_index+1,while_statement_node)

    # while identifier node
    while_identifier_node=Node()
    while_identifier_node.type='while'
    while_identifier_node.text='while'
    while_identifier_node.parent=while_statement_node
    while_statement_node.addchild(while_identifier_node)

    comparison_operator_node=Node()
    comparison_operator_node.type='comparison_operator'
    comparison_operator_node.parent=while_statement_node
    while_statement_node.addchild(comparison_operator_node)

    #i node 2, for example: while i<10
    i_node_2=Node()
    i_node_2.type='identifier'
    i_node_2.text=var
    i_node_2.parent=comparison_operator_node
    comparison_operator_node.addchild(i_node_2)

    # binary operator '<' , for example: while i < 2 ,the second token -> i
    binary_operator_node=Node()
    binary_operator_node.type='<'
    binary_operator_node.text='<'
    binary_operator_node.parent=comparison_operator_node
    comparison_operator_node.addchild(binary_operator_node)

    end_node.parent=comparison_operator_node
    comparison_operator_node.addchild(end_node)

    # colon node, for example : while i < 12 : the sixth token -> :
    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=while_statement_node
    while_statement_node.addchild(colon_node)

    # block
    block_node=node.children[5]
    block_node.parent=while_statement_node
    while_statement_node.addchild(block_node)

    #we first add the i=i+step_node to the end of block statement
    expression_statement_node_2=Node()
    expression_statement_node_2.type='expression_statement'
    expression_statement_node_2.parent=block_node
    block_node.addchild(expression_statement_node_2)

    assigement_node_2=Node()
    assigement_node_2.type='assignment'
    assigement_node_2.parent=expression_statement_node_2
    expression_statement_node_2.addchild(assigement_node_2)
    # because we should add the statement: i=i+step_node so we will create 2 i node and 1 '=' node
    i_node_3=Node()
    i_node_3.type='identifier'
    i_node_3.text=var
    i_node_3.parent=assigement_node_2
    assigement_node_2.addchild(i_node_3)

    equation_node_2=Node()
    equation_node_2.type='='
    equation_node_2.text='='
    equation_node_2.parent=assigement_node_2
    assigement_node_2.addchild(equation_node_2)

    binary_operator=Node()
    binary_operator.type='binary_operator'
    binary_operator.parent=assigement_node_2
    assigement_node_2.addchild(binary_operator)

    i_node_4 = Node()
    i_node_4.type = 'identifier'
    i_node_4.text = var
    i_node_4.parent = binary_operator
    binary_operator.addchild(i_node_4)

    add_binary_operator_node=Node()
    add_binary_operator_node.type='+'
    add_binary_operator_node.text='+'
    add_binary_operator_node.parent=binary_operator
    binary_operator.addchild(add_binary_operator_node)

    step_node.parent=binary_operator
    binary_operator.addchild(step_node)

    # we must process the subtree of block where continue in the subtree
    continue_list=FindWhileContinue(block_node)
    for i in range(0,len(continue_list)):
        ProcessContinue(continue_list[i],expression_statement_node_2)
    #recrunode(while_statement_node)
    ResetLevelPY(expression_statement_node_1)
    ResetLevelPY(while_statement_node)




# if continue statement in the block, we should process it, whe reason is that: for example
# for i in range (0,12):
#     if i ==10:
#         continue
#     else:
#         print(i)
# but in while statement:
# while(i<12):
#     if i ==10:
#         continue
#     else:
#         print(i)
#     i=i+1
# because of the continue statement, the while statement will not stop
def FindWhileContinue(node):
    continue_list=[]
    if node.type=='continue_statement':
        continue_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            if child.type=='while_statement' or child.type=='for_statement':
                continue
            else:
                result=FindWhileContinue(child)
                if len(result)!=0:
                    for i in range(0,len(result)):
                        continue_list.append(result[i])
    else:
        pass
    return continue_list

# we will process the continue by easily add i=i+step_node before the continue statement
# for example:
# i=i+1
# continue
def ProcessContinue(continue_node,expression_node):
    expression_node_2=Node()
    CopySubtreePY(expression_node,expression_node_2)
    continue_node_index=continue_node.parent.children.index(continue_node)
    continue_node.parent.children.insert(continue_node_index,expression_node_2)
    expression_node_2.parent=continue_node

