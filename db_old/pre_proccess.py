import re


def clear(word):
    # origin:            трц Сity-mall
    # remove stop word:  Сity-mall
    # remove symvols:    Сity mall
    # lowercase:         city mall
    # translate:         сити молл
    # merge:             ситимола
    # stemmer:           ситимол

    word = re.sub(r'[^\w]', ' ', word.strip().lower())
    word = word.replace('тц','').replace('тд','').replace('торговый центр','').replace('торговый дом','').replace('супермаркет','').replace('мини маркет','').replace('маркет','').strip()
    word = word.replace('продуктовый магазин','').replace('магазин продуктов','').replace('магазин','').replace('продукты','').strip()

    return word