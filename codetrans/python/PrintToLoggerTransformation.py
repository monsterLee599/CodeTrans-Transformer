from Node import Node
from AstToTree import *

# we will convert print statement/function into logger.info
#param: the root node of the tree generated from ast
def PrintToLogger(tree_root_node):
    result=FindPrint(tree_root_node)
    if len(result)==0:
        return 0
    else:
        ImportPprint(tree_root_node)
        for node in result:
            ProcessPrint(node)

    code=TreeToTextPy(tree_root_node)
    return code

#if the source code has print statement/method, we shoule return true, else,we return false
#
def IsPrint(node):
    if (node.text=='print' and node.type=='print') or (node.type=='identifier' and node.text=='print' and node.parent.type=='call'):
        return True
    if len(node.children)!=0:
        for child in node.children:
            result=IsPrint(child)
            if result==True:
                return True
        return False

    else:
        return False

def FindPrint(node):
    print_list=[]
    #python2.x and python3.x
    #if (node.type=='print' and node.text=='print') or (node.type=='identifier' and node.text=='print' and node.parent.type=='call'):
        #print_list.append(node)
    if node.type=='identifier' and node.text=='print' and node.parent.type=='call':
        print_list.append(node)
    elif node.type=='print' and node.text=='print':
        judge=True
        for child in node.parent.children:
            if child.type=='chevron':
                judge=False
        if judge==True:
            print_list.append(node)
        else:
            pass

    #internal node
    if len(node.children)!=0:
        for child in node.children:
            result=FindPrint(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    print_list.append(result[i])
    else:
        pass

    return print_list

#we will convert print to pprint.pprint function, the pprint module is the same in both python2.x and python3.x
#first we will import pprint library ,then we use pprint.pprint() instead of print
#for example: print('hello world')
#the new code is :
#import pprint
#pprint.pprint('hello world')

def ImportPprint(tree_root_node):
    # we first import pprint library
    import_statement_node = Node()
    import_statement_node.type = 'import_statement'
    import_statement_node.parent = tree_root_node
    tree_root_node.children.insert(0, import_statement_node)

    import_node = Node()
    import_node.type = 'import'
    import_node.text = 'import'
    import_node.parent = import_statement_node
    import_statement_node.addchild(import_node)

    dotted_name_node = Node()
    dotted_name_node.type = 'dotted_name'
    dotted_name_node.parent = import_statement_node
    import_statement_node.addchild(dotted_name_node)

    method_name_node = Node()
    method_name_node.type = 'identifier'
    method_name_node.text = 'pprint'
    method_name_node.parent = dotted_name_node
    dotted_name_node.addchild(method_name_node)
    ResetLevelPY(import_statement_node)

def ProcessPrint(node):

    #print method/statement -> pprint.pprint() method
    #python3.x
    if node.type=='identifier':
        parent=node.parent
        index=parent.children.index(node)

        attribute_node=Node()
        attribute_node.type='attribute'
        attribute_node.parent=parent
        parent.children[index]=attribute_node

        module_name_node=Node()
        module_name_node.type='identifier'
        module_name_node.text='pprint'
        module_name_node.parent=attribute_node
        attribute_node.addchild(module_name_node)

        dot_node=Node()
        dot_node.type='.'
        dot_node.text='.'
        dot_node.parent=attribute_node
        attribute_node.addchild(dot_node)

        method_name_node=Node()
        method_name_node.type='identifier'
        method_name_node.text='pprint'
        method_name_node.parent=attribute_node
        attribute_node.addchild(method_name_node)

        #reset the level
        ResetLevelPY(parent)


    #python2.x
    elif node.type=='print':
        parent=node.parent.parent
        index=parent.children.index(node.parent)

        expression_statement_node=Node()
        expression_statement_node.type='expression_statement'
        expression_statement_node.parent=parent
        parent.children[index]=expression_statement_node

        call_node=Node()
        call_node.type='call'
        call_node.parent=expression_statement_node
        expression_statement_node.addchild(call_node)

        attribute_node=Node()
        attribute_node.type='attribute'
        attribute_node.parent=call_node
        call_node.addchild(attribute_node)

        module_name_node=Node()
        module_name_node.type='identifier'
        module_name_node.text='pprint'
        module_name_node.parent=attribute_node
        attribute_node.addchild(module_name_node)

        dot_node=Node()
        dot_node.type='.'
        dot_node.text='.'
        dot_node.parent=attribute_node
        attribute_node.addchild(dot_node)

        method_name_node=Node()
        method_name_node.type='identifier'
        method_name_node.text='pprint'
        method_name_node.parent=attribute_node
        attribute_node.addchild(method_name_node)

        argument_list_node=Node()
        argument_list_node.type='argument_list'
        argument_list_node.parent=call_node
        call_node.addchild(argument_list_node)

        left_parenthesis_node=Node()
        left_parenthesis_node.type='('
        left_parenthesis_node.text='('
        left_parenthesis_node.parent=argument_list_node
        argument_list_node.addchild(left_parenthesis_node)

        # add param
        for i in range(1,len(node.parent.children)):
            node.parent.children[i].parent=argument_list_node
            argument_list_node.addchild(node.parent.children[i])

        right_parenthesis_node=Node()
        right_parenthesis_node.type=')'
        right_parenthesis_node.text=')'
        right_parenthesis_node.parent=argument_list_node
        argument_list_node.addchild(right_parenthesis_node)
        #reset the level
        ResetLevelPY(expression_statement_node)






