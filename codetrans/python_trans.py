import os
import sys
import json
import argparse

sys.path.append('./scripts')

from GetAST import *
from AstToTree import *
from python.rename.rename import *
from python.rename.FunctionRename_v2 import *
# from python.rename.FunctionRenameTransformation import *
from python.rename.VariableRenameTransformation import *
from python.ImportTransformation.ImportTransformation import *
from python.BoolToIntTransformation import *
from python.IntToBoolTransformation import *
from python.AddCommentTransformation.AddCommentTransformation import *
from python.DelCommentTransformation import *
from python.IfStatenemtTransformer import *
from python.LiteralTransformation import *
from python.ComparisonOperatorTransformer import  *
from python.AugmentedAssignmentTransformation import *
from python.ForToWhileTransformation import *
from python.LogicalNotTransformation import *
from python.AddReturnTransformation import *
from python.IntToFloatTransformation import *
from python.DelPrintTransformation import *
from python.ElifToElseIfTransformation import *
from python.ElseIfToEliftransformation import *
from python.AddJunkCodeTransformation import *
from python.IntToLongTransformation import *
from python.PrintToLoggerTransformation import *
from python.AugmentedAssignmentTransformation import *
from python.WhileToForTransformation import *
from python.BinaryOperatorTransformation import *
from python.CreateFunctionTransformation import *
from python.InputTransformation import *
from python.RemoveVariableTransformation import *
from python.IfNotTransformation import *

from GetParseTree import *







# preocess and get tree
def Gen_tree(code_dict, language='python'):
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

        break
        # non_code = DelComment(tree_root_node)
        # # print(non_code)
        # ast_root_node_non=generateASt(non_code,language)
        # byte_code_non=ByteCode(non_code)
        # tree_root_node_non=getTreePY(ast_root_node_non,byte_code_non)

        # ast_root_node_dict[name_i] = ast_root_node_non
        # tree_root_node_dict[name_i] = tree_root_node_non

    return ast_root_node_dict, tree_root_node_dict

def DelComment_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    num = 0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        non_code = DelComment(tree_root_node).strip()
        num += 1
        trans_code_dict[name_i] = trans_code
        parse_code = parse_file(trans_code)
        parse_code_dict[name_i] = parse_code

    print('the number of DelComment_Transformation is',num) 
    return trans_code_dict, parse_code_dict


def Import_Transformation(tree_root_node_dict, insert_num=5):
    trans_code_dict = dict()
    parse_code_dict = dict()
    num = 0

    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code = importlibrary(tree_root_node, insert_num)
        num += 1
        trans_code_dict[name_i] = trans_code
        parse_code = parse_file(trans_code)
        parse_code_dict[name_i] = parse_code

    print('the number of ImportLibrary_Transformation is',num) 
    return trans_code_dict, parse_code_dict

def Bool2Int_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        bool_int_code,bool_int_code_judge=BoolToInt(tree_root_node)

        if bool_int_code_judge==True:
            number=number+1
            trans_code_dict[name_i] = bool_int_code
            parse_code = parse_file(bool_int_code)
            parse_code_dict[name_i] = parse_code
    
    print('the number of Bool2Int_Transformation is',number)
    return trans_code_dict, parse_code_dict

def Int2Bool_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        int_bool_code, int_bool_code_judge=IntToBool(tree_root_node)
        if int_bool_code_judge==True:   
            number=number+1
            trans_code_dict[name_i] = int_bool_code
            parse_code = parse_file(int_bool_code)
            parse_code_dict[name_i] = parse_code
    print('the number of Int2Bool_Transformation is',number)
    return trans_code_dict, parse_code_dict

def IfStatement_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
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

def Literal2Variable_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=LiteralToVariable(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of RefactorReturn_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def Comparison_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ComparisonTransformer(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code


    print('the number of Comparison_Transformation is',number) 
    return trans_code_dict, parse_code_dict

def AugmentedAssignment_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=AugmentedAssignment(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of AugmentedAssignment_Transformation is',number)    
    return trans_code_dict, parse_code_dict


def LogicalNot_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=LogicalNot(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of LogicalNOT_Transformation is',number)    
    return trans_code_dict,parse_code_dict

def AddReturn_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=AddReturn(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of AddReturn_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def Int2Float_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=IntToFloat(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of Int2Float_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def DelPrint_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=DelPrint(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of DelPrint_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def ElifToElseIf_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElifToElseIf(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code

    print('the number of ElifToElseIf_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def ElseIfToElif_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=ElseIfToElif(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code

    print('the number of ElseIfToElif_Transformation is',number)    
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

def Input_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=InputToRawInput(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code

    print('the number of Input_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def IntToLong_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=IntToLong(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            # parse_code = parse_file(trans_code)
            # parse_code_dict[name_i] = parse_code
    print('the number of IntToLong_Transformation is',number)    
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

def PrintToLogger_Transformation(tree_root_node_dict):

    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=PrintToLogger(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of PrintToLogger_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def IfNot_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
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

def CreateFunction_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=CreateFunction(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of CreateFunction_Transformation is',number)    
    return trans_code_dict, parse_code_dict

def RemoveVariableTransformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code=RemoveUnusedVariable(tree_root_node)
        if trans_code==0:
            pass
        else:        
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code
    print('the number of RemoveVariableTransformation is',number)    
    return trans_code_dict, parse_code_dict



def Load_data(filename):
    with open(filename, 'r') as file:
        data_dict = {}
        for line in file:
            line_dict = json.loads(line.strip())
            data_dict.update(line_dict)
    return data_dict


def parse_file(code):

    return(parse_py_file(code))


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



def For2While_Transformation(tree_root_node_dict):
    trans_code_dict = dict()
    parse_code_dict = dict()
    number=0
    for name_i in tree_root_node_dict.keys():
        tree_root_node = tree_root_node_dict[name_i]
        trans_code = ForToWhile(tree_root_node)
        if trans_code:
            number=number+1
            trans_code_dict[name_i] = trans_code
            parse_code = parse_file(trans_code)
            parse_code_dict[name_i] = parse_code


    print('the number of For2While_Transformation is',number)    
    return trans_code_dict, parse_code_dict


def Process_code_transformation(args, tree_root_node_dict):
    def save_transformation(trans_code_dict, parse_code_dict, save_name):
        Save_dict_to_json(args.save_dir, args.language, trans_code_dict, save_name)
        Save_dict_to_json(args.save_dir, args.language, parse_code_dict, f'{save_name}_parse')

    transformations = {
        'B-1': ('For2While_Transformation', 'fortowhile'),
        'B-3': ('ElifToElseIf_Transformation', 'eliftoelseif'),
        'B-4': ('ElseIfToElif_Transformation', 'elseiftoelif'),
        'B-5': ('IfNot_Transformation', 'ifnot'),
        'B-6': ('IfStatement_Transformation', 'ifstatement'),
        'B-7': ('CreateFunction_Transformation', 'ceratefunction'),
        'ID-2': ('AddJunkCode_Transformation', 'addjunkcode'),
        'ID-3': ('AddReturn_Transformation', 'addreturn'),
        'ID-4': ('Import_Transformation', 'importlibrary'), 
        'ID-5': ('DelComment', 'deletecomment'), 
        'ID-6': ('DelPrint_Transformation', 'delprintln'),
        'ID-7': ('RemoveVariableTransformation', 'removevariable'),
        'GS-1': ('Literal2Variable_Transformation', 'return'),
        'GS-5': ('LogicalNot_Transformation', 'logicalnot'),
        'GS-6': ('Comparison_Transformation', 'comparison'),
        'GS-7': ('AugmentedAssignment_Transformation', 'augmentedassignment'),
        'GT-1': ('Bool2Int_Transformation', 'booltoint'), 
        'GT-2': ('Int2Bool_Transformation', 'inttobool'), 
        'GT-3': ('Int2Float_Transformation', 'inttofloat'),
        'GT-4': ('IntToLong_Transformation', 'inttolong'), # only can be parsed in Python 2.X
        'GT-5': ('Input_Transformation', 'inputtrans'),
        'GT-6': ('PrintToLogger_Transformation', 'printtopprint'),
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
    parser.add_argument('--language', type=str, choices=['java', 'python'], default='python', help='The programming language to use (default: python)')
    parser.add_argument('--info', type=str, choices=['train', 'valid', 'test'], default='test', help='The type of information to extract (default: test)')
    parser.add_argument('--save_dir', type=str, default='./dataset/trans_data')
    parser.add_argument('--code_trans', type=str, required=True, help='Code translation ID')

    args = parser.parse_args()
    

    trans_data = os.path.join(args.data_dir, args.language, args.info, 'code_test.json')
    trans_code_dict = Load_data(trans_data)
    print("extract data done")

    ast_root_node_dict, tree_root_node_dict = Gen_tree(trans_code_dict, language='python')
    print("generate tree done")


    Process_code_transformation(args, tree_root_node_dict)



