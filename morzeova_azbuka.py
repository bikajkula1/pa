class Node:
    def __init__(self, parent=None, left=None, right=None, data=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.data = data


class Tree:
    def __init__(self, root=None):
        self.root = root

    def insert(self, node):
        y = None
        x = self.root
        while x is not None:
            y = x
            if node.data[0] < x.data[0]:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            # tree was empty
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        return node

    def inorder_tree_walk(self, node):
        if node is None:
            return
        self.inorder_tree_walk(node.left)
        print(node.data[1])
        self.inorder_tree_walk(node.right)

    '''
    def search_tree(self, lista_enkodovana, node, key):
        if node.data[1] == key:
            return True
        if node == None:
            return
        left = self.search_tree(node.left)
        right = self.search_tree(node.right)
        if left == True:
            '''
    def find_key(self, node, key):
        if node is None:
            return None
        if node.data[1] == key:
            return node
        left = self.find_key(node.left, key)
        right =self.find_key(node.right, key)
        if left is not None:
            return left
        if right is not None:
            return right
        return None

    def search_tree(self, root_node, key):
        node = self.find_key(root_node, key)
        enkodovana_sekvenca = ''
        node_par = None
        while node.parent is not None:
            node_par = node.parent
            if node_par.left == node:
                enkodovana_sekvenca += '.'
            else:
                enkodovana_sekvenca += '-'
            node = node_par
        return enkodovana_sekvenca[::-1]

    def find_character(self, sekvenca):
        node = self.root
        for char in sekvenca:
            if char == '.':
                node = node.left
            else:
                node = node.right
        return node.data[1]

    def dekodovanje(self, ulaz):
        izlaz = ''
        reci = ulaz.split(' / ')
        for rec in reci:
            slova = rec.split(' ')
            for slovo in slova:
                izlaz += self.find_character(slovo)
            izlaz += ' '
        return izlaz

    def enkodovanje(self, ulaz):
        izlaz = ''
        reci = ulaz.split(' ')
        i = len(reci)
        for rec in reci:
            for slovo in rec:
                izlaz += self.search_tree(self.root, slovo)
                izlaz += ' '
            if i > 1:
                izlaz += ' / '
                i -= 1

        return izlaz

    def print_tree(self):
        def display(root):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            # No child.
            if root.right is None and root.left is None:
                line = '%s' % root.data[1]
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if root.right is None:
                lines, n, p, x = display(root.left)
                s = '%s' % root.data[1]
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if root.left is None:
                lines, n, p, x = display(root.right)
                s = '%s' % root.data[1]
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = display(root.left)
            right, m, q, y = display(root.right)
            s = '%s' % root.data[1]
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
    morzeovo_stablo = ["5", "H", "4", "S", "", "V", "3", "I", "", "F", "", "U", "", "", "2", "E", "", "L", "", "R", "+",
                       "", "", "A", "", "P", "", "W", "", "J", "1", "start", "6", "B", "=", "D", "/", "X", "", "N", "",
                       "C", "", "K", "", "Y", "", "T", "7", "Z", "", "G", "", "Q", "", "M", "8", "", "", "O", "9", "",
                       "0"]
    morze_obj = enumerate(morzeovo_stablo)
    morze_obj = list(morze_obj)
    #print(list(morze_obj))
    insert_order = [31,15,47,7,23,39,55,3,11,19,27,35,43,51,59,1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62]
    tree = Tree()
    for br in insert_order:
        br2 = morze_obj[br]
        tree.insert(Node(data=br2))

    #tree.print_tree()

    #zadatak pod a
    #tree.inorder_tree_walk(tree.root)

    enkodovani_string = tree.search_tree(tree.root, '')
    #print(enkodovani_string)
    karakter = tree.find_character('-.--')
    #print(karakter)
    dekodovani_string = tree.dekodovanje('.--. . .-. .- / .--. . .-. .. -.-.')
    print(dekodovani_string)
    enkodovani_string = tree.enkodovanje('NA KURCU TE N8')
    print(enkodovani_string)