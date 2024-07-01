import ast
import json
# import javalang


def parse_py_file(code):

    tree = ast.parse(code)
    
    json_tree = []
    def gen_identifier(identifier, node_type = 'identifier'):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = node_type
        json_node['value'] = identifier
        return pos
    
    def traverse_list(l, node_type = 'list'):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = node_type
        children = []
        for item in l:
            children.append(traverse(item))
        if (len(children) != 0):
            json_node['children'] = children
        return pos
        
    def traverse(node):
        pos = len(json_tree)
        json_node = {}
        json_tree.append(json_node)
        json_node['type'] = type(node).__name__
        children = []
        if isinstance(node, ast.Name):
            json_node['value'] = node.id
        elif isinstance(node, ast.Num):
            json_node['value'] = str(node.n)
        elif isinstance(node, ast.Str):
            json_node['value'] = node.s
        elif isinstance(node, ast.alias):
            json_node['value'] = str(node.name)
            if node.asname:
                children.append(gen_identifier(node.asname))
        elif isinstance(node, ast.FunctionDef):
            json_node['value'] = str(node.name)
        elif isinstance(node, ast.ClassDef):
            json_node['value'] = str(node.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                json_node['value'] = str(node.module)
        elif isinstance(node, ast.Global):
            for n in node.names:
                children.append(gen_identifier(n))
        elif isinstance(node, ast.keyword):
            # origin
            json_node['value'] = str(node.arg)



        # Process children.
        if isinstance(node, ast.For):
            children.append(traverse(node.target))
            children.append(traverse(node.iter))
            children.append(traverse_list(node.body, 'body'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))
        elif isinstance(node, ast.If) or isinstance(node, ast.While):
            children.append(traverse(node.test))
            children.append(traverse_list(node.body, 'body'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))

        # elif isinstance(node, ast.With):
        #     children.append(traverse(node.context_expr))
        #     if node.optional_vars:
        #         children.append(traverse(node.optional_vars))
        #     children.append(traverse_list(node.body, 'body'))

        elif isinstance(node, ast.With):
            for item in node.items:  # 修改此处，遍历items属性
                children.append(traverse(item.context_expr))
                if item.optional_vars:
                    children.append(traverse(item.optional_vars))
            children.append(traverse_list(node.body, 'body'))

        elif isinstance(node, ast.Try):
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.handlers, 'handlers'))
            children.append(traverse_list(node.finalbody, 'finalbody'))
            if node.orelse:
                children.append(traverse_list(node.orelse, 'orelse'))
        # elif isinstance(node, ast.TryFinally):
        #     children.append(traverse_list(node.body, 'body'))
        #     children.append(traverse_list(node.finalbody, 'finalbody'))
        elif isinstance(node, ast.arguments):
            children.append(traverse_list(node.args, 'args'))
            children.append(traverse_list(node.defaults, 'defaults'))
            if node.vararg:
                children.append(gen_identifier(node.vararg.arg, 'vararg'))  # add arg
            if node.kwarg:
                children.append(gen_identifier(node.kwarg.arg, 'kwarg')) # add arg
        # elif isinstance(node, ast.ExceptHandler):
        #     if node.type:
        #         children.append(traverse_list([node.type], 'type'))
        #     if node.name:
        #         children.append(traverse_list([node.name], 'name'))
        #     children.append(traverse_list(node.body, 'body'))
        elif isinstance(node, ast.ExceptHandler):
            if node.type:
                children.append(traverse(node.type))
            if node.name:
                children.append(gen_identifier(node.name, 'name'))  
            children.append(traverse_list(node.body, 'body'))

        elif isinstance(node, ast.ClassDef):
            children.append(traverse_list(node.bases, 'bases'))
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.decorator_list, 'decorator_list'))
        elif isinstance(node, ast.FunctionDef):
            children.append(traverse(node.args))
            children.append(traverse_list(node.body, 'body'))
            children.append(traverse_list(node.decorator_list, 'decorator_list'))
        else:
            # Default handling: iterate over children.
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.expr_context) or isinstance(child, ast.operator) or isinstance(child, ast.boolop) or isinstance(child, ast.unaryop) or isinstance(child, ast.cmpop):
                    # Directly include expr_context, and operators into the type instead of creating a child.
                    json_node['type'] = json_node['type'] + type(child).__name__
                else:
                    children.append(traverse(child))
                
        if isinstance(node, ast.Attribute):
            children.append(gen_identifier(node.attr, 'attr'))
                
        if (len(children) != 0):
            json_node['children'] = children
        return pos
    
    traverse(tree)
    return json.dumps(json_tree, separators=(',', ':'), ensure_ascii=False)




def parse_java_file(tree_root_node):



    def ProcessTree(tree_root_node):
        node_list=[]
        #internal node
        #{'node':node,'type':node.type,children:[...]}
        if len(tree_root_node.children)!=0:
            node={'node':tree_root_node,'type':tree_root_node.type,'children':[]}

        #leaf node
        #{'node':node,'type':node.type,'value':node.text}
        else:
            node={'node':tree_root_node,'type':tree_root_node.type,'value':tree_root_node.text}

        node_list.append(node)

        if len(tree_root_node.children)!=0:
            for child in tree_root_node.children:
                result=ProcessTree(child)
                for i in range(0,len(result)):
                    node_list.append(result[i])

        else:
            pass

        return node_list
    # in this function, we will add the children for the internal node
    def GetChildren(node_list):

        for i in range(0,len(node_list)):
            node=node_list[i]['node']
            parent=node.parent
            for j in range(0,len(node_list)):
                if node_list[j]['node']==parent:
                    node_list[j]['children'].append(i)

        return node_list
    #in this function, we will delete the key 'node' in the dict
    def DelNode(node_list):
        for i in range(0,len(node_list)):
            node_list[i].pop('node')

        return node_list

    node_list=ProcessTree(tree_root_node)
    node_list = GetChildren(node_list)
    node_list = DelNode(node_list)

    return json.dumps(node_list, separators=(',', ':'), ensure_ascii=False)
