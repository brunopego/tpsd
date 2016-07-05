import socket
from random import randrange

class Equipamento:

    # Cricao das variaveis referentes ao socket ao endereco ip / porta do controlador
    controlador = None
    endr = None

    hostSensorFinal = '127.0.0.1'
    portaSensorFinal = 4006

    # Metodo que define o endereco da linha de producao e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 4005
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)


    # Metodo que "verifica" se a materia prima esta ou nao com defeito (apenas gera um numero aleatorio)
    def verificarMateriaPrima(self, qtd):
        print("Entrou equipamento")
        produtosComDefeito = 0
        i = 0

        while(i < qtd):
            defeito = randrange(0, 10)
            if defeito == 1:
                produtosComDefeito += 1
            i += 1

        msg = str(qtd-produtosComDefeito)
        socketEquipamento = socket.socket()
        socketEquipamento.connect((self.hostSensorFinal, self.portaSensorFinal))
        socketEquipamento.send(msg.encode('utf-8'))
        socketEquipamento.close()


# Metodo principal que cria um objeto do tipo linha de producao e que ira receber uma conexao do controlador
def main():
    equipamento = Equipamento()
    while True:
        equipamento.controlador, equipamento.endr = equipamento.s.accept()
        msg = equipamento.controlador.recv(128).decode('utf-8')
        msg = int(msg)
        equipamento.verificarMateriaPrima(msg)


if __name__ == '__main__':
    main()