import socket
from random import randrange

class LinhaProducao:

    # Crição das variáveis referentes ao sockete ao endereço ip / porta do controlador
    controlador = None
    endr = None

    # Método que define o endereço da linha de produção e sua porta
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5002
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)

    # Método que fará o produto (recebe a quantidade de produto que deve ser feito)
    def produz(self, qtd):
        nqtd = int(qtd)

        # Inicialmente define uma váriavel i como contador para o laço e outra
        # que vai contar o número de produtos defeituosos
        # o laço trata em cada if se o produto está defeituoso e caso sim adiciona +1 em produtosComDefeitos
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

    # Método que "verifica" se a matéria prima está ou não com defeito (apenas gera um número aleatório)
    def sensorInicial(self):
        defeito = randrange(0, 10)
        if defeito == 1:
            return False
        return True

    # Método que "verifica" o produto durante o processo de produção (apenas gera um número aleatório)
    def equipamentoDeProducao(self):
        defeito = randrange(0, 10)
        if defeito == 2:
            return False
        return True

    # Método que "verifica" o produto final (apenas gera um número aleatório)
    def sensorFinal(self):
        defeito = randrange(0, 10)
        if defeito == 2:
            return False
        return True

    # Metodo para retornar o resultado para o controlador de produção
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

# Mètodo principal que cria um objeto do tipo linha de produção e que irá receber uma conexão do controlador
def main():
    linhaProducao = LinhaProducao()
    while True:
        linhaProducao.controlador, linhaProducao.endr = linhaProducao.s.accept()
        msg = linhaProducao.controlador.recv(128).decode('utf-8')
        linhaProducao.produz(msg)


if __name__ == '__main__':
    main()