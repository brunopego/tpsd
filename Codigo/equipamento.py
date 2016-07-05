import socket
from random import randrange

class Equipamento:

    # Crição das variáveis referentes ao socket ao endereço ip / porta do controlador
    controlador = None
    endr = None

    hostSensorFinal = '127.0.0.1'
    portaSensorFinal = '6002'

    # Método que define o endereço da linha de produção e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6001
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)


    # Método que "verifica" se a matéria prima está ou não com defeito (apenas gera um número aleatório)
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
        socketEquipamento.connect(self.hostEquipamento, self.portaEquipamento)
        socketEquipamento.send(msg)
        socketEquipamento.send(self.controlador)
        socketEquipamento.close()


# Método principal que cria um objeto do tipo linha de produção e que irá receber uma conexão do controlador
def main():
    equipamento = Equipamento()
    while True:
        equipamento.controlador, equipamento.endr = equipamento.s.accept()
        msg = equipamento.controlador.recv(128).decode('utf-8')
        controladorProducao = equipamento.controlador.recv(1024)
        equipamento.verificarMateriaPrima(msg)


if __name__ == '__main__':
    main()