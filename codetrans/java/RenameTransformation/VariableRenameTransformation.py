# this method will rename the variable name
# we transform the code snippet, so it is hard to identifier class name and variable name,that is to say, sometimes, we may rename the class name

from AstToTree import *
from GetAST import *
from Node import Node
import json

# the function will rename the variable name and we will not rewrite the token store in keyword.json
# param: tree_root_node: the root node of tree generated from ast
#        rename_list: you must give us the variable name you want to change into
# return: code: the new code that rename the variable
#         rename_dict: { old_variable: new_variable }
def VariableRename(tree_root_node,rename_list):
    identifier_list=FindIdentifier(tree_root_node)
    variable_list=FindVariable(identifier_list)
    variable_no_keyword_list=VariableDelkeywords(variable_list)
    variable_name_list=[]

    for i in range(0,len(variable_no_keyword_list)):
        if variable_no_keyword_list[i].text not in variable_name_list:
            variable_name_list.append(variable_no_keyword_list[i].text)

    if len(variable_name_list)>len(rename_list):
        print('the length of rename_list must larger than number of variable')
        return 0
    else:
        rename_dict={}
        for i in range(0,len(variable_name_list)):
            if variable_name_list[i] not in rename_dict:
                rename_dict[variable_name_list[i]]=rename_list[i]

        for i in range(0,len(identifier_list)):
            if identifier_list[i].text not in rename_dict:
                pass
            else:
                identifier_list[i].text=rename_dict[identifier_list[i].text]

        code=TreeToTextJava(tree_root_node)
        return code,rename_dict


# find and return all the nodes which type is identifier
# param: tree_root_node: the root node of tree generated from ast
# return: the list of nodes which type is identifier
def FindIdentifier(tree_root_node):
    identifier_list = []

    if tree_root_node.type == 'identifier':
        identifier_list.append(tree_root_node)

    if len(tree_root_node.children) != 0:
        for child in tree_root_node.children:
            result = FindIdentifier(child)
            if len(result) != 0:
                for i in range(0, len(result)):
                    identifier_list.append(result[i])

    else:
        pass

    return identifier_list

# this will find all the variable from identifier list
# param: identifier_list: the list of node which type is identifier
# return : list of nodes, which text is variable name
def FindVariable(identifier_list):
    variable_list = []
    for i in range(0, len(identifier_list)):
        if identifier_list[i].parent.type != 'method_declaration' and identifier_list[
            i].parent.type != 'method_invocation' and identifier_list[i].parent.type != 'class_declaration':
            variable_list.append(identifier_list[i])
        else:
            pass
    return variable_list

# we if the function name in keywords, we will not rename it, so we only select the other variable
# param: the list of variable name
# return: the list of variable name without keywords
def VariableDelkeywords(variable_list):
    with open('java/RenameTransformation/keywords.json','r') as f:
        keywords_list=json.load(f)

    variable_no_keyword_list=[]
    for i in range(0,len(variable_list)):
        if variable_list[i].text in keywords_list:
            pass
        else:
            variable_no_keyword_list.append(variable_list[i])

    return variable_no_keyword_list

