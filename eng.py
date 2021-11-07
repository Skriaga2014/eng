"""
Программа изучения слов иностранного языка.
Выводит случайное слово из числа (VARS_NUM) слов, которые были верно переведены минимальное число раз.
Направление перевода (на русский или с русского) выбирается случайным образом.
"""

import pandas as pd
import datetime as dt
import os
import random as rnd


# load dictionary
def get_base():
    # проверка, есть ли nan в shows и/или result
    try:
        base = pd.read_csv(BASE_FILE, dtype={'shows': int, 'result': int})
    except ValueError:  # если nan найдено
        base = pd.read_csv(BASE_FILE).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})
    except KeyError:    # если проблема с базой в результате сбоя предыдущей выгрузки
        base = pd.read_csv(BASE_FILE_RESERVE).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})

    if len(base) < VARS_NUM:    # если количество слов в базе меньше
        vars_num = len(base)
    else:
        vars_num = VARS_NUM

    base = base.sort_values('result')
    base_new = base.head(vars_num).sample(frac=1)
    base_add = base.tail(len(base) - vars_num)

    return base_new, base_add


def to_log(log):    # date,variants, type,id,task,target,answer,result
    line = f'\n{dt.datetime.now()},{SHOW_VARIANTS},'
    log_items = ['lang', 'idx', 'task', 'right_answer', 'answer', 'check']
    line += ','.join([str(log[i]) for i in log_items])
    print(line)

    with open(LOG_FILE, 'a') as f:
        f.write(line)


def base_update(base, base_add, log):
    base.loc[base['id'] == log['idx'], ['shows']] += 1
    if log['check']:
        base.loc[base['id'] == log['idx'], ['result']] += 1
    base_final = pd.concat([base, base_add])

    base_final.to_csv(BASE_FILE, index=0)
    base_final.to_csv(BASE_FILE_RESERVE, index=0)


def get_task(base, lang):
    sample = base.sample()
    if lang == 'en':
        task = sample['translate'].iloc[0]
        right_answer = sample['word'].iloc[0]
    else:
        task = sample['word'].iloc[0]
        right_answer = sample['translate'].iloc[0]
    if '/' in task:
        task = task.split('/')
    idx = sample['id'].iloc[0]
    return idx, task, right_answer


def get_check(answer, right_answer):
    if answer == right_answer or answer in right_answer:
        print('yes')
        return 1
    else:
        print('no')
        print(f'({right_answer})')
        return 0


def run(base, lang):
    idx, task, right_answer = get_task(base, lang)
    if SHOW_VARIANTS:
        print(task)
        variants = base['translate'] if lang == 'ru' else base[['word', 'transcription']]
        variants.index = range(1, len(base) + 1)
        print(variants)
        answer = input('Enter number or word: ')
        if answer.isdigit():
            if lang == 'ru':
                answer = variants.loc[int(answer)]
            else:
                answer = variants.loc[int(answer), 'word']
    else:
        answer = input(f'{task}: ')

    check = get_check(answer, right_answer)

    return {'check': check, 'idx': idx, 'task': task,
            'right_answer': right_answer,
            'answer': answer, 'lang': lang}


# main
def go():
    lang = rnd.choice(['en', 'ru'])
    base, base_add = get_base()
    log = run(base, lang)
    to_log(log)
    base_update(base, base_add, log)


SHOW_VARIANTS = False    # показывать ли варианты ответов
VARS_NUM = 5
BASE_FILE = os.path.join(os.getcwd(), 'my_dict.csv')
BASE_FILE_RESERVE = os.path.join(os.getcwd(), 'my_dict_r.csv')
LOG_FILE = os.path.join(os.getcwd(), 'log.csv')


pd.set_option('display.expand_frame_repr', False)
while 1:
    go()




