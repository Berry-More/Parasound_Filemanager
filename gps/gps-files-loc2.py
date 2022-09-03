import os
import pandas as pd
import PySimpleGUI as sg


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

    header = ['PR_X', 'PR_Y', 'PR_Z', 'DT',
              'T2X', 'T2Y', 'T1X', 'T1Y']

    file = open(path)
    all_parts = []
    a1 = [1]
    while len(a1) != 0:

        part = []
        a1 = file.readline()
        a2 = file.readline()
        a3 = file.readline()
        file.readline()
        three_lines = [a1, a2, a3]

        element = ''
        for line in three_lines:
            for i in line:
                if i != ',' and i != '\n':
                    element = element + i
                else:
                    if len(element) != 0:
                        for head_name in header:
                            if head_name in element:
                                if 'DT' in element:
                                    if three_lines.index(line) == 0:
                                        part.append(element)
                                else:
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

    data['Date'] = []
    data['Hours'] = []
    data['Minutes'] = []
    data['Seconds'] = []

    for i in data['DT']:
        form = time_to_list(i)
        data['Date'].append(form[0])
        data['Hours'].append(form[1])
        data['Minutes'].append(form[2])
        data['Seconds'].append(form[3])

    data.pop('DT')
    df = pd.DataFrame(data)
    df.to_csv(out, index=False)

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
                new_name = 'newfile.csv'
            else:
                new_name = new_name + '.csv'

            folder_path = os.path.join(folder_path, new_name)

            change_file(filename, folder_path)
            sg.Print('Ready!')
