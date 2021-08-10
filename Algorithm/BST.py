class BST:
    class node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key):
        if self.root == None:
            self.root = self.node(key)
            self.size += 1
        else:
            res, pos = self.search(key)
            print(res, pos)
            if res == True:
                print("ERROR: key already exists in tree.")
                return False
            else:
                pos = self.node(key)
                self.size += 1
        return True
    
    def search(self, key):
        if self.root == None:
            print("root")
            return False, self.root
        else:
            present = self.root
            while present != None:
                if (key == present.key):
                    return True, present
                elif (key < present.key):
                    present = present.left
                else:
                    present = present.right
            return False, present

    def delete(self):
        pass
    def self_check(self):
        """
        BST have following characteristics. Binary Search Tree의 특성
        1. one key per node. every node has unique key. 한 노드는 중복되지 않는 하나의 키값을 가진다.
        2. root node is placed on top level of the tree. 루트 노드는 최상위 레벨에 위치한다.
        3. A node can have as many as two children. 각 노드는 최대 두 개의 자식 노드를 가진다. 
        4. every node's key is bigger then the whold nodes on the left side of it, and smaller than the right. 임의의 노드의 키 값은 자신의 왼쪽에 있는 모든 노드의 키 값보다 크고, 오른쪽에 있는 모든 노드의 키 값보다 작다.
        """
        pass
    def traverse(self):
        def _traverse(root):
            if not root:
                pass
            else:
                print(root.key)
                _traverse(root.left)
                _traverse(root.right)
        _traverse(self.root)

if __name__ == "__main__":
    mytree = BST()
    mytree.insert(12)
    mytree.insert(8)
    mytree.insert(9)
    mytree.traverse()