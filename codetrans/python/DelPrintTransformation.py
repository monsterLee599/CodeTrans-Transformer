from Node import Node
from AstToTree import *

#we will delete the print statement in this transformation
#notice that print is not same in python2.x and python3.x

def DelPrint(tree_root_node):
    print_list=FindPrint(tree_root_node)
    if len(print_list)==0:
        return 0
    else:
        for i in range(0,len(print_list)):
            ProcessPrint(print_list[i])

    #generate the new code
    code=TreeToTextPy(tree_root_node)
    return code

#if the code has print, we will return true,else we will return false
#para: node of te tree generated from ast
#return : true/false
def IsPrint(node):
    # python2.x
    if node.type=='print_statement':
        return True
    #python3.x
    elif node.type=='call' and node.children[0].text=='print':
        return True
    else:
        if len(node.children)!=0:
            for child in node.children:
                result=IsPrint(child)
                if result==True:
                    return True
            return False
        else:
            return False


#find and return the list of print
#param: node of the tree generated from ast
#return: the list of print statement/method
def FindPrint(node):
    print_list=[]
    if node.type=='print_statement':
        print_list.append(node)
    elif node.type=='call' and node.children[0].text=='print':
        print_list.append(node)

    if len(node.children)!=0:
        for child in node.children:
            result=FindPrint(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    print_list.append(result[i])
    else:
        pass

    return print_list

#delf the print statement/method
#param:node of the tree generated from ast
#return :None
def ProcessPrint(node):
    #create the pass statement
    pass_statement_node=Node()
    pass_statement_node.type='pass_statement'

    pass_node=Node()
    pass_node.type='pass'
    pass_node.text='pass'
    pass_node.parent=pass_statement_node
    pass_statement_node.addchild(pass_node)

    #python3.x
    if node.type=='call':
        node_index=node.parent.parent.children.index(node.parent)
        node.parent.parent.children[node_index]=pass_statement_node
        pass_statement_node.parent=node.parent.parent
        # reset the level
        ResetLevelPY(pass_statement_node)

    #python2.x
    elif node.type=='print_statement':
        node_index=node.parent.children.index(node)
        node.parent.children[node_index]=pass_statement_node
        pass_statement_node.parent=node.parent
        #reset the level
        ResetLevelPY(pass_statement_node)


