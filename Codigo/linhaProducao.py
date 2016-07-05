import socket
from random import randrange

class LinhaProducao:

    # Cricao das variaveis referentes ao sockete ao endereco ip / porta do controlador
    controlador = None
    endr = None

    # Metodo que define o endereco da linha de producao e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5002
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)

    # Metodo que fara o produto (recebe a quantidade de produto que deve ser feito)
    def produz(self, qtd):
        nqtd = int(qtd)

        # Inicialmente define uma variavel i como contador para o laco e outra
        # que vai contar o numero de produtos defeituosos
        # o laco trata em cada if se o produto esta defeituoso e caso sim adiciona +1 em produtosComDefeitos
        # Faz um produto de cada vez
        i = 0
        produtosComDefeitos = 0
        while i < nqtd:
            if self.sensorInicial() == True:
                if self.equipamentoDeProducao() == True:
                    if self.sensorFinal() == True:
                        print("Produto produzido: ", i+1)
                    else:
                        produtosComDefeitos += 1
                else:
                    produtosComDefeitos += 1
            else:
                produtosComDefeitos += 1

            i += 1
        # Finalmente retorna o resultado de produtos com defeito e a quantidade produzida independente do defeito
        self.retornaResultado(produtosComDefeitos, nqtd)

    # Metodo que "verifica" se a materia prima esta ou nao com defeito (apenas gera um numero aleatorio)
    def sensorInicial(self):
        defeito = randrange(0, 10)
        if defeito == 1:
            return False
        return True

    # Metodo que "verifica" o produto durante o processo de producao (apenas gera um numero aleatorio)
    def equipamentoDeProducao(self):
        defeito = randrange(0, 10)
        if defeito == 2:
            return False
        return True

    # Metodo que "verifica" o produto final (apenas gera um numero aleatorio)
    def sensorFinal(self):
        defeito = randrange(0, 10)
        if defeito == 2:
            return False
        return True

    # Metodo para retornar o resultado para o controlador de producao
    def retornaResultado(self, produtosComDefeitos: int, qtd: int):
        if produtosComDefeitos == 0:
            print("Produtos prontos para serem entregues! ")
            print("Quantidade de produto com defeito: ", produtosComDefeitos)
            self.controlador.send(str(produtosComDefeitos).encode('utf-8'))
            #self.controlador.close()

        else:
            print("Alguns produtos foram descartados por serem defeituosos!")
            qtdProdutos = qtd - produtosComDefeitos
            print("Quantidade de produtos produzido: ", qtdProdutos + produtosComDefeitos)
            print("Quantidade de produtos com defeito: ", produtosComDefeitos)
            print("Solicitando materiais para cobrir os defeituosos ...")
            self.controlador.send(str(produtosComDefeitos).encode('utf-8'))
            resp = self.controlador.recv(128).decode('utf-8')
            self.produz(resp)

# Mètodo principal que cria um objeto do tipo linha de producao e que ira receber uma conexao do controlador
def main():
    linhaProducao = LinhaProducao()
    while True:
        linhaProducao.controlador, linhaProducao.endr = linhaProducao.s.accept()
        msg = linhaProducao.controlador.recv(128).decode('utf-8')
        linhaProducao.produz(msg)


if __name__ == '__main__':
    main()