def search4letters (phrase:str , letters:str='qwerty') -> set:
    """Ищет в фразе то, что просит пользователь"""
    return set(phrase).intersection(set(letters))
# print(search4letters(phrase = input('vvedi phrase:'),letters = input('chto ickat:')))
# letters = input('chto ickat:')
# print(search4letters('qasdy','xzc'))