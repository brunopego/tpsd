import socket

'''
Esta classe será a classe com a qual o usuário irá interagir solicitando
a quantidade de produto que deseja comprar
'''

class cliente():

    #Construtor contendo o endereço ip da máquina que roda o controlador
    #o endereço do próprio cliente e a porta do controlador por onde será feita a comunicação
    def __init__(self):
        self.hostconnectControlador = '127.0.0.1'
        self.host = '127.0.0.1'
        self.port = 5005


    #Método onde se cria um socket para comunicação com o controlador de produção
    def pedido(self, resp, v = None):

        #O bloco abaixo cria o socket, conecta ao controlador e envia a quantidade de produtos que o usuário digitou
        self.s = socket.socket()
        self.s.connect((self.hostconnectControlador, self.port))
        self.s.send(resp.encode('utf-8'))
        #A linha abaixo fica esperando a resposta do controlador e logo após fecha o socket de comunicação
        msg = self.s.recv(128).decode('utf-8')
        print("Resposta do Controlador de Produção: " + msg)
        self.s.close()


    #Esta função serve apenas para receber a resposta do controlador de produção
    def respostaControlador(self):
        msg = self.s.recv(128).decode('utf-8')
        print("Resposta do Controlador de Produção: " + msg)
        return 0


#Método principal onde se chama o construtor do cliente
def main():
    print("Fábrica")
    cli = cliente()

    #Laço em que o usuário terá a opção de escolher se deseja fazer um pedido
    while True:
        resp = input("Deseja fazer um pedido [s/n]? ")

        #Se o usuário digita 's' ou 'S' então ele digita uma quantidade de produtos para fazer
        if resp.lower() == 's':
            resp = input("Quantas cadeiras voce deseja que sejam produzidas? ")
            cli.pedido(resp)

        # Se o usuário digita 'n' ou 'N' então ele sai da aplicação e a conexão é fechada
        # Caso o primeiro comando seja 'n' ou 'N', não houve criação do socket, logo deve-se tratar
        # e sair sem tentar fechar socket
        elif resp.lower() == 'n':
            try:
                cli.s.close()
            except Exception:
                pass
            break

if __name__ == '__main__':
    main()