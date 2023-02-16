class Node:
    """
    Node class for the FP-Tree
    """
    def __init__(self, item, count, parent):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}

class FPGrowth:
    """
    Class for the Frequency Pattern Growth algorithm
    """
    def __init__(self, min_support):
        self.min_support = min_support
        self.freq_patterns = []

    def _get_item_counts(self, transactions):
        """
        Count the frequency of each item in the transactions
        """
        item_counts = {}
        for transaction in transactions:
            for item in transaction:
                item_counts[item] = item_counts.get(item, 0) + 1
        return item_counts

    def _remove_infrequent_items(self, item_counts):
        """
        Remove infrequent items from the item_counts dictionary
        """
        item_counts = {k: v for k, v in item_counts.items() if v >= self.min_support}
        return item_counts

    def _sort_items(self, item_counts):
        """
        Sort the frequent items in descending order of their frequency
        """
        items = sorted(item_counts.items(), key=lambda x: (-x[1], x[0]))
        return [x[0] for x in items]

    def _construct_tree(self, transactions, items):
        """
        Construct the FP-Tree for the transactions
        """
        root = Node(None, None, None)
        for transaction in transactions:
            curr_node = root
            for item in items:
                if item in transaction:
                    child_node = curr_node.children.get(item)
                    if child_node is None:
                        child_node = Node(item, 1, curr_node)
                        curr_node.children[item] = child_node
                    else:
                        child_node.count += 1
                    curr_node = child_node
        return root

    def _mine_patterns(self, tree, prefix):
        """
        Mine frequent itemsets from the FP-Tree
        """
        if tree.children == {}:
            return

        for item, node in tree.children.items():
            pattern = prefix + [item]
            self.freq_patterns.append((pattern, node.count))
            self._mine_patterns(node, pattern)

    def fit(self, transactions):
        """
        Fit the FPGrowth model on the transactions
        """
        item_counts = self._get_item_counts(transactions)
        frequent_items = self._sort_items(self._remove_infrequent_items(item_counts))
        root = self._construct_tree(transactions, frequent_items)
        self._mine_patterns(root, [])

    def get_frequent_patterns(self):
        """
        Get the frequent itemsets discovered by the FPGrowth algorithm
        """
        return self.freq_patterns
