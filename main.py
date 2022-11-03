from sqlalchemy import or_
import PySimpleGUI as sg
from assets.index import Index, CadastroGui
from db.Connection import db_connection, Base, Transaction
from db.Livro import Livro
from helpers.get_arg import get_arg
from helpers.window import window


def disponibilidade(disp_livro):
    livro = Transaction \
        .query(Livro) \
        .filter(or_(Livro.codigo == disp_livro,Livro.nome.like("%{}%".format(disp_livro)))) \
        .first()

    if livro.disponivel:
        return 'Disponivel'

    return 'Indisponivel'

def devolucao(dev_codigo):
    livro = Transaction \
        .query(Livro) \
        .filter(Livro.codigo == dev_codigo) \
        .first()

    if not livro.disponivel:
        confirmacao = input("Deseja Realmente devolver o livro: " + livro.nome + "? [s/N]: ")
        livro.disponivel = False
        Transaction.commit()
        print('Livro devolvido com sucesso!')
        livro.disponivel = True
        Transaction.commit()
    return livro

def cadastro(nome, codigo, endereco):
    livro = Livro(nome=nome, codigo=codigo, endereco=endereco)
    Transaction.add(livro)
    Transaction.commit()
    return livro


def emprestimo(isbn):
    livro = Transaction \
        .query(Livro) \
        .filter(Livro.codigo == isbn) \
        .first()

    if livro.disponivel:
        confirmacao = input("Deseja Realmente emprestar o livro: " + livro.nome + "? [s/N]: ")
        if confirmacao == 's' or confirmacao == 'S':
            livro.disponivel = False
            Transaction.commit()
            print('Livro emprestado com sucesso!')
    else:
        print('Livro indisponivel para emprestimo!')
    return


def atualizacao(session, livro, novo_nome,novo_codigo,novo_endereco):


        if novo_nome != '':
            livro.nome = novo_nome
        if novo_codigo != '':
            livro.codigo = novo_codigo
        if novo_endereco != '':
            livro.endereco = novo_endereco

        session.commit()

        return livro


def consultar(consul_livro):

    livros = Transaction \
        .query(Livro) \
        .filter(or_(Livro.nome.like("%{}%".format(consul_livro)), Livro.codigo == consul_livro)) \
        .all()
    return livros


def excluir(exclu_livro):

    livro_excluido = Transaction \
        .query(Livro) \
        .filter(Livro.codigo == exclu_livro) \
        .first()

    confirmacao = input("Deseja Realmente excluir o livro: " + livro_excluido.nome + "? [s/N]: ")
    if confirmacao == 's' or confirmacao == 'S':
        Transaction.delete(livro_excluido)
        Transaction.commit()

    return True


def menu_options():
    print('[1] - Cadastrar Livro')
    print('[2] - Atualizar livro')
    print('[3] - Consultar livro')
    print('[4] - Excluir livro')
    print('[5] - Empréstimo de livro')
    print('[6] - Devolução de livro')
    print('[7] - Disponibilidade de livro')
    print('[0] - Sair')
    print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')


def menu(opcao=-1):
    menu_options()

    while opcao != 0:
        opcao = int(input('Qual opção voce deseja escolher:'))

        match opcao:
            case 1:
                print('Cadastrar Livro')
                nome = input('Qual nome do livro? ')
                codigo = input('Qual ISBN do livro? ')
                endereco = input('Qual o endereço do livro? ')
                livro = cadastro(nome=nome, codigo=codigo, endereco=endereco)
                print(livro)
                menu()
            case 2:
                print('Atualizar Livro')
                novo_nome = input('Digite o nome atualizado [{}]: '.format(livro.nome))
                novo_codigo = input('Digite um novo codigo ISBN [{}]: '.format(livro.codigo))
                novo_endereco = input('Digite o novo endereço do livro [{}]: '.format(livro.endereco))
                menu()
            case 3:
                consul_livro = input('Digite o nome do livro ou codigo ISBN')
                print('Consultar Livro')
                livros = consultar(consul_livro)

                for livro in livros:
                    print("O que deseja fazer com o livro: " + livro.nome + "?")
                    print("[1] - Atualizar")
                    print("[2] - Excluir")
                    print("[ENTER] - continuar")
                    opcao = input('Qual opção voce deseja escolher:')

                    if opcao == '1':
                        novo_nome = input('Digite o nome atualizado [{}]: '.format(livro.nome))
                        novo_codigo = input('Digite um novo codigo ISBN [{}]: '.format(livro.codigo))
                        novo_endereco = input('Digite o novo endereço do livro [{}]: '.format(livro.endereco))

                        atualizacao(Transaction, livro,novo_nome ,novo_codigo,novo_endereco)
                    elif opcao == '2':
                        Transaction.delete(livro)
                        Transaction.commit()
                        print('Livro excluido com sucesso!')
                menu()

            case 4:
                exclu_livro = input('Qual O ISBN voce deseja excluir: ')
                print('Excluir Livro')
                excluir(exclu_livro)
                menu()
            case 5:
                print('Emprestimo de Livro')
                isbn = input('Digite o ISBN do livro que deseja emprestar: ')
                emprestimo(isbn)
                menu()

            case 6:
                print('Devolução de Livro')
                dev_codigo = input('Qual livro voce deseja devolver (ISBN)')
                devolucao(dev_codigo)
                menu()

            case 7:
                print('Disponibilidade de Livro')
                disp_livro = input('Qual livro gostaria de saber se está disponível ')
                livro_disponivel = disponibilidade(disp_livro)
                print(livro_disponivel)
                disponibilidade(disp_livro)
                menu()
            case 0:
                print('Saindo...')
                break
            case _:
                menu()

    return

def Appplication():
    layout = [[sg.Button("Cadastrar Livro")], [sg.Button("Listar Livros")], [sg.Button("Atualizar Livro")],
              [sg.Button("Excluir Livro")], [sg.Button("Emprestar Livro")], [sg.Button("Devolver Livro")],
              [sg.Button("Sair")]]
    windowgui = window(layout)


    while True:
        event, values = windowgui.read()
        match event:
            case 'Cadastrar Livro':
                cadastro_livro = CadastroGui()
                livro = cadastro(nome=cadastro_livro[0], codigo=cadastro_livro[1], endereco=cadastro_livro[2])
            case 'Listar Livros':
                    livros = Transaction.query(Livro).all()
                    Index(livros)
        if event == "Sair" or event == sg.WIN_CLOSED:
            break
    return

def init_db():
    print('Inicializando banco de dados...')
    print(Base.metadata.create_all(db_connection()))
    print('Banco de dados inicializado com sucesso!')


def main():
    print("Iniciando SBA - Sistema do Bibliotecário Autônomo")
    if get_arg('gui') == 'true':
        print("Iniciando GUI")
        Appplication()
        return

    if get_arg('init_db') == 'true':
        init_db()
        return

    print('Iniciando menu...')
    menu()
    print('SBA - Sistema do Bibliotecário Autônomo finalizado')

if __name__ == '__main__':
    main();
