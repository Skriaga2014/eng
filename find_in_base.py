import pandas as pd

WORDS = ["foreign", "obvious", "surprising", "try on", "these", "trousers", "spend on"]
N = 3



base = pd.read_csv('111.csv')


def get_str(word):
    for i in range(N + 1):
        if i != 0:
            try:
                print(*base.loc[base['word'] == word[:-i]].iloc[0], sep=',')
                break
            except IndexError:
                None
        else:
            try:
                print(*base.loc[base['word'] == word].iloc[0], sep=',')
                break
            except IndexError:
                None
        if i == N:
            print('слово не найдено')

for word in WORDS:
    get_str(word)

#
# try:
#     print(*base.loc[base['word'] == WORD].iloc[0], sep=',')
# except IndexError:
#     try:
#         print(*base.loc[base['word'] == WORD[:-1]].iloc[0], sep=',')
#     except IndexError:
#         print('слово не найдено')
#




