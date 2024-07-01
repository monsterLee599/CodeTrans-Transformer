import json
from AstToTree import *
# get the keywords
# keywords=''

#param:tree_root_node: the root node of new geneated tree
#     rename_list: the list like [iden_1,iden_2,iden_3,...]
#return: rename_dict: dict like {original_iden1,iden_1,original_iden_2,iden_2}
#        code : the new code that the all the identifiers are repalced
def identifier_rename(tree_root_node,rename_list):
    result=getidenfifiers(tree_root_node)
    _,identifiers_list,identifiers_list_del=get_identifiers_no_keywords(result)
    if len(rename_list)<len(identifiers_list_del):
        print('-- length of rename_list must larger than the number of variables --')
        return 0
    else:
        rename_dict={}
        for i in range(0,len(identifiers_list_del)):
            if identifiers_list_del[i] not in rename_dict:
                rename_dict[identifiers_list_del[i]]=rename_list[i]

        # change the tree node.text
        for i in range(0,len(identifiers_list)):
            identifiers_list[i].text=rename_dict[identifiers_list[i].text]

        code=TreeToTextPy(tree_root_node)
        return rename_dict, code





# get the number of identifiers
# param: the root node of tree generated grom ast
# return: number of variables; the list of variables
def identifiers_number(tree_root_node):

    result=getidenfifiers(tree_root_node)
    number,identifiers_list,identifiers_list_del=get_identifiers_no_keywords(result)
    return number,identifiers_list_del


# get all identifiers
# param: root node of the tree generated from ast
# return: all the identifiers
def getidenfifiers(tree_root_node):
    if len(tree_root_node.children)!=0:
        variable_list=[]
        for child in tree_root_node.children:
            result=getidenfifiers(child)
            if type(result)==list:
                for i in range(0,len(result)):
                    variable_list.append(result[i])
            elif result==None:
                continue
            else:
                variable_list.append(result)

        return variable_list

    else:
        if tree_root_node.type=='identifier':
            return tree_root_node
        else:
            return None



#del keywords in the identifiers
#param: result: the identifiers include keywords
#return : count: the number of identifiers
#         identifiers_list: list of identifiers del keywords
#         identifiers_list_del: list of identifiers del keywords
def get_identifiers_no_keywords(result):
    with open('python/rename/keywords.json', 'r') as f:
        keywords = json.load(f)
        number = 0
        identifiers_list = []
        identifiers_list_del = []
        for i in range(0,len(result)):
            if result[i].text in keywords:
                continue
            else:
                identifiers_list.append(result[i])

        for i in range(0,len(identifiers_list)):
            if identifiers_list[i].text not in identifiers_list_del:
                identifiers_list_del.append(identifiers_list[i].text)
                number=number+1
            else:
                continue

        return number,identifiers_list,identifiers_list_del