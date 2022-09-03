import os
import numpy as np
import pandas as pd
import PySimpleGUI as sg


def change_file(path, out):
    df = pd.read_csv(path, header=None)

    head = []
    for i in df:
        head.append(i)

    data = {}
    for i in head:
        if type(df[i][0]) == str:
            data['Date'] = df[i]
        if type(df[i][0]) == np.float64:
            if df[i][0] > 500 and df[i][0] < 1000000:
                data['X'] = df[i]
            if df[i][0] > 1000000:
                data['Y'] = df[i]

    edit_file = open(out, 'w')
    for j in range(len(data['X'])):
        edit_file.write(str(data['Date'][j]).replace(':', '\t') + '\t' + str(data['X'][j]) + '\t' + str(data['Y'][j]) + '\n')

    edit_file.close()

    return


sg.theme('SystemDefaultForReal')
sg.set_options(font='Cambria 12')

left_col = [[sg.Text('Choose gps file')],
            [sg.Button('Load')],
            [sg.Input(key='NAME')]]

right_col = [[sg.Text('Path to new file')],
             [sg.Button('Save')]]

layout = [[sg.Column(left_col, element_justification='c'),
           sg.VSeparator(),
           sg.Column(right_col, element_justification='c')]]

window = sg.Window('File redactor', layout)

filename = 0
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Load':
        filename = sg.popup_get_file('Load data', multiple_files=False, no_window=True)

    if event == 'Save':
        if filename == 0:
            sg.Print('Not found!', text_color='white', background_color='orange')
        else:
            folder_path = sg.popup_get_folder('Folder for save', no_window=True)
            new_name = window['NAME'].get()
            if new_name == '':
                new_name = 'newfile.txt'
            else:
                new_name = new_name + '.txt'

            folder_path = os.path.join(folder_path, new_name)

            change_file(filename, folder_path)
            sg.Print('Ready!')
