import os
import shutil
import PySimpleGUI as sg


# Чтение CSV файла, где значения идут через запятую
def read_file(file):
    head_line = file.readline()
    data = {}

    if ',' in head_line:
        separator = ','
    if ';' in head_line:
        separator = ';'

    element = ''
    for i in head_line:
        if i != separator and i != '\n':
            element = element + i
        else:
            data[element] = []
            element = ''

    value = ''
    for line in file:
        col_number = 0
        for i in line:
            if i != separator and i != '\n':
                value = value + i
            else:
                data[list(data.keys())[col_number]].append(value)
                value = ''
                col_number += 1

    return data


# Создание недостающих папок профилей и копирование файлов профиля по папкам
def file_selection(path_in, path_out, tab, lines_col, files_col):

    # Сначала создаю все папки, которые встречаются в табличке
    line_folders = os.listdir(path_out)
    for i in tab[lines_col]:
        if i in line_folders:
            continue
        else:
            os.mkdir(os.path.join(path_out, i))
            line_folders = os.listdir(path_out)

    # Копирую недостающие файлы в созданные ранее папки
    for i in range(len(tab[files_col])):
        if tab[files_col][i] in os.listdir(os.path.join(path_out, tab[lines_col][i])):
            continue
        else:
            shutil.copy(os.path.join(path_in, tab[files_col][i]),
                        os.path.join(path_out, tab[lines_col][i]))
            shutil.copy(os.path.join(path_in, tab[files_col][i] + '.idx'),
                        os.path.join(path_out, tab[lines_col][i]))
    return


# Отрисовка окна программы.

sg.theme('BrightColors')
sg.set_options(font='Cambria 12')

col1 = [
    [sg.Text('Path to .acf folder')],
    [sg.Button('Data', size=10)],
    [sg.Text('Path to lines catalog')],
    [sg.Button('Catalog', size=10)],
    [sg.Text("Operator's report")],
    [sg.Button('.csv', size=10)],
]

col2 = [
    [sg.Text('IPGG Industries', font='Arial 20')],
    [sg.Output(size=(35, 5)), sg.Listbox(['File names'], key='LISTBOX-F', size=(10, 5)),
     sg.Listbox(['Lines'], key='LISTBOX-L', size=(5, 5))],
    [sg.Button('Select', size=50)]
]

layout = [[sg.Column(col1, element_justification='c'),
           sg.VSeparator(),
           sg.Column(col2, element_justification='c')]]

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
            print(data_path)
        else:
            sg.popup_error('Folder not found!')

    # Обработка фалов и сохранение
    if event == 'Catalog':
        catalog_path = sg.popup_get_folder('Choose catalog folder', no_window=True)
        if len(catalog_path) != 0:
            print(catalog_path)
        else:
            sg.popup_error('Folder not found!')

    # Подгрузка .csv файла
    if event == '.csv':
        csv_path = sg.popup_get_file('Load .csv file', multiple_files=False, no_window=True)
        if len(csv_path) != 0:
            print(csv_path)
            csv_file = open(csv_path)
            tab = read_file(csv_file)
            window['LISTBOX-F'].update(values=list(tab.keys()))
            window['LISTBOX-F'].set_value(list(tab.keys())[0])
            window['LISTBOX-L'].update(values=list(tab.keys()))
            window['LISTBOX-L'].set_value(list(tab.keys())[0])
        else:
            sg.popup_error('File not found!')

    if event == 'Select':
        if len(data_path) == 0 or len(catalog_path) == 0 or len(csv_path) == 0:
            sg.popup_error('Data not found!')
        else:
            # Чтение выбранных столбцов
            files_col_name = window['LISTBOX-F'].get()[0]
            lines_col_name = window['LISTBOX-L'].get()[0]
            print('Starting selection... ')
            print('File names column = "' + files_col_name + '"')
            print('Lines column = "' + lines_col_name + '"')

            # Папочный передел
            file_selection(data_path, catalog_path, tab, lines_col_name, files_col_name)
            print('Selection end!!!')
