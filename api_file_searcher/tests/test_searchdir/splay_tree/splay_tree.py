# Copyright 2021 aaaaaaaalesha

from collections import deque
import sys

sys.setrecursionlimit(5000)


class SplayTree:
    """
    Implementation of data structure splay tree with unique integer keys.
    """

    class Node:
        """
        Structure for node in SplayTree.
        """

        def __init__(self, key: int, value, left=None, right=None, parent=None):
            self.key = key
            self.value = value
            self.left = left
            self.right = right
            self.parent = parent

        def __str__(self):
            if self is None:
                return '_'

            return f"[{self.key} {self.value}{'' if self.parent is None else ' ' + str(self.parent.key)}]"

        def __bool__(self):
            return self is not None

        def __eq__(self, other):
            return self is other

    def __init__(self, root=None):
        self.__root = root

    def __bool__(self):
        return self.__root is not None

    def __getitem__(self, key: int):
        if not isinstance(key, int):
            raise TypeError(f"Key {key} should have type int.")

        node = self.__search(key, self.__root)
        if node is None:
            raise KeyError(f"Where is no key {key}.")

        return node.value

    def __setitem__(self, key: int, value):
        """
        Method implements updating node's value with existing key.
        """
        if not self or self[key] is None:
            raise KeyError(f"Where is no key {key}.")

        self.__root.value = value

    def __contains__(self, key: int) -> bool:
        return self.__search(key, self.__root) is not None

    @staticmethod
    def __update_parents(node: Node):
        """
        Method updates parent links for node's left and right children after rotations.
        """
        if node.left is not None:
            node.left.parent = node
        if node.right is not None:
            node.right.parent = node

    def __rotation(self, parent: Node, child: Node):
        """
        Method implements a rotation around the parent.
        """
        grandpa = parent.parent
        if grandpa is not None:
            if grandpa.left == parent:
                grandpa.left = child
            else:
                grandpa.right = child

        if parent.left == child:
            # Rotate right.
            parent.left, child.right = child.right, parent
        else:
            # Rotate left.
            parent.right, child.left = child.left, parent

        child.parent = grandpa
        self.__update_parents(parent)
        self.__update_parents(child)
        if parent == self.__root:
            self.__root = child

    def __splay(self, node: Node) -> Node:
        """
        Method implements splay operation in tree. Main idea is move node to the root of SplayTree using 3 operations:
        Zig: when node's parent is root;
        Zig-Zig: when links between grandparent-parent-node is left-left or right-right;
        Zig-Zag: otherwise (when left-right or right-left).
        """
        if node.parent is None:
            # If node is root, just return it.
            return node

        grandpa = node.parent.parent
        if grandpa is None:
            # Zig.
            self.__rotation(node.parent, node)
            return node

        if not ((node.parent.left == node) ^ (node.parent == grandpa.left)):
            # Zig-zig.
            self.__rotation(grandpa, node.parent)
            self.__rotation(node.parent, node)
        else:
            # Zig-Zag.
            self.__rotation(node.parent, node)
            self.__rotation(grandpa, node)

        return self.__splay(node)

    def __search(self, key: int, node: Node):
        """
        Method implements recursive search in SplayTree by key.
        :return: node with equal key or None if where is no key in SplayTree.
        """
        if not self:
            return None

        if key == node.key:
            return self.__splay(node)
        if key < node.key and node.left is not None:
            return self.__search(key, node.left)
        if key > node.key and node.right is not None:
            return self.__search(key, node.right)

        # If there is no key in SplayTree, just splay leaf, which was last in process of searching.
        self.__splay(node)
        return None

    def __min(self, node: Node):
        while node.left is not None:
            node = node.left
        self.__splay(node)

        return node

    def __max(self, node: Node):
        while node.right is not None:
            node = node.right
        self.__splay(node)

        return node

    def add(self, key: int, value):
        """
        Method implements an addition in SplayTree.
        """
        if self.__root is None:
            self.__root = SplayTree.Node(key, value)
            return

        node_parent = None
        node = self.__root

        # Descent down.
        while node is not None:
            node_parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:  # key == node.key
                self.__splay(node)
                return

                # Insertion.
        node = SplayTree.Node(key, value)
        if key > node_parent.key:
            node_parent.right = node
        else:
            node_parent.left = node
        node.parent = node_parent
        self.__splay(node)

    def remove(self, key: int):
        """
        Method implements removing node from SplayTree.
        """
        if not self or self[key] is None:
            raise KeyError(f"Where is no key {key}.")

        # Subtrees for root.
        left = self.__root.left
        right = self.__root.right

        if left is not None and right is not None:
            self.__max(left)
            self.__root.right.parent = None
            self.__root.right = self.__root.right.right
            self.__root.right.parent = self.__root
        elif left is None and right is not None:
            right.parent = None
            self.__root = right
        elif right is None and left is not None:
            left.parent = None
            self.__root = left
        else:
            self.__root = None

    def min(self):
        """
        Method implements searching of node with min key.
        """
        if not self:
            raise RuntimeError("Tree is empty.")

        return self.__min(self.__root)

    def max(self):
        """
        Method implements searching of node with max key.
        """
        if not self:
            raise RuntimeError("Tree is empty.")

        return self.__max(self.__root)

    def print(self, out) -> None:
        """
        Method outputs SplayTree in  by levels (breath traversal).
        """
        if not self:
            print('_', file=out)
            return

        queue = deque()
        queue.append(self.__root)

        children_queue = deque()
        out_str = str()
        is_there_nodes = False

        while queue:
            curr = queue.popleft()
            if not isinstance(curr, SplayTree.Node):
                out_str += '_ '
                children_queue.append(curr)
                children_queue.append(curr)
            else:
                out_str += str(curr) + ' '
                if curr.left:
                    is_there_nodes = True
                    children_queue.append(curr.left)
                else:
                    children_queue.append('_')

                if curr.right:
                    is_there_nodes = True
                    children_queue.append(curr.right)
                else:
                    children_queue.append('_')

            if is_there_nodes and not queue:
                children_queue, queue = queue, children_queue
                print(out_str.rstrip(), file=out)
                out_str = str()
                is_there_nodes = False
        if out_str:
            print(out_str.rstrip(), file=out)
