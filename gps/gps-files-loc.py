import os
import pandas as pd
import PySimpleGUI as sg


def time_to_list(time):

    date = []

    element = ''
    for i in range(len(time)):
        if time[i] != ' ' and time[i] != ':' and i != len(time)-1:
            element = element + time[i]
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

    f = open(path)
    a1 = f.readline()
    a2 = f.readline()
    a3 = f.readline()

    for_header = [a1, a2, a3]

    header = make_header(for_header)

    f = open(path)
    block_data = []
    line = '1'
    while len(line) > 0:
        line = f.readline()
        element = ''
        for i in line:
            if i != ',' and i != '\n' and i != line[-1]:
                element = element + i
            else:
                block_data.append(element)
                element = ''

    data = {}
    for i in header:
        data[i] = []

    for i in block_data:
        for j in header:
            if j in i:
                data[j].append(i[len(j):])

    data['Date'] = []
    data['Hours'] = []
    data['Minutes'] = []
    data['Seconds'] = []

    for i in data['PR_DateTime']:
        form = time_to_list(i)
        data['Date'].append(form[0])
        data['Hours'].append(form[1])
        data['Minutes'].append(form[2])
        data['Seconds'].append(form[3])
        # data['PR_DateTime'][i] = data['PR_DateTime'][i].replace(' ', ',')
        # data['PR_DateTime'][i] = data['PR_DateTime'][i].replace(':', ',')

    data.pop('PR_DateTime')
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
