#create the new tree from ast created by tee-sitter and add the text

from Node import Node
from tree_sitter import Tree
from tree_sitter import Parser
from tree_sitter import Language



python_statement=['class_definition', 'decorated_definition', 'for_statement', 'function_definition', 'if_statement', 'try_statement', 'while_statement',
                  'with_statement', 'assert_statement', 'break_statement', 'continue_statement', 'delete_statement', 'exec_statement', 'expression_statement',
                  'future_import_statement', 'global_statement', 'import_from_statement', 'import_statement', 'nonlocal_statement', 'pass_statement',
                  'print_statement', 'raise_statement', 'return_statement', '_compound_statement', '_simple_statement', 'decorator', 'elif_clause', 'else_clause',
                  'except_clause', 'finally_clause', 'star_expressions', 'yield_statement', 'match_statement','exec']
python_addition=['comment']
#'identifier', 'operator_name','parameter_declaration','pointer_declarator',, 'init_declarator',
cpp_statement=['abstract_array_declarator', 'abstract_function_declarator', 'abstract_parenthesized_declarator', 'abstract_pointer_declarator', 'abstract_reference_declarator',
               'array_declarator', 'attributed_declarator', 'destructor_name', 'function_declarator', 'parenthesized_declarator', 'qualified_identifier',
               'reference_declarator', 'structured_binding_declarator', 'template_function', 'field_identifier', 'template_method', 'break_statement', 'case_statement', 'co_return_statement',
               'co_yield_statement', 'compound_statement', 'continue_statement', 'do_statement', 'expression_statement', 'for_range_loop', 'for_statement', 'goto_statement', 'if_statement',
               'labeled_statement', 'return_statement', 'switch_statement', 'throw_statement', 'try_statement', 'while_statement', 'type_identifier', 'alias_declaration', 'attribute_declaration',
               'attributed_statement', 'declaration', 'declaration_list', 'field_declaration', 'field_declaration_list', 'friend_declaration', 'new_declarator', 'optional_parameter_declaration',
               'optional_type_parameter_declaration',  'static_assert_declaration', 'template_declaration', 'template_template_parameter_declaration', 'type_parameter_declaration', 'using_declaration',
               'variadic_declarator', 'variadic_parameter_declaration', 'variadic_type_parameter_declaration', 'statement_identifier','preproc_if'
               ]


def ByteCode(code):
    code = code.split('\n')
    for i in range(0,len(code)):
        tmp=bytes(code[i],'utf-8')
        code[i]=tmp

    return code


def getTreePY(root_node,code):
    #print('-- generate tree --')
    tree_root_node=Node()
    tree_root_node.setLevel(0)
    tree_root_node.settype(root_node.type)

    def getText(code,start_point,end_point):
        text=bytes('','utf-8')
        if start_point[0]==end_point[0]:
            text=code[int(start_point[0])][int(start_point[1]):int(end_point[1])]
        else:
            for i in range(int(start_point[0]),int(end_point[0])+1):
                if i == int(start_point[0]):
                    text=text+code[i][int(start_point[1]):]
                elif i==int(end_point[0]):
                    text=text+code[i][:int(end_point[1])]
                else:
                    text=text+code[i][:]
        return text.decode('utf-8')

    def gettree(tree_node,ast_node,code,level):
        for child in ast_node.children:
            tree_child=Node()
            if child.type=='block':
                tree_child.setLevel(level+1)
            else:
                tree_child.setLevel(level)
            tree_child.settype(child.type)
            tree_child.setparent(tree_node)
            tree_node.addchild(tree_child)

            #type string
            if child.type=='string':
                text=getText(code,child.start_point,child.end_point)

                tree_child.settext(text)

            #internal node
            elif len(child.children)!=0:
                gettree(tree_child,child,code,tree_child.getlevel())

            #leaf node
            else:
                text=getText(code,child.start_point,child.end_point)
                tree_child.settext(text)


    gettree(tree_root_node,root_node,code,tree_root_node.getlevel())

    return tree_root_node


def TreeToTextPy(tree_root_node):

    def getoriginaltext(tree_root_node):
        text=[]
        #text=''
        for child in tree_root_node.children:
            if len(child.children)!=0:
                child_text=getoriginaltext(child)
                if child.type in python_statement:
                    #text=text+'\n'+'    '*(int(child.level))+child_text
                    text.append('\n')
                    text.append(' '*(int(child.level)*4))
                    for i in range(0,len(child_text)):
                        text.append(child_text[i])
                elif child.type in python_addition:
                    text.append('\n')
                    text.append(' ' * (int(child.level) * 4))
                    for i in range(0, len(child_text)):
                        text.append(child_text[i])
                    text.append('\n')
                else:
                    #text=text+' '+child_text
                    for i in range(0,len(child_text)):
                        text.append(child_text[i])
            elif child.text!=None:
                #text=text+' '+child.text
                if child.type in python_statement:
                    text.append('\n')
                    text.append(' ' * (int(child.level) * 4))
                    #text.append(child.text.decode('utf-8'))
                    text.append(child.text)
                elif child.type in python_addition:
                    text.append('\n')
                    text.append(' ' * (int(child.level) * 4))
                    #text.append(child.text.decode('utf-8'))
                    text.append(child.text)
                    text.append('\n')
                else:
                    #text.append(child.text.decode('utf-8'))
                    text.append(child.text)
        return text
    originaltext=getoriginaltext(tree_root_node)
    #print(originaltext)

    text=''
    #print(originaltext)
    #print(' '.join(originaltext))
    for i in range(0,len(originaltext)):
        #print(originaltext[i])
        if originaltext[i]=='\n' or originaltext[i].replace(' ','')=='':
            text=text+originaltext[i]
        else:
            text=text+originaltext[i]+' '
    return text

# generate the token list of source code(it can be the input of DL model, but if you want to get AST, please use the source code)
def TreeToTokenPy(tree_root_node):

    def getoriginaltext(tree_root_node):
        text=[]
        for child in tree_root_node.children:
            if len(child.children)!=0:
                child_text=getoriginaltext(child)
                for i in range(0,len(child_text)):
                    text.append(child_text[i])
            elif child.text!=None:
                #text.append(child.text.decode('utf-8'))
                text.append(child.text)

        return text

    token_list=getoriginaltext(tree_root_node)
    return token_list



#reset the level of a hole block
def ResetLevelPY(node):
    #print(node.parent)
    #print(node.type)
    if node.type=='block':
        node.level=node.parent.level+1
    else:
        node.level=node.parent.level

    if len(node.children)!=0:
        for child in node.children:
            ResetLevelPY(child)
    else:
        pass

# copy a subtree, the given node as the root of the subtree
#param: the node as root of the subtree
# return :none
def CopySubtreePY(old_node,new_node):
    new_node.type=old_node.type
    new_node.text=old_node.text

    if len(old_node.children)!=0:
        for old_child_node in old_node.children:
            new_child_node=Node()
            new_child_node.parent=new_node
            new_node.addchild(new_child_node)
            CopySubtreePY(old_child_node,new_child_node)
    else:
        pass

#this method wil return the list of the leaf node.text ,it equals to the source code
def GetLeafNodePY(tree_root_node):
    leaf_list=[]
    if len(tree_root_node.children)==0:
        leaf_list.append(tree_root_node.text)
    else:
        pass

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=GetLeafNodePY(child)
            for i in range(0,len(result)):
                leaf_list.append(result[i])
    else:
        pass

    return leaf_list


def getTreeJAVA(root_node,code):
    #we need not to use the level attribute
    tree_root_node=Node()
    tree_root_node.settype(root_node.type)

    def getText(code,start_point,end_point):
        text=''
        if start_point[0]==end_point[0]:
            text=code[int(start_point[0])][int(start_point[1]):int(end_point[1])]
        else:
            for i in range(int(start_point[0]),int(end_point[0])+1):
                if i==int(start_point[0]):
                    text=text+code[i][int(start_point[1]):]
                elif i==int(end_point[0]):
                    text=text+code[i][:int(end_point[1])]
                else:
                    text=text+code[i][:]

        return text

    # we need not the level attribute in java
    def gettree(tree_node,ast_node,code):
        for child in ast_node.children:
            tree_child=Node()
            tree_child.settype(child.type)
            tree_child.setparent(tree_node)
            tree_node.addchild(tree_child)
            #internal node
            if len(child.children)!=0:
                gettree(tree_child,child,code)
            #leaf node
            else:
                text=getText(code,child.start_point,child.end_point)
                tree_child.settext(text)

    gettree(tree_root_node,root_node,code)

    return  tree_root_node

#tree to text in java language
def TreeToTextJava(tree_root_node):

    def getoriginaltext(tree_root_node):
        text=[]
        for child in tree_root_node.children:
            if len(child.children)!=0:
                child_text=getoriginaltext(child)
                for i in range(0,len(child_text)):
                    text.append(child_text[i])

                if child.type=='comment' or child.type==';' or child.type=='{' or child.type=='}':
                    text.append('\n')

            else:
                if child.type=='comment' or child.type==';' or child.type=='{' or child.type=='}':
                    text.append(child.text)
                    text.append('\n')
                else:
                    text.append(child.text)
        return text

    originaltext=getoriginaltext(tree_root_node)

    text=''

    for i in range(0,len(originaltext)):
        if originaltext[i]=='\n' or originaltext[i].replace(' ','')=='':
            text=text+originaltext[i]
        else:
            text=text+originaltext[i]+' '

    return text

#copy a subtree from the tree which root node is the old_node
#param: old_node, new_node
#return: None
def CopySubtreeJava(old_node,new_node):
    new_node.type=old_node.type
    new_node.text=old_node.text
    if len(old_node.children)!=0:
        for old_child_node in old_node.children:
            new_child_node=Node()
            new_child_node.parent=new_node
            new_node.addchild(new_child_node)
            CopySubtreeJava(old_child_node,new_child_node)
    else:
        pass

# this method will return the list of leaf node.text,
# it will be useful when you want the source code from ast
def GetLeafNodeJava(tree_root_node):
    leaf_list = []
    if len(tree_root_node.children) == 0:
        leaf_list.append(tree_root_node.text)
    else:
        pass
    # internal node
    if len(tree_root_node.children) != 0:
        for child in tree_root_node.children:
            result = GetLeafNodeJava(child)
            for i in range(0, len(result)):
                leaf_list.append(result[i])
    else:
        pass

    return leaf_list

#c++
def getTreeCPP(root_node,code):
    tree_root_node=Node()
    tree_root_node.settype(root_node.type)

    def getText(code,start_point,end_point):
        text=bytes('','utf-8')
        if start_point[0]==end_point[0]:
            text=code[int(start_point[0])][int(start_point[1]):int(end_point[1])]
            if int(end_point[1])==len(code[int(end_point[0])]):
                text=text+bytes('\n','utf-8')
        else:
            for i in range(int(start_point[0]),int(end_point[0])+1):
                if i==int(start_point[0]):
                    text=text+code[i][int(start_point[1]):]
                    text=text+bytes('\n','utf-8')
                elif i==int(end_point[0]):
                    text=text+code[i][:int(end_point[1])]
                    if end_point[1]==len(code[int(end_point[0])]):
                        text=text+bytes('\n','utf-8')
                else:
                    text=text+code[i][:]
                    text=text+bytes('\n','utf-8')
        return text.decode('utf-8')

    def gettree(tree_node,ast_node,code):
        for child in ast_node.children:
            tree_child=Node()
            tree_child.settype(child.type)
            tree_child.setparent(tree_node)
            tree_node.addchild(tree_child)

            # if type is string or char
            if child.type=='string_literal' or child.type=='char_literal':
                text=getText(code,child.start_point,child.end_point)
                tree_child.settext(text)

            # internal node
            elif len(child.children)!=0:
                gettree(tree_child,child,code)

            #leaf node
            else:
                text=getText(code,child.start_point,child.end_point)
                tree_child.settext(text)

    gettree(tree_root_node,root_node,code)
    return tree_root_node



def TreeToTextCpp(tree_root_node):

    def getoriginaltext(tree_root_node):
        text=[]
        for child in tree_root_node.children:
            if len(child.children)!=0:
                child_text=getoriginaltext(child)

                for i in range(0,len(child_text)):
                    text.append(child_text[i])

                #if child.type=='comment' or child.type==';' or child.type=='{' or child.type=='}':
                    #text.append('\n')
            else:
                #if child.type=='comment' or child.type==';' or child.type=='{' or child.type=='}':
                #    text.append(child.text)
                #    text.append('\n')
                #else:
                #    text.append(child.text)
                 text.append(child.text)

        return text

    originaltext=getoriginaltext(tree_root_node)

    text=''

    for i in range(0,len(originaltext)):
        if originaltext[i]=='\n' or originaltext[i].replace(' ','')=='':
            text=text+originaltext[i]
        else:
            text=text+originaltext[i]+' '

    return text





