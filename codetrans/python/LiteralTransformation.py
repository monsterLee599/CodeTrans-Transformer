from Node import Node
from AstToTree import *

#1、judge if there is return integer
#2、find the variable and the variable we set must different
#3、transform the code

#change the integer literal to variant in the return statement, for example: return 0 -> x=0 return x
#param: tree_root_node: the node of the tree
# return the ew code
def LiteralToVariable(tree_root_node):
    return_list=GetReturn(tree_root_node)
    #return return_list
    return_literal_list=[]
    for i in range(0,len(return_list)):
        result=ReturnLiteral(return_list[i])
        if result==True:
            return_literal_list.append(return_list[i])
        else:
            continue

    #return return_literal_list
    if len(return_literal_list)==0:
        return 0

    base_identifier='return_identifier_'
    for i in range(0,len(return_literal_list)):
        identifier=base_identifier+str(i)
        # expression statement
        experssion_statement_node=Node()
        experssion_statement_node.type='expression_statement'
        experssion_statement_node.parent=return_literal_list[i].parent
        index=return_literal_list[i].parent.children.index(return_literal_list[i])
        return_literal_list[i].parent.children.insert(index,experssion_statement_node)

        # assignment node
        assignment_node=Node()
        assignment_node.type='assignment'
        assignment_node.parent=experssion_statement_node
        experssion_statement_node.addchild(assignment_node)

        # return identifier
        identifier_node=Node()
        identifier_node.type='identifier'
        identifier_node.text=identifier
        identifier_node.parent=assignment_node
        assignment_node.addchild(identifier_node)

        #equivalent node
        equivalent_node=Node()
        equivalent_node.type='='
        equivalent_node.text='='
        equivalent_node.parent=assignment_node
        assignment_node.addchild(equivalent_node)

        #return content
        return_literal_list[i].children[1].parent=assignment_node
        assignment_node.addchild(return_literal_list[i].children[1])

        # return identifier node
        return_identifier_node=Node()
        return_identifier_node.type='identifier'
        return_identifier_node.text=identifier
        return_identifier_node.parent=return_literal_list[i]
        return_literal_list[i].children[1]=return_identifier_node

        # refresh the level
        ResetLevelPY(return_literal_list[i])
        ResetLevelPY(experssion_statement_node)

    code=TreeToTextPy(tree_root_node)
    return code



#return the return statement node
#param: node of the tree
#return : the list of root node of return statement
def GetReturn(node):
    return_list=[]
    if node.type=='return_statement':
        return_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=GetReturn(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    return_list.append(result[i])

    else:
        pass

    return return_list

# if the return statement return the type of data ,we will change it, for example : return list -> x=list return x
#param: the root node of return statement
# return : if the return statement return the type of data
def ReturnLiteral(return_statement_node):
    type_list=[ 'tuple','false', 'true','list', 'dictionary', 'string', 'integer', 'float','set']
    if len(return_statement_node.children)==2:
        if return_statement_node.children[1].type in type_list:
            return True
        else:
            return False
    else:
        return False


# change the return statement
# param : root node of the return statement
# return : none
def ChangeReturn(node):
    pass