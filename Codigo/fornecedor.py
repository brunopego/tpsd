import socket
import _thread as t

class Fornecedor:

    cliente = None
    endr = None

    # Metodo que define o endereco IP / porta do fornecedor
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5001
        self.s = socket.socket()
        self.s.bind((self.host, self.port))

        self.s.listen(1)

    # Metodo que recebe a quantidade de materia prima deve ser enviada e as retornam
    def fornecerMateriaPrima(self, cliente, endr):
        msg = cliente.recv(128).decode('utf-8')
        qtd_solicitada = int(msg)
        print(msg + " unidades de MP solicitadas...")
        print("Enviando " + str(qtd_solicitada) + " unidades de MP.")
        cliente.send(str(qtd_solicitada).encode('utf-8'))
        cliente.close()

# Metodo principal que cria um objeto do tipo fornecedor e que ira receber uma conexao do controlador
def main():
    fornecedor = Fornecedor()

    while True:
        fornecedor.cliente, fornecedor.endr = fornecedor.s.accept()
        t.start_new_thread(fornecedor.fornecerMateriaPrima, tuple([fornecedor.cliente, fornecedor.endr]))


if __name__ == '__main__':
    main()