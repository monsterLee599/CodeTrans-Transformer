from tree_sitter import Parser
from tree_sitter import Tree
from tree_sitter import Language

Language.build_library(
    'build/my-languages.so',
    [
        'build/tree-sitter-cpp',
        'build/tree-sitter-python',
        'build/tree-sitter-java'
    ]
)

CPP_LANGUAGE=Language('build/my-languages.so','cpp')
JAVA_LANGUAGE=Language('build/my-languages.so','java')
PYTHON_LANGUAGE=Language('build/my-languages.so','python')


parser=Parser()

#useful
def CodeProcess(code):
    code_list=code.split('\n')
    return code_list


#language:python java cpp
def generateASt(code,language):
    if language=='java':
        parser.set_language(JAVA_LANGUAGE)
    elif language=='cpp':
        parser.set_language(CPP_LANGUAGE)
    elif language=='python':
        parser.set_language(PYTHON_LANGUAGE)
    else:
        print('--wrong langauge--')
        return 0
    tree=parser.parse(bytes(code,encoding='utf-8'))
    root_node=tree.root_node
    return root_node


#if error in source code
def ASTERROR(ast_root_node,boolean):
    if ast_root_node.type=='ERROR':
        boolean=False
        return boolean
    for child in ast_root_node.children:
        if child.type=='ERROR':
            boolean=False
            return boolean
        elif len(child.children)!=0:
            boolean=ASTERROR(child,boolean)
        else:
            if ast_root_node.type=="ERROR":
                boolean=False
                return  boolean
    return boolean
