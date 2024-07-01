import json
import random
from Node import Node
from AstToTree import *
# import some libraries at the beginning of code
# param: tree_root_node: root node of the tree generated from ast
#                number: the number of libraries that you want to import
def importlibrary(tree_root_node,number):
    with open('python/ImportTransformation/library.json','r')as f:
        library=json.load(f)
    #print(len(library))
    for i in range(0,len(library)):
        library[i]=library[i].split(' ')
    sample=random.sample(range(226),k=number)

    for i in range(0,len(sample)):
        insertimport(tree_root_node,library[sample[i]])

    return TreeToTextPy(tree_root_node)


def insertimport(tree_root_node,library):
    #import ...
    if len(library)==2:
        keyword_import_node=Node()
        keyword_import_node.level=0
        keyword_import_node.type='import_statement'
        keyword_import_node.parent=tree_root_node
        #import
        import_name_node=Node()
        import_name_node.level=0
        import_name_node.type='import'
        import_name_node.text='import'
        import_name_node.parent=keyword_import_node
        keyword_import_node.addchild(import_name_node)
        #dotted_name
        dotted_name_node=Node()
        dotted_name_node.level=0
        dotted_name_node.type='dotted_name'
        dotted_name_node.parent=keyword_import_node
        keyword_import_node.addchild(dotted_name_node)
        #library_name
        library_name_node=Node()
        library_name_node.level=0
        library_name_node.type='identifier'
        library_name_node.text=library[1]
        library_name_node.parent=dotted_name_node
        dotted_name_node.addchild(library_name_node)
        tree_root_node.children.insert(0,keyword_import_node)
    #from ... import ...
    elif len(library)==4 and 'from' in library:
        import_from_node=Node()
        import_from_node.level=0
        import_from_node.type='import_from_statement'
        import_from_node.parent=tree_root_node

        #keyword_from
        keyword_from_node=Node()
        keyword_from_node.level=0
        keyword_from_node.type='from'
        keyword_from_node.text='from'
        keyword_from_node.parent=import_from_node
        import_from_node.addchild(keyword_from_node)

        #dotted_name 1
        dotted_name1_node=Node()
        dotted_name1_node.level=0
        dotted_name1_node.type='dotted_name'
        dotted_name1_node.parent=import_from_node
        import_from_node.addchild(dotted_name1_node)

        #library1
        library_name1_node=Node()
        library_name1_node.level=0
        library_name1_node.type='identifier'
        library_name1_node.text=library[1]
        library_name1_node.parent=dotted_name1_node
        dotted_name1_node.addchild(library_name1_node)

        #keyword_import
        keyword_import_node=Node()
        keyword_import_node.level=0
        keyword_import_node.type='import'
        keyword_import_node.text='import'
        keyword_import_node.parent=import_from_node
        import_from_node.addchild(keyword_import_node)

        #dotted_name 2
        dotted_name2_node=Node()
        dotted_name2_node.level=0
        dotted_name2_node.type='dotted_name'
        dotted_name2_node.parent=import_from_node
        import_from_node.addchild(dotted_name2_node)

        #library2
        library_name2_node=Node()
        library_name2_node.level=0
        library_name2_node.type='identifier'
        library_name2_node.text=library[3]
        library_name2_node.parent=dotted_name2_node
        dotted_name2_node.addchild(library_name2_node)
        #add child import_from_node
        tree_root_node.children.insert(0,import_from_node)
    #import ... as ...
    elif len(library)==4 and 'as' in library:

        import_as_node=Node()
        import_as_node.level=0
        import_as_node.type='import_statement'
        import_as_node.parent=tree_root_node

        #keyword import
        keyword_import_node=Node()
        keyword_import_node.level=0
        keyword_import_node.type='import'
        keyword_import_node.text='import'
        keyword_import_node.parent=import_as_node
        import_as_node.addchild(keyword_import_node)

        #aliased_import
        aliased_import_node=Node()
        aliased_import_node.level=0
        aliased_import_node.type='aliased_import'
        aliased_import_node.parent=import_as_node
        import_as_node.addchild(aliased_import_node)

        #dotted_name
        dotted_name_node=Node()
        dotted_name_node.level=0
        dotted_name_node.type='dotted_name'
        dotted_name_node.parent=aliased_import_node
        aliased_import_node.addchild(dotted_name_node)

        #library name
        library_name_node=Node()
        library_name_node.level=0
        library_name_node.type='identifier'
        library_name_node.text=library[1]
        library_name_node.parent=dotted_name_node
        dotted_name_node.addchild(library_name_node)

        #as node
        as_node=Node()
        as_node.level=0
        as_node.type='as'
        as_node.text='as'
        as_node.parent=aliased_import_node
        aliased_import_node.addchild(as_node)

        #identifier node
        identifier_node=Node()
        identifier_node.level=0
        identifier_node.type='identifier'
        identifier_node.text=library[3]
        identifier_node.parent=aliased_import_node
        aliased_import_node.addchild(identifier_node)

        #add child import_as_node
        tree_root_node.children.insert(0,import_as_node)



