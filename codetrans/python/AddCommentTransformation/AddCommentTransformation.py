from Node import Node
import random
import json
from AstToTree import *

#add some comments at the start of code
#param: tree_root_node: the root node of tree generated from ast
#       number: the number of comments you want to add
#       pattern: if the value is 0,we will select n comments from the 5W comment, if you select 1, we will generate new comments use the token vocabulary in comment.json
#output: the new code tha add many unuseful comments
def AddComment(tree_root_node,pattern,number,comments):
    #comment_path='python/AddCommentTransformation/comments.json'

    #with open(comment_path,'r') as f:
    #    comments=json.load(f)
    #print(comments.keys())
    original_comments=comments['original_comment']
    comments_token=comments['comment_token']
    #select n comments from original_comments
    if pattern==0:
        sample_list=random.sample(range(55417),k=number)
        for i in range(0,len(sample_list)):
            comment='# '+original_comments[sample_list[i]]
            addcomment(tree_root_node,comment)

        return TreeToTextPy(tree_root_node)
    #generate new comments using comments_token //26984 tokens
    elif pattern==1:
        for i in range(0,number):
            # the comment must has n_tokens tokens
            n_tokens=random.randint(5,50)
            sample_list=random.sample(range(26984),k=n_tokens)
            comment='#'
            for j in range(0,n_tokens):
                comment=comment+' '+comments_token[sample_list[j]]
            addcomment(tree_root_node,comment)

        return TreeToTextPy(tree_root_node)
    else:
        print('--the pattern must be 0 or 1--')
        return 0

    print(len(original_comments))
    print(len(comments_token))

#add comment to the root node of the tree
#param: tree_root_node: the root node of tree generated from ast
#       comment : the comment you want to add to the code
def addcomment(tree_root_node,comment):
    # comment node
    comment_node=Node()
    comment_node.setLevel(0)
    comment_node.settype('comment')
    comment_node.setparent(tree_root_node)
    tree_root_node.children.insert(0,comment_node)

    #string node
    string_node=Node()
    string_node.setLevel(0)
    string_node.settype('string')
    string_node.settext(comment)
    string_node.setparent(comment_node)
    comment_node.addchild(string_node)
