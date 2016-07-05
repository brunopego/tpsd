import _thread as t
import socket
import time

# Esta variavel global define o tanto de materia prima em estoque
estoque = 50


# Esta e a classe onde se trata o pedido dos clientes, solicita materia prima do fornecedor,
# envia materia prima para producao do produto final e retorna ao cliente o produto pronto
class controladorProducao:

    # O bloco abaixo contem o socket de comunicacao com o cliente e a tupla com IP e porta
    # e outras variaveis sobre fornecedor e linha de producao
    cliente = None
    endr = None
    porta_fornecedor = 4001
    porta_linhaProducao = 4002
    capacidade_linhaProducao = 30


    # Construtor onde se define por quais enderecos IPs ira se conectar a linha de producao e ao fornecedor
    def __init__(self):
        self.hostLinhaProducao = '127.0.0.1'
        self.hostFornecedor = '127.0.0.1'
        self.host = '127.0.0.1'
        self.port = 4000

        #Cria-se entao um socket para receber conexoes
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(1)


    # Abaixo o metodo de tratar pedido recebido pelo cliente e direcionar se precisa de mais materia prima
    # se precisa de reenviar para linha de producao materia prima para producao de outro produto (substituir defeituoso)
    def tratarPedido(self, cliente, endr):
        global estoque
        print("Tem " + str(estoque) + " unidades de MP em estoque.")

        # Abaixo Fica à espera de uma mensagem do cliente, se a msg nao conter nada entao fecha a conexao
        msg = cliente.recv(128).decode('utf-8')
        if not msg:
            cliente.close()
        print("Cliente: " + str(endr), "-> Producao solicitada: " + msg + " Cadeiras.")


        # Abaixo e feita a converao da msg recebida em um numero INT
        qtd_solicitada = int(msg)

        # Se o tanto de materia prima para fazer um produto for menor que a quantidade solicitada pelo cliente
        # entao e chamada a funcao de solicitar mais materias primas ao fornecedor, logo apos e feita a subtracao
        # no estoque a quantidade referente a solicitacao do cliente
        if(estoque < qtd_solicitada):
            print(str(estoque) + " unidades de MP em estoque...")
            print("Solicitando materia prima...")
            self.solicitarMateriaPrima(str(qtd_solicitada - estoque))
            print("Materia prima recebida...")
        estoque -= qtd_solicitada

        # A linha de producao tem uma capacidade que e definida pela variavel "capacidade_linhaProducao"
        # que e solicitado a cada iteracao do laco e caso necessario e feito no final uma solicitacao do restante
        # Abaixo tambem e medido o tempo gasto pela linha de producao para fazer os produtos
        tempo_inicial = time.time()
        while qtd_solicitada != qtd_solicitada % self.capacidade_linhaProducao:
            print("Em producao: " + str(self.capacidade_linhaProducao))
            self.enviarParaProducao(str(self.capacidade_linhaProducao))
            qtd_solicitada -= self.capacidade_linhaProducao

        if(qtd_solicitada > 0):
            print("Em producao: " + str(qtd_solicitada))
            self.enviarParaProducao(qtd_solicitada)
        print("O tempo de producao foi: %s segundos" %(time.time() - tempo_inicial))

        # Como todos produtos ja estao prontos agora e so chamar o metodo de enviar a resposta para o cliente
        print("Todos os produtos solicitados estao prontos!")
        print("Estoque atual: " + str(estoque) + " unidades de MP em estoque.")
        self.enviarPedidoParaCliente(cliente)

        # Agora a conexao pode ser fechada
        cliente.close()


    # Metodo de solicitar materia prima ao fornecedor
    def solicitarMateriaPrima(self, qtd):

        qtd = str(qtd)

        # Usa-se a variavel de estoque global que recebera a materia prima do fornecedor
        global estoque
        sm = socket.socket()
        sm.connect((self.hostFornecedor, self.porta_fornecedor))
        sm.send(qtd.encode('utf-8'))
        materia_prima_recebida = sm.recv(128).decode('utf-8')
        estoque += int(materia_prima_recebida)
        sm.close()
        return 0


    # Metodo que envia para a linha de producao a materia prima (nesse caso quantidade de materia prima)
    def enviarParaProducao(self, qtd):

        qtd = str(qtd)
        # Usa-se a variavel referente ao estoque para controle ao retirar materias primas dele
        global estoque

        # e criado entao um socket para tais transacoes
        lp = socket.socket()
        lp.connect((self.hostLinhaProducao, self.porta_linhaProducao))
        lp.send(qtd.encode('utf-8'))

        # A resposta e a quantidade de materiais com defeito que deverao ser reenviados para a Linha de Producao
        resposta = lp.recv(128).decode('utf-8')

        # Enquanto a resposta e diferente de zero significa que ha necessidade de pegar materia prima no
        # estoque e enviar a linha de producao para repor os produtos defeituosos. Caso contrario significa
        # que nao houve perda de produtos ou defeitos na linha de producao, entao fecha a conexao
        while resposta != '0':

            if(estoque < int(resposta)):
                print("Houve um erro na producao...")
                print("Estoque insuficiente - Solicitando materiais...")
                self.solicitarMateriaPrima(resposta)
                lp.send(resposta.encode('utf-8'))
                estoque -= int(resposta)
            else:
                print("Houve um erro na producao...")
                lp.send(resposta.encode('utf-8'))
                estoque -= int(resposta)

            resposta = lp.recv(128).decode('utf-8')

        print("Producao concluida!")
        lp.close()


    # Metodo para enviar para o cliente o produto final
    def enviarPedidoParaCliente(self, cliente):
        cliente.send("Produtos Prontos!".encode('utf-8'))
        return 0

#Metodo principal que criara um controlador para manipular conexoes e transacoe de informacao entre os sistemas distribuidos
def main():
    cp = controladorProducao()

    while True:

            cp.cliente, cp.endr = cp.s.accept()
            print("Conectado de: " + str(cp.endr))
            t.start_new_thread(cp.tratarPedido, tuple([cp.cliente, cp.endr]))


if __name__ == '__main__':
    main()