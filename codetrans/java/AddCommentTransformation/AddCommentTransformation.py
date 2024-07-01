#we will add some comments in the source code

from Node import Node
from AstToTree import *
import random

#add comments in this function
#para: tree_root_node: the root node of the tree generated from ast
#      pattern: 0/1 -> you want to add the comment from the train dataset or generate the new comment randomly
#      number: the number of comments you want to add
#      comments: the comments.json, you should load the file
def AddComment(tree_root_node,pattern,number,comments):
    original_comments=comments['original_comment']
    comments_token=comments['comment_token']

    #if pattern is 0, we will add comment from the original comments we select from the 6978 comments
    if pattern==0:
        sample_list=random.sample(range(69707),k=number)
        for i in range(0,len(sample_list)):
            comment='// '+original_comments[sample_list[i]]
            addcomment(tree_root_node,comment)

        return TreeToTextJava(tree_root_node)

    #if pattern is 1, we will randomly generate new comments use tokens
    elif pattern==1:
        for i in range(0,number):
            #the new generated comment must has n tokens
            n_tokens=random.randint(5,50)
            sample_list = random.sample(range(28046), k=n_tokens)
            comment='//'
            for j in range(0,len(sample_list)):
                comment=comment+' '+comments_token[sample_list[j]]

            addcomment(tree_root_node,comment)

        return TreeToTextJava(tree_root_node)

    else:
        print('--the pattern must be 0 or 1--')
        return 0


#this method will add a comment at the beginning of the original code
#param:tree_root_node: the root node of the tree generated from ast
#return :None
def addcomment(tree_root_node,comment):
    comment_node=Node()
    comment_node.type='comment'
    comment_node.text=comment
    tree_root_node.children.insert(0,comment_node)
    comment_node.parent=tree_root_node


