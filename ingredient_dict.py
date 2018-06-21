import json

class __Trie(object):
    class __TrieNode(object):
        def __init__(self, parent):
            self.parent = parent
            self.children = {}
            self.prefix_of = 1
            self.end_of_word = False

    def __init__(self):
        self.root = self.__TrieNode(None)
        self.words = 0

    def add(self, word):
        curr = self.root
        for char in word:
            if char in curr.children:
                curr.prefix_of += 1
            else:
                curr.children[char] = self.__TrieNode(curr)
            curr = curr.children[char]

        curr.end_of_word = True
        self.words += 1

    def find(self, word):
        curr = self.root
        for char in word:
            if char in curr.children:
                curr = curr.children[char]
            else:
                return False

        return curr.end_of_word

    # def delete(self, word):
    #     curr = self.root
    #     for char in word:
    #         if char in curr.children:
    #             curr = curr.children[char]
    #         else:
    #             # word not found in trie
    #             return False
    #
    #     if curr.prefix_of > 1: # word is a prefix of a longer word
    #         curr.end_of_word = False
    #         while not curr.parent:
    #             curr.prefix_of -= 1
    #             curr = curr.parent
    #     else:
    #         while curr.parent and not curr.end_of_word: # word is unique or has a prefix
    #             parent = curr.parent
    #             del parent.children[curr.char]
    #             curr = parent
    #
    #     self.words -= 1
    #     return word

__ingredient_dict = __Trie()
MAX_LEN = 0

with open('ingredients_list.json', 'r') as file:
    ingredient_list = json.loads(file.read())
    for ingredient in ingredient_list:
        __ingredient_dict.add(ingredient)
        length = len(ingredient)
        if length > MAX_LEN:
            MAX_LEN = length

def find(word):
    return __ingredient_dict.find(word)
