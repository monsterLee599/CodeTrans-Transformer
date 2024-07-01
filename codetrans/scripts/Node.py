#node of ast
class Node():
    def __init__(self):
        self.level=0
        self.type=None
        self.text=None
        self.children=[]
        self.parent=None

    def setLevel(self,level):
        self.level=level

    def settype(self,type):
        self.type=type

    def settext(self,text):
        self.text=text

    def addchild(self,child):
        self.children.append(child)

    def setparent(self,parent):
        self.parent=parent

    def getlevel(self):
        return self.level

