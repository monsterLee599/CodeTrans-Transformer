# get type of java
from Node import Node
from AstToTree import *
from GetAST import *
import json

# java
language='python'
with open('/home/syqi/CodeTransformation/build/tree-sitter-python/src/node-types.json','r') as f:
    node_type=json.load(f)

print(len(node_type))
all_type=[]

for i in range(0,len(node_type)):
    all_type.append(node_type[i]['type'])
    if 'subtypes' not in node_type[i]:
        continue
    else:
        for subtype in node_type[i]['subtypes']:
            all_type.append(subtype['type'])
print(len(all_type))
data_list=[]
with open('/data/syqi/data/code2nl/CodeSearchNet/python/train.jsonl','r') as f:
    for line in f:
        data_list.append(json.loads(line))
code_list=[]
for i in range(0,len(data_list)):
    #class_name = data_list[i]['func_name'].split('.')[0]
    #code = 'public class ' + class_name + '{\n' + data_list[i]['code'] + '\n}'
    code=data_list[i]['code']
    code_list.append(code)
print('-- get source code finish --')



ast_root_node_list=[]
for i in range(0,len(code_list)):
    ast_root_node_list.append(generateASt(code_list[i],language))

print('-- generate ast finish --')

def TraverserAST(root_node):
    type_list=[]
    if root_node.type not in type_list:
        type_list.append(root_node.type)

    if len(root_node.children)!=0:
        for child in root_node.children:
            result=TraverserAST(child)
            if len(result)!=0:
                for i in range(0,len(result)):
                    if result[i] not in type_list:
                        type_list.append(result[i])
    else:
        pass

    return  type_list

for i in range(0,len(ast_root_node_list)):
    type=TraverserAST(ast_root_node_list[i])
    for j in range(0,len(type)):
        if type[j] not in all_type:
            print(type[j])
            all_type.append(type[j])

print(len(all_type))

with open('/data/syqi/code-transformation/nodetype/python.json','w')as f:
    json.dump(all_type,f)

print('-- load finish --')
with open('/data/syqi/code-transformation/nodetype/python.json','r') as f:
    type=json.load(f)
print(len(type))