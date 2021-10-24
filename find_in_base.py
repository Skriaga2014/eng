import pandas as pd

WORD = 'fluently'
N = 3

base = pd.read_csv('111.csv')
print(base)
print(base['word'].iloc[8048])


for i in range(N + 1):
    if i != 0:
        try:
            print(*base.loc[base['word'] == WORD[:-i]].iloc[0], sep=',')
            break
        except IndexError:
            None
    else:
        try:
            print(*base.loc[base['word'] == WORD].iloc[0], sep=',')
            break
        except IndexError:
            None
    if i == N:
        print('слово не найдено')



#
# try:
#     print(*base.loc[base['word'] == WORD].iloc[0], sep=',')
# except IndexError:
#     try:
#         print(*base.loc[base['word'] == WORD[:-1]].iloc[0], sep=',')
#     except IndexError:
#         print('слово не найдено')
#




