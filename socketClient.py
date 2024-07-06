import socket
import os

# Função para verificar se o arquivo de relatório existe e criá-lo se não existir
def verificar_arquivo(relatorio_restaurante):
    if not os.path.isfile(relatorio_restaurante):
        with open(relatorio_restaurante, "w") as arquivo:
            arquivo.write("numeroPedido;prato;TempoPreparo;Valor;Status\n")
        print(f"Arquivo {relatorio_restaurante} criado")
        return False
    return True

# Função para adicionar um novo pedido ao arquivo
def adicionar_pedido(relatorio_restaurante, numero_pedido, prato, tempo_preparo, valor):
    with open(relatorio_restaurante, "a") as arquivo:
        arquivo.write(f"{numero_pedido};{prato};{tempo_preparo};{valor};Pendente\n")
    print(f"Pedido adicionado ao arquivo {relatorio_restaurante}")

# Função para listar os pedidos ordenados pelo número de registro
def listar_pedidos(relatorio_restaurante):
    if not verificar_arquivo(relatorio_restaurante):
        return "Arquivo de pedidos não encontrado."
    
    with open(relatorio_restaurante, "r") as arquivo:
        lines = arquivo.readlines()
    
    # Ignora a primeira linha (cabeçalho)
    lines = lines[1:]
    
    # Verifica se há pedidos para listar
    if not lines:
        return "Não há pedidos registrados."
    
    # Ordena os pedidos pelo número de registro (primeiro campo)
    lines.sort(key=lambda x: int(x.split(';')[0]))
    
    lista_pedidos = []
    for line in lines:
        numero_pedido, prato, tempo_preparo, valor, status = line.strip().split(';')
        lista_pedidos.append(f"N° pedido: {numero_pedido}, Prato: {prato}, Tempo de preparo: {tempo_preparo}, Valor: {valor}, Status: {status}")
    
    # Retorna a lista formatada
    return "\n".join(lista_pedidos)

# Função para excluir um pedido do arquivo
def excluir_pedido(relatorio_restaurante, numero_pedido):
    if not verificar_arquivo(relatorio_restaurante):
        return "Arquivo de pedidos não encontrado."
    
    with open(relatorio_restaurante, "r") as arquivo:
        lines = arquivo.readlines()
    
    # Procura pelo pedido com o número especificado
    encontrado = False
    with open(relatorio_restaurante, "w") as arquivo:
        for line in lines:
            if line.startswith(numero_pedido + ";"):
                encontrado = True
                # Altera o status para "Finalizado e Pago"
                arquivo.write(line.replace("Pendente", "Finalizado e Pago"))
            else:
                arquivo.write(line)
    
    if encontrado:
        lista_atualizada = listar_pedidos(relatorio_restaurante)
        return f"Pedido número {numero_pedido} transferido para Finalizado e Pago.\n\nLista atualizada:\n{lista_atualizada}"
    else:
        return f"Pedido número {numero_pedido} não encontrado."

# Função principal para lidar com as conexões dos clientes
def handle_client_connection(client_socket, relatorio_restaurante):
    while True:
        # Recebe os dados do cliente
        request = client_socket.recv(1024).decode()
        
        if not request:
            break
        
        # Processa a solicitação do cliente
        partes = request.split(';')
        comando = partes[0]
        
        if comando == "INCLUIR":
            if len(partes) == 5:
                _, numero_pedido, prato, tempo_preparo, valor = partes
                adicionar_pedido(relatorio_restaurante, numero_pedido, prato, tempo_preparo, valor)
                response = "Pedido adicionado com sucesso."
            else:
                response = "Formato inválido para adicionar pedido."
        
        elif comando == "LISTAR":
            response = listar_pedidos(relatorio_restaurante)
        
        elif comando == "ALTERAR":
            if len(partes) == 5:
                _, numero_pedido, prato, tempo_preparo, valor = partes
                # Lógica para alterar o pedido (ainda a ser implementada)
                response = "Funcionalidade de alteração ainda não implementada."
            else:
                response = "Formato inválido para alterar pedido."
        
        elif comando == "EXCLUIR":
            if len(partes) == 2:
                _, numero_pedido = partes
                response = excluir_pedido(relatorio_restaurante, numero_pedido)
            else:
                response = "Formato inválido para excluir pedido."
        
        elif comando == "TRANSFERIR":
            if len(partes) == 2:
                _, numero_pedido = partes
                response = excluir_pedido(relatorio_restaurante, numero_pedido)
            else:
                response = "Formato inválido para transferir pedido."
        
        else:
            response = "Comando inválido."
        
        # Envia a resposta de volta para o cliente
        client_socket.sendall(response.encode())
    
    client_socket.close()

# Função principal do servidor
def main():
    # Configuração do servidor
    server_host = 'localhost'
    server_port = 12345
    relatorio_restaurante = 'Pedidos.txt'
    
    # Criação do socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Liga o socket ao host e porta especificados
    server_socket.bind((server_host, server_port))
    
    # Coloca o socket em modo de escuta
    server_socket.listen(5)
    print(f"Servidor escutando em {server_host}:{server_port}...")
    
    try:
        # Loop principal para aceitar conexões de clientes
        while True:
            # Espera por uma conexão
            client_socket, client_address = server_socket.accept()
            print(f"Conexão estabelecida com {client_address}")
            
            # Manipula a conexão do cliente em uma thread separada
            handle_client_connection(client_socket, relatorio_restaurante)
    
    except Exception as e:
        print(f"Erro no servidor: {e}")
    
    finally:
        # Fecha o socket do servidor ao finalizar
        server_socket.close()
        print("Servidor encerrado.")

if __name__ == '__main__':
    main()
