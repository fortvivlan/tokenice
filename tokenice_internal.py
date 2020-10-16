import re
from time import time

# основной принцип работы токенизатора - делим по границам слов (делимитерам)


def defiledsplitter(token):
    """Минифункция для разделения слов по дефису, если они не в списке"""
    res = []
    if token.count('-') == 1 and \
            ((token.startswith('-') and token[1:].isdigit()) or
             token[:token.index('-')].isdigit() or token[token.index('-') + 1:].isdigit()):
        return [token]      # если слово заканчивается на дефис, не делим; если начинается и это цифра, тоже
    matches = re.finditer('-', token)
    start = 0
    for match in matches:
        chunk = token[start:match.start()]
        if chunk:
            res.append(chunk)
        res.append(match.group(0))
        start = match.end()
        if not re.search('-', token[start:]):
            res.append(token[start:])
    return res


def delimitercheck(delim):
    """Функция разделения делимитера по категориям на пунктуацию, скобки-кавычки, текстовые смайлики и эмодзи.
    Спасибо Маше за список эмодзи в юникоде"""
    punct = r'[.,?!…—–]+'
    twos = r'[:;](?!=[)(*])'
    bracketsquotes = r'[\'"\{\[\(\}\]\)«“‘»”’„]'
    smiles = r'(?:[=:;][)(]{1,})|(?:\){2,}|\({2,}|[)(]{1,3}:|[=:;]\*+)'
    emoji = r'''(?:[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|
[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|
[\U0001FA70-\U0001FAFF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251])+'''
    other = r'[$@%\^&*+=\\/<>~]+|[\U000000A1-\U000000BF]+'    # другие знаки, какие пришли в голову и могут встретиться
    if delim.isspace():
        return []
    delimiters = f'{smiles}|{bracketsquotes}|{punct}|{emoji}|{twos}|{other}'
    pattern = re.compile(delimiters)
    matches = [match for match in re.findall(pattern, delim) if match]
    return matches


def tokenize(string):
    """Собственно функция токенизации"""
    if string.isspace():
        return []
    abbr = set()  # словарь сокращений
    with open(r'abbrev', 'r', encoding='utf8') as file:
        for line in file:
            abbr.add(line[:-1])

    defis = []  # закрытый список слов, которые не делим по дефису
    with open('defis', 'r', encoding='utf8') as defile:
        for line in defile:
            defis.append(line[:-1])

    doubledefis = []    # еще один закрытый список слов, которые не делим по дефису
    with open('dobledefis.txt', 'r', encoding='utf8') as doubledefiled:
        for line in doubledefiled:
            doubledefis.append(line[:-1])

    pattern = r'[^-\w\d#\']+'
    dpattern = 'D+|3+|з+|З+'

    if not re.search(pattern, string):
        return [string]

    start = 0
    result = []
    delimitcheck = True
    dsmile = False
    joinstring = ''
    matches = re.finditer(pattern, string)

    if not matches:
        return [string]

    for match in matches:
        left_token = string[start:match.start()]
        delimiter = match.group(0)
        start = match.end()

        ''' проверка токена, который оказывается с левой стороны от делимитера '''

        if dsmile:      # для учета смайлов вида :D, :3, :з
            jaw = re.search(dpattern, left_token)
            if jaw:
                if jaw.group(0) == left_token and result:
                    if len(result[-1]) == 1:
                        result[-1] += left_token
                    else:
                        result.append(result[-1][-1] + left_token)
                        result[-2] = result[-2][:-1]
                else:
                    result.append(left_token)
            dsmile = False

        elif not result and left_token.isdigit() and delimiter.startswith(')'):   # bullets (но только в начале строки)
            result.append(left_token + delimiter[0])
            if len(delimiter) > 1:
                delimiter = delimiter[1:]
            else:
                delimitcheck = False

        elif joinstring:  # если нам что-то надо было слить (цифры), проверяем это
            if left_token.isdigit():
                if len(delimiter) == 1 and delimiter in '.,:/':
                    joinstring += left_token + delimiter
                    delimitcheck = False
                else:
                    joinstring += left_token
                    result.append(joinstring.strip())
                    joinstring = ''
            else:
                result.append(joinstring.strip())
                joinstring = ''
                result.append(left_token)

        elif left_token == '_' and delimiter[0] in '.*^' and result:   # для смайлов вида *_*
            if result[-1] == delimiter[0]:
                result[-1] += left_token + delimiter[0]
                delimiter = delimiter[1:]
            else:
                result.append(left_token)

        elif left_token.count('#') > 1:     # для хешей
            result.extend(re.findall(r'#.+?(?=#|$)', left_token))

        elif left_token == '-' and result:  # для смайлов с - посередине
            if re.search(r'[:;]', result[-1]) and delimiter:
                result[-1] += left_token + delimiter[0]
                if len(delimiter) != 1:
                    delimiter = delimiter[1:]
                else:
                    delimitcheck = False
            else:
                result.append(left_token)

        elif '-' in left_token and len(left_token) > 1:     # для токенов с дефисом внутри
            defiled = 0
            for elem in defis:
                if left_token.lower().startswith(elem) or left_token.lower().endswith(elem):
                    result.append(left_token)
                    defiled = 1
                    break
            for elem in doubledefis:
                if elem in left_token.lower():
                    result.append(left_token)
                    defiled = 1
                    break
            if not defiled:
                result.extend(defiledsplitter(left_token))

        elif left_token.isdigit() and len(delimiter) == 1 and delimiter in '.,:/':
            # для цифр вида 20.00, 20:00, 20 000, 20,00, 20/00
            if string[start].isdigit():
                joinstring = left_token + delimiter
                delimitcheck = False
            else:
                result.append(left_token)

        elif (left_token in abbr or len(left_token) == 1) \
                and delimiter.startswith('.') and not delimiter.startswith('..'):
            # временное решение для аббревиатур: обычно если один буквенный символ с точкой, это сокращение
            result.append(left_token + delimiter[0])
            delimiter = delimiter[1:]
        else:
            result.append(left_token)       # основное добавление токена в результирующий список

        ''' проверка делимитера '''

        if (delimiter.endswith(':') or delimiter.endswith(';')) and string[start:]:
            if string[start] in 'D3з':
                dsmile = True
        if delimitcheck and not delimiter.isspace():
            delimiters = delimitercheck(delimiter)
            if delimiters:
                result.extend(delimiters)
        delimitcheck = True

        ''' проверка хвоста '''

        if not re.search(pattern, string[start:]):  # хвост добавляем
            last_token = string[start:].strip()
            if joinstring:
                result.append(joinstring)
            if last_token:
                if last_token.isdigit() and joinstring:
                    result[-1] += last_token
                elif result[-1] in ':;' and re.search(dpattern, last_token):
                    result[-1] += last_token
                else:
                    result.append(last_token)
    return result


# t = time()
# dump = open(r'F:\Python\files\datasets\tokenicecheckintnorm.txt', 'w', encoding='utf8')
#
# with open(r'F:\Python\files\datasets\norm_20190208.txt', 'r', encoding='utf8') as source:
#     for line in source:
#         tokenized = tokenize(line)
#         if tokenized:
#             print(*tokenized, sep='\n', file=dump)
#
# dump.close()
# print(time() - t)
# print(*tokenize(input()), sep='\n')
