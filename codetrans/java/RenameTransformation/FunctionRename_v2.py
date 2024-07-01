# this function will rename the function/method name
# but in this function, we only rename the class/function which type is declaration, if a method is called, we will ignore it
# for example:
# public int f(){
# int x=f2();
# return x;
# }
# we only rename method f, so the result is:
# public int func_1(){
# int x=f2();
# return x;
# }

from AstToTree import *
from GetAST import *
from Node import Node
import json

# this function will rename the function name
# param: tree_root_node: the root node of the tree generated from ast
#        rename_list: the new name, [func_1,func_2,...]
# return: code: the code that we rename the function name
#         rename_dict: the dict of old name and new name: {old1:new2,old2:new2,...}

def FunctionRename(tree_root_node,rename_list):
    identifier_list=FindIdentifier(tree_root_node)
    function_list=FindFunction(identifier_list)
    function_no_keyword_list=FunctionDelKeywords(function_list)
    functions_name_list=[]
    for i in range(0,len(function_no_keyword_list)):
        if function_no_keyword_list[i].text not in functions_name_list:
            functions_name_list.append(function_no_keyword_list[i].text)

    if len(rename_list)<len(functions_name_list):
        print('the length of rename list must larger than the number of function/class')
        return 0,{}

    elif len(functions_name_list)==0:
        return 0,{}

    else:
        rename_dict={}
        for i in range(0,len(functions_name_list)):
            if functions_name_list[i] not in rename_dict:
                rename_dict[functions_name_list[i]]=rename_list[i]

        for i in range(0,len(identifier_list)):
            if identifier_list[i].text in rename_dict:
                identifier_list[i].text=rename_dict[identifier_list[i].text]
            else:
                continue

    code=TreeToTextJava(tree_root_node)
    # if the length of rename dict is 0, it means we do not modifier the code
    return code,rename_dict


# find and return all the nodes which type is identifier
# param: tree_root_node: the root node of tree generated from ast
# return: the list of nodes which type is identifier
def FindIdentifier(tree_root_node):
    identifier_list=[]

    if tree_root_node.type=='identifier' or tree_root_node.type=='type_identifier':
        identifier_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindIdentifier(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    identifier_list.append(result[i])

    else:
        pass

    return identifier_list

# this function will find all the function from identifier list
# param: identifier_list: the list of node which type is identifier
# return: list of nodes, which text is function/class name
def FindFunction(identifier_list):
    function_list=[]
    for i in range(0,len(identifier_list)):
        if identifier_list[i].parent.type=='method_declaration' or identifier_list[i].parent.type=='class_declaration':
            function_list.append(identifier_list[i])
        else:
            pass
    return function_list

# we if the function name in keywords, we will not rename it, so we only select the other function
# param: the list of function name
# return: the list of function name without keywords
def FunctionDelKeywords(function_list):
    with open('java/RenameTransformation/keywords.json','r') as f:
        keywords_list=json.load(f)

    function_no_keyword_list=[]
    for i in range(0,len(function_list)):
        if function_list[i].text in keywords_list:
            continue
        else:
            function_no_keyword_list.append(function_list[i])

    return function_no_keyword_list
