import PySimpleGUI as sg


layout = [[sg.Text("SBA - Sistema de Bibliotecário Autônomo")], [sg.Button("OK")]]


def Index(livros):
    layout = [[sg.Text("SBA - Sistema de Bibliotecário Autônomo")], [sg.Text("Livros Cadastrados")],
              [sg.Listbox(values=livros, size=(40, 20))], [sg.Button("OK")]]
    window = sg.Window('SBA - Sistema de Bibliotecário Autônomo', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'OK':
            break
    window.close()


def CadastroGui():
    layout = [[sg.Text("Cadastro de Livros")], [sg.Text("Nome do Livro"), sg.InputText()],
              [sg.Text("Código do Livro"), sg.InputText()], [sg.Text("Endereço do Livro"), sg.InputText()],
              [sg.Button("Cadastrar")], [sg.Button("Voltar")]]
    window = sg.Window('SBA - Sistema de Bibliotecário Autônomo', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Voltar':
            break
        if event == 'Cadastrar':
            return values[0], values[1], values[2]
            break

    window.close()