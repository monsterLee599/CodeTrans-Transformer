# we will add curly brace if the statement is a single statement
# for examle:
# if(x==0)
# continue;
# it can be transformed to :
# if(x=0){
# continue;
# }
# we only take if、for、while into consider

from AstToTree import *
from GetAST import *
from Node import Node

def AddCurlyBrace(tree_root_node):
    compound_list=FindCompoundStatement(tree_root_node)
    simple_statement_list=FindSimpleStatement(compound_list)
    if len(simple_statement_list)==0:
        return 0
    else:
        for i in range(0,len(simple_statement_list)):
            ProcessCompoundStatement(simple_statement_list[i])

        code=TreeToTextJava(tree_root_node)
        return code

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

def FindCompoundStatement(tree_root_node):
    compound_list = ['for_statement', 'if_statement', 'while_statement']
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

def FindSimpleStatement(compound_list):
    simple_statement_list=[]
    for i in range(0,len(compound_list)):
        # in for and while statement, we can easily find the body of the if/while statement and if the body type is not block, we can add curly brace
        if compound_list[i].type=='for_statement' or compound_list[i].type=='while_statement':
            if compound_list[i].children[len(compound_list[i].children)-1].type!='block':
                simple_statement_list.append(compound_list[i].children[len(compound_list[i].children)-1])
        # but in if statement, because it maybe has else/else if, so we should carefully judge it
        # if the children of if statement has comment, we just skip it
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
                loc=0
                for child in compound_list[i].children:
                    if child.type=='else':
                        loc=compound_list[i].children.index(child)
                        no_else=False
                        break
                # no else/else if, like for and while statement
                if no_else==True:
                    if compound_list[i].children[len(compound_list[i].children)-1].type!='block':
                        simple_statement_list.append(compound_list[i].children[len(compound_list[i].children)-1])
                # if the if statement has else/else if
                else:
                    if compound_list[i].children[loc-1].type!='block':
                        simple_statement_list.append(compound_list[i].children[loc-1])
                    if compound_list[i].children[loc+1].type!='block' and compound_list[i].children[loc+1].type!='if_statement':
                        simple_statement_list.append(compound_list[i].children[loc+1])
    return simple_statement_list


def ProcessCompoundStatement(node):
    # what we should know is that if the last node of the compound statement is block, then the body must has curly braces
    # so, if the last node of the compound statement is not block, it must be single statement
    # we can easily add curly braces, and the transformation is finished
    # but for is statement, because it maybe has "else", so we should
    block=Node()
    block.type='block'
    block.parent=node.parent
    loc=node.parent.children.index(node)
    node.parent.children[loc]=block

    left_brace=Node()
    left_brace.type='{'
    left_brace.text='{'
    left_brace.parent=block
    block.addchild(left_brace)

    node.parent=block
    block.addchild(node)

    right_brace=Node()
    right_brace.type='}'
    right_brace.text='}'
    right_brace.parent=block
    block.addchild(right_brace)
