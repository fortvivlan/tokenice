import re
import pickle
from time import time


defis = pickle.load(open('defis', 'rb'))
doubledef = {'-ан-дер-', '-апон-', '-д’', '-да-', '-де-', '-дель-', '-ди-', '-ду-', '-дус-', '-душ-', '-дю-', '-иль-',
             '-ин-', '-ла-', '-мин-', '-на-', '-над-', '-о-', '-он-', '-оф-', '-сюр-', '-уш-', '-эз-', '-эль-', '-эс-',
             '-эш-', '-на-'}
startdef = pickle.load(open('startswith', 'rb'))
enddef = pickle.load(open('endswith', 'rb'))


def abbr(token):
    abbrev = {'etc', 'ibid', 'vs', 'абс', 'авар', 'авг', 'австр', 'австрал', 'авт', 'агр', 'адм', 'азерб', 'ак', 'акад',
              'акк', 'акц', 'алб', 'алл', 'алт', 'амер', 'англ', 'аннот', 'антич', 'ап', 'апок', 'апр', 'араб',
              'аргент', 'арм', 'арт', 'арх', 'архиеп', 'архим', 'архит', 'асс', 'ассир', 'астр', 'ат', 'атм', 'афг',
              'афр', 'бал', 'барр', 'басс', 'безв', 'бельг', 'библ', 'бл', 'богосл', 'болг', 'больн', 'бот', 'бр',
              'браз', 'брит', 'буд', 'букв', 'бул', 'буль', 'бульв', 'бум', 'бурж', 'бурят', 'бут', 'бух', 'бухг',
              'бюлл', 'вал', 'вв', 'вдз', 'вдхр', 'вед', 'вел', 'венг', 'верх', 'вет', 'веч', 'вкл', 'включ', 'вм',
              'вмц', 'вмч', 'внеш', 'внутр', 'воен', 'возвр', 'возд', 'возм', 'вор', 'воскр', 'вост', 'вр', 'втор',
              'выкл', 'вып', 'выс', 'высш', 'вых', 'г/р', 'гал', 'гг', 'где-л', 'ген', 'геогр', 'геол', 'геом', 'герм',
              'гл', 'глаг', 'голл', 'гор', 'гос', 'госп', 'гр', 'гражд', 'граф', 'греч', 'грн', 'губ', 'гц', 'дал',
              'действ', 'дек', 'ден', 'деп', 'дер', 'дес', 'детск', 'дж', 'диал', 'диам', 'диз', 'дир', 'дисс', 'дист',
              'дифф', 'дл', 'дн', 'доб', 'дов', 'док', 'докл', 'докт', 'дол', 'долл', 'доп', 'дополн', 'дор', 'доц',
              'др', 'драм', 'евр', 'европ', 'егип', 'египетск', 'ед', 'ежедн', 'ежемес', 'еженед', 'ек', 'екк', 'еккл',
              'еп', 'еф', 'ефр', 'жарг', 'жен', 'женск', 'жит', 'журн', 'зав', 'загл', 'зак', 'зал', 'зам', 'зап',
              'зарег', 'заруб', 'засл', 'зв', 'зем', 'зн', 'знач', 'зоол', 'иак', 'игум', 'иез', 'иер', 'иером', 'иж',
              'избр', 'изд', 'изм', 'изр', 'илл', 'им', 'имп', 'инв', 'инд', 'инж', 'иностр', 'инст', 'инстр', 'инт',
              'инф', 'ирл', 'ирон', 'искаж', 'исл', 'исп', 'испр', 'иссл', 'ист', 'истор', 'исх', 'итал', 'каб', 'каз',
              'какой-л', 'кан', 'канад', 'канд', 'кап', 'кар', 'карел', 'кат', 'кбм', 'кв', 'кг', 'кельтск', 'кем',
              'кирг', 'кл', 'клб', 'клх', 'км', 'кн', 'книжн', 'когда-л', 'колич', 'ком', 'комм', 'коммерч', 'комн',
              'кон', 'конгр', 'конф', 'кооп', 'коп', 'кор', 'корп', 'корр', 'косв', 'котл', 'коэф', 'коэфф', 'кр',
              'кратк', 'крб', 'крд', 'креп', 'крест', 'кто-л', 'куб', 'куда-л', 'кулин', 'курс', 'лаб', 'лат', 'латв',
              'лейт', 'лек', 'ленингр', 'леч', 'лингв', 'лит', 'лк', 'лог', 'лок', 'магн', 'макс', 'максим', 'мат',
              'матем', 'матер', 'маш', 'мед', 'межвед', 'межд', 'междунар', 'мекс', 'мес', 'местн', 'мет', 'мех', 'мин',
              'минер', 'миним', 'митр', 'миф', 'мкр', 'мл', 'млн', 'млрд', 'мн', 'множ', 'моб', 'мол', 'молд', 'мор',
              'моск', 'муж', 'мужск', 'муз', 'муниц', 'мур', 'мусульм', 'мч', 'наб', 'наз', 'назв', 'наиб', 'наим',
              'накл', 'напр', 'нар', 'народн', 'наст', 'науч', 'нац', 'нач', 'нед', 'неизв', 'нем', 'неопр', 'неопред',
              'нерж', 'неск', 'нидерл', 'ниж', 'низм', 'норв', 'норм', 'нояб', 'об', 'обл', 'обр', 'объед', 'одновр',
              'однокр', 'оз', 'ок', 'оконч', 'окр', 'окт', 'оптим', 'опубл', 'ор', 'орг', 'ориг', 'осет', 'осн', 'отв',
              'отд', 'отеч', 'откр', 'откуда-л', 'отл', 'отм', 'относит', 'отриц', 'отч', 'офиц', 'пад', 'пам', 'парт',
              'пасп', 'пасс', 'пат', 'патол', 'патр', 'пед', 'пер', 'первонач', 'переим', 'перем', 'перен', 'перс',
              'пищ', 'пл', 'плем', 'плотн', 'пн', 'пов', 'пог', 'погов', 'подп', 'пол', 'полит', 'полн', 'польск',
              'пом', 'попер', 'порт', 'португ', 'порядк', 'пос', 'посл', 'пост', 'пп', 'пр', 'правосл', 'превосх',
              'превосходн', 'пред', 'предисл', 'предл', 'предс', 'презр', 'преим', 'преимущ', 'пренебр', 'преп',
              'пресв', 'прибл', 'придат', 'прил', 'прилож', 'прим', 'примеч', 'притяж', 'прич', 'пров', 'прогр',
              'прод', 'прож', 'произв', 'произн', 'происх', 'пром', 'прор', 'просп', 'прот', 'противоп', 'протопресв',
              'проф', 'проц', 'проч', 'прош', 'прп', 'псевд', 'психол', 'публ', 'пуд', 'пун', 'раб', 'равноап', 'разг',
              'разд', 'разл', 'разр', 'разраб', 'распред', 'распростр', 'рац', 'реаб', 'револ', 'ред', 'редк', 'реж',
              'религ', 'рем', 'респ', 'реф', 'рим', 'римск', 'рис', 'род', 'рожд', 'росс', 'руб', 'руг', 'рук', 'рукоп',
              'рум', 'рус', 'русск', 'руч', 'сальвад', 'сам', 'сан', 'санскр', 'сауд', 'сб', 'св', 'свв', 'своб', 'свт',
              'свят', 'свящ', 'сев', 'сек', 'секр', 'сел', 'сем', 'сент', 'сер', 'сербск', 'сеч', 'сиб', 'симф',
              'сирийск', 'сист', 'сканд', 'скв', 'скл', 'сконч', 'сл', 'след', 'словац', 'словен', 'словосочет', 'см',
              'сниж', 'соб', 'собр', 'собств', 'сов', 'совм', 'совр', 'согл', 'содерж', 'соед', 'сокр', 'сокращ',
              'соотв', 'сопр', 'сост', 'сотр', 'сохр', 'соц', 'социал', 'соч', 'сочет', 'союзн', 'сп', 'спб', 'спец',
              'спорт', 'спр', 'ср', 'срав', 'сравн', 'сравнит', 'средн', 'ст', 'станд', 'стат', 'стихотв', 'стр',
              'страд', 'суб', 'сут', 'сущ', 'схем', 'сч', 'сщмч', 'таб', 'табл', 'так наз', 'танц', 'тб', 'тв', 'твор',
              'тез', 'тел', 'телегр', 'телеф', 'теор', 'терр', 'тех', 'техн', 'тж', 'тип', 'тит', 'тлт', 'тм', 'тов',
              'толщ', 'торг', 'трансп', 'трлн', 'тт', 'тум', 'туп', 'тур', 'тыс', 'тюркск', 'ув', 'увелич', 'уг', 'уд',
              'удовл', 'уз', 'узб', 'указ', 'укр', 'ул', 'ум', 'уменьш', 'уорнер браз', 'упак', 'употр', 'упр', 'ур',
              'урож', 'урожд', 'уругв', 'усилит', 'усл', 'устар', 'утв', 'уч', 'учеб', 'ущ', 'фак', 'фам', 'фарм',
              'февр', 'фиг', 'физ', 'физиол', 'филос', 'фин', 'флам', 'фотогр', 'фр', 'франц', 'хим', 'хир', 'хоз',
              'хол', 'холод', 'хор', 'хр', 'христ', 'хрон', 'худ', 'худож', 'хут', 'цв', 'церк', 'час', 'част', 'чей-л',
              'чел', 'черт', 'четв', 'чеч', 'чеш', 'чешск', 'числ', 'числит', 'чл', 'чтв', 'что-л', 'что-н', 'шв',
              'швед', 'швейц', 'шилл', 'шир', 'шотл', 'шт', 'шутл', 'щел', 'эвенк', 'эвфем', 'экв', 'эквив', 'экз',
              'эккл', 'экон', 'эксп', 'элев', 'электротех', 'элем', 'эпид', 'эск', 'эст', 'югосл', 'юж', 'юр', 'юридич',
              'яз', 'языч', 'якут', 'янв', 'яп', 'япон', 'ящ', 'ёмк'}
    if token.lower() in abbrev:
        return True
    return False


def defile(token):
    tokenl = token.lower()
    if tokenl in defis:
        return [token]
    if tokenl[0].isalpha():
        for elem in startdef:
            if tokenl.startswith(elem):
                return [token]
    if tokenl[1].isalpha():
        for elem in enddef:
            if tokenl.endswith(elem):
                return [token]
    for elem in doubledef:
        if elem in tokenl:
            return [token]
    res = []
    matches = re.finditer('-', token)
    start = 0
    for match in matches:
        chunk = token[start:match.start()]
        if chunk:
            res.append(chunk)
        res.append(match.group(0))
        start = match.end()
        if not re.search('-', token[start:]):
            if token[start:]:
                res.append(token[start:])
    if res:
        if len([char for char in res if (char.isdigit() or char == '-')]) == len(res) and res[0] != '-' and res[-1] != '-':
            return [token]
        if res[0].isdigit() and len(res) > 2:
            if res[2].isalpha():
                return [token]
    return res


def tokenicer(string):
    if string.isspace():
        return
    punct = r'[.?!]+'
    spaces = ' \t'
    twos = r'[:;](?!=[)(*])'
    bracketsquotes = r'\'"\{\[\(\}\]\)«“‘»”’„'
    smiles = r'(?:[=:;][)(]{1,})|(?:\){2,}|\({2,}|[)(]{1,3}:|[=:;]\*+)'
    emoji = r'''(?:[\U0001F1E0-\U0001F1FF]|[\U0001F300-\U0001F5FF]|[\U0001F600-\U0001F64F]|[\U0001F680-\U0001F6FF]|
    [\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]|[\U0001F900-\U0001F9FF]|[\U0001FA00-\U0001FA6F]|
    [\U0001FA70-\U0001FAFF]|[\U00002702-\U000027B0]|[\U000024C2-\U0001F251])+'''
    other = r'[©$@%№\^&*+=\\/<>~]+|[\U000000A1-\U000000BF]+'  # другие знаки, какие пришли в голову и могут встретиться
    singles = r'[,…—– \t\'"\{\[\(\}\]\)\|«“‘»”’„]'
    delimiters = f'{smiles}|{twos}|{singles}|{punct}|{emoji}|{other}'  # emoji slows down for 2 sec
    pattern = re.compile(delimiters)
    if not re.search(pattern, string):
        return [string]
    matches = re.finditer(pattern, string)
    start = 0
    result = []
    joined = False
    addedlt = False
    bullet = False
    joinstring = []

    for match in matches:
        left_token = string[start:match.start()]
        delimit = match.group(0)
        if delimit.strip():
            delimiter = delimit.strip()
        else:
            delimiter = delimit
        start = match.end()

        if not result and left_token.isdigit() and not joinstring:
            if delimiter in '.)':
                result.append(left_token + delimiter)
                joined = True
                bullet = True

        if joinstring:
            if not left_token.isdigit():
                if len(joinstring) <= 2:
                    result.extend(joinstring)
                joinstring = []

        if left_token:
            check = re.findall(r'^([\d]+)([^\d]+)$', left_token)
            if check and (check[0][1]).isalpha():
                result.append(check[0][0])
                result.append(check[0][1])
                addedlt = True
                if delimiter == '.':
                    result[-1] += delimiter
                    joined = True
            if left_token.isdigit() and not bullet:
                if delimiter and delimiter in '.:\\/':
                    joinstring.append(left_token)
                    joinstring.append(delimiter)
                    joined = True
                elif joinstring:
                    result.append(''.join(joinstring) + left_token)
                    joinstring = []
                    addedlt = True

            if delimiter == '.' and not left_token.isdigit():
                if len(left_token) == 1:
                    if result:
                        if result[-1] == 'т.':
                            result[-1] += (left_token + delimiter)
                            joined = True
                    if not joined:
                        result.append(left_token + delimiter)
                        joined = True
                elif abbr(left_token):
                    result.append(left_token + delimiter)
                    joined = True
            if '-' in left_token and len(left_token) > 1:
                result.extend(defile(left_token))
                addedlt = True

            if not joined and not addedlt:
                result.append(left_token)

        if not delimiter.isspace():
            if not joined:
                result.append(delimiter)

        joined = False
        addedlt = False
        bullet = False

        if not re.search(pattern, string[start:]):
            if joinstring:
                if len(joinstring) <= 2 and not string[start:].isdigit():
                    result.extend(joinstring)
                    joinstring = []
                else:
                    if string[start:].isdigit():
                        result.append(''.join(joinstring) + string[start:])
                        joined = True
                    else:
                        result.append(''.join(joinstring))
                    joinstring = []
            if string[start:] and not joined:
                check = re.findall(r'^([\d]+)([^\d]+)$', string[start:])
                if check:
                    result.append(check[0][0])
                    result.append(check[0][1])
                else:
                    result.append(string[start:])
                joined = False

    return result


def tokenice(file):
    res = []
    for line in file:
        if line.strip():
            chunk = tokenicer(line.strip())
            if chunk:
                res.extend(chunk)
    return res


# path = open(r'F:\Python\files\datasets\norm_20190208.txt', 'r', encoding='utf8')
# t = time()
# # with open(r'F:\Python\files\datasets\interim.txt', 'w', encoding='utf8') as dumper:
# #     print(*tokenice(path), sep='\n', file=dumper)
# d = open(r'F:\Python\files\datasets\interimliner.txt', 'w', encoding='utf8')
# for line in path:
#     if line.strip():
#         print(line.strip(), file=d)
#         print(*tokenicer(line.strip()), sep='  |  ', file=d)
#         print('~' * 30, file=d)
# print(time() - t)
# path.close()
# d.close()

# s = ['Цена 200р']
# print(s)
# print(*tokenice(s), sep='  |  ')
