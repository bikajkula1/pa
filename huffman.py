import heapq

def GetHistogram(ulazni_karakteri):
    histogram_dict = {}
    for slovo in ulazni_karakteri:
        if slovo in histogram_dict:
            histogram_dict[slovo] += 1
        else:
            histogram_dict[slovo] = 1
    return histogram_dict


class Node:
    def __init__(self, parent=None, left=None, right=None, data=None, freq=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.data = data
        self.freq = freq

    def __lt__(self,other):
        return self.freq < other.freq


class Tree:
    def __init__(self, root = None):
        self.root = root

    def initialize(self, histogram_dict):
        node_list = []
        for key,value in histogram_dict.items():
            node_list.append(Node(data=key,freq=value))

        node_list_sorted = sorted(node_list, key=lambda x: x.freq, reverse=True)
        priority_queue = []
        for node in node_list_sorted:
            heapq.heappush(priority_queue, node)

        while len(priority_queue) > 1:
            left_node = heapq.heappop(priority_queue)
            right_node = heapq.heappop(priority_queue)
            new_freq = left_node.freq + right_node.freq
            new_node = Node(data=None, freq=new_freq)
            new_node.left = left_node
            new_node.right = right_node
            left_node.parent = new_node
            right_node.parent = new_node
            heapq.heappush(priority_queue, new_node)

        return heapq.heappop(priority_queue)

    def get_min(self, node):
        if node.data != None:
            return node
        left = self.get_min(node.left)
        right = self.get_min(node.right)
        if left.freq < right.freq:
            return left
        else:
            return right

    def find_el(self, key, node):
        if node == None:
            return None
        if node.data == key:
            return node
        left = self.find_el(key, node.left)
        right =self.find_el(key, node.right)
        if left != None:
            return left
        if right != None:
            return right
        return None

    def delete_el(self, key):
        node = self.find_el(key,self.root)

        parent = node.parent.parent
        if node.parent.left == node:
            brother = node.parent.right
        else:
            brother = node.parent.left

        if parent.left == node.parent:
            parent.left = brother
        else:
            parent.right = brother

        while parent != None:
            parent.freq -= node.freq
            parent = parent.parent

    def encode(self, node):
        encoded_string = ''
        parent = node
        while parent.parent is not None:
            parent = parent.parent
            if parent.left == node:
                encoded_string += '0'
            else:
                encoded_string += '1'
            node = parent
        return encoded_string[::-1]

    def huffman_coding(self, sequence):
        histogram = {}
        histogram_dict = GetHistogram(sequence)
        self.root = self.initialize(histogram_dict)
        for key, value in histogram_dict.items():
            node = self.find_el(key, self.root)
            kod = self.encode(node)
            print(node.data, kod)
            histogram[node.data] = kod
        output_str = ''
        for slovo in sequence:
            output_str += histogram[slovo]
        return output_str


    def print_tree(self):
        def display(root):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if root.right is None and root.left is None:
                line = '%s (%s)' % (root.data, root.freq)
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if root.right is None:
                lines, n, p, x = display(root.left)
                s = '%s (%s)' % (root.data, root.freq)
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if root.left is None:
                lines, n, p, x = display(root.right)
                s = '%s (%s)' % (root.data, root.freq)
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = display(root.left)
            right, m, q, y = display(root.right)
            s = '%s (%s)' % (root.data, root.freq)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

        lines, *_ = display(self.root)
        for line in lines:
            print(line)

if __name__ == "__main__":
    niz = "david i danilo"
    print(GetHistogram(niz))
    tree = Tree()
    tree.root = tree.initialize(GetHistogram(niz))
    tree.print_tree()
    node = tree.get_min(tree.root)
    print(node.freq, node.data)
    tree.delete_el('o')
    tree.print_tree()
    encoded_sequence = tree.huffman_coding(niz)
    print(encoded_sequence)