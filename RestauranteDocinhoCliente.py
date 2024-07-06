import socket

def enviar_pedido(servidor, dados):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_address = (servidor, 12345)
        print(f"Conectando-se a {server_address}")
        sock.connect(server_address)

        sock.sendall(dados.encode())

        response = sock.recv(4096).decode()
        print(f"Resposta do servidor:\n{response}")

    except Exception as e:
        print(f"Erro ao enviar dados para o servidor: {e}")

    finally:
        sock.close()

def menu_cliente():
    while True:
        print("---------- Restaurante Docinho ----------")
        print("| 1. Registrar Pedido                    |")
        print("| 2. Listar Pedidos                      |")
        print("| 3. Alterar Pedido                      |")
        print("| 4. Excluir Registro                    |")
        print("| 5. Transferir Pedido para Finalizado e Pago |")
        print("| 6. Sair                                |")
        print("-----------------------------------------")
        opcao = input("Selecione a opção: ")

        if opcao == '1':
            numero_pedido = input("Número do pedido: ")
            prato = input("Prato: ")
            tempo_preparo = input("Tempo de Preparo (min): ")
            valor = input("Valor (R$): ")
            dados = f"INCLUIR;{numero_pedido};{prato};{tempo_preparo};{valor}"
            enviar_pedido('localhost', dados)

        elif opcao == '2':
            dados = "LISTAR"
            enviar_pedido('localhost', dados)

        elif opcao == '3':
            numero_pedido = input("Número do pedido a alterar: ")
            prato = input("Novo Prato (deixe em branco para manter): ")
            tempo_preparo = input("Novo Tempo de Preparo (deixe em branco para manter): ")
            valor = input("Novo Valor (deixe em branco para manter): ")
            dados = f"ALTERAR;{numero_pedido};{prato};{tempo_preparo};{valor}"
            enviar_pedido('localhost', dados)

        elif opcao == '4':
            numero_pedido = input("Número do pedido a excluir: ")
            dados = f"EXCLUIR;{numero_pedido}"
            enviar_pedido('localhost', dados)

        elif opcao == '5':
            numero_pedido = input("Número do pedido a transferir para Finalizado e Pago: ")
            dados = f"TRANSFERIR;{numero_pedido}"
            enviar_pedido('localhost', dados)

        elif opcao == '6':
            print("Obrigado por utilizar nossos serviços!")
            break

        else:
            print("Opção inválida")

if __name__ == '__main__':
    menu_cliente()
