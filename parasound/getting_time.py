import os
import numpy as np
import pandas as pd
import PySimpleGUI as sg
from datetime import datetime


# 09/08/22
# При написании этого скрипта была совершена тотальная ошибка
# Я читал .acf файлы функцией open() и при чтении файла как file.readline() возникало множество ошибок
# всвязи с тем, что формат данных был динамичный. Эти ошибки не контрились try\except.
# Решение было гениально простым. Читать файл по байтово open(name, 'rb')


# Функции для подгрузки данных
def get_timeTRG(line):  # Получить из строки где есть фраза "timeTRG" значения времени
    h = ''
    value = ''
    for i in line:
        if 'timeTRG="' not in h:
            h = h + i
        if 'timeTRG="' in h and i != '"':
            value = value + i
        if 'timeTRG="' in h and len(value) != 0 and i == '"':
            break
    return float(value)


def get_coord(line):
    h = ''
    value = ''
    for i in line:
        if value != '' and i == ' ':
            break
        if '">' in h:
            value = value + i
        if '">' not in h:
            h = h + i
    return float(value)


def acf_to_dict(path, acf_name):

    file_acf = open(os.path.join(path, acf_name), 'rb')
    file_idx = open(os.path.join(path, acf_name + '.idx'))

    idx = []
    for line in file_idx:
        if line != '':
            line = line.replace('\n', '')[-37:]
            idx.append(line)
    file_idx.close()

    data_set = {'asd': [], 'acf': [], 'time': [], 'lat': [], 'lon': []}

    ind_number = -1
    for line in file_acf:
        a = str(line)

        if 'calibrDate' in a:
            ind_number = ind_number + 1
        if 'lat noItems' in a:
            lat = get_coord(a)
        if 'lon noItems' in a:
            lon = get_coord(a)
        if 'timeTRG' in a:
            data_set['time'].append(get_timeTRG(a))
            data_set['asd'].append(idx[ind_number])
            data_set['acf'].append(acf_name)
            data_set['lat'].append(lat)
            data_set['lon'].append(lon)
    file_acf.close()

    return data_set


def folder_to_dict(path):
    file_names = os.listdir(path)

    line = []
    for i in file_names:
        if i[-3:] == 'acf':
            line.append(acf_to_dict(path, i))

    full_dict = {i: [] for i in line[0]}
    for i in line:
        for j in i:
            full_dict[j] = full_dict[j] + i[j]

    return full_dict


# Функция для подгрузки .loc файла
def change_file(path):

    header = ['PSX', 'PSY', 'DT']

    file = open(path)
    all_parts = []
    for ps in file:

        part = []
        element = ''
        if header[0] in ps and len(ps) < 70:  # длина строки подобрана опытным путем
            for i in ps:
                if i != ',' and i != '\n':
                    element = element + i
                else:
                    if len(element) != 0:
                        for head_name in header:
                            if head_name in element:
                                part.append(element)
                    element = ''

            if len(part) == len(header):
                all_parts.append(part)

    data = {}
    for i in header:
        data[i] = []

    for part in all_parts:
        for element in part:
            for head in header:
                if head in element:
                    if 'DT' in element:
                        data[head].append(element[len(head):])
                    else:
                        data[head].append(float(element[len(head):]))

    time_1970 = []
    for i in data['DT']:
        date_class = datetime.strptime(i[:-4], '%d.%m.20%y %H:%M:%S')
        time_1970.append(date_class.timestamp() + float(i[-4:]))

    data['DT'] = time_1970

    return data


# Отрисовка окна программы

sg.theme('DarkAmber')
sg.set_options(font='Cambria 12')

col = [
    [sg.Text('Profilograph GPS maker', font='Cambria 15', pad=(0, 20))],
    [sg.Button('Loc file', size=10)],
    [sg.Button('Data folder', size=10)],
    [sg.Button('Save', size=10)]
]

layout = [[sg.VSeparator(),
           sg.Column(col, element_justification='c'),
           sg.VSeparator()]]

window = sg.Window('IPGG Industries', layout)

save_file_name = ''
folder_path = ''
loc_path = ''
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # Подгрузка .loc файла
    if event == 'Loc file':
        loc_path = sg.popup_get_file('Load .loc file', multiple_files=False, no_window=True)

        if len(loc_path) != 0:
            loc = change_file(loc_path)
            sg.popup_ok('Loc file loaded!')
        else:
            sg.popup_error('File not found!')

    # Подгрузка данных
    if event == 'Data folder':
        folder_path = sg.popup_get_folder('Choose data folder', no_window=True)

        if len(folder_path) != 0:
            prof_data = folder_to_dict(folder_path)
            sg.popup_ok('Data loaded!')
        else:
            sg.popup_error('Folder not found!')

    # Обработка фалов и сохранение
    if event == 'Save':
        if len(folder_path) != 0:
            path_to_save = sg.popup_get_folder('Path to save .csv', no_window=True)
            save_file_name = sg.popup_get_text('Enter file name')

            inter_x = np.interp(prof_data['time'], loc['DT'], loc['PSX'])
            inter_y = np.interp(prof_data['time'], loc['DT'], loc['PSY'])

            prof_data['X'] = inter_x
            prof_data['Y'] = inter_y

            # Отрисовка координат от времени
            # fig = plt.figure()
            # plt.plot((np.array(loc['DT']) - min(np.array(loc['DT'])))/3600, loc['PSX'], '.')
            # plt.plot((np.array(prof_data['time']) - min(np.array(loc['DT'])))/3600, prof_data['X'], '.')
            # plt.show()
            #
            # fig = plt.figure()
            # plt.plot((np.array(loc['DT']) - min(np.array(loc['DT'])))/3600, loc['PSY'], '.')
            # plt.plot((np.array(prof_data['time']) - min(np.array(loc['DT'])))/3600, prof_data['Y'], '.')
            # plt.show()

            df = pd.DataFrame(prof_data)

            # Выгрузка данных .loc и .acf для проверки
            # time_data = np.array(prof_data['time'])
            # loc_data = np.array(loc['DT'])
            # loc_x = np.array(loc['PSX'])
            #
            # np.save('time_data.npy', time_data)
            # np.save('loc_data.npy', loc_data)
            # np.save('loc_x.npy', loc_x)

            df.to_csv(os.path.join(path_to_save, save_file_name)+'.csv', index=False)
            sg.popup_ok('File created!')

        else:
            sg.popup_error('Choose folder!')
