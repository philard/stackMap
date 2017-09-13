from datetime import datetime


# class One(dict):
#     def __init__(self, fname):
#         dict.__init__(self, fname=fname)

# f = One('tasks.txt')
# print(json.dumps(f))

class Node(dict):
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)

    def __init__(self, name):
        self.children = []
        self.time = str(datetime.now())
        self.name = name
        dict.__init__(self, name=self.name, children=self.children, time=self.time)

    def add_child(self, node):
        self.children.append(node)

    def add_children(self, nodes):
        for node in nodes:
            self.add_child(node)

    @staticmethod
    def merge_nodes(existing_node, node):
        if existing_node is None:
            existing_node = Node("empty")
        if node is None:
            node = Node("empty")
        merged_node = Node(node.name)
        if len(existing_node.children) > 0:
            if len(node.children) > 0:
                children = merge(node.children, existing_node.children)
            else:
                children = [] + existing_node.children
        else:
            children = [] + node.children
        merged_node.add_children(children)
        return merged_node


def merge(children_left, children_right):
    unique_by_name = {}
    for node in children_left + children_right:
        name = node.name
        existing_node = unique_by_name.get(name)
        if existing_node is None:
            unique_by_name[name] = node
        else:
            unique_by_name[name] = Node.merge_nodes(existing_node, node)
    return unique_by_name.values()

# a = {'first': {'all_rows': {'pass': 'dog', 'number': '1'}}}
# b = {'first': {'all_rows': {'fail': 'cat', 'number': '5'}}}

# root = Node("root")
# c1 = Node("one")
# root.add_child(c1)
#
# rootTwo = Node("root")
# c2 = Node("one")
# c3 = Node("two")
# rootTwo.add_child(c2)
# rootTwo.add_child(c3)


# print(merge(root.children, rootTwo.children))

# print(merge_nodes(root, rootTwo))
