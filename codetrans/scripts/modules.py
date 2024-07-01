from Node import Node
from AstToTree import *
from GetAST import *

#get value/text from the node
def GetASTNodeText(ast_node,code):
    code=code.split('\n')
    text=''
    if ast_node.start_point[0]==ast_node.end_point[0]:
        text=code[int(ast_node.start_point[0])][int(ast_node.start_point[1]):int(ast_node.end_point[1])]
    else:
        for i in range(int(ast_node.start_point[0]),int(ast_node.end_point[0])+1):
            if i==int(ast_node.start_point[0]):
                text=text+code[i][int(ast_node.start_point[1]):]
            elif i==int(ast_node.end_point[0]):
                text=text+code[i][:int(ast_node.end_point[1])]
            else:
                text=text+code[i][:]

    return text

#return the list of node according the node type
def FindTypeNode(ast_root_node,node_type):
    node_list=[]
    if ast_root_node.type==node_type:
        node_list.append(ast_root_node)

    if len(ast_root_node.children)!=0:
        for child in ast_root_node.children:
            result=FindTypeNode(child,node_type)
            if len(result)!=0:
                for i in range(0,len(result)):
                    node_list.append(result[i])
            else:
                continue
    else:
        pass

    return node_list