# in this transformation, we will delete System.out.println("")/print("")
# because the print does not effect the code, so delete it is ok

from AstToTree import *
from Node import Node

# this is the main function of delete println/print transformation
# param: tree_root_node: the root node of the tree generated from ast
# return: the new code
def DelPrintln(tree_root_node):
    println_list=FindPrintln(tree_root_node)
    if len(println_list)==0:
        return 0
    else:
        for i in range(0,len(println_list)):
            ProcessPrintln(println_list[i])
        code=TreeToTextJava(tree_root_node)
        return code

# if the code has System.out.println()/System.out.print(), we will return true, else we will return false
# param: the root node of the ast generated from ast
# return: true/false
def IsPrintln(tree_root_node):
    if tree_root_node.type=='expression_statement' and tree_root_node.children[0].type=='method_invocation' and len(tree_root_node.children)==2:
        method_invocation=tree_root_node.children[0];
        if len(method_invocation.children)==4 and method_invocation.children[0].type=='field_access' and method_invocation.children[1].type=='.' and \
        method_invocation.children[2].type=='identifier' and(method_invocation.children[2].text=='println' or method_invocation.children[2].text=='print')\
        and method_invocation.children[3].type=='argument_list' :
            field_access=method_invocation.children[0]
            if len(field_access.children)==3 and (field_access.children[0].type=='identifier' and field_access.children[0].text=='System') and field_access.children[1].type=='.'\
            and (field_access.children[2].type=='identifier' and field_access.children[2].text=='out'):
                return True

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=IsPrintln(child)
            if result==True:
                return True
        return False

    else:
        return False

# find and all the println/print statement in the code
# param: tree_root_node: the root node of the tree generated from ast
# return: the list of println/print
def FindPrintln(tree_root_node):
    println_list=[]
    if tree_root_node.type == 'expression_statement' and tree_root_node.children[0].type == 'method_invocation' and len(
            tree_root_node.children) == 2:
        method_invocation = tree_root_node.children[0];
        if len(method_invocation.children) == 4 and method_invocation.children[0].type == 'field_access' and \
                method_invocation.children[1].type == '.' and \
                method_invocation.children[2].type == 'identifier' and (
                method_invocation.children[2].text == 'println' or method_invocation.children[2].text == 'print') \
                and method_invocation.children[3].type == 'argument_list':
            field_access = method_invocation.children[0]
            if len(field_access.children) == 3 and (
                    field_access.children[0].type == 'identifier' and field_access.children[0].text == 'System') and \
                    field_access.children[1].type == '.' \
                    and (field_access.children[2].type == 'identifier' and field_access.children[2].text == 'out'):
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

# we will use ';' to repalce 'System.out.println/print'
# param: println_node: tree node
# return: none
def ProcessPrintln(println_node):
    index=println_node.parent.children.index(println_node)
    semicolon=Node()
    semicolon.type=';'
    semicolon.text=';'
    semicolon.parent=println_node.parent
    println_node.parent.children[index]=semicolon
