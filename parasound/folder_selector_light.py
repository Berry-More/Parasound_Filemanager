import os
import shutil
import PySimpleGUI as sg
from datetime import datetime


# Создание недостающих папок профилей и копирование файлов профиля по папкам
def file_selection(path_in, path_out, time_start, time_end, folder_name):

    time_start = datetime.strptime(time_start, '%d_%m_%y-%H_%M_%S')
    time_end = datetime.strptime(time_end, '%d_%m_%y-%H_%M_%S')

    line_folder = os.path.join(path_out, folder_name)
    os.mkdir(line_folder)

    file_names = os.listdir(path_in)

    for i in file_names:
        if i[-4:] == '.acf' or i[-4:] == '.idx':
            ftime = datetime.strptime(i[7:24], '20%y-%m-%dT%H%M%S')
            if ftime >= time_start and ftime <= time_end:
                shutil.copy(os.path.join(path_in, i), line_folder)

    return


# Отрисовка окна программы
# 'Reddit'

sg.theme('LightBrown6')
sg.set_options(font='Cambria 12')

col1 = [
    [sg.Text('IPGG Industries', font='Arial 20', pad=(0, 10))],
    [sg.Text('Path to .acf folder')],
    [sg.Button('Data', size=10)],
    [sg.Text('Path to lines catalog')],
    [sg.Button('Catalog', size=10)]
]

col2 = [
    [sg.Text('Data start (format: dd_mm_yy-hh_mm_ss)')],
    [sg.InputText(size=(50, 5), key='TSTART')],
    [sg.Text('Data end (format: dd_mm_yy-hh_mm_ss)')],
    [sg.InputText(size=(50, 5), key='TEND')],
    [sg.Text('Folder name')],
    [sg.InputText(size=(50, 5), key='FNAME')],
    [sg.Button('Select', size=10, pad=(0, 10))]
]

layout = [[sg.Column(col1, element_justification='c'),
           sg.VSeparator(),
           sg.Column(col2, element_justification='l')]]

window = sg.Window('IPGG Industries', layout)

data_path = ''
catalog_path = ''
csv_path = ''
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    # Подгрузка данных
    if event == 'Data':
        data_path = sg.popup_get_folder('Choose data folder', no_window=True)
        if len(data_path) != 0:
            sg.popup_ok('Good job!')
        else:
            sg.popup_error('Folder not found!')

    # Обработка фалов и сохранение
    if event == 'Catalog':
        catalog_path = sg.popup_get_folder('Choose catalog folder', no_window=True)
        if len(catalog_path) != 0:
            sg.popup_ok('You fantastic!')
        else:
            sg.popup_error('Folder not found!')

    if event == 'Select':
        if len(data_path) == 0 or len(catalog_path) == 0:
            sg.popup_error('Data not found!')
        else:
            t_start = window['TSTART'].get()
            t_end = window['TEND'].get()
            folder = window['FNAME'].get()

            # Папочный передел
            file_selection(data_path, catalog_path, t_start, t_end, folder)

            sg.popup_ok('New line created!')
