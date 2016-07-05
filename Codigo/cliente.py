import socket

'''
Esta classe sera a classe com a qual o usuario ira interagir solicitando
a quantidade de produto que deseja comprar
'''

class cliente():

    #Construtor contendo o endereco ip da maquina que roda o controlador
    #o endereco do proprio cliente e a porta do controlador por onde sera feita a comunicacao
    def __init__(self):
        self.hostconnectControlador = '127.0.0.1'
        #self.host = '127.0.0.1'
        #self.port = 5005
        self.portControlador = 4000


    #Metodo onde se cria um socket para comunicacao com o controlador de producao
    def pedido(self, resp, v = None):

        #O bloco abaixo cria o socket, conecta ao controlador e envia a quantidade de produtos que o usuario digitou
        self.s = socket.socket()
        self.s.connect((self.hostconnectControlador, self.portControlador))
        self.s.send(resp.encode('utf-8'))
        #A linha abaixo fica esperando a resposta do controlador e logo apos fecha o socket de comunicacao
        msg = self.s.recv(128).decode('utf-8')
        print("Resposta do Controlador de Producao: " + msg)
        self.s.close()


    #Esta funcao serve apenas para receber a resposta do controlador de producao
    def respostaControlador(self):
        msg = self.s.recv(128).decode('utf-8')
        print("Resposta do Controlador de Producao: " + msg)
        return 0


#Metodo principal onde se chama o construtor do cliente
def main():
    print("Fabrica")
    cli = cliente()

    #Laco em que o usuario tera a opcao de escolher se deseja fazer um pedido
    while True:
        resp = input("Deseja fazer um pedido [s/n]? ")

        #Se o usuario digita 's' ou 'S' entao ele digita uma quantidade de produtos para fazer
        if resp.lower() == 's':
            resp = input("Quantas cadeiras voce deseja que sejam produzidas? ")
            cli.pedido(resp)

        # Se o usuario digita 'n' ou 'N' entao ele sai da aplicacao e a conexao e fechada
        # Caso o primeiro comando seja 'n' ou 'N', nao houve criacao do socket, logo deve-se tratar
        # e sair sem tentar fechar socket
        elif resp.lower() == 'n':
            try:
                cli.s.close()
            except Exception:
                pass
            break

if __name__ == '__main__':
    main()