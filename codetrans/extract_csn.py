import os
import sys
import json
import argparse
import ast

sys.path.append('./scripts')

from GetAST import *
from AstToTree import *
from python.DelCommentTransformation import *
from java.DelCommentTransformation import *
from GetParseTree import *


class PrintCalculatorVisitor(ast.NodeVisitor):
    def __init__(self):
        self.contains_calculation = False

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            for arg in node.args:
                if self.is_calculating(arg):
                    self.contains_calculation = True
        self.generic_visit(node)

    def is_calculating(self, node):

        if isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Call)):
            return True
        if isinstance(node, ast.BoolOp):
            return any(self.is_calculating(value) for value in node.values)
        if isinstance(node, ast.Compare):
            return any(self.is_calculating(comp) for comp in node.comparators)
        return False

def contains_print_calculation(code):
    try:
        tree = ast.parse(code)
        visitor = PrintCalculatorVisitor()
        visitor.visit(tree)
        return visitor.contains_calculation
    except SyntaxError:
        return False





# Process and get tree
def Process_python(code_dict, func_dict, language='python'):
    non_code_dict = {}
    parse_dict = {}
    number = 0
    for name_i, code_i in code_dict.items():
        # print("=================")
        # print(code_i)
        ast_root_node = generateASt(code_i, language)
        byte_code = ByteCode(code_i)
        tree_root_node = getTreePY(ast_root_node, byte_code)
        non_code = Del_Python_Comment(tree_root_node).strip()

        # 157 code in python are python2 format, in our paper we have converted them into python3 in data process
        # this repo directly uses original codesearchnet dataset, so we filter them
        try:
            parse_code = parse_py_file(non_code)
            non_code_dict[name_i] = non_code
            parse_dict[name_i] = parse_code
            number += 1
            # print("========")
            # print(non_code)
            # print(parse_code)
            # break

        except SyntaxError:
            pass
            # break
    # print(number)
    return non_code_dict, parse_dict



def Process_java(code_dict, func_dict, language='java'):
    non_code_dict = {}
    parse_dict = {}
    number = 0
    for name_i, code_i in code_dict.items():
        # print("=================")
        # print(code_i)
        class_name = func_dict[name_i].split('.')[0]

        java_code = 'public class '+class_name+ '{\n'+ code_i + '\n}'

        ast_root_node = generateASt(java_code, language)
        byte_code = ByteCode(java_code)
        tree_root_node = getTreePY(ast_root_node, byte_code)

        # if no comment, it will return 0
        try :
            non_code = Del_Java_Comment(tree_root_node).strip()
            # print(non_code)

        except AttributeError:
            non_code = java_code
            # print(non_code)

        non_ast_root_node = generateASt(non_code, language)
        non_byte_code = ByteCode(non_code)
        non_tree_root_node = getTreePY(non_ast_root_node,non_byte_code)

        parse_code = parse_java_file(non_tree_root_node)
        # print(parse_code)
            
        

        non_code_dict[name_i] = non_code
        parse_dict[name_i] = parse_code
        number += 1


    # print(number)
    return non_code_dict, parse_dict




def extract_csn_code(language, info):
    input_file = os.path.join('./dataset/CodeSearchNet', language, f'{info}.jsonl')
    code_dict = {}
    func_dict = {}
    text_dict = {}
    path_dict = {}

    with open(input_file, encoding="utf-8") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            js = json.loads(line)
            js.setdefault('idx', idx)

            func_name = js['func_name']
            func_dict[idx] = func_name

            code = js['code']
            code_dict[idx] = code

            nl = ' '.join(js['docstring_tokens']).replace('\n', '')
            text_dict[idx] = nl

            path = js['path']
            path_dict[idx] = path




    return code_dict, text_dict, path_dict, func_dict

def save_data(language, info, data, file_name, data_type='text'):
    save_data_dir = os.path.join('./dataset/csn_data', language, info)
    os.makedirs(save_data_dir, exist_ok=True)

    if data_type == 'text':
        save_name = os.path.join(save_data_dir, f'{file_name}_{info}.txt')
        with open(save_name, 'w', encoding="utf-8") as file:
            for key, value in data.items():
                file.write(value + '\n')

    elif data_type == 'json':
        save_name = os.path.join(save_data_dir, f'{file_name}_{info}.json')
        with open(save_name, 'w', encoding='utf-8') as json_file:
            for key, value in data.items():
                if file_name.startswith("parse"):
                    json_file.write(value + '\n')
                else:
                    json.dump({key: value}, json_file)
                    json_file.write('\n')
 
def filter_dict(original_dict, refer_dict):
    filtered_dict = {key: value for key, value in original_dict.items() if key in refer_dict}
    return filtered_dict






if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract CSN code based on language and info type.")
    parser.add_argument('--language', type=str, choices=['java', 'python'], default='python', help='The programming language to use (default: python)')
    parser.add_argument('--info', type=str, choices=['train', 'valid', 'test'], default='test', help='The type of information to extract (default: test)')
    
    args = parser.parse_args()

    code_dict, text_dict, path_dict, func_dict = extract_csn_code(args.language, args.info)

    if args.language == 'java':
        Process_code = Process_java
    else :
        Process_code = Process_python


    non_code_dict, parse_dict = Process_code(code_dict, func_dict, language=args.language)

    text_dict = filter_dict(text_dict, non_code_dict)
    path_dict = filter_dict(path_dict, non_code_dict)


    save_data(args.language, args.info, text_dict, "target")
    save_data(args.language, args.info, path_dict, "file_path")
    save_data(args.language, args.info, non_code_dict, "code", data_type='json')
    save_data(args.language, args.info, parse_dict, "parse", data_type='json')

