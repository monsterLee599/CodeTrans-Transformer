#in this file, we wil convert println function to print function
#System.out.println -> System.out.print
from Node import Node
from AstToTree import *

def PrintlnToPrint(tree_root_node):
    result=FindPrintln(tree_root_node)
    if len(result)==0:
        return 0
    else:
        for i in range(0,len(result)):
            ProcessPrint(result[i])

    code=TreeToTextJava(tree_root_node)
    return code

#if the code has println function, if it has println function, return true, else return false
#param: the root node of the tree geerated from the ast
#return: True/False
def IsPrintln(tree_root_node):
    if tree_root_node.type=='identifier' and tree_root_node.text=='println':
        return True
    elif len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsPrintln(child)
            if result==True:
                return True

        return False
    else:
        return False

#return the list of println function
#param: the root node of the tree generated from the ast
#return: the list of the println function
def FindPrintln(tree_root_node):
    println_list=[]
    if tree_root_node.type=='identifier' and tree_root_node.text=='println' and tree_root_node.parent!=None:
        if tree_root_node.parent.type=='method_invocation':
            println_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindPrintln(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    println_list.append(result[i])

    else:
        pass

    return println_list

#process the println function println -> print
#param: the node of the ast which value is println
#return : None
def ProcessPrint(node):
    #we can easily convert println to print and then add "\n" at the end of the argument_list
    node.text='print'
    argument_list_index=node.parent.children.index(node)+1
    argument_list_node=node.parent.children[argument_list_index]

    # only have ( and )
    if len(argument_list_node.children)==2:
        enter_node=Node()
        enter_node.type='string_literal'
        enter_node.text='\"\\n\"'
        enter_node.parent=argument_list_node
        argument_list_node.children.insert(1,enter_node)

    #have argument, for example: System.out.println("hello world"); -> System.out.println("hello world"+"\n");
    else:
        arg_node=argument_list_node.children[len(argument_list_node.children)-2]
        binary_expression_node=Node()
        binary_expression_node.type='binary_expression'
        binary_expression_node.parent=argument_list_node
        argument_list_node.children[len(argument_list_node.children)-2]=binary_expression_node
        arg_node.parent=binary_expression_node
        binary_expression_node.addchild(arg_node)

        plus_node=Node()
        plus_node.type='+'
        plus_node.text='+'
        plus_node.parent=binary_expression_node
        binary_expression_node.addchild(plus_node)

        enter_node=Node()
        enter_node.type='string_literal'
        enter_node.text='\"\\n\"'
        enter_node.parent=binary_expression_node
        binary_expression_node.addchild(enter_node)



