import os
import pandas as pd
import PySimpleGUI as sg
from datetime import datetime


def time_to_list(time):

    date = []

    element = ''
    for i in range(len(time)):
        if time[i] != ' ' and time[i] != ':' and i != len(time) - 1:
            element = element + time[i]
        else:
            if i == len(time) - 1:
                element = element + time[i]
                date.append(element)
                element = ''
            else:
                date.append(element)
                element = ''

    return date


def make_header(lines):

    names = ['X', 'Y', 'Z']

    elements = []
    element = ''
    for j in lines:
        for i in j:
            if i != '_':
                element = element + i
            else:
                elements.append(element)
                element = ''
                break

    header = []
    for i in elements:
        for j in names:
            header.append(i + '_' + j)

    header.append('PR_DateTime')

    return header


def change_file(path, out):

    header = ['PSX', 'PSY', 'DT']

    file = open(path)
    all_parts = []
    ps = [1]
    while len(ps) != 0:

        part = []
        file.readline()
        file.readline()
        file.readline()
        ps = file.readline()

        element = ''
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
                    data[head].append(element[len(head):])

    time_1970 = []
    for i in data['DT']:
        date_class = datetime.strptime(i[:-4], '%d.%m.20%y %H:%M:%S')
        time_1970.append(date_class.timestamp() + float(i[-4:]))

    data['DT'] = time_1970

    df = pd.DataFrame(data)
    df.to_csv(out, index=False)

    return


sg.theme('DarkAmber')
sg.set_options(font='Cambria 12')

left_col = [[sg.Text('Choose gps file')],
            [sg.Button('Load')]]

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
            new_name = sg.popup_get_text('Enter file name')
            if new_name == '':
                new_name = 'newfile.csv'
            else:
                new_name = new_name + '.csv'

            folder_path = os.path.join(folder_path, new_name)

            change_file(filename, folder_path)
            sg.Print('Ready!')
