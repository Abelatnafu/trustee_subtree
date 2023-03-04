import numpy as np
from trustee.utils.tree import get_dt_dict



def get_subtree(dt, target_class, class_labels, features, threshold = -1):
    # change tree to dict
    dict_dt = get_dt_dict(dt)
    # node details
    nodes = dict_dt["nodes"]
    class_values = dict_dt["values"]
    node_class = {}
    prev = {}
    child = {}
    # For target node indices
    targ = [-1]

    for i in range(len(nodes)):
        # find the class of each node by the max value index
        node_class[i] = np.argmax(class_values[i])
        # if leaf
        if nodes[i][0] == -1 and nodes[i][1] == -1:
            # if leaf and target class
            if node_class[i] == target_class:
                # save the target node index
                # if target leaf nodes are found
                if  targ != [-1]:
                    targ.append(i)
                # if no target leaf nodes are found
                else:
                    targ = [i]

        else:
            # save the index of the left and right child
            child[i] = [nodes[i][0], nodes[i][1]]
    # save parent of nodes for backtracking
    for key, value in child.items():
        for kid in value:
            prev[kid] = key


    # sub_tree.append(nodes[targ[0]])
    # k = targ[0]
    # Function to walk through all possible target leaf
    def walk_back (index, threshold):
        sub_tree = []
        # start by appending target leaf node and its index
        sub_tree.append((nodes[targ[index]], targ[index]))
        k = targ[index]

        if threshold == -1:
            # while node has a parent
            while k in prev.keys():
                k = prev[k]
                sub_tree.append((nodes[k], k))
        else:
            # Threshold not implemented yet
            while k in prev.keys() and threshold > 0:
                k = prev[k]
                sub_tree.append((nodes[k], k))
                threshold -= 1

        # print(prev)
        # print(child)
        # print(sub_tree)
        # Details being outputted
        details = ["feature", "threshold", "impurity", "samples", "weighted_samples"]

        print(f"Target class is {class_labels[target_class]}.")
        print(f"The height of the Target leaf is {len(sub_tree)}.")
        print("+++++++++++++++")

        # Keep track of family line
        ancestor = len(sub_tree) - 2
        # reverse subtree to start from root
        sub_tree = sub_tree[::-1]
        ishead = False
        for path in range(len(sub_tree)):
            # If its not the target leaf node
            if path != (len(sub_tree) - 1):
                # Top of the tree
                if path == 0:
                    print("***Root***")
                    ishead = True

                # Parent of target leaf node
                elif path == len(sub_tree) - 2:
                    print(f"***Parent***")
                    ishead = False

                # Other ancestors
                else:
                    print(f"***Ancestor {ancestor}***")
                    ishead = False
                    ancestor -= 1

                # If not head then print the branching logic
                if not ishead:
                    print(f"Branching from previous node logic = \'{'<=' if (child[sub_tree[path - 1][1]][0] == sub_tree[path][1]) else '>'}'")

                # Print all the feature details for node
                for p in range(2,len(sub_tree[path][0]) - 1):
                    # if feature print the name of the feature
                    if details[p - 2] != "feature":
                        print(f"{details[p - 2]} = {sub_tree[path][0][p]}")
                    else:
                        print(f"{details[p - 2]} = {features[sub_tree[path][0][p]]}")

                print("++++++++++")


            # If its the target node
            else:
                print(f"***{class_labels[node_class[targ[index]]]} Leaf***")
                print(f"Branching from previous node logic = \'{'<=' if (child[sub_tree[path - 1][1]][0] == targ[index]) else '>'}'")
                for p in range(2,len(sub_tree[path][0]) - 1):
                    # if feature print the name of the feature
                    if details[p - 2] != "feature":
                        print(f"{details[p - 2]} = {sub_tree[path][0][p]}")
                    else:
                        print(f"{details[p - 2]} = {features[sub_tree[path][0][p]]}")

                # Print class name of target node
                print(f"class_Name = {class_labels[node_class[targ[index]]]}")
                print("++++++++++")

    # for each target leaf node
    for targets_ in range(len(targ)):
        print(f"*****************Sub-tree {targets_}*****************")
        walk_back(targets_, threshold)

