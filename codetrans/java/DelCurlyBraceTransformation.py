# in this transformation, we will remove curly brace
# if the body of compound statement has just one statement, remove curly brace is okey
# for example:
# while(true){
# continue;
# }
# it can be converted to
# while(true)
# continue;
from AstToTree import *
from Node import Node

# this is the main method that remove curly brace
# param: tree_root_node: the root node of the tree generated from ast
# return: new code
def DelCurlyBrace(tree_root_node):
    compound_list=FindCompoundStatement(tree_root_node)
    block_list=FindBlock(compound_list)
    block_simple_list=BlockSimpleStatement(block_list)
    if len(block_simple_list)==0:
        return 0
    else:
        for i in range(0,len(block_simple_list)):
            ProcessCompoundStatement(block_simple_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

# if the code has compound statement, it will return true, else it will return false
# param: tree_root_node: the root node of tree generated from ast
# return: true/false
def IsCompoundStatement(tree_root_node):
    compound_list=['for_statement','if_statement','while_statement']
    if tree_root_node.type in compound_list:
        return True
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsCompoundStatement(child)
            if result==True:
                return True
        return False

    else:
        return False

# we will return all the compound statement(for, while, if)
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of compound statement(we only consider for,while,if)
def FindCompoundStatement(tree_root_node):
    compound_list =['for_statement','if_statement','while_statement']
    find_list=[]
    if tree_root_node.type in compound_list:
        find_list.append(tree_root_node)
    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindCompoundStatement(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    find_list.append(result[i])

    else:
        pass

    return find_list

# return the list of block node, the block node is the children of for statement/ while statement/ if statement
# param: compound_list: the list of for statement/ while statement/ if statement
# return: the list of block
def FindBlock(compound_list):
    block_list=[]

    for i in range(0,len(compound_list)):
        # if the node type if for_statement or whle_statement, then the last child of for_statement/while_statement is what we want
        if compound_list[i].type=='for_statement' or compound_list[i].type=='while_statement':
            if compound_list[i].children[len(compound_list[i].children)-1].type=='block':
                block_list.append(compound_list[i].children[len(compound_list[i].children)-1])

        # for if_statement, we should take the else/ else if and comment into consider
        # so if the if_statement has comment, we delete it directly
        # if the if_statement has else, it may has to block, you can see the source code
        elif compound_list[i].type=='if_statement':
            is_comment=False
            for child in compound_list[i].children:
                if child.type=='comment':
                    is_comment=True
                    break
            if is_comment:
                pass
            else:
                no_else=True
                for child in compound_list[i].children:
                    if child.type=='else':
                        loc=compound_list[i].children.index(child)
                        no_else=False
                        break

                if no_else==True:
                    if compound_list[i].children[len(compound_list[i].children)-1].type=='block':
                        block_list.append(compound_list[i].children[len(compound_list[i].children)-1])
                    else:
                        pass
                else:
                    if compound_list[i].children[loc-1].type=='block':
                        block_list.append(compound_list[i].children[loc-1])
                    if compound_list[i].children[loc+1].type=='block':
                        block_list.append(compound_list[i].children[loc+1])

    return block_list

# because the block maybe has many statements, but only the number of statement is just one, we can delete curly brace
# param: block_list: the list of nodes-> type is block
# return: return the list of block node which has three children
def BlockSimpleStatement(block_list):
    block_simple_list=[]
    for i in range(0,len(block_list)):
        if len(block_list[i].children)==3 and block_list[i].children[1].type!='comment':
            block_simple_list.append(block_list[i])
        else:
            continue

    return block_simple_list

# this method will extract the simple statement in the block: { simple_statement }
# param: block_node: the node of tree which type is block and has three childrens: { simple_statement }
# return: None
def ProcessCompoundStatement(block_node):
    simple_statement=block_node.children[1]
    index=block_node.parent.children.index(block_node)
    simple_statement.parent=block_node.parent
    block_node.parent.children[index]=simple_statement

