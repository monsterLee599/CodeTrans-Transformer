# this transformation will import java library

import json
import random
from Node import Node
from AstToTree import *

# this method is the main function to add library
# param: tree_root_node: the root node of the tree generated from ast
#        number: the number of libraries you want to import
# return: the new code
def ImportLibrary(tree_root_node,number):
    with open('java/ImportTransformation/library.json','r')as f:
        library=json.load(f)

    sample=random.sample(range(len(library)-1),k=number)

    for i in range(0,len(sample)):
        #print(i)
        #print(library[sample[i]])
        InsertImport(tree_root_node,library[sample[i]])

    code=TreeToTextJava(tree_root_node)
    return code

# this function will import library in the beginning of the code
# and the library is like a.b.c;
# also, if you want to import other library, you should modify the source code
# param: tree_root_node: the root node of the tree generated from ast
#        library: the java library you want to import
# return: none
def InsertImport(tree_root_node,library):
    library=library.split('.')

    import_declaration=Node()
    import_declaration.type='import_declaration'
    import_declaration.parent=tree_root_node
    tree_root_node.children.insert(0,import_declaration)

    import_node=Node()
    import_node.type='import'
    import_node.text='import'
    import_node.parent=import_declaration
    import_declaration.addchild(import_node)

    scoped_identifier_1=Node()
    scoped_identifier_1.type='scoped_identifier'
    scoped_identifier_1.parent=import_declaration
    import_declaration.addchild(scoped_identifier_1)

    scoped_identifier_2=Node()
    scoped_identifier_2.type='scoped_identifier'
    scoped_identifier_2.parent=scoped_identifier_1
    scoped_identifier_1.addchild(scoped_identifier_2)

    identifier_1=Node()
    identifier_1.type='identifier'
    identifier_1.text=library[0]
    identifier_1.parent=scoped_identifier_2
    scoped_identifier_2.addchild(identifier_1)

    point_1=Node()
    point_1.type='.'
    point_1.text='.'
    point_1.parent=scoped_identifier_2
    scoped_identifier_2.addchild(point_1)

    identifier_2=Node()
    identifier_2.type='identifier'
    identifier_2.text=library[1]
    identifier_2.parent=scoped_identifier_2
    scoped_identifier_2.addchild(identifier_2)

    point_2=Node()
    point_2.type='.'
    point_2.text='.'
    point_2.parent=scoped_identifier_1
    scoped_identifier_1.addchild(point_2)

    identifier_3=Node()
    identifier_3.type='identifier'
    identifier_3.text=library[2]
    identifier_3.parent=scoped_identifier_1
    scoped_identifier_1.addchild(identifier_3)

    semicolon=Node()
    semicolon.type=';'
    semicolon.text=';'
    semicolon.parent=import_declaration
    import_declaration.addchild(semicolon)




