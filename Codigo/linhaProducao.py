import socket

class LinhaProducao:

    # Cricao das variaveis referentes ao sockete ao endereco ip / porta do controlador
    controlador = None
    endr = None

    hostSensorInicial = '127.0.0.1'
    portaSensorInicial = 4004

    # Metodo que define o endereco da linha de producao e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 4002
        self.portaRespostaSensorFinal = 4003
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(1)

        self.socketRecebeSensorFinal = socket.socket()
        self.socketRecebeSensorFinal.bind((self.host, self.portaRespostaSensorFinal))
        self.socketRecebeSensorFinal.listen(1)

    # Metodo que fara o produto (recebe a quantidade de produto que deve ser feito)
    def produz(self, qtd):

        socketSensorInicial = socket.socket()
        socketSensorInicial.connect((self.hostSensorInicial, self.portaSensorInicial))
        socketSensorInicial.send(str(qtd).encode('utf-8'))
        socketSensorInicial.close()



        socketSensorFinal, sensorFinalEndr = self.socketRecebeSensorFinal.accept()
        msg = socketSensorFinal.recv(128).decode('utf-8')
        print("Recebeu do final -> "+msg)
        #socketRecebeSensorFinal.close()

        produtosComDefeitos = int(qtd) - int(msg)

        # Finalmente retorna o resultado de produtos com defeito e a quantidade produzida independente do defeito
        self.retornaResultado(produtosComDefeitos, int(qtd))


    # Metodo para retornar o resultado para o controlador de producao
    def retornaResultado(self, produtosComDefeitos: int, qtd: int):
        if produtosComDefeitos == 0:
            print("Produtos prontos para serem entregues! ")
            print("Quantidade de produto com defeito: ", produtosComDefeitos)
            self.controlador.send(str(produtosComDefeitos).encode('utf-8'))

        else:
            print("Alguns produtos foram descartados por serem defeituosos!")
            qtdProdutos = qtd - produtosComDefeitos
            print("Quantidade de produtos produzido: ", qtdProdutos + produtosComDefeitos)
            print("Quantidade de produtos com defeito: ", produtosComDefeitos)
            print("Solicitando materiais para cobrir os defeituosos ...")
            self.controlador.send(str(produtosComDefeitos).encode('utf-8'))
            resp = self.controlador.recv(128).decode('utf-8')
            self.produz(resp)

# Metodo principal que cria um objeto do tipo linha de producao e que ira receber uma conexao do controlador
def main():
    linhaProducao = LinhaProducao()
    while True:
        linhaProducao.controlador, linhaProducao.endr = linhaProducao.s.accept()
        msg = linhaProducao.controlador.recv(128).decode('utf-8')
        msg = int(msg)
        linhaProducao.produz(msg)


if __name__ == '__main__':
    main()