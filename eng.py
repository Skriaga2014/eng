import pandas as pd
import datetime as dt


VARS_NUM = 5
TYPE = 'en'  # 'ru_en'/'en_ru'/'ru'/'en'
BASE_FILE = 'my_dict.csv'
BASE_FILE_RESERVE = 'my_dict_r.csv'


# load dictionary
def get_base(vars_num=VARS_NUM):
    # проверка, не затесалось ли nan в shows и/или result
    try:
        base = pd.read_csv(BASE_FILE, dtype={'shows': int, 'result': int})
    except ValueError:
        base = pd.read_csv(BASE_FILE).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})
    except KeyError:
        base = pd.read_csv(BASE_FILE_RESERVE).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})

    base = base.sample(frac=1)
    len_base = len(base)

    if len_base < vars_num:
        vars_num = len_base

    if TYPE in ['en', 'ru']:
        sorted_base = base.sort_values('result')
        base = sorted_base.head(vars_num)
        base2 = sorted_base.tail(len_base - vars_num)
        print(base, '\n', base2)
    else:
        base2 = None

    return base, base2


# create task and variants
def get_task_vars(base):
    def show_question(task, variants):
        if TYPE == 'ru_en':
            print(task['translate'].iloc[0])
            print(variants[['word', 'transcription']])
        elif TYPE == 'en_ru':
            print(task['word'].iloc[0], task['transcription'].iloc[0])
            print(variants['translate'])
        elif TYPE == 'ru':
            print(task['word'].iloc[0], task['transcription'].iloc[0])
        elif TYPE == 'en':
            print(task['translate'].iloc[0])
        else:
            exit(f'unknown TYPE: {TYPE}')

    if TYPE in ['ru_en', 'en_ru']:
        if len(base) < 4:
            exit('ERROR: Too short len of base')
        variants = base.sample(VARS_NUM)
        variants.index = [i for i in range(1, VARS_NUM + 1)]
        task = variants.sample()
    else:
        task = base.sample()
        variants = None

    # print('task:', task)
    # print('variants:', variants)

    show_question(task, variants)
    return task, variants


# Проверка ответа 0/1
def get_check(answer, task):
    if (answer.isnumeric() and int(answer) == task.index.tolist()[0]) or \
        (TYPE == 'ru' and answer == task['translate'].tolist()[0]) or \
        (TYPE == 'en' and answer == task['word'].tolist()[0]):
        return 1
    else:
        return 0


def to_log(task, variants, answer, check, file):
    line = f'\n{dt.datetime.now()};'
    match TYPE:
        case 'eng' | 'ru_en':
            if TYPE == 'ru_en':
                answer = variants.iloc[answer]['word'].to_list()[0]
            line += f'{TYPE};{task["id"].to_list()[0]};' \
                    f'{task["translate"].to_line()[0]};' \
                    f'{task["word"].to_list()[0]};'
        case 'ru' | 'en_ru':
            if TYPE == 'ru_en':
                answer = variants.iloc[answer]['translate'].to_list()[0]
            line += f'{TYPE};{task["id"].to_list()[0]};' \
                    f'{task["word"].to_list()[0]};' \
                    f'{task["translate"].to_list()[0]};'

    line += f'{answer};{check}'
    print(line)

    with open(file, 'a') as f:
        f.write(line)


def base_update(base, base2, task, check):
    base.loc[base['id'] == task['id'].iloc[0], ['shows']] += 1
    if check:
        base.loc[base['id'] == task['id'].iloc[0], ['result']] += 1
    print(type(base))
    print(type(base2))
    if type(base2) != int:
        base = pd.concat([base, base2])
    base.to_csv(BASE_FILE, index=0)
    base.to_csv(BASE_FILE_RESERVE, index=0)


# main
def go():
    base, base2 = get_base() # base2 may be not exists (== 0)
    task, variants = get_task_vars(base)
    answer = input('answer: ')
    check = get_check(answer, task)  # 1/0
    print('right' if check else f'wrong ({task["word"].tolist()[0]})\n')
    base_update(base, base2, task, check)
    to_log(task, variants, answer, check, 'log.csv')


while 1:
    go()




