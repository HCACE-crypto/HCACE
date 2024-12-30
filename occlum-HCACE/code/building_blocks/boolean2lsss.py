class TreeNode:
    def __init__(self, value, vector=None):
        self.value = value
        self.left = None
        self.right = None
        self.vector = vector if vector is not None else []

    def __str__(self):
        return f"{self.value} with vector {self.vector}"

def parse_expression(expr):
    expr = expr.replace('(', ' ( ').replace(')', ' ) ').replace('AND', ' AND ').replace('OR', ' OR ').replace('or', ' OR ')
    return expr.split()

def precedence(op):
    if op == 'OR':
        return 1
    if op == 'AND':
        return 2
    return 0

def apply_op(op):
    return TreeNode(op)

def to_boolean_tree(tokens):
    values = []
    ops = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                op = ops.pop()
                right = values.pop()
                left = values.pop()
                op_node = apply_op(op)
                op_node.left = left
                op_node.right = right
                values.append(op_node)
            ops.pop()  # Remove '('
        elif token in ['AND', 'OR']:
            while (ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token)):
                op = ops.pop()
                right = values.pop()
                left = values.pop()
                op_node = apply_op(op)
                op_node.left = left
                op_node.right = right
                values.append(op_node)
            ops.append(token)
        else:
            values.append(TreeNode(token))
        i += 1

    while ops:
        op = ops.pop()
        right = values.pop()
        left = values.pop()
        op_node = apply_op(op)
        op_node.left = left
        op_node.right = right
        values.append(op_node)

    return values[0]

def label_tree(node: TreeNode, isRoot, c=1):
    if node.value == 'OR':
        if isRoot:
            node.vector = [1]
        if node.left:
            node.left.vector = node.vector.copy()
            label_tree(node.left, False, c)
        if node.right:
            node.right.vector = node.vector.copy()
            label_tree(node.right, False, c)
    elif node.value == 'AND':
        node.vector += [0] * (c - len(node.vector))
        if isRoot:
            node.vector = [1]
        if node.left:
            node.left.vector = node.vector + [1]
            label_tree(node.left, False, c + 1)
        if node.right:
            node.right.vector = [0] * c + [-1]
            label_tree(node.right, False, c + 1)

def find_max_vector_length(node: TreeNode):
    max_length = len(node.vector)
    if node.left:
        max_length = max(max_length, find_max_vector_length(node.left))

    if node.right:
        max_length = max(max_length, find_max_vector_length(node.right))
    return max_length

def extract_matrix(node: TreeNode, current_row=[], map=[], max_length=None):
    if max_length is None:
        max_length = find_max_vector_length(node)

    if (not node.left) and (not node.right):
        # It's a leaf node, pad the vector to the max length
        node.vector += [0] * (max_length - len(node.vector))
        current_row.append(node.vector)
        map.append(node.value)
    else:
        extract_matrix(node.right, current_row, map, max_length)
        extract_matrix(node.left, current_row, map, max_length)

    return current_row, map


def print_tree(node: TreeNode, level=0):
    indent = '  ' * level
    print(f"{indent}{node}")
    if node.left:
        print_tree(node.left, level + 1)
    if node.right:
        print_tree(node.right, level + 1)

def boolean2lsss(expr):
    tokens = parse_expression(expr)
    
    root = to_boolean_tree(tokens)
    label_tree(root, True)
    
    matrix, map = extract_matrix(root)
    
    return matrix, map

if __name__ == "__main__":
    expr = "(A11 OR A20 OR A30 OR A40) AND (A10 OR A20 OR A31 OR A41)"
    tokens = parse_expression(expr)
    root = to_boolean_tree(tokens)
    label_tree(root, True)
    print("Tree Structure:")
    print_tree(root)

    matrix, map = extract_matrix(root)
    print("\nLSSS Matrix:")
    for row in matrix:
        print(row)

    for row in map:
        print(row)
