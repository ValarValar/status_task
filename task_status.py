import itertools

# ЗАДАНИЕ
# Есть массив объектов, которые имеют поля id и parent, через которые их можно связать в дерево и некоторые произвольные поля.

# Нужно написать класс, который принимает в конструктор массив этих объектов и реализует 4 метода:
#  - getAll() Должен возвращать изначальный массив элементов.
#  - getItem(id) Принимает id элемента и возвращает сам объект элемента;
#  - getChildren(id) Принимает id элемента и возвращает массив элементов, являющихся дочерними для того элемента,
# чей id получен в аргументе. Если у элемента нет дочерних, то должен возвращаться пустой массив;
#  - getAllParents(id) Принимает id элемента и возвращает массив из цепочки родительских элементов,
# начиная от самого элемента, чей id был передан в аргументе и до корневого элемента,
# т.е. должен получиться путь элемента наверх дерева через цепочку родителей к корню дерева. Порядок элементов важен!

# Требования: максимальное быстродействие, следовательно, минимальное количество обходов массива при операциях,
# в идеале, прямой доступ к элементам без поиска их в массиве.


# Исходные данные:
class TreeStore:

    def __init__(self, items):
        '''
            Gets list of dicts, every dict contains an elem
            {"id":int, "parent":Union[int,str], named args
            for example: [{"id": 1, "parent": "root"}, {"id": 2, "parent": 1, "type": "test"},]
        '''
        self.__items = {}
        self.__children = {}

        for item in items:
            self.__items[item['id']] = item

        for key, group in itertools.groupby(items, key=lambda x: x['parent']):
            if isinstance(key, int):
                self.__children[key] = list(group)

    def getAll(self):
        '''
            returns a list of elements
        '''
        return list(self.__items.values())

    def getItem(self, id):
        '''
            returns elem by its' id
            note: returns an empty dict for not existing id
        '''
        item = self.__items.get(id)
        if item is None:
            return {}

        return item

    def getChildren(self, id):
        '''
            returns elem by its' id
            note: return an empty list for not existing id
            or elem with no children
        '''
        children_ids = self.__children.get(id)

        if children_ids is None:
            return []
        else:
            return [x for x in children_ids]

    def getAllParents(self, id):
        '''
            returns elem by its' id
            note: return an empty list for not existing id
            or elem with no parents (first elem)
        '''
        res = []
        item = self.__items.get(id)

        if item is None:
            return res

        item_parent_id = item["parent"]
        while item_parent_id != "root":
            item = self.__items.get(item_parent_id)
            item_parent_id = item["parent"]
            res.append(item)
        return res


items = [
    {"id": 1, "parent": "root"},
    {"id": 2, "parent": 1, "type": "test"},
    {"id": 3, "parent": 1, "type": "test"},
    {"id": 4, "parent": 2, "type": "test"},
    {"id": 5, "parent": 2, "type": "test"},
    {"id": 6, "parent": 2, "type": "test"},
    {"id": 7, "parent": 4, "type": None},
    {"id": 8, "parent": 4, "type": None}
]
ts = TreeStore(items)

# Примеры использования:
assert ts.getAll() == [{"id": 1, "parent": "root"}, {"id": 2, "parent": 1, "type": "test"},
                       {"id": 3, "parent": 1, "type": "test"}, {"id": 4, "parent": 2, "type": "test"},
                       {"id": 5, "parent": 2, "type": "test"}, {"id": 6, "parent": 2, "type": "test"},
                       {"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]

assert ts.getAll() != [{"id": 2, "parent": "root"}, {"id": 2, "parent": 1, "type": "test"},
                       {"id": 3, "parent": 1, "type": "test"}, {"id": 4, "parent": 2, "type": "test"},
                       {"id": 5, "parent": 2, "type": "test"}, {"id": 6, "parent": 2, "type": "test"},
                       {"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
#
assert ts.getItem(7) == {"id": 7, "parent": 4, "type": None}
assert ts.getItem(7) != {"id": 7, "parent": 5, "type": None}
assert ts.getItem(10) == {}
#
assert ts.getChildren(4) == [{"id": 7, "parent": 4, "type": None}, {"id": 8, "parent": 4, "type": None}]
assert ts.getChildren(5) == []
assert ts.getChildren(10) == []
#
assert ts.getAllParents(7) == [{"id": 4, "parent": 2, "type": "test"}, {"id": 2, "parent": 1, "type": "test"},
                               {"id": 1, "parent": "root"}]
assert ts.getAllParents(1) == []
assert ts.getAllParents(10) == []
