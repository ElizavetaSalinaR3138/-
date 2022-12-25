from typing import Iterable, Any
from collections import Counter
import pickle
import sys

class Queue: # очередь
    def __init__(self):
        self.__values = []

    def push(self, value): # добавление элемента в очередь и сортировка по возрастанию
        self.__values.append(value)
        self.__values.sort(key=lambda obj: obj.get_priority())

    def get(self): # брать 1 элемент очереди, а затем удалять его из очереди
        value = self.__values[0]
        del self.__values[0]
        return value

    def empty(self): # проверять является ли очередь пустой
        return len(self.__values) == 0

    def __len__(self): # длина очереди
        return len(self.__values)

# класс узла дерева
class Node:
    def __init__(self, value, left=None, right=None):  # значение и ссылки на "детей"
        self.value = value
        self.left = left
        self.right = right

    def __getitem__(self, index): # брать значение по индексу
        if index == 0:
            return self.value
        return None

    def get_priority(self):
        return self.value.get_priority()

# функция прохождения по дереву. рекурсия
def walk(root: Node, code=''):
    # если у вершины нет "детей", то она лист и ей присваивается код
    if root.left is None and root.right is None:
        return {root.value.value: code}
    # прохождение по ветвям последовательно
    return walk(root.left, code + '0') | walk(root.right, code + '1')

# класс пар: вероятность-значение
class Pair:
    def __init__(self, probability, value):
        self.probability = probability
        self.value = value

    def __lt__(self, other): # сравнение (меньше чем)
        return self.probability < other.probability

    def get_priority(self):
        return self.probability

# подсчет частоты
def get_frequency(items: Iterable):
    frequency = Counter(items)
    return frequency

# подсчет вероятности
def get_probabilities(items: Iterable):
    frequency = get_frequency(items)
    amount = sum(frequency.values())
    probabilities = {key: value / amount for key, value in frequency.items()}
    return probabilities

# дерево Хаффмана
def huffman(items: Iterable): # принимает итерируемые объекты
    probabilities = get_probabilities(items)
    queue = Queue() #  создание очереди
    for item, probability in probabilities.items():
        queue.push(Node(value=Pair(probability, item))) # добавление в очередь пар из вероятности и символа

    while len(queue) != 1:
        t1 = queue.get()
        t2 = queue.get()
        probability = t1.value.probability + t2.value.probability
        temp = Node(value=Pair(probability, None), left=t1, right=t2) # создание класса узла с ссылками на детей
        queue.push(temp)

    root = queue.get()
    return walk(root) if len(probabilities) > 1 else {root.value.value: '0'} # если длина очереди 1 присваиваем 0, иначе проходимся по дереву


def encoding(items: Iterable, codes: dict[Any, str]):
    result = ''
    for item in items:
        result += codes[item]
    return result


def decoding(encoded: str, codes: dict[Any, str]):
    reverse_codes = {value: key for key, value in codes.items()}
    result = []
    subsequent = '' # подмножество (набираем строку символ за сиволом, чтобы проверить если ли такой код в словаре
    for bit in encoded: # для каждого символа 0/1
        subsequent += bit
        if subsequent in reverse_codes:
            result.append(reverse_codes[subsequent])
            subsequent = ''
    return result

def makeCodes(oldcodes):
    oldcodes = oldcodes.replace(oldcodes[0], "")
    oldcodes = oldcodes.replace(oldcodes[-1], "")
    dataCodes = {}
    codesArray = oldcodes.split(", ")
    for code in codesArray:
        letter = code.split(": ")[0]
        value = code.split(": ")[1]
        letter = letter.replace("'", "", 2)
        value = value.replace("'", "", 2)
        dataCodes[letter] = value
    return dataCodes

def decoding1(text):
    result = ""

    for i in text:
        char = str(bin(int(ord(i)))[2:])
        char = "0"*(8-len(char)) + char
        result += char

    return result

def encode(input_file, output_file):
    text = open(input_file).read()

    dict_code = huffman(text)
    encoded_text = encoding(text, dict_code)
    probabilities = get_probabilities(text)

    if len(encoded_text) % 8 != 0:
        encoded_text += '0' * (8 - len(encoded_text)%8)

    bit = ''
    for j in range(0, len(encoded_text), 8):
        bit += chr(int(encoded_text[j:j+8], 2))
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(chr(len(probabilities)) + '/////')
        f.write(str(dict_code) + '/////')
        f.write(bit)
        # f.write(''.join('{}{}'.format(key, val) for key, val in dict_code.items()) + '/////')

def decode(input_file, output_file):
    inp_f = open(input_file, 'r', encoding="utf-8")
    out_ = open(output_file, 'w')
    string_ = inp_f.read()
    array = string_.split('/////')
    codes = makeCodes(array[1])
    text = decoding1(array[2])

    result = ''.join(decoding(text, codes))
    out_.write(str(result))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        method = sys.argv[1]
        input_file = sys.argv[2]
        out_file = sys.argv[3]
        if method == '--encode':
            encode(input_file, out_file)

        if method == '--decode':
            decode(input_file, out_file)
