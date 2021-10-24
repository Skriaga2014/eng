import pandas as pd
import datetime as dt


VARS_NUM = 5
TYPE = 'en' # 'ru_en'/'en_ru'/'ru'/'en'
BASE_FILE = 'my_dict.csv'
BASE_FILE_RESERVE = 'my_dict_r.csv'


# load dictionary
def get_base(file, file_r, type_=TYPE, vars_num=VARS_NUM):
    # проверка, не затесалось ли nan в shows и/или result
    #file = '1231.csv'
    try:
        base = pd.read_csv(file, dtype={'shows': int, 'result': int})
    except ValueError:
        base = pd.read_csv(file).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})
    except KeyError:
        base = pd.read_csv(file_r).fillna(0)
        base = base.astype({'shows': 'int32', 'result': int})

    if len(base) < vars_num:
        vars_num = len(base)

    if type_ in ['en', 'ru']:
        base = base.sort_values('result').head(vars_num)
    #base = base.set_index(base['id'])
    print(base)
    return base


# create task and variants
def get_task_vars(base, VARS_NUM, TYPE):
    def show_question(task, variants, TYPE):
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
        variants = base.sample(VARS_NUM)
        variants.index = [i for i in range(1, VARS_NUM + 1)]
        task = variants.sample()
    else:
        if len(base) < 4:
            exit('ERROR: Too short len of base')
        task = base.sample(VARS_NUM)
        variants = None

    show_question(task, variants, TYPE)
    return task, variants


# Проверка ответа 0/1
def get_check(answer, task, TYPE):
    if (answer.isnumeric() and int(answer) == task.index.tolist()[0]) or \
        (TYPE == 'ru' and answer == task['translate'].tolist()[0]) or \
        (TYPE == 'en' and answer == task['word'].tolist()[0]):
        return 1
    else:
        return 0


def to_log(typee, task, variants, answer, check, file):
    line = f'\n{dt.datetime.now()};'
    match typee:
        case 'eng' | 'ru_en':
            if typee == 'ru_en':
                answer = variants.iloc[answer]['word'].to_list()[0]
            line += f'{typee};{task["id"].to_list()[0]};' \
                    f'{task["translate"].to_line()[0]};' \
                    f'{task["word"].to_list()[0]};'
        case 'ru' | 'en_ru':
            if typee == 'ru_en':
                answer = variants.iloc[answer]['translate'].to_list()[0]
            line += f'{typee};{task["id"].to_list()[0]};' \
                    f'{task["word"].to_list()[0]};' \
                    f'{task["translate"].to_list()[0]};'

    line += f'{answer};{check}'
    print(line)

    with open(file, 'a') as f:
        f.write(line)


def base_update(base, task, check, base_file, base_file_reserve):
    base.loc[base['id'] == task['id'][0], ['shows']] += 1
    if check:
        base.loc[base['id'] == task['id'][0], ['result']] += 1
    base.to_csv(base_file, index=0)
    base.to_csv(base_file_reserve, index=0)

# main
def go():
    base = get_base(BASE_FILE, BASE_FILE_RESERVE)
    task, variants = get_task_vars(base, VARS_NUM, TYPE)
    answer = input('answer: ')
    check = get_check(answer, task, TYPE)
    base_update(base, task, check, BASE_FILE, BASE_FILE_RESERVE)
    print('right' if check else f'wrong ({task["translate"].tolist()[0]})\n')
    to_log(TYPE, task, variants, answer, check, 'log.csv')


while 1:
    go()




