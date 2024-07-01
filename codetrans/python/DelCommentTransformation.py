from Node import Node
from AstToTree import *
from GetAST import *

#delete comments in the source code
#param: tree_rootnode: root node of the tree generated from ast\
#return : comment_code : the new code without comments

def Del_Python_Comment(tree_root_node):
    comment_list=findcomment(tree_root_node)
    # print(comment_list)
    if len(comment_list)==0:
        return TreeToTextPy(tree_root_node)
    else:
        for i in range(0,len(comment_list)):
            comment_list[i].parent.children.remove(comment_list[i])

        comment_code=TreeToTextPy(tree_root_node)

        return comment_code


# def DelComment(code):
    
#     byte_code=ByteCode(code)
#     ast_root_node=generateASt(code,'python')
#     tree_root_node=getTreePY(ast_root_node,byte_code)
#     comment_list=findcomment(tree_root_node)
#     if len(comment_list)==0:
#         return 0
#     else:
#         for i in range(0,len(comment_list)):
#             comment_list[i].parent.children.remove(comment_list[i])

#         comment_code=TreeToTextPy(tree_root_node)

#         return comment_code

#get all the comments node and det them
#param: the node of tree

# def findcomment(node):
#     comment_list=[]

#     if node.type=='comment':
#         comment_list.append(node)
#     elif node.type=='expression_statement' and len(node.children)==1 and node.children[0].type=='string' and len(node.parent.children)>1:
#         text=node.children[0].text

#         if len(text)>=6:
#             #because in tree-sitter the '''...''' and """...""" is not parsered to comment, so we should delete it also
#             judge=text[0]+text[1]+text[2]+text[len(text)-3]+text[len(text)-2]+text[len(text)-1]
#             #print(judge)
#             if judge=='""""""' or judge=="''''''" or judge == 'r""""""':
#                 comment_list.append(node)

#     #internal node
#     if len(node.children)!=0:
#         for child in node.children:
#             result=findcomment(child)
#             if len(result)!=0:
#                 for i in range(0,len(result)):
#                     comment_list.append(result[i])
#     #leaf node
#     else:
#         pass

#     return comment_list



def findcomment(node):
    comment_list = []

    if node.type == 'comment':
        comment_list.append(node)
    elif node.type == 'expression_statement' and len(node.children) == 1 and node.children[0].type == 'string' and len(node.parent.children) > 1:
        text = node.children[0].text

        if (text.startswith('"""') and text.endswith('"""')) or (text.startswith("'''") and text.endswith("'''")):
            comment_list.append(node)
        elif (text.startswith('r"""') and text.endswith('"""')) or (text.startswith("r'''") and text.endswith("'''")) or \
             (text.startswith('R"""') and text.endswith('"""')) or (text.startswith("R'''") and text.endswith("'''")):
            comment_list.append(node)
        elif (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
            comment_list.append(node)
        elif (text.startswith('r"') and text.endswith('"')) or (text.startswith("r'") and text.endswith("'")) or \
             (text.startswith('R"') and text.endswith('"')) or (text.startswith("R'") and text.endswith("'")):
            comment_list.append(node)
        elif (text.startswith('u"""') and text.endswith('"""')) or (text.startswith("u'''") and text.endswith("'''")) or \
             (text.startswith('U"""') and text.endswith('"""')) or (text.startswith("U'''") and text.endswith("'''")):
            comment_list.append(node)
        elif (text.startswith('b"""') and text.endswith('"""')) or (text.startswith("b'''") and text.endswith("'''")) or \
             (text.startswith('B"""') and text.endswith('"""')) or (text.startswith("B'''") and text.endswith("'''")):
            comment_list.append(node)
        elif (text.startswith('b"') and text.endswith('"')) or (text.startswith("b'") and text.endswith("'")) or \
             (text.startswith('B"') and text.endswith('"')) or (text.startswith("B'") and text.endswith("'")):
            comment_list.append(node)

    if len(node.children) != 0:
        for child in node.children:
            result = findcomment(child)
            if result:
                comment_list.extend(result)
    return comment_list
