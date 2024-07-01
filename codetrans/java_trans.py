import os
import sys
import json
import argparse

sys.path.append('./scripts')

from GetParseTree import *
from Node import Node
from AstToTree import *
from GetAST import *
from java.AddCommentTransformation.AddCommentTransformation import *
from modules import FindTypeNode
from java.PrintlnToPrintTransformation import *
from java.ArgumentedAssignmentTransformation import *
from java.UnaryTransformation import *
from java.ComparisonOperatorTransformation import *
from java.ElifToElseIfTransformation import *
from java.IfStatementTransformation import *
from java.RenameTransformation.FunctionRenameTransformation import *
from java.RenameTransformation.VariableRenameTransformation import *
from java.IntegralTypeTransformation import *
from java.FloatingPointTransformation import *
from java.DelCurlyBraceTransformation import *
from java.AddCurlyBraceTransformation import *
from java.ReturnTransformation import *
from java.VariableDeclarationTransformation import *
from java.ForTransformation.MoveOutTransformation import *
from java.ForTransformation.MoveInTransformation import *
from java.LogicalNotTransformation import *
from java.ImportTransformation.ImportTransformation import *
from java.AddReturnTransformation import *
from java.DelPrintlnTransformation import *
from java.WhileToForTransformation import *
from java.ForToWhileTransformation import *
from java.AddJunkCodeTransformation import *
from java.RemoveVariableTransformation import *
from java.IfNotTransformation import *
from java.ElseIfToElifTransformation import *
from java.RenameTransformation.FunctionRename_v2 import *
from java.DelCommentTransformation import *








# preocess and get tree
def Gen_tree(code_dict, language='java'):
    ast_root_node_dict = dict()
    tree_root_node_dict = dict()

    for name_i in code_dict.keys():
        code_i = code_dict[name_i]
        # print(code_i)
        ast_root_node=generateASt(code_i,language)
        byte_code=ByteCode(code_i)
        tree_root_node=getTreePY(ast_root_node,byte_code)

        ast_root_node_dict[name_i] = ast_root_node
        tree_root_node_dict[name_i] = tree_root_node

        # break
        # non_code = DelComment(tree_root_node)
        # # print(non_code)
        # ast_root_node_non=generateASt(non_code,language)
        # byte_code_non=ByteCode(non_code)
        # tree_root_node_non=getTreePY(ast_root_node_non,byte_code_non)

        # ast_root_node_dict[name_i] = ast_root_node_non
        # tree_root_node_dict[name_i] = tree_root_node_non

    return ast_root_node_dict, tree_root_node_dict



def Import_Transformation(tree_root_node_dict, insert_num=5):
    trans_code_dict = dict()
    parse_code_dict = dict()
    num = 0

    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code = ImportLibrary(tree_root_node, insert_num)
        num += 1
        trans_code_dict[name_i] = trans_code
        parse_code = parse_file(trans_code)
        parse_code_dict[name_i] = parse_code

    print('the number of ImportLibrary_Transformation is',num) 
    return trans_code_dict, parse_code_dict



def UnaryToBinary_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=UnaryToBinary(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of UnaryToBinary_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def FloatingPoint_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        result=FloatingTransformation(tree_root_node)
        if result==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = result
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIftoElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of FloatingPoint_Transformation is',number)    
    return trans_code_dict

def IfStatement_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=IfStatement(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of IfStatement_Transformation is',number)   
    return trans_code_dict, parse_code_dict

def Comparison_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ComparisonTransformation(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of Comparison_Transformation is ',number)    
    return trans_code_dict,parse_code_dict

def Return_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ReturnTransformation(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of Return_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def VariableDeclaration_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=VariableDecl(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of VariableDeclaration_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def MoveIn_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=MoveInVariable(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of MoveIn_Transformation is ',number)
    return trans_code_dict, parse_code_dict

def MoveOut_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=MoveOutVariable(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of MoveOut_Transformation is ',number)    
    return trans_code_dict , parse_code_dict

def Integral_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=IntegralTransformation(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code

        
    print('number of Integral_Transformation is ',number)    
    return trans_code_dict, trans_code_dict

def Floating_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=FloatingTransformation(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of Floating_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def LogicalNot_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=LogicalNot(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of LogicalNot_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def AddCurlyBrace_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=AddCurlyBrace(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of AddCurlyBrace_Transformation is ',number)    
    return trans_code_dict,parse_code_dict

def DelCurlyBrace_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=DelCurlyBrace(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of DelCurlyBrace_Transformation is ',number)    
    return trans_code_dict, trans_code_dict

def AugmentedAssignment_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ArgumentedAssinment(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('number of AugmentedAssignment_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def ForToWhile_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ForToWhile(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of ForToWhile_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def WhileToFor_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=WhileToFor(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of WhileToFor_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def AddReturn_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=AddReturn(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIftoElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of AddReturn_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def DelPrint_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=DelPrintln(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIftoElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of DelPrint_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def ElifToElseIf_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElifToElseIf(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code

    print('the number of ElifToElseIf_Transformation is ',number)    
    return trans_code_dict, parse_code_dict

def ElseIfToElif_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIftoElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of ElseIfToElif_Transformation is ',number)    
    return trans_code_dict, parse_code_dict



def AddJunkCode_Transformation(tree_root_node_dict, insert_num=3, insert_loc=0):
    # 0 is the random mode: we will add junk code randomly;
    # 1 is the head mode: we will add junk code at the start of the code;
    # 2 is the tail mode: we will add the junk code at the end of the code
    trans_code_dict = dict()
    parse_code_dict = dict()
    num = 0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=AddJunkCode(tree_root_node,insert_num,insert_loc)
        num += 1
        trans_code_dict[name_i] = trans_code
        parse_code = parse_file(trans_code)
        parse_code_dict[name_i] = parse_code
    print('the number of AddJunkCode_Transformation is',num) 
    return trans_code_dict,parse_code_dict





def FuncRename_Transformation(tree_root_node_dict, rename_pattern='func_',max_num=70):
    trans_code_dict = dict()
    parse_code_dict = dict()
    rename_list = list()
    number=0
    for i in range(0,max_num):
        rename_list.append(rename_pattern + str(i))
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        rename_code, _ = FunctionRename(tree_root_node,rename_list)
        if rename_code==0:
            pass
        else:
            number += 1
            trans_code_dict[name_i] = rename_code
            parse_code = parse_file(rename_code)
            parse_code_dict[name_i] = parse_code
    print('the number of FuncRename_Transformation is',number) 
    return trans_code_dict, parse_code_dict



# another approach
# def FuncRename_Transformation(tree_root_node_dict):
#     trans_code_dict = dict()

#     for name_i in tree_root_node_dict.keys():
#         code = tree_root_node_dict[name_i]
#         try:
#             methd_name = Extract_java_method_names(code)[0]
#         except javalang.parser.JavaSyntaxError:
#             methd_name = 'f_gold'
#             print("JavaSyntaxError: %s"  % name_i)
            
#         rename_code = code.replace(methd_name, 'func_0')
#         trans_code_dict[name_i] = rename_code
#     return trans_code_dict


def VariableRename_Transformation(tree_root_node_dict, rename_pattern='var_',max_num=70):
    trans_code_dict = dict()
    parse_code_dict = dict()
    rename_list = list()
    number=0
    for i in range(0,max_num):
        rename_list.append(rename_pattern + str(i))

    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        rename_code, _ = VariableRename(tree_root_node,rename_list)
        if rename_code==0:
            pass
        else:
            number += 1
            trans_code_dict[name_i] = rename_code
            parse_code = parse_file(rename_code)
            parse_code_dict[name_i] = parse_code
            
    print('the number of VariableRename_Transformation is',number)
    return trans_code_dict, parse_code_dict


def PrintlnToPrint_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=PrintlnToPrint(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of PrintlnToPrint_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def IfNot_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=IfNotTransformation(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of IfNot_Transformation is',number)    
    return trans_code_dict, parse_code_dict





def RemoveVariable_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=RemoveUnusedVariable(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of RemoveVariable_Transformation is',number) 
    return trans_code_dict , parse_code_dict

    # another approach 
    # trans_code_dict = dict()
    # number = 0  # This will count how many methods had unused variables removed

    # for name_i, java_code in tree_root_node_dict.items():
    #     wrapped_code = 'public class MockClass {' + java_code + '}'
    #     tree = javalang.parse.parse(wrapped_code)
    #     to_remove = []

    #     # Track the usage of variables
    #     used_variables = set()
    #     for _, node in tree.filter(javalang.tree.MemberReference):
    #         used_variables.add(node.member)

    #     # Identify variable declarations that are not used
    #     for _, node in tree.filter(javalang.tree.LocalVariableDeclaration):
    #         for declarator in node.declarators:
    #             if declarator.name not in used_variables:
    #                 to_remove.append(declarator)

    #     if to_remove:  # If there are variables to remove, increment the count
    #         number += 1

    #         # Remove unused variables by reconstructing the code
    #         lines = java_code.split('\n')
    #         for declarator in to_remove:
    #             # Find the line number of the declaration and set it to an empty string
    #             position = declarator.position
    #             if position:
    #                 line_index = position.line - 2  # Adjusting line number because of the class wrapping
    #                 lines[line_index] = ""

    #         # Reconstruct the code and remove empty lines
    #         new_code = '\n'.join(line for line in lines if line.strip())
    #         # print(new_code)
    #         trans_code_dict[name_i] = new_code

    # # Print the number of methods that had unused variables removed
    # print('The number of methods with removed unused variables is:', number)    
    # return trans_code_dict





def IntegralType_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        result=IntegralTransformation(tree_root_node)
        if result==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = result
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        # print(name_i)
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIftoElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of IntegralType_Transformation is',number)    
    return trans_code_dict



def Load_data(filename):
    with open(filename, 'r') as file:
        data_dict = {}
        for line in file:
            line_dict = json.loads(line.strip())
            data_dict.update(line_dict)
    return data_dict


def parse_file(non_code, language='java'):

    non_ast_root_node = generateASt(non_code, language)
    non_byte_code = ByteCode(non_code)
    non_tree_root_node = getTreePY(non_ast_root_node,non_byte_code)
    parse_code = parse_java_file(non_tree_root_node)

    return parse_code

def Save_dict_to_json(save_dir, language, data, file_name):

    save_data_dir = os.path.join(save_dir, language)

    os.makedirs(save_data_dir, exist_ok=True)

    save_name = os.path.join(save_data_dir, f'{file_name}.json')
    with open(save_name, 'w', encoding='utf-8') as json_file:
        for key, value in data.items():

            if file_name.endswith("parse"):
                json_file.write(value + '\n')
            else:
                json.dump({key: value}, json_file)
                json_file.write('\n')





def Process_code_transformation(args, tree_root_node_dict):
    def save_transformation(trans_code_dict, parse_code_dict, save_name):
        Save_dict_to_json(args.save_dir, args.language, trans_code_dict, save_name)
        Save_dict_to_json(args.save_dir, args.language, parse_code_dict, f'{save_name}_parse')

    transformations = {
        'B-1': ('ForToWhile_Transformation', 'fortowhile'),
        'B-2': ('WhileToFor_Transformation', 'whiletofor'),
        'B-3': ('ElifToElseIf_Transformation', 'eliftoelseif'),
        'B-4': ('ElseIfToElif_Transformation', 'elseiftoelif'),
        'B-5': ('IfNot_Transformation', 'ifnot'),
        'B-6': ('IfStatement_Transformation', 'ifstatement'),
        'B-7': ('CreateFunction_Transformation', 'ceratefunction'),
        'ID-2': ('AddJunkCode_Transformation', 'addjunkcode'), # it
        'ID-3': ('AddReturn_Transformation', 'addreturn'),
        'ID-4': ('Import_Transformation', 'importlibrary'), 
        'ID-5': ('DelComment', 'deletecomment'), 
        'ID-6': ('DelPrint_Transformation', 'delprintln'),
        'ID-7': ('RemoveVariable_Transformation', 'removevariable'), #
        'GS-1': ('Return_Transformation', 'return'),
        'GS-2': ('MoveIn_Transformation', 'formovein'),
        'GS-3': ('MoveOut_Transformation', 'formoveout'),
        'GS-4': ('VariableDeclaration_Transformation', 'variabledeclaration'),
        'GS-5': ('LogicalNot_Transformation', 'logicalnot'),
        'GS-6': ('Comparison_Transformation', 'comparison'),
        'GS-7': ('AugmentedAssignment_Transformation', 'augmentedassignment'),
        'GS-8': ('UnaryToBinary_Transformation', 'unary'),
        'GS-9': ('AddCurlyBrace_Transformation', 'addcurlybrace'),
        'GS-10': ('DelCurlyBrace_Transformation', 'delcurlybrace'),
        'GT-3': ('Floating_Transformation', 'inttofloat'),
        'GT-4': ('Integral_Transformation', 'inttolong'), 
        'GT-6': ('PrintlnToPrint_Transformation', 'printtopprint'),
        'I-1': ('FuncRename_Transformation', 'function_rename'),
        'I-2': ('VariableRename_Transformation', 'variable_rename')
    }


    if args.code_trans in transformations:
        transformation_function_name, save_name = transformations[args.code_trans]
        trans_code_dict, parse_code_dict = globals()[transformation_function_name](tree_root_node_dict)
        save_transformation(trans_code_dict, parse_code_dict, save_name)




if __name__ == "__main__":


    parser = argparse.ArgumentParser(description="Extract CSN code based on language and info type.")
    parser.add_argument('--data_dir', type=str, default='./dataset/csn_data')
    parser.add_argument('--language', type=str, choices=['java', 'python'], default='java', help='The programming language to use (default: java)')
    parser.add_argument('--info', type=str, choices=['train', 'valid', 'test'], default='test', help='The type of information to extract (default: test)')
    parser.add_argument('--save_dir', type=str, default='./dataset/trans_data')
    parser.add_argument('--code_trans', type=str, required=True, help='Code translation ID')
    
    args = parser.parse_args()
    

    trans_data = os.path.join(args.data_dir, args.language, args.info, 'code_test.json')
    trans_code_dict = Load_data(trans_data)
    # print(trans_code_dict['0'])
    print("extract data done")

    ast_root_node_dict, tree_root_node_dict = Gen_tree(trans_code_dict, language='java')
    print("generate tree done")



    Process_code_transformation(args, tree_root_node_dict)

