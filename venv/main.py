import tkinter
import customtkinter
import math
import pymongo

# init global variables
RADIUS = 25
ARROW_OFFSET_X = 24
ARROW_OFFSET_Y = 8
ARROW_LENGTH_X = 320
ARROW_LENGTH_Y = 80
CHILD_X = 330
CHILD_Y = 105
MANAGER = "EylomYaakov"

time_offset = 750

uri = """mongodb+srv://eylomy:gzBZbEKGzCOrTXZy@datastructers.aklcqk1.mongodb.net/?retryWrites=true&w=majority&appName=
dataStructers"""
client = pymongo.MongoClient(uri)
database = client["datastructers"]
collection = database["users"]


user = None


class BinaryHeapNode:
    """A class to represent a node of the binary heap, each instance has both attributes related to the node itself(such
    as key) and attributes related do the draw of the node(such as circle)
    Attributes:
        key: the key of the node(the number inside the circle, that represent the value of the node)
        canvas: the canvas that the node is drawn in
        arrow: the draw of the arrow that enter the node(the arrow from the father to the node)
        x: the x value of the center of the circle of the node
        y: the y value of the center of the circle of the node
        circle: the draw of the circle represent the node
        text: the draw of the node key inside the circle
        node_number: the draw of the node number that appears above the node circle"""
    def __init__(self, key, canvas, level, node_number=1, father_x=0, father_y=0, child_type="root"):
        """Init instance of class according to the key, the type of the node(root, left or right), the father x
         and y(if exist) and the level in the heap of the node"""
        self.key = key
        self.canvas = canvas
        child_circle_y = father_y + CHILD_Y
        child_arrow_y = father_y + ARROW_OFFSET_Y
        child_arrow_length_y = father_y + ARROW_LENGTH_Y
        child_circle_x, child_arrow_x, child_arrow_length_x = father_x, father_x, father_x
        if child_type == "right":
            child_arrow_x += ARROW_OFFSET_X
            if level < 4:
                child_circle_x += CHILD_X/level
                child_arrow_length_x += ARROW_LENGTH_X/level
            else:
                child_circle_x += CHILD_X/12
                child_arrow_length_x += ARROW_LENGTH_X/12
            self.arrow = canvas.create_line(child_arrow_x, child_arrow_y, child_arrow_length_x, child_arrow_length_y,
                                            arrow="last")
        elif child_type == "left":
            child_arrow_x -= ARROW_OFFSET_X
            if level < 4:
                child_circle_x -= CHILD_X/level
                child_arrow_length_x -= ARROW_LENGTH_X/level
            else:
                child_circle_x -= CHILD_X/12
                child_arrow_length_x -= ARROW_LENGTH_X/12

            self.arrow = canvas.create_line(child_arrow_x, child_arrow_y, child_arrow_length_x, child_arrow_length_y,
                                            arrow="last")
        elif child_type == "root":
            child_circle_x = 700
            child_circle_y = 80
            self.arrow = None
        self.x = child_circle_x
        self.y = child_circle_y
        self.circle = canvas.create_oval(child_circle_x-RADIUS, child_circle_y-RADIUS, child_circle_x+RADIUS,
                                         child_circle_y+RADIUS, outline="red")
        self.text = canvas.create_text((child_circle_x, child_circle_y), text=str(key))
        self.node_number = canvas.create_text((child_circle_x, child_circle_y-40), text=str(node_number))

    def change_text(self, new_text):
        """A method that get a text and replace the text inside the circle with the new text"""
        self.canvas.itemconfig(self.text, text=new_text)

    def change_outline_color(self, color):
        """A method that get a color and replace the color of the outline of the circle with the new color"""
        self.canvas.itemconfig(self.circle, outline=color)

    @staticmethod
    def swap_nodes(node1, node2, i, delete=False):
        """A static method that gets two nodes and swap them in the screen and swap their attributes"""
        node1.node_number, node2.node_number = node2.node_number, node1.node_number
        node1.arrow, node2.arrow = node2.arrow, node1.arrow
        node1.x, node2.x = node2.x, node1.x
        node1.y, node2.y = node2.y, node1.y
        node1.circle, node2.circle = node2.circle, node1.circle
        node1.text, node2.text = node2.text, node1.text
        circle1, circle2 = node1.circle, node2.circle
        text1, text2 = node1.text, node2.text
        BinaryHeap.canvas.after(time_offset * i, lambda: BinaryHeap.canvas.itemconfig(circle1, outline="red"))
        BinaryHeap.canvas.after(time_offset * i, lambda: BinaryHeap.canvas.itemconfig(circle2, outline="white"))
        BinaryHeap.canvas.after(time_offset * i, lambda: BinaryHeap.canvas.itemconfig(text2, text=str(node2.key)))
        # if we use this method for deleting, change the text to -∞ instead of to the other's node key
        if not delete:
            BinaryHeap.canvas.after(time_offset * i, lambda: BinaryHeap.canvas.itemconfig(text1, text=str(node1.key)))
        else:
            BinaryHeap.canvas.after(time_offset * i, lambda: BinaryHeap.canvas.itemconfig(text1, text="-∞"))


class BinaryHeap:
    """A class that represent binary heap.
    Attributes:
        canvas: a static attribute of the canvas that the heap is drawn in
        nodes: a list of the heap nodes"""

    canvas = None

    @staticmethod
    def set_canvas(canvas):
        """A static method that changes the canvas of the class"""
        BinaryHeap.canvas = canvas

    def __init__(self):
        """Init the nodes with empty list(because the heap is empty in initialization)"""
        self.nodes = []

    def bubble_up(self, index, i=1, delete=False):
        """A method that gets index of node in the nodes list and bubble the node up (replace with the father of the
        node) until the heap is ordered"""
        node = self.nodes[index]
        father_index = int((index-1)/2)
        father = self.nodes[father_index]
        while father.key > node.key and index != 0:
            self.nodes[index], self.nodes[father_index] = self.nodes[father_index], self.nodes[index]
            BinaryHeapNode.swap_nodes(node, father, i, delete)
            index = father_index
            father_index = int((index+1)/2)-1
            father = self.nodes[father_index]
            i += 1
        BinaryHeap.canvas.after(time_offset * i, lambda: node.change_outline_color("white"))
        return i

    def bubble_down(self, index, i=1):
        """A method that gets index of node in the nodes list and bubble the node down(replace the node with his min-key
        child) until the heap is ordered"""
        left_index = 2*index
        right_index = left_index+1
        node = self.nodes[index-1]
        while len(self.nodes) >= left_index:
            left = self.nodes[left_index-1]
            # first case: there are two children
            if len(self.nodes) >= right_index:
                right = self.nodes[right_index-1]
                # check if we need any replacement
                if right.key < node.key or left.key < right.key:
                    # replace with right child
                    if right.key < left.key:
                        self.nodes[index-1], self.nodes[right_index-1] = self.nodes[right_index-1], self.nodes[index-1]
                        BinaryHeapNode.swap_nodes(node, right, i)
                        index = right_index
                    # replace with left child
                    else:
                        self.nodes[index-1], self.nodes[left_index-1] = self.nodes[left_index-1], self.nodes[index-1]
                        BinaryHeapNode.swap_nodes(node, left, i)
                        index = left_index
                    left_index = 2 * index
                    right_index = left_index + 1
                    i += 1
                    BinaryHeap.canvas.after(time_offset * i, lambda: node.change_outline_color("white"))
                else:
                    BinaryHeap.canvas.after(time_offset * i, lambda: node.change_outline_color("white"))
                    break
            # second case: there is only left child
            else:
                if left.key < node.key:
                    self.nodes[index-1], self.nodes[left_index-1] = self.nodes[left_index-1], self.nodes[index-1]
                    BinaryHeapNode.swap_nodes(node, left, i)
                    i += 1
                BinaryHeap.canvas.after(time_offset * i, lambda: node.change_outline_color("white"))
                break

    def insert(self, key):
        """A method that gets a key, create a node with this key and insert the node to the heap"""
        # first case: the heap is empty and therefore the new node is the root
        if len(self.nodes) == 0:
            root = BinaryHeapNode(key, BinaryHeap.canvas, 1)
            self.nodes.append(root)
            BinaryHeap.canvas.after(time_offset*2, lambda: root.change_outline_color("white"))
        # second case: the heap is full
        elif len(self.nodes) == 31:
            full_message = BinaryHeap.canvas.create_text((730, 15), text="heap is full!", font=("Ariel", 20))
            BinaryHeap.canvas.after(time_offset*2, lambda: BinaryHeap.canvas.delete(full_message))
        # third case: the new node isn't the root and the heap has more space
        else:
            length = len(self.nodes)+1
            if int(length/2) == length/2:
                child_type = "left"
            else:
                child_type = "right"
            father_index = int(length/2)-1
            father = self.nodes[father_index]
            level = int(math.log(length, 2))
            # insert the new node as the rightmost heap in the lest level
            new_node = BinaryHeapNode(key, BinaryHeap.canvas, level, length, father.x, father.y, child_type)
            self.nodes.append(new_node)
            # bubble the node up until the heap is ordered
            self.bubble_up(length - 1, 2)

    def decrease_key(self, index, new_key, delete=False):
        """A method that gets index of node and key and decrease the node key to the new key """
        index -= 1
        # check if the new key is bigger than the current key
        if self.nodes[index].key < new_key:
            error_message(BinaryHeap.canvas)
            return
        # set the key of the node to the new key
        self.nodes[index].key = new_key
        if not delete:
            self.nodes[index].change_outline_color("red")
            BinaryHeap.canvas.after(time_offset*2, lambda: self.nodes[index].change_text(str(new_key)))
        # bubble the node up until the heap is ordered
        return self.bubble_up(index, 3, delete)

    def delete_rightmost(self, i):
        """A method that deletes the rightmost node in the last level in the heap """
        rightmost = self.nodes[len(self.nodes)-1]
        self.nodes = self.nodes[:-1]
        BinaryHeap.canvas.after(time_offset*i, lambda: BinaryHeap.canvas.delete(rightmost.circle))
        BinaryHeap.canvas.after(time_offset*i, lambda: BinaryHeap.canvas.delete(rightmost.text))
        BinaryHeap.canvas.after(time_offset*i, lambda: BinaryHeap.canvas.delete(rightmost.node_number))
        if rightmost.arrow is not None:
            BinaryHeap.canvas.after(time_offset*i, lambda: BinaryHeap.canvas.delete(rightmost.arrow))

    def delete(self, index):
        """A method that gets index of node and delete the node by decrease the node key to -∞ and then delete the min
        key node(the root) in the heap"""
        self.nodes[index-1].change_outline_color("red")
        text = self.nodes[index-1].text
        # decrease the key to -∞
        BinaryHeap.canvas.after(time_offset*2, lambda: BinaryHeap.canvas.itemconfig(text, text="-∞"))
        i = self.decrease_key(index, self.nodes[0].key-1, True)
        rightmost_index = len(self.nodes)-1
        rightmost = self.nodes[rightmost_index]
        head = self.nodes[0]
        BinaryHeap.canvas.after(time_offset*i, lambda: head.change_outline_color("red"))
        i += 1
        # replace the root with the rightmost node
        self.nodes[0], self.nodes[rightmost_index] = self.nodes[rightmost_index], self.nodes[0]
        BinaryHeapNode.swap_nodes(head, rightmost, i, True)
        i += 1
        # delete the rightmost node
        self.delete_rightmost(i)
        i += 1
        # bubble down the new root until the heap is ordered
        if len(self.nodes) > 0:
            BinaryHeap.canvas.after(time_offset * i, lambda: self.nodes[0].change_outline_color("red"))
            i += 1
            self.bubble_down(1, i)

    def clear(self):
        """A method that clear the heap's canvas and delete the heap"""
        BinaryHeap.canvas.delete('all')
        self.nodes = []


class BinomialHeapNode:
    """A class to represent a node of the binomial heap, each instance has both attributes related to the node
    itself(such as key) and attributes related do the draw of the node(such as circle)
    Attributes:
        nodes: a static attribute that count how many nodes has been created
        children: a list of the nodes that are the children of the node
        key: the key of the node(the number inside the circle, that represent the value of the node)
        x: the x value of the center of the circle of the node
        y: the y value of the center of the circle of the node
        canvas: the canvas that the node is drawn in
        arrow: the draw of the arrow that enter the node(the arrow from the father to the node)
        circle: the draw of the circle represent the node
        text: the draw of the node key inside the circle
        node_number: the draw of the node number that appears above the node circle"""

    nodes = 1

    def __init__(self, key, canvas):
        """Init instance of class by drawing it in the left up corner of the screen"""
        self.children = []
        self.key = key
        self.x = 1300
        self.y = 80
        self.canvas = canvas
        self.arrow = None
        self.node_number = BinomialHeapNode.nodes
        tag = "node" + str(self.node_number)
        self.circle = canvas.create_oval(self.x-RADIUS, self.y-RADIUS, self.x+RADIUS, self.y+RADIUS, outline="white",
                                         tags=tag)
        self.text = canvas.create_text((self.x, self.y), text=str(key), tags=tag)
        BinomialHeapNode.nodes += 1

    def tree_size(self):
        """A method that returns the size of the binomial tree rooted by the node(the number of descendants
         a node have)"""
        height = 0
        node = self
        while len(node.children) != 0:
            node = node.children[-1]
            height += 1
        return 2**height

    def update(self, x_offset, y_offset):
        """A method that gets x and y values, and update the node and all its descendants x and y values by adding these
        values to them"""
        self.x += x_offset
        self.y += y_offset
        for child in self.children:
            child.update(x_offset, y_offset)

    def update_tag(self, tag):
        """A method that gets a tag and replace the tag of the node and all its descendants with that tag"""
        BinomialHeap.canvas.itemconfig(self.circle, tags=tag)
        BinomialHeap.canvas.itemconfig(self.text, tags=tag)
        BinomialHeap.canvas.itemconfig(self.arrow, tags=tag)
        for child in self.children:
            child.update_tag(tag)

    def connect(self, i, father=None, root_tag=1, x=0, y=0):
        """A method that gets a father and connect the node to the father"""
        # first case: the father is None and therefore the node should be root
        if father is None:
            self.canvas.delete(self.circle)
            self.canvas.delete(self.text)
            self.x = x
            self.y = y
            self.circle = self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS, outline="white",
                                                  tags=root_tag)
            self.text = self.canvas.create_text((x, y), text=str(self.key), tags=root_tag)
            return self
        # second case: the father is not None, connect the node to the father
        arrow_x = father.x
        arrow_y = father.y + RADIUS
        arrow_length_y = father.y + ARROW_LENGTH_Y
        if len(father.children) == 0:
            arrow_length_x = father.x
        else:
            arrow_length_x = father.leftmost_descendant() - 100
        father.children.append(self)
        tag = self.canvas.itemcget(father.circle, "tags")
        self.canvas.after(time_offset*i, lambda: self.add_arrow(arrow_x, arrow_y, arrow_length_x, arrow_length_y,
                                                                "last", tag))
        move_x = arrow_length_x - self.x
        move_y = arrow_length_y + RADIUS - self.y
        move_tag = self.canvas.itemcget(self.circle, "tags")
        end_y = max(self.y, father.y) - father.y
        end_x = min(self.x, father.x) - father.x
        self.canvas.after(time_offset*i, lambda: BinomialHeap.delete_line(self))
        self.canvas.after(time_offset*i, lambda: self.canvas.move(move_tag, move_x, move_y))
        self.canvas.after(time_offset*i, lambda: self.canvas.itemconfig(move_tag, tags=tag))
        self.update(move_x, move_y)
        self.canvas.after(time_offset*i, lambda: self.canvas.move(tag, end_x, end_y))
        self.canvas.after(time_offset*i, lambda: BinomialHeap.delete_line(father))
        father.update(end_x, end_y)
        return father, self

    def add_arrow(self, x1, y1, x2, y2, arrow, tag):
        """A method that adds arrow according to the x, y, arrow type and tag it gets"""
        self.arrow = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow, tags=tag)

    def leftmost_descendant(self, y=False):
        """A method that return the x value of the leftmost descendant if y=False(default) and the y value of the
        leftmost descendant if y=True"""
        node = self
        sons = self.children
        while len(sons) != 0:
            node = sons[-1]
            sons = node.children
        if y:
            return node.y
        return node.x

    def change_outline_color(self, color):
        """A method that get a color and replace the color of the outline of the circle with the new color"""
        self.canvas.itemconfig(self.circle, outline=color)


class BinomialHeap:
    """A class that represent binomial heap.
    Attributes:
        canvas: a static attribute of the canvas that the heap is drawn in
        root_lines: a dictionary that its values are the lines connected the roots, the key of each line is the root
        that the line start from
        root: a list of the roots of the heap"""
    canvas = None
    roots_lines = {}

    @staticmethod
    def set_canvas(page):
        """A static method that changes the canvas of the class"""
        BinomialHeap.canvas = page

    @staticmethod
    def add_line(root, x1, y1, x2, y2, tag):
        """A static method that adds line to the canvas and to the lines dictionary according to the x, y and tag it
        gets"""
        line = BinomialHeap.canvas.create_line(x1, y1, x2, y2, tags=tag)
        BinomialHeap.roots_lines[root] = line

    @staticmethod
    def delete_line(root):
        """A static method that delete a line(if exists) according to the root the line start from(the key of the line
        in the dictionary of the lines)"""
        if root in BinomialHeap.roots_lines.keys():
            BinomialHeap.canvas.delete(BinomialHeap.roots_lines[root])

    @staticmethod
    def delete_root(root, right_root):
        """A static method that delete a root from the canvas"""
        circle = root.circle
        text = root.text
        BinomialHeap.canvas.delete(circle)
        BinomialHeap.canvas.delete(text)
        BinomialHeap.delete_line(root)
        BinomialHeap.delete_line(right_root)
        for child in root.children:
            arrow = child.arrow
            BinomialHeap.canvas.delete(arrow)

    def __init__(self, roots=None):
        """Init the roots list with the given roots, and set the list to be empty list if the given roots are
        None(default)"""
        if roots is None:
            self.roots = []
        else:
            self.roots = roots

    def heap_size(self):
        """A method that returns the size of the heap(the number of nodes in the heap)"""
        size = 0
        for root in self.roots:
            size += root.tree_size()
        return size

    def add_root(self, root, i, x=0, y=0):
        """A method that gets a root and add it to the heap"""
        tag = BinomialHeap.canvas.itemcget(root.circle, "tags")
        self.roots.append(root)
        # first case: the root is the first root in the heap, no need for line
        if len(self.roots) == 1:
            move_x = x - root.x
            move_y = y - root.y
        # second case: the root is not the first root in the heap, connect the root with line to the other roots
        else:
            leftmost_root = self.roots[-2]
            leftmost_x = leftmost_root.leftmost_descendant()
            line_tag = BinomialHeap.canvas.itemcget(leftmost_root.circle, "tags")
            x = leftmost_root.x
            y = leftmost_root.y
            BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.add_line(leftmost_root, x-RADIUS, y,
                                                                                   leftmost_x-60, y, line_tag))
            move_x = leftmost_x - 60 - RADIUS - root.x
            move_y = leftmost_root.y - root.y
        BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.delete_line(root))
        BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.canvas.move(tag, move_x, move_y))
        root.update(move_x, move_y)

    def place_new_root(self, root, wait_time, heap1, heap2):
        """A method that gets a root and two heaps, and calculate where to place the root on the screen"""
        x, y = 0, 0
        # first case: the heap is empty but the given heaps are not empty, place the root on the left side of the
        # screen, below both of the heaps
        if len(self.roots) == 0 and len(heap1.roots) > 0 and len(heap2.roots) > 0:
            x = 1000
            y = max(heap1.roots[-1].leftmost_descendant(True), heap2.roots[-1].leftmost_descendant(True)) + 100
        # second case: one of the given heaps is empty, place the root in the start of the non-empty heap
        elif len(heap1.roots) == 0:
            x, y = heap2.roots[0].x, heap2.roots[0].y
        elif len(heap2.roots) == 0:
            x, y = heap1.roots[0].x, heap1.roots[0].y
        self.add_root(root, wait_time, x, y)

    def union(self, heap2):
        """A function that gets a heap and union the current heap(self) with the given heap.
        the union is similar to binary addition. we represent the number of nodes in each heap in binary, and in each
        digit in the place i, if the digit is 1 there is a binomial tree from order i in the heap.
        if both of the heaps has 1 in the i-th digit for some i, union these trees to binomial tree of order i+1"""
        bin_heap1 = bin(self.heap_size())[-1:1:-1]
        bin_heap2 = bin(heap2.heap_size())[-1:1:-1]
        heap1_pointer = 0
        heap2_pointer = 0
        carry = 0
        new_heap = BinomialHeap()
        wait_time = 2
        # add zeros the shortest number for the numbers to be in the same length
        if len(bin_heap1) > len(bin_heap2):
            diff = len(bin_heap1) - len(bin_heap2)
            bin_heap2 = bin_heap2 + "0"*diff
        elif len(bin_heap1) < len(bin_heap2):
            diff = len(bin_heap2) - len(bin_heap1)
            bin_heap1 = bin_heap1 + "0"*diff
        for i in range(len(bin_heap1)):
            root = None
            son = None
            # first case: both heaps has binomial tree of order i, union these tree and create binomial tree of order
            # i+1, therefor set carry to 1, because we "carry" another tree of i+1 order to the next digits
            if bin_heap1[i] == "1" and bin_heap2[i] == "1":
                root = self.roots[heap1_pointer]
                son = heap2.roots[heap2_pointer]
                # replace between the son and the father in case that the son's key is lower than the father's
                # key(because the father's key must be lower than all his children keys)
                if son.key < root.key:
                    son, root = root, son
                new_heap.place_new_root(root, wait_time, self, heap2)
                wait_time += 1
                root, son = son.connect(wait_time, root)
                root = None
                wait_time += 1
                heap1_pointer += 1
                heap2_pointer += 1
                carry = 1
            # second case: not both heaps has binomial heap of order i, but carry=1 meaning there is binomial heap of
            # order i from the last addition
            elif carry == 1:
                # if only one of the heaps has binomial tree of order i, union this tree with the previous tree
                if bin_heap1[i] == "1":
                    son = self.roots[heap1_pointer]
                    root = new_heap.roots[-1]
                    # replace between the son and the father in case that the son's key is lower than the father's
                    # key(because the father's key must be lower than all his children keys)
                    if son.key < root.key:
                        new_heap.roots[-1] = son
                        son, root = root, son
                    root, son = son.connect(wait_time, root)
                    root = None
                    heap1_pointer += 1
                    wait_time += 1
                elif bin_heap2[i] == "1":
                    son = heap2.roots[heap2_pointer]
                    root = new_heap.roots[-1]
                    # replace between the son and the father in case that the son's key is lower than the father's
                    # key(because the father's key must be lower than all his children keys)
                    if son.key < root.key:
                        new_heap.roots[-1] = son
                        son, root = root, son
                    root, son = son.connect(wait_time, root)
                    root = None
                    heap2_pointer += 1
                    wait_time += 1
                # if none of the heaps has binomial tree of order i, set carry to 0
                else:
                    carry = 0
            # third case: carry = 0 and just one of the heaps has binomial tree of order i, add this tree to the new
            # united heap
            elif bin_heap1[i] == "1":
                root = self.roots[heap1_pointer]
                heap1_pointer += 1
            elif bin_heap2[i] == "1":
                root = heap2.roots[heap2_pointer]
                heap2_pointer += 1
            # if node that become a son is in the roots list, remove it from the list(it's not root anymore)
            if son in new_heap.roots:
                new_heap.roots.remove(son)
            # add root if needed
            if root is not None:
                new_heap.place_new_root(root, wait_time, self, heap2)
                wait_time += 1
        # place the heap in the right position again
        BinomialHeap.canvas.after(time_offset*wait_time, lambda: self.place_heap(new_heap.roots))
        return wait_time

    def place_heap(self, roots):
        """A method that gets a roots and change the heap roots to the given roots, and after that move the heap to
        the default position, near the right left corner"""
        self.change_roots(roots)
        y = 80 - self.roots[0].y
        x = 1000 - self.roots[0].x
        for root in self.roots:
            tag = BinomialHeap.canvas.itemcget(root.circle, "tags")
            BinomialHeap.canvas.move(tag, x, y)
            root.update(x, y)

    def insert(self, key):
        """A method that gets key, create a node with that key and insert the node to the heap"""
        node = BinomialHeapNode(key, BinomialHeap.canvas)
        # first case: the heap is empty, just create and position the node
        if len(self.roots) == 0:
            tag = BinomialHeap.canvas.itemcget(node.circle, "tags")
            node.connect(1, None, tag, 900, 80)
            self.roots.append(node)
        # second case: the heap is not empty, create a heap containing only this node and union this heap with our heap
        else:
            roots = [node]
            heap = BinomialHeap(roots)
            self.union(heap)

    def find_min(self, show_message=True):
        """A method that find the min-key node in the heap
        each father must have key lower(or equal to) than all his children, therefore, the min must be one of the roots,
        the method search in the roots for the min"""
        if len(self.roots) > 0:
            min_key = self.roots[0].key
            min_root = self.roots[0]
            i = 2
            for root in self.roots:
                BinomialHeap.canvas.after(time_offset*i, lambda cap_root=root: cap_root.change_outline_color("red"))
                i += 1
                BinomialHeap.canvas.after(time_offset*i, lambda cap_root=root: cap_root.change_outline_color("white"))
                if root.key < min_key:
                    min_key = root.key
                    min_root = root
            message = "the min is: " + str(min_key)
            BinomialHeap.canvas.after(time_offset * i, lambda: min_root.change_outline_color("red"))
            if show_message:
                BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.canvas.create_text(
                    (800, 15), text=message, font=("Ariel", 20), tags="min_message"))
                BinaryHeap.canvas.after(time_offset*(i+1), lambda: BinomialHeap.canvas.delete("min_message"))
                BinaryHeap.canvas.after(time_offset*(i+1), lambda: min_root.change_outline_color("white"))
            return min_root, i+1

    def change_roots(self, new_roots):
        """A method that gets a roots and change the heap roots to the new roots"""
        self.roots = new_roots

    def delete_min(self):
        """A method that deletes the min-key node in the heap.
        first, we search the min-key node, after that we delete these node and connect his children and union the two
        heaps that created as a result from the deletion"""
        # find the min root
        min_root, i = self.find_min(False)
        # heap 1 contains the roots from the original heap, except the min root
        heap1 = BinomialHeap()
        # heap 2 contains the children of the min node
        heap2 = BinomialHeap()
        # left contains the roots from the original heap that appears left to the min root
        left = BinomialHeap()
        # right contains the roots from the original heap that appears right to the min root
        right = BinomialHeap()
        right_flag = 1
        right_root = None
        prev = None
        children = min_root.children
        # fill heap1, heap2, right and left
        for root in self.roots:
            if root != min_root:
                heap1.roots.append(root)
                if right_flag:
                    right.roots.append(root)
                else:
                    left.roots.append(root)
                prev = root
            else:
                right_flag = 0
                right_root = prev
        for child in children:
            heap2.roots.append(child)
        # delete the min root
        BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.delete_root(min_root, right_root))
        # update the tags of the children
        for child in min_root.children:
            tag = "node" + str(child.node_number)
            child.update_tag(tag)
        i += 1
        # connect all the children to get one heap
        for j in range(len(children)-1):
            start_x, start_y = children[j].x, children[j].y
            end_x, end_y = children[j+1].x, children[j+1].y
            root = children[j]
            tag = BinomialHeap.canvas.itemcget(root.circle, "tags")
            BinomialHeap.canvas.after(
                                      time_offset * i,
                                      lambda child_root=root, start_x_child=start_x, start_y_child=start_y,
                                      end_x_child=end_x, end_y_child=end_y, child_tag=tag: BinomialHeap.add_line(
                                          child_root, start_x_child - RADIUS, start_y_child, end_x_child + RADIUS,
                                          end_y_child, child_tag))
            if j == len(children) - 2:
                i += 1
        # if the right roots heap and the children heap are not empty, swap their positions(in order to be able to
        # connect the right and left heap)
        if len(right.roots) != 0 and len(heap2.roots) != 0:
            rightmost = right.roots[0]
            move_x_heap2 = rightmost.x - heap2.roots[0].x
            move_y_heap2 = rightmost.y - heap2.roots[0].y
            # move the children to the right heap place
            for root in heap2.roots:
                tag_heap2 = BinomialHeap.canvas.itemcget(root.circle, "tags")
                BinomialHeap.canvas.after(time_offset*i, lambda cap_tag_heap2=tag_heap2: BinomialHeap.canvas.move(
                    cap_tag_heap2, move_x_heap2, move_y_heap2))
                root.update(move_x_heap2, move_y_heap2)
            leftmost = heap2.roots[-1]
            move_x_right = leftmost.x - 60 - RADIUS - rightmost.x
            move_y_right = leftmost.y - rightmost.y
            # move the right heap roots to the children place
            for root in right.roots:
                tag_right = BinomialHeap.canvas.itemcget(root.circle, "tags")
                BinomialHeap.canvas.after(time_offset*i, lambda cap_tag_right=tag_right: BinomialHeap.canvas.move(
                    cap_tag_right, move_x_right, move_y_right))
                root.update(move_x_right, move_y_right)
            i += 1
        # if the left and right heaps are not empty, connect them
        if len(right.roots) != 0 and len(left.roots) != 0:
            root_right = right.roots[-1]
            root_left = left.roots[0]
            start_x, start_y = root_right.x, root_right.y
            end_x, end_y = root_left.x, root_left.y
            tag_right_circle = BinomialHeap.canvas.itemcget(root_right.circle, "tags")
            BinomialHeap.canvas.after(time_offset*i, lambda: BinomialHeap.add_line(
                root_right, start_x - RADIUS, start_y, end_x + RADIUS, end_y, tag_right_circle))
            i += 1
        # set the self roots as the non-children roots
        self.roots = heap1.roots
        # union the 2 heaps(the children heap and the non-children heap)
        BinomialHeap.canvas.after(time_offset*i, lambda: self.union(heap2))

    def clear(self):
        """A method that clear the heap's canvas and delete the heap"""
        BinomialHeap.canvas.delete('all')
        self.roots = []


def error_message(canvas):
    """A function that shows error message in case not valid value enters"""
    text = canvas.create_text((85, 15), text="please enter valid values")
    canvas.after(time_offset, lambda: canvas.delete(text))


class DataStructures:
    """A class that contains the data structures"""
    def __init__(self):
        self.binary_heap = BinaryHeap()
        self.binomial_heap = BinomialHeap()

    def command(self, data_structure, title, entry=None):
        """A method that gets a command according to the user actions and handle the command"""
        global user
        to_add = 0
        if data_structure == "binary_heap":
            try:
                if title == "insert":
                    self.binary_heap.insert(int(entry))
                    to_add = 1
                elif title == "delete":
                    self.binary_heap.delete(int(entry))
                    to_add = 1
                elif title == "decrease key":
                    entry = entry.split(",")
                    node_number, new_key = entry[0], entry[1]
                    self.binary_heap.decrease_key(int(node_number), int(new_key))
                    to_add = 1
                elif title == "clear":
                    self.binary_heap.clear()
            except (ValueError, IndexError):
                error_message(BinaryHeap.canvas)

        elif data_structure == "binomial_heap":
            try:
                if title == "insert":
                    self.binomial_heap.insert(int(entry))
                    to_add = 1
                elif title == "find min":
                    self.binomial_heap.find_min()
                    to_add = 1
                elif title == "delete min":
                    self.binomial_heap.delete_min()
                    to_add = 1
                elif title == "clear":
                    self.binomial_heap.clear()
            except ValueError:
                error_message(BinomialHeap.canvas)
        if to_add == 1:
            data_structure_update = user[data_structure]
            old_value = data_structure_update[title]
            new_value = {"$set": {data_structure + "." + title: old_value+1}}
            collection.update_one(user, new_value)
            username = user["username"]
            user = collection.find_one({"username": username})
            old_total = user["total"]
            new_total = {"$set": {"total": old_total+1}}
            collection.update_one(user, new_total)
            username = user["username"]
            user = collection.find_one({"username": username})


data_structures = DataStructures()


def create_page(page, title, scroll=True):
    """A function that create a default and basic page to the data structures"""
    # create top
    page.rowconfigure(0, weight=1)
    page.rowconfigure(1, weight=10)
    page.columnconfigure(0, weight=1)
    top = customtkinter.CTkFrame(page)
    top.grid(row=0, column=0, sticky="news")
    title = customtkinter.CTkLabel(top, text=title, font=("Ariel", 30, "bold"))
    title.pack()
    back_button = customtkinter.CTkButton(top, text="back", command=lambda: App.change_page("home_page"))
    back_button.place(relx=0, rely=0)
    # create bottom, with scroll if needed
    if scroll:
        bottom = customtkinter.CTkCanvas(page, scrollregion=(-10000, 0, 10000, 10000))
        bottom.grid(row=1, column=0, sticky="news")
        vertical_scrollbar = customtkinter.CTkScrollbar(master=bottom, command=bottom.yview)
        horizontal_scrollbar = customtkinter.CTkScrollbar(master=bottom, orientation="horizontal",
                                                          command=bottom.xview)
        vertical_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        horizontal_scrollbar.place(relx=0, rely=1, relwidth=1, anchor='sw')
        bottom.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    else:
        bottom = customtkinter.CTkCanvas(page)
        bottom.grid(row=1, column=0, sticky="news")
    return top, bottom


def clear(entry):
    """A function that gets an entry and clear it"""
    entry.delete(0, customtkinter.END)


def entry_pressed(entry, title, data_structure):
    """A function that executed when entry pressed"""
    entered = entry.get()
    clear(entry)
    data_structures.command(data_structure, title, entered)


def create_entry(page, command, data_structure, x_label, x_entry, y_label, text=""):
    """A function that create entry according to the given values of x, y, the command(the label before the entry) and
    the text(the text that written inside the entry(if there is)"""
    label = customtkinter.CTkLabel(page, text=command + ": ")
    label.place(x=x_label, y=y_label)
    entry = customtkinter.CTkEntry(page)
    if text != "":
        entry.insert(0, text)
    entry.place(x=x_entry, y=y_label)
    entry.bind("<Return>", lambda event: entry_pressed(entry, command, data_structure))


def create_button(page, command, data_structure, x_button, y_button):
    """A function that crates a button according the given values x, y and command"""
    button = customtkinter.CTkButton(page, text=command, command=lambda: data_structures.command(data_structure,
                                                                                                 command))
    button.place(x=x_button, y=y_button)


def change_animation_speed(option):
    """A function that changes the animation speed when the option menu pressed according to the chosen option"""
    global time_offset
    if option == "very slow":
        time_offset = 1550
    elif option == "slow":
        time_offset = 1150
    elif option == "average":
        time_offset = 750
    elif option == "fast":
        time_offset = 550
    elif option == "very fast":
        time_offset = 350


class App(customtkinter.CTk):
    """A class that represent the app of the project with all it pages.
    Attributes:
        pages: a static attribute of dictionary that its values are the pages of the app, to key to each page is his
        name
        geometry: the size of the screen of the app
        title: the app's title"""
    pages = {}

    @staticmethod
    def change_page(next_page):
        """A static method that given a page and change the display to the given page"""
        for page in App.pages.keys():
            # unpack all the non-given pages
            if page != next_page:
                App.pages[page].pack_forget()
            # pack the given page
            else:
                App.pages[page].pack(fill=tkinter.BOTH, expand=True)

    def __init__(self):
        """Init the app with the geometry and title and display the home page"""
        super().__init__()
        self.geometry("1024x768")
        self.title("data structures visualization")
        main_container = customtkinter.CTkFrame(self)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        App.pages["home_page"] = HomePage(main_container)
        App.pages["binary_heap"] = BinaryHeapPage(main_container)
        App.pages["binomial_heap"] = BinomialHeapPage(main_container)
        App.pages["login_page"] = LoginPage(main_container)
        App.pages["signup_page"] = SignUpPage(main_container)
        App.pages["manager_page"] = ManagerPage(main_container)
        App.pages["user_stats_page"] = UserStatsPage(main_container)
        App.pages["login_page"].pack(fill=tkinter.BOTH, expand=True)


class BinomialHeapPage(customtkinter.CTkFrame):
    """A class for binomial heap page"""
    def __init__(self, container):
        """Init method that create the canvas and the top with the entries and the buttons of the page"""
        super().__init__(container)
        top, bottom = create_page(self, "binomial heap")
        BinomialHeap.set_canvas(bottom)
        create_entry(top, "insert", "binomial_heap", 5, 45, 50)
        create_button(top, "find min", "binomial_heap", 200, 50)
        create_button(top, "delete min", "binomial_heap", 350, 50)
        create_button(top, "clear", "binomial_heap", 1350, 50)


class BinaryHeapPage(customtkinter.CTkFrame):
    """A class for binary heap page"""
    def __init__(self, container):
        """Init method that create the canvas and the top with the entries and the buttons of the page"""
        super().__init__(container)
        top, bottom = create_page(self, "binary heap", False)
        BinaryHeap.set_canvas(bottom)
        create_entry(top, "insert", "binary_heap", 5, 45, 50)
        create_entry(top, "delete", "binary_heap", 200, 250, 50, "node number")
        create_entry(top, "decrease key", "binary_heap", 400, 490, 50, "node number, new key")
        create_button(top, "clear", "binary_heap", 1350, 50)


class HomePage(customtkinter.CTkFrame):
    """A class for the home page"""
    def __init__(self, container):
        """Init method that create the home page with buttons for the binary and binomial heaps and option menu to
        choose the animation speed"""
        super().__init__(container)
        title = customtkinter.CTkLabel(self, text="which data structure do you want to visualize?")
        title.pack()
        binary_heap_button = customtkinter.CTkButton(self, text="binary heap",
                                                     command=lambda: App.change_page("binary_heap"))
        binary_heap_button.pack(padx=10, pady=10)
        binomial_heap_button = customtkinter.CTkButton(self, text="binomial heap",
                                                       command=lambda: App.change_page("binomial_heap"))
        binomial_heap_button.pack(padx=10, pady=10)
        speed_options = ["very fast", "fast", "average", "slow", "very slow"]
        animation_speed_label = customtkinter.CTkLabel(self, text="choose animation speed:")
        animation_speed_label.pack(padx=10, pady=10)
        speed_menu = customtkinter.CTkOptionMenu(master=self, values=speed_options, command=change_animation_speed)
        speed_menu.pack(padx=10, pady=2)
        # set the default animation speed to average
        speed_menu.set("average")
        # create logout button
        logout_button = customtkinter.CTkButton(self, text="logout", command=lambda: HomePage.logout(speed_menu))
        logout_button.place(x=0, y=0)
        # create stats button
        stats_button = customtkinter.CTkButton(self, text="stats", command=lambda: HomePage.stats())
        stats_button.pack(padx=10, pady=10)

    @staticmethod
    def stats():
        """A static method that update the stats screen and load the screen according to the user type(regular or
        manager)"""
        username = user["username"]
        if username == MANAGER:
            App.pages["manager_page"].create_table()
            App.change_page("manager_page")
        else:
            App.pages["user_stats_page"].show_stats()
            App.change_page("user_stats_page")

    @staticmethod
    def set_speeed_menu(menu, speed):
        menu.set(speed)
        change_animation_speed(speed)

    @staticmethod
    def logout(speed_menu):
        """A static method that logs out the current user"""
        global user
        user = None
        HomePage.set_speeed_menu(speed_menu, "average")
        data_structures.binary_heap.clear()
        data_structures.binomial_heap.clear()
        App.change_page("login_page")


class UserPage(customtkinter.CTkFrame):
    """A class for the user pages, the pages of the login and signup"""
    def __init__(self, container, text):
        """Init method that create the screen with the entries for username and password"""
        super().__init__(container)
        title_label = customtkinter.CTkLabel(self, text=text, font=("Ariel", 30, "bold"))
        title_label.place(x=650, y=10)
        username_label = customtkinter.CTkLabel(self, text="username: ")
        username_label.place(x=690, y=120)
        self.username_entry = customtkinter.CTkEntry(self)
        self.username_entry.place(x=770, y=120)
        password_label = customtkinter.CTkLabel(self, text="password: ")
        password_label.place(x=690, y=200)
        self.password_entry = customtkinter.CTkEntry(self, show="*")
        self.password_entry.place(x=770, y=200)
        self.password_state = "*"
        self.password_button = customtkinter.CTkButton(self, text="show", width=60,
                                                       command=lambda: self.change_password_state())
        self.password_button.place(x=915, y=200)
        self.message_label = ""

    def change_password_state(self):
        """A method to change the password state between the 2 states: decrypted(shows '*') and regular"""
        # first case: current state is decrypt(need to change to regular)
        if self.password_state == "*":
            self.password_state = ""
            self.password_button.configure(text="hide")
            self.password_entry.configure(show="")
        # second case: current state is regular(need to change to decrypt)
        else:
            self.password_state = "*"
            self.password_button.configure(text="show")
            self.password_entry.configure(show="*")

    def clear_entries(self):
        """A method that returns the content in the username and password entries and clear them"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        clear(self.username_entry)
        clear(self.password_entry)
        return username, password

    def delete_message(self):
        """A method that deletes the message that appears on the screen"""
        self.message_label.destroy()
        self.message_label = ""


class LoginPage(UserPage):
    """A class for the login page"""
    def __init__(self, container):
        """Init method that creates the screen for the login page"""
        title = "login to your account"
        super().__init__(container, title)
        enter = customtkinter.CTkButton(self, text="enter", command=lambda: self.login())
        enter.place(x=745, y=280)
        sign_up_label = customtkinter.CTkLabel(self, text="don't have an account? ")
        sign_up_label.place(x=650, y=380)
        sign_up_button = customtkinter.CTkButton(self, text="sign up here", command=lambda: App.change_page(
            "signup_page"))
        sign_up_button.place(x=800, y=380)

    def login(self):
        """A method that checks if the username and password that entered are in the database"""
        global user
        username, password = self.clear_entries()
        username_database = collection.find_one({"username": username})
        message = ""
        # if the user exists
        if username_database:
            if password == username_database['password']:
                user = username_database
                App.change_page("home_page")
            else:
                message = "username and password do not match"
        else:
            message = "username didn't found"
        if message != "":
            if self.message_label != "":
                self.message_label.destroy()
            self.message_label = customtkinter.CTkLabel(self, text=message)
            if message == "username didn't found":
                self.message_label.place(x=745, y=320)
                self.message_label.after(time_offset * 2, lambda: self.delete_message())
            else:
                self.message_label.place(x=680, y=320)
                self.message_label.after(time_offset * 2, lambda: self.delete_message())


class SignUpPage(UserPage):
    """A class for the signup page"""
    def __init__(self, container):
        """Init method that creates the screen for the signup page"""
        title = "create you account"
        super().__init__(container, title)
        sign_up_button = customtkinter.CTkButton(self, text="sign up", command=lambda: self.sign_up())
        sign_up_button.place(x=740, y=270)
        back_button = customtkinter.CTkButton(self, text="back to login", command=lambda: App.change_page("login_page"))
        back_button.place(x=0, y=0)

    def sign_up(self):
        """A method that signs up a new user to the app"""
        username = self.username_entry.get()
        already_exists = collection.find_one({"username": username})
        if already_exists:
            message = "this username already exists. try another one"
            if self.message_label != "":
                self.message_label.destroy()
            self.message_label = customtkinter.CTkLabel(self, text=message)
            self.message_label.place(x=680, y=300)
            self.message_label.after(time_offset * 2, lambda: self.delete_message())
            return
        password = self.password_entry.get()
        if self.check_password(password):
            username, password = self.clear_entries()
            # add the user data to the database
            binary_heap_stats = {"insert": 0, "delete": 0, "decrease key": 0}
            binomial_heap_stats = {"insert": 0, "find min": 0, "delete min": 0}
            to_add = {"username": username, "password": password, "binary_heap": binary_heap_stats,
                      "binomial_heap": binomial_heap_stats, "total": 0}
            collection.insert_one(to_add)

    def check_password(self, password):
        """A method that gets a password and check if the password satisfy the condition"""
        if len(password) < 8:
            message = "the length of the password should be at least 8!"
        else:
            number = 0
            lowercase_letter = 0
            capital_letter = 0
            for char in password:
                if char.isnumeric():
                    number = 1
                elif char.isalpha() and char.islower():
                    lowercase_letter = 1
                elif char.isalpha() and char.isupper():
                    capital_letter = 1
            if lowercase_letter == 0:
                message = "the password must contain at least one lower case letter!"
            elif capital_letter == 0:
                message = "the password must contain at least one capital letter!"
            elif number == 0:
                message = "the password must contain at least one number!"
            else:
                message = "successfully registered!"
        if self.message_label != "":
            self.message_label.destroy()
        self.message_label = customtkinter.CTkLabel(self, text=message)
        if message != "successfully registered!":
            self.message_label.place(x=680, y=300)
            self.message_label.after(time_offset * 2, lambda: self.delete_message())
            return False
        self.message_label.place(x=730, y=300)
        self.message_label.after(time_offset*2, lambda: self.delete_message())
        return True


class ManagerPage(customtkinter.CTkCanvas):
    """A class for the manager stats page, the page contains the stats of all the users"""
    def __init__(self, container):
        super().__init__(container, scrollregion=(0, 0, 0, 10000))
        scrollbar = customtkinter.CTkScrollbar(master=self, command=self.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        self.configure(yscrollcommand=scrollbar.set)

    def create_table(self):
        """A method that draws and creates the stats table of the manager"""
        # delete the old stats
        self.delete('all')
        self.create_text((850, 35), text="stats table", font=("Ariel", 40, "bold"))
        back_button = customtkinter.CTkButton(self, text="back", command=lambda: App.change_page("home_page"))
        back_button.grid(row=0, column=0)
        count = collection.count_documents({})
        if count == 0:
            count = 1
        line_len = max(620, 20+(count+4)*35)
        # draw the table
        self.create_line(400, 100, 400, line_len)
        self.create_line(310, 130, 1390, 130)
        self.create_line(850, 100, 850, line_len)
        self.create_line(1290, 100, 1290, line_len)
        self.create_text((625, 120), text="Binary Heap", font=("Ariel", 20, "bold"))
        self.create_text((1075, 120), text="Binomial Heap", font=("Ariel", 20, "bold"))
        self.create_text((1335, 120), text="total", font=("Ariel", 20, "bold"))
        self.create_text((350, 150), text="username")
        self.create_text((470, 150), text="insert")
        self.create_line(550, 130, 550, line_len)
        self.create_text((620, 150), text="delete")
        self.create_line(700, 130, 700, line_len)
        self.create_text((770, 150), text="decrease key")
        self.create_text((920, 150), text="insert")
        self.create_line(1000, 130, 1000, line_len)
        self.create_text((1070, 150), text="find min")
        self.create_line(1150, 130, 1150, line_len)
        self.create_text((1220, 150), text="delete min")
        data = collection.find({})
        users_total = {}
        totals = []
        # add every user to the dictionary
        for document in data:
            username = document["username"]
            total = document["total"]
            if total in totals:
                users_total[total].append(username)
            else:
                users_total[total] = [username]
                totals.append(total)
        # sort the total in descending way
        totals.sort()
        totals = totals[::-1]
        y = 165
        for total in totals:
            usernames = users_total[total]
            # add all the users to the table
            for username in usernames:
                database_user = collection.find_one({"username": username})
                self.add_user(database_user, y)
                y += 35

    def add_user(self, database_user, y):
        """A method that gets a user and adds his data to the stats table"""
        self.create_line(310, y, 1390, y)
        self.create_text((350, y+20), text=str(database_user["username"]))
        self.create_text((470, y+20), text=str(database_user["binary_heap"]["insert"]))
        self.create_text((620, y+20), text=str(database_user["binary_heap"]["delete"]))
        self.create_text((770, y+20), text=str(database_user["binary_heap"]["decrease key"]))
        self.create_text((920, y+20), text=str(database_user["binomial_heap"]["insert"]))
        self.create_text((1070, y+20), text=str(database_user["binomial_heap"]["find min"]))
        self.create_text((1220, y+20), text=str(database_user["binomial_heap"]["delete min"]))
        self.create_text((1335, y+20), text=str(database_user["total"]))


class UserStatsPage(customtkinter.CTkFrame):
    """A class for the pages of the stats for regular user, the page contains the stats of the current user only"""
    def __init__(self, container):
        """Init method that creates the page"""
        super().__init__(container)

    def show_stats(self):
        """A method that add the stats of the user to the page"""
        # delete the old stats
        for widget in self.winfo_children():
            widget.destroy()
        title = customtkinter.CTkLabel(self, text="my stats", font=("Ariel", 40, "bold"))
        title.place(x=650, y=35)
        back_button = customtkinter.CTkButton(self, text="back", command=lambda: App.change_page("home_page"))
        back_button.place(x=0, y=0)
        binary_heap_label = customtkinter.CTkLabel(self, text="Binary Heap:", font=("Ariel", 30, "bold"))
        binary_heap_label.place(x=5, y=100)
        self.create_row("binary_heap", "insert", 90, 135)
        self.create_row("binary_heap", "delete", 90, 170)
        self.create_row("binary_heap", "decrease key", 160, 205)
        binomial_heap_label = customtkinter.CTkLabel(self, text="Binomial Heap:", font=("Ariel", 30, "bold"))
        binomial_heap_label.place(x=5, y=250)
        self.create_row("binomial_heap", "insert", 90, 285)
        self.create_row("binomial_heap", "find min", 110, 320)
        self.create_row("binomial_heap", "delete min", 130, 355)
        total_label = customtkinter.CTkLabel(self, text="total: ", font=("Ariel", 25))
        total_label.place(x=5, y=400)
        total_num_label = customtkinter.CTkLabel(self, text=str(user["total"]), font=("Ariel", 25))
        total_num_label.place(x=65, y=400)

    def create_row(self, data_structure, text, x, y):
        """A method that create a row of type command: number of uses(for example, insert: 20)"""
        text_label = customtkinter.CTkLabel(self, text="-" + text + ":", font=("Ariel", 20))
        text_label.place(x=20, y=y)
        num_label = customtkinter.CTkLabel(self, text=str(user[data_structure][text]), font=("Ariel", 20))
        num_label.place(x=x, y=y)


def main():
    # create an app
    app = App()
    # run the app
    app.mainloop()


if __name__ == '__main__':
    main()
