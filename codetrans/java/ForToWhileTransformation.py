# this transformation will convert for statement to while statement
from AstToTree import *
from Node import Node
from GetAST import *

# this is the main function to convert the for statement to while statement
# tree_root_node: the root node of the tree generated from ast
# return: the new code
def ForToWhile(tree_root_node):
    for_list=FindForStatement(tree_root_node)
    if len(for_list)==0:
        return 0
    else:
        for i in range(0,len(for_list)):
            ProcessForStatement(for_list[i])
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

# this function will convert the for statement to while statement, you can see the source code for the details
# param: for_statement: the node which type is 'for_statement'
# return: None
def ProcessForStatement(for_statement):
    #find and store the continue_statement, and then we will use them
    continue_list=FindForContinue(for_statement)

    # replace for statement with while statement
    for_parent=for_statement.parent
    for_index=for_parent.children.index(for_statement)

    # the for statement to while statement is like:
    # parent:
    # for (ini;condition;update) {...}
    # so, the transformed while statement is:
    # parent:
    # ini ;
    # while(condition){... update}
    # but if the parent is compound statement, like if, for example: if(x==0) for(ini;condition;update){...}
    # but if(x==0) ini; while(condition)... is wrong
    # we must add braces, if(x==0){ ini; while(condition)... }
    parent_block=Node()
    parent_block.type='block'
    parent_block.parent=for_parent
    for_parent.children[for_index]=parent_block

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=parent_block
    parent_block.addchild(left_brace)

    while_statement=Node()
    while_statement.type='while_statement'
    while_statement.parent=parent_block
    # parent_block.addchild(while_statement)

    while_node=Node()
    while_node.type='while'
    while_node.text='while'
    while_node.parent=while_statement
    while_statement.addchild(while_node)

    # find the content between '(' and ')'
    for i in range(1,len(for_statement.children)):
        if for_statement.children[i].type=='(':
            left_parenthesized_index=i
            break
        else:
            while_statement.addchild(for_statement.children[i])
            for_statement.children[i].parent=while_statement

    for i in range(left_parenthesized_index+1,len(for_statement.children)):
        if for_statement.children[i].type==')':
            right_parenthesized_index=i

    # the content in the for statement is (ini;condition;update), so we should find the three parts

    # find the ini
    isinistmt=False
    for i in range(left_parenthesized_index+1,right_parenthesized_index):
        if for_statement.children[i].type=='comment':
            continue
        elif for_statement.children[i].type=='local_variable_declaration':
            isinistmt=True
            ini_index=i
            break
        else:
            for j in range(i,right_parenthesized_index):
                if for_statement.children[j].type==';':
                    ini_index=j
                    break
            break


    # find the condition
    for i in range(ini_index+1,right_parenthesized_index):
        if for_statement.children[i].type==';':
            condition_index=i
            break

    # find the update

    update_index=right_parenthesized_index-1

    # add the ini expression
    if isinistmt==False:
        ini_index=ini_index-1
    for i in range(left_parenthesized_index+1,ini_index+1):
        if for_statement.children[i].type==',':
            continue

        if for_statement.children[i].type=='comment' or 'declaration' in for_statement.children[i].type or 'statement' in for_statement.children[i].type:
            for_statement.children[i].parent=parent_block
            parent_block.addchild(for_statement.children[i])

        else:

            expression_statement=Node()
            expression_statement.type='expression_statement'
            expression_statement.parent=parent_block
            parent_block.addchild(expression_statement)

            for_statement.children[i].parent=expression_statement
            expression_statement.addchild(for_statement.children[i])

            semicolon=Node()
            semicolon.type=';'
            semicolon.text=';'
            semicolon.parent=expression_statement
            expression_statement.addchild(semicolon)

    # add while statement
    parent_block.addchild(while_statement)
    parenthesized_expression=Node()
    parenthesized_expression.type='parenthesized_expression'
    parenthesized_expression.parent=while_statement
    while_statement.addchild(parenthesized_expression)

    left_parenthesized=Node()
    left_parenthesized.type='('
    left_parenthesized.text='('
    left_parenthesized.parent=parenthesized_expression
    parenthesized_expression.addchild(left_parenthesized)

    # add condition
    if isinistmt==False:
        ini_index=ini_index+1
    for i in range(ini_index+1,condition_index):
        for_statement.children[i].parent=parenthesized_expression
        parenthesized_expression.addchild(for_statement.children[i])

    right_parenthesized=Node()
    right_parenthesized.type=')'
    right_parenthesized.text=')'
    right_parenthesized.parent=parenthesized_expression
    parenthesized_expression.addchild(right_parenthesized)

    # add content
    for i in range(right_parenthesized_index+1,len(for_statement.children)):
        for_statement.children[i].parent=while_statement
        while_statement.addchild(for_statement.children[i])

    # add update
    if while_statement.children[len(while_statement.children)-1].type!='block':
        content=while_statement.children[len(while_statement.children)-1]
        while_block=Node()
        while_block.type='block'
        while_block.parent=while_statement
        while_statement.children[len(while_statement.children)-1]=while_block

        while_left_brace=Node()
        while_left_brace.type='{'
        while_left_brace.text='{'
        while_left_brace.parent=while_block
        while_block.addchild(while_left_brace)

        content.parent=while_block
        while_block.addchild(content)

        while_right_brace=Node()
        while_right_brace.type='}'
        while_right_brace.text='}'
        while_right_brace.parent=while_block
        while_block.addchild(while_right_brace)
    else:
        pass

    while_block=while_statement.children[len(while_statement.children)-1]
    block_add_index=len(while_block.children)-1
    for i in range(condition_index+1,right_parenthesized_index):
        if for_statement.children[i].type==',':
            continue

        if for_statement.children[i].type=='comment' or 'declaration' in for_statement.children[i].type or 'statement' in for_statement.children[i].type:
            for_statement.children[i].parent=while_block
            while_block.children.insert(block_add_index,for_statement.children[i])

        else:
            expression_statement=Node()
            expression_statement.type='expression_statement'
            expression_statement.parent=while_block
            while_block.children.insert(block_add_index,expression_statement)

            for_statement.children[i].parent=expression_statement
            expression_statement.addchild(for_statement.children[i])
            semicolon=Node()
            semicolon.type=';'
            semicolon.text=';'
            semicolon.parent=expression_statement
            expression_statement.addchild(semicolon)


    # if the content of for statement has no continue_statement, the transformation is finished
    if len(continue_list)==0:
        pass
    # if the content of for statement has continue_statement, we should add the 'update' before every continue_statement
    else:
        for i in range(0,len(continue_list)):
            index=continue_list[i].parent.children.index(continue_list[i])
            block=Node()
            block.type='block'
            block.parent=continue_list[i].parent
            continue_list[i].parent.children[index]=block

            left_brace=Node()
            left_brace.type='{'
            left_brace.text='{'
            left_brace.parent=block
            block.addchild(left_brace)
            for j in range(condition_index+1,right_parenthesized_index):
                if for_statement.children[j].type==',':
                    continue

                if for_statement.children[j].type == 'comment' or 'declaration' in for_statement.children[j].type or 'statement' in for_statement.children[j].type:
                    # copy the new sub-tree of the content
                    copy_node=Node()
                    CopySubtreeJava(for_statement.children[j],copy_node)
                    copy_node.parent = block
                    block.addchild(copy_node)

                else:
                    expression_statement = Node()
                    expression_statement.type = 'expression_statement'
                    expression_statement.parent = block
                    block.addchild(expression_statement)

                    copy_node = Node()
                    CopySubtreeJava(for_statement.children[j], copy_node)
                    copy_node.parent=expression_statement
                    expression_statement.addchild(copy_node)
                    semicolon = Node()
                    semicolon.type = ';'
                    semicolon.text = ';'
                    semicolon.parent = expression_statement
                    expression_statement.addchild(semicolon)

            continue_list[i].parent=block
            block.addchild(continue_list[i])

            right_brace=Node()
            right_brace.type='}'
            right_brace.text='}'
            right_brace.parent=block
            block.addchild(right_brace)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=while_statement
    while_statement.addchild(right_brace)



# return the list of continue in for statement
# param: node: the node which type if for_statement
# return: the list of continue statement in for statement
def FindForContinue(node):

    continue_list=[]
    if node.type=='continue_statement':
        continue_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            # if the continue statement in for/while, we do not consider it
            if child.type=='while_statement' or child.type=='for_statement':
                continue
            else:
                result=FindForContinue(child)
                if len(result)!=0:
                    for i in range(0,len(result)):
                        continue_list.append(result[i])

    else:
        pass

    return continue_list









