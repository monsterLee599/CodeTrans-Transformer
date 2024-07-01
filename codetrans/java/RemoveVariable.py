# this transformation will remove the variable if it is never used
# for example, we declarate a variable, and the code has not use the variable, we can delete the variable
# for example: public int hello(){
#                  int x=0;
#


def RemoveVariable(tree_root_node):
    pass

def FindAllIdentifier(tree_root_node):
    identifier_list=[]
    if tree_root_node.type=='identifier':
        identifier_list.append(tree_root_node)

    if len(tree_root_node.children)!=0:
        for child in tree_root_node.children:
            result=FindAllIdentifier(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    identifier_list.append(result[i])

    else:
        pass

    return identifier_list