import os.path
import csv
from copy import copy 

class Item:
    def __init__(self, name, aisle, bin_):
        self.name = name
        self.aisle = aisle
        self.bin = bin_
        self.number = 0
    
    def __repr__(self):
        return f"[{self.name}]: Aisle {self.aisle} Bin {self.bin} Number {self.number}"

class MarketMap:
    def __init__(self):
        self.anchors = set()
        self.connections = {}

    def build_from_csv(self, csvfile):

        # Read graph definition
        with open(csvfile, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                primary_anchor = row[0]
                self.anchors.add(primary_anchor)

                neighbours = row[1:]                

                if primary_anchor not in self.connections:
                    self.connections[primary_anchor] = set()

                for neighbour in neighbours:
                    self.connections[primary_anchor].add(neighbour)
                    self.anchors.add(neighbour)

    def find_shortest_path(self, source, dest):
        visited = set(source)
        node = {
            "anchor": source,
            "path": []
        }
        queue = [node]

        while len(queue) > 0:
            tmp_node = queue.pop(0)
            path = copy(tmp_node['path'])
            path.append(tmp_node['anchor'])

            neighbours = self.connections[tmp_node['anchor']]

            for neighbour in neighbours:
                if neighbour == dest:
                    return path
                
                if neighbour in visited:
                    continue

                visited.add(neighbour)                
                queue.append({
                    "anchor": neighbour,
                    "path": path
                })

        return None


class DataContainer:
    def __init__(self):
        self.shopping_list = []
        self.item_metadata = {}
        self.bin_anchor_metadata = {}
        self.market_map = MarketMap()

    def setup(self):

        item_metadata = {}
        number_of_types_of_items = 0

        # Read bin anchors
        with open(os.path.join(os.path.dirname(__file__), 'bin_anchor.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                aisle = row[0]
                bin = row[1]
                anchor = row[2]

                if aisle not in self.bin_anchor_metadata:
                    self.bin_anchor_metadata[aisle] = {}
                
                self.bin_anchor_metadata[aisle][bin] = anchor

        # print(self.bin_anchor_metadata)

        # Read items definition
        with open(os.path.join(os.path.dirname(__file__), 'items.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                name = row[0]
                aisle = row[1]
                bin_ = row[2]

                item_metadata[name] = Item(name, aisle, bin_)
                number_of_types_of_items += 1

        self.item_metadata = item_metadata

        self.market_map.build_from_csv(os.path.join(os.path.dirname(__file__), 'graph_path.csv'))

    def get_item_metadata(self):
        return self.item_metadata

    def add_to_shopping_list(self, item):
        """ Add an item into the shopping list, if the list already contains the item, increase its count instead"""        
        existing = list(filter(lambda e: e.name == item.name, self.shopping_list))

        if len(existing) > 0:
            temp_item = existing[0]
            temp_item.count = temp_item.count + 1
            return

        temp_item = copy(item)
        temp_item.count = 1

        self.shopping_list.append(temp_item)

    def get_shopping_list_items(self):
        return self.shopping_list

    def calculateRoutePlan(self):
        items = self.shopping_list

        start = 'A'

        item = items[0]
        step = self.bin_anchor_metadata[item.aisle][item.bin]

        path = self.market_map.find_shortest_path(start, step)

        print(start, step, path)
        