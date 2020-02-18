import os.path
import csv, copy

class Item:
    def __init__(self, name, aisle, bin_):
        self.name = name
        self.aisle = aisle
        self.bin = bin_
        self.number = 0
    
    def __repr__(self):

        return f"[{self.name}]: Aisle {self.aisle} Bin {self.bin}"


class DataContainer:
    def __init__(self):
        self.shopping_list = []
        self.item_metadata = {}

    def setup(self):

        item_metadata = {}
        number_of_types_of_items = 0

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

        # print(self.item_metadata)

        pass

    def get_item_metadata(self):
        return self.item_metadata

    def add_to_shopping_list(self, item):
        """ Add an item into the shopping list, if the list already contains the item, increase its count instead"""        
        existing = list(filter(lambda e: e.name == item.name, self.shopping_list))

        if len(existing) > 0:
            temp_item = existing[0]
            temp_item.count = temp_item.count + 1
            return

        temp_item = copy.copy(item)
        temp_item.count = 1

        self.shopping_list.append(temp_item)

    def get_shopping_list_items(self):
        return self.shopping_list
        