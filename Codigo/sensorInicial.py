import socket
from random import randrange

class SensorInicial:

    # Cricao das variaveis referentes ao socket ao endereco ip / porta do controlador
    controlador = None
    endr = None

    hostEquipamento = '127.0.0.1'
    portaEquipamento = '6001'

    # Metodo que define o endereco da linha de producao e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6000
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
        socketEquipamento = socket.socket()
        socketEquipamento.connect((self.hostEquipamento, self.portaEquipamento))
        socketEquipamento.send(msg.encode('utf-8'))
        socketEquipamento.close()


# Metodo principal que cria um objeto do tipo linha de producao e que ira receber uma conexao do controlador
def main():
    sensorInicial = SensorInicial()
    while True:
        sensorInicial.controlador, sensorInicial.endr = sensorInicial.s.accept()
        msg = sensorInicial.controlador.recv(128).decode('utf-8')
        msg = int(msg)
        sensorInicial.verificarMateriaPrima(msg)


if __name__ == '__main__':
    main()