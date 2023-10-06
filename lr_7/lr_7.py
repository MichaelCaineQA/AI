import pymorphy3

morph = pymorphy3.MorphAnalyzer(lang='ru')
a = input()
word = morph.parse(a)[0]
wordCase = str(word.tag.case)

print("Ввдённое слово:", a)
match wordCase:
    case "nomn":
        print("Именительный падеж")
    case "gent":
        print("Родительный падеж")
    case "datv":
        print("Дательный падеж")
    case "accs":
        print("Винительный падеж")
    case "ablt":
        print("Творительный падеж")
    case "loct":
        print("Предложный падеж")
    case "voct":
        print("Звательный падеж")
    case "gen1":
        print("Первый родительный падеж")
    case "gen2":
        print("Второй родительный (частичный) падеж")
    case "acc2":
        print("Второй винительный падеж")
    case "loc1":
        print("Первый предложный падеж")
    case "loc2":
        print("Второй предложный (местный) падеж")

print("Склонения:")
if 'NOUN' in word.tag.POS:
    print('Единственное число:')
    print('Именительный падеж:', word.inflect({'nomn'}).word)
    print('Родительный падеж:', word.inflect({'gent'}).word)
    print('Дательный падеж:', word.inflect({'datv'}).word)
    print('Винительный падеж:', word.inflect({'accs'}).word)
    print('Творительный падеж:', word.inflect({'ablt'}).word)
    print('Предложный падеж:', word.inflect({'loct'}).word)
    print('Множественное число:')
    print('Именительный падеж:', word.inflect({'nomn', 'plur'}).word)
    print('Родительный падеж:', word.inflect({'gent', 'plur'}).word)
    print('Дательный падеж:', word.inflect({'datv', 'plur'}).word)
    print('Винительный падеж:', word.inflect({'accs', 'plur'}).word)
    print('Творительный падеж:', word.inflect({'ablt', 'plur'}).word)
    print('Предложный падеж:', word.inflect({'loct', 'plur'}).word)
else:
    print('Не существительное')
