import _thread as t
import socket
import time

# Esta variável global define o tanto de matéria prima em estoque
estoque = 50


# Esta é a classe onde se trata o pedido dos clientes, solicita matéria prima do fornecedor,
# envia matéria prima para produção do produto final e retorna ao cliente o produto pronto
class controladorProducao:

    # O bloco abaixo contém o socket de comunicação com o cliente e a tupla com IP e porta
    # e outras variáveis sobre fornecedor e linha de produção
    cliente = None
    endr = None
    porta_fornecedor = 5001
    porta_linhaProducao = 5002
    capacidade_linhaProducao = 30


    # Construtor onde se define por quais endereços IPs irá se conectar a linha de produção e ao fornecedor
    def __init__(self):
        self.hostLinhaProducao = '127.0.0.1'
        self.hostFornecedor = '127.0.0.1'
        self.host = '127.0.0.1'
        self.port = 5005

        #Cria-se então um socket para receber conexões
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(1)


    # Abaixo o método de tratar pedido recebido pelo cliente e direcionar se precisa de mais matéria prima
    # se precisa de reenviar para linha de produção matéria prima para produção de outro produto (substituir defeituoso)
    def tratarPedido(self, cliente, endr):
        global estoque
        print("Tem " + str(estoque) + " unidades de MP em estoque.")

        # Abaixo Fica à espera de uma mensagem do cliente, se a msg não conter nada então fecha a conexão
        msg = cliente.recv(128).decode('utf-8')
        if not msg:
            cliente.close()
        print("Cliente: " + str(endr), "-> Produção solicitada: " + msg + " Cadeiras.")


        # Abaixo é feita a converão da msg recebida em um número INT
        qtd_solicitada = int(msg)

        # Se o tanto de matéria prima para fazer um produto for menor que a quantidade solicitada pelo cliente
        # então é chamada a função de solicitar mais matérias primas ao fornecedor, logo após é feita a subtração
        # no estoque a quantidade referente a solicitação do cliente
        if(estoque < qtd_solicitada):
            print(str(estoque) + " unidades de MP em estoque...")
            print("Solicitando matéria prima...")
            self.solicitarMateriaPrima(str(qtd_solicitada - estoque))
            print("Matéria prima recebida...")
        estoque -= qtd_solicitada

        # A linha de producao tem uma capacidade que é definida pela variável "capacidade_linhaProducao"
        # que é solicitado a cada iteração do laço e caso necessário é feito no final uma solicitação do restante
        # Abaixo também é medido o tempo gasto pela linha de produção para fazer os produtos
        tempo_inicial = time.time()
        while qtd_solicitada != qtd_solicitada % self.capacidade_linhaProducao:
            print("Em produção: " + str(self.capacidade_linhaProducao))
            self.enviarParaProducao(str(self.capacidade_linhaProducao))
            qtd_solicitada -= self.capacidade_linhaProducao

        if(qtd_solicitada > 0):
            print("Em produção: " + str(qtd_solicitada))
            self.enviarParaProducao(qtd_solicitada)
        print("O tempo de produção foi: %s segundos" %(time.time() - tempo_inicial))

        # Como todos produtos já estão prontos agora é só chamar o método de enviar a resposta para o cliente
        print("Todos os produtos solicitados estão prontos!")
        print("Estoque atual: " + str(estoque) + " unidades de MP em estoque.")
        self.enviarPedidoParaCliente(cliente)

        # Agora a conexão pode ser fechada
        cliente.close()


    # Método de solicitar matéria prima ao fornecedor
    def solicitarMateriaPrima(self, qtd):

        qtd = str(qtd)

        # Usa-se a variável de estoque global que receberá a matéria prima do fornecedor
        global estoque
        sm = socket.socket()
        sm.connect((self.hostFornecedor, self.porta_fornecedor))
        sm.send(qtd.encode('utf-8'))
        materia_prima_recebida = sm.recv(128).decode('utf-8')
        estoque += int(materia_prima_recebida)
        sm.close()
        return 0


    # Método que envia para a linha de produção a matéria prima (nesse caso quantidade de matéria prima)
    def enviarParaProducao(self, qtd):

        qtd = str(qtd)
        # Usa-se a variável referente ao estoque para controle ao retirar materias primas dele
        global estoque

        # É criado então um socket para tais transações
        lp = socket.socket()
        lp.connect((self.hostLinhaProducao, self.porta_linhaProducao))
        lp.send(qtd.encode('utf-8'))

        # A resposta é a quantidade de materiais com defeito que deverão ser reenviados para a Linha de Produção
        resposta = lp.recv(128).decode('utf-8')

        # Enquanto a resposta é diferente de zero significa que há necessidade de pegar matéria prima no
        # estoque e enviar a linha de produção para repor os produtos defeituosos. Caso contrário significa
        # que não houve perda de produtos ou defeitos na linha de produção, então fecha a conexão
        while resposta != '0':

            if(estoque < int(resposta)):
                print("Houve um erro na produção...")
                print("Estoque insuficiente - Solicitando materiais...")
                self.solicitarMateriaPrima(resposta)
                lp.send(resposta.encode('utf-8'))
                estoque -= int(resposta)
            else:
                print("Houve um erro na produção...")
                lp.send(resposta.encode('utf-8'))
                estoque -= int(resposta)

            resposta = lp.recv(128).decode('utf-8')

        print("Produção concluída!")
        lp.close()


    # Método para enviar para o cliente o produto final
    def enviarPedidoParaCliente(self, cliente):
        cliente.send("Produtos Prontos!".encode('utf-8'))
        return 0


#Método principal que criará um controlador para manipular conexões e transaçõe de informação entre os sistemas distribuidos
def main():
    cp = controladorProducao()

    while True:

            cp.cliente, cp.endr = cp.s.accept()
            print("Conectado de: " + str(cp.endr))
            t.start_new_thread(cp.tratarPedido, tuple([cp.cliente, cp.endr]))


if __name__ == '__main__':
    main()