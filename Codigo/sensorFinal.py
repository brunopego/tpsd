import socket
from random import randrange

class SensorFinal:

    # Cricao das variaveis referentes ao socket ao endereco ip / porta do controlador
    controlador = None
    endr = None

    hostLinhaProducao = '127.0.0.1'
    portaRespostaLinhaProducao = '7000'

    # Metodo que define o endereco da linha de producao e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6002
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)


    # Metodo que "verifica" se a materia prima esta ou nao com defeito (apenas gera um numero aleatorio)
    def verificarMateriaPrima(self, qtd):

        produtosComDefeito = 0
        i = 0

        while(i < qtd):
            defeito = randrange(0, 10)
            if defeito == 1:
                produtosComDefeito += 1
        i += 1

        msg = str(qtd-produtosComDefeito)
        socketLinhaProducao = socket.socket()
        socketLinhaProducao.connect((self.hostLinhaProducao, self.portaRespostaLinhaProducao))
        socketLinhaProducao.send(msg.encode('utf-8'))
        socketLinhaProducao.close()


# Metodo principal que cria um objeto do tipo linha de producao e que ira receber uma conexao do controlador
def main():
    sensorFinal = SensorFinal()
    while True:
        sensorFinal.controlador, sensorFinal.endr = sensorFinal.s.accept()
        msg = sensorFinal.controlador.recv(128).decode('utf-8')
        msg = int(msg)
        sensorFinal.verificarMateriaPrima(msg)


if __name__ == '__main__':
    main()