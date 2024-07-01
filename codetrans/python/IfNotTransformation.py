# this function will transform the if statement
# for example:
# if (x>=0):
#     block1
# else:
#     block2
# we can transform it to:
# if(!(x>=0)):
#     block2
# else:
# block1
# 由于python的ast类似于:     if_statement
#                       |     |            |
#                      block1  elif_clause  else_clause
# 那么就不能像java那样仅对if条件进行分析
# 这样的话，其实是需要递归进行transform的
# 举例来说: if(x==0): block1 elif(x==2): block2 else: block3 -> if(not x==0) if (x==2) block2 else: block3 else: block1
# 但是因为在转换后的第一个if (not x==0)中又包含了新的if语句，是需要进行新的处理的，所以我们需要再次转换才可以得到一个完全的转换后的结果的
# 这样其实是与java不一样的，这是由于java的ast和python的ast不一样导致的
# python的转换进行多次递归也可以得到相同的结果

from Node import Node
from AstToTree import *
from GetAST import *

def IfNotTransformation(tree_root_node):
    if_list=FindIfAndElse(tree_root_node)
    if_list=Delcomment(if_list)
    if len(if_list)==0:
        return 0
    else:
        for i in range(0,len(if_list)):
            ProcessIfNot(if_list[i])
        code=TreeToTextPy(tree_root_node)
        return code

def IsIfAndElse(tree_root_node):
    if tree_root_node.type=='if_statement':
        for child in tree_root_node.children:
            if child.type=='elif_clause' or child.type=='else_clause':
                return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsIfAndElse(child)
            if result==True:
                return True
        return False
    else:
        return False



def FindIfAndElse(tree_root_node):
    if_list=[]
    if tree_root_node.type == 'if_statement':
        for child in tree_root_node.children:
            if child.type == 'elif_clause' or child.type == 'else_clause':
                if_list.append(tree_root_node)
                break

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindIfAndElse(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    if_list.append(result[i])
    else:
        pass

    return if_list

def Delcomment(if_list):
    if_no_comment_list=[]
    for i in range(0,len(if_list)):
        is_comment=False
        for child in if_list[i].children:
            if child.type=='comment' or child.type=='string':
                is_comment=True
                break
        if not is_comment:
            if_no_comment_list.append(if_list[i])

    return if_no_comment_list



def ProcessIfNot(if_statement_node):

    iselif=False
    elif_index=0
    for child in if_statement_node.children:
        if child.type=='elif_clause':
            iselif=True
            elif_index=if_statement_node.children.index(child)
            break
    # 找到if语句的条件，然后取反
    condition=if_statement_node.children[1]
    not_operator=Node()
    not_operator.type='not_operator'
    not_operator.parent=if_statement_node
    if_statement_node.children[1]=not_operator

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

    condition.parent=parenthesized_expression
    parenthesized_expression.addchild(condition)

    right_paren=Node()
    right_paren.type=')'
    right_paren.text=')'
    right_paren.parent=parenthesized_expression
    parenthesized_expression.addchild(right_paren)

    block_node=if_statement_node.children[3]
    # for statement中存在elif
    # 创建新的block 并且将elif_clause 和 else_clause移动到这里面去
    if iselif:

        new_block=Node()
        new_block.type='block'
        new_block.parent=if_statement_node
        if_statement_node.children[3]=new_block
        # 因为在if语句中有elif的存在，那么其实是需要把第一个elif转换成if的，因为需要在block中创建一个新的if语句
        new_if_statement=Node()
        new_if_statement.type='if_statement'
        new_if_statement.parent=new_block
        new_block.addchild(new_if_statement)

        if_node=Node()
        if_node.type='if'
        if_node.text='if'
        if_node.parent=new_if_statement
        new_if_statement.addchild(if_node)

        # 将第一个elif中的子节点移动到这里，但是注意第一个节点是'elif',因此其实是从第二个节点开始移动的
        for i in range(1,len(if_statement_node.children[elif_index].children)):
            if_statement_node.children[elif_index].children[i].parent=new_if_statement
            new_if_statement.addchild(if_statement_node.children[elif_index].children[i])

        #将后续的所有节点都作为新的if语句的子节点即可

        for i in range(elif_index+1,len(if_statement_node.children)):
            if_statement_node.children[i].parent=new_if_statement
            new_if_statement.addchild(if_statement_node.children[i])

        # 从原始的if语句中删除我们添加到新的if条件语句中的elif和else
        if_statement_node.children=if_statement_node.children[0:elif_index]

    # 如果没有elif，那么就只有else语句了，而且肯定是最后一个节点
    # 此时只需要将else中的block代替if中的block即可
    if not iselif:
        else_node=if_statement_node.children[-1]
        for child in else_node.children:
            if child.type=='block':
                else_block=child
                break

        else_block.parent=if_statement_node
        if_statement_node.children[3]=else_block
        if_statement_node.children=if_statement_node.children[:-1]

    # 为if后面的block添加一个else clause

    else_clause=Node()
    else_clause.type='else_clause'
    else_clause.parent=if_statement_node
    if_statement_node.addchild(else_clause)

    else_node=Node()
    else_node.type='else'
    else_node.text='else'
    else_node.parent=else_clause
    else_clause.addchild(else_node)

    colon_node=Node()
    colon_node.type=':'
    colon_node.text=':'
    colon_node.parent=else_clause
    else_clause.addchild(colon_node)

    block_node.parent=else_clause
    else_clause.addchild(block_node)

    ResetLevelPY(if_statement_node)



