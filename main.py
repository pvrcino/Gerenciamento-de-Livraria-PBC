import os;

#Variavel global para armazenar o saldo da loja
saldo = 0.0;
#Lista para armazenar os dicts Livros
EstoqueLivros = [];
#Lista para armazenas as tuplas das vendas realizadas.
HistoricoVendas = [];



def clear():
  ''' Funcao para limpar o terminal de execucao dependendo do S.O.'''
  os.system('cls' if os.name == 'nt' else 'clear')



def getLivroByISBN(isbn: int) -> dict:
  ''' Funcao que retorna um dict Livro recebendo um determinado ISBN referente a este.'''
  #Chamada da variavel global EstoqueLivros
  global EstoqueLivros;
  #Varre pelo EstoqueLivros procurando um ISBN igual ao ISBN procurado
  for i in EstoqueLivros:
    if (i['ISBN'] == isbn):
      return i
  return None



def getLivroByTitulo(titulo: str) -> dict:
  ''' Funcao que retorna um dict Livro recebendo um determinado Titulo referente a este.'''
  #Chamada da variavel global EstoqueLivros
  global EstoqueLivros;
  #Varre pelo EstoqueLivros procurando um titulo igual ao titulo procurado (sendo ambos comparados com lowerCase)
  for i in EstoqueLivros:
    if (i['Titulo'].lower() == titulo.lower()):
      return i
  return None



def cadastrarLivro(titulo: str, isbn: int, valor: float, estoque: int) -> dict:
  ''' Funcao que armazena o dict Livro criado no vetor EstoqueLivros.
  @param titulo: Titulo do livro a ser cadastrado.
  @param isbn: ISBN do livro a ser cadastrado.
  @param valor: Valor do livro a ser cadastrado.
  @param estoque: Estoque do livro a ser cadastrado.'''
  #Chamada da variavel global EstoqueLivros
  global EstoqueLivros;

  #Procura um livro com o mesmo ISBN recebido como parâmetro
  Livro = getLivroByISBN(isbn);
  #Caso não seja encontrado, cria um novo dict Livro e adiciona a lista EstoqueLivros
  if (Livro == None):
    Livro = { 'Titulo':titulo, 
    'ISBN':isbn, 
    'Valor':valor, 
    'QuantidadeEstoque':estoque }
    EstoqueLivros.append(Livro)
  else:
    #Caso seja encontrado adiciona ao seu estoque a quantidade informada como parâmetro da funcao
    Livro['QuantidadeEstoque'] += estoque
  return Livro



def venderLivro(isbn: int, qtd: int):
  ''' Funcao que armazena a tupla Venda criado no vetor EstoqueLivros.

  @param isbn: ISBN do livro a ser vendido.
  @param qtd: Quantidade de livros a serem vendidos.'''
  #Chamada da variavel global saldo e HistoricoVendas
  global saldo
  global HistoricoVendas

  #Procura um livro com o mesmo ISBN recebido como parâmetro
  Livro = getLivroByISBN(isbn)
  if (Livro == None):
    #Caso não seja encontrado, retorna None
    return None
  elif (Livro['QuantidadeEstoque'] < qtd):
    #Caso a quantidade informada como parâmetro seja superior a quantidade em estoque, retorna que a operacao falhou
    return False
  else:
    #Caso contrário, remove da quantidade em estoque do livro, a quantidade informada como parâmetro da funcao
    Livro['QuantidadeEstoque'] -= qtd

    value = qtd * Livro['Valor']

    #Adiciona a tupla Venda ao HistoricoVendas.
    Venda = (Livro['Titulo'], qtd, value)
    HistoricoVendas.append(Venda)
    return value



def lerArquivos():
  ''' Funcao para realizar a abertura dos arquivos de database e armazenamento dentro dos vetores.'''

  #Verifica se existe a pasta DB, caso não exista, cria uma nova
  if (not(os.path.isdir("./db"))):
    os.mkdir('./db')

  #Chamada da variavel global saldo
  global saldo;


  #Abertura do arquivo estoque.txt e armazenamento dos livros no vetor EstoqueLivros
  try:
    arq_estoque = open("db/estoque.txt", "r")
  except FileNotFoundError:
    arq_estoque = open("db/estoque.txt", "w")
    
  contador = 0
  temp = []
  for linha in arq_estoque:
    contador+=1
    if (contador != 1):
      temp.append(linha.rstrip().replace("\t", ""))
      if contador == 5:
        cadastrarLivro(temp[0], int(temp[1]),float(temp[2]),int(temp[3]))
        temp = []
        contador = 0

  arq_estoque.close()
  #Fechamento do arquivo de estoque
  

  #Abertura do arquivo saldo.txt e armazenamento do saldo informado em uma variavel
  try:
    arq_saldo = open("db/saldo.txt", "r")
  except FileNotFoundError:
    arq_saldo = open("db/saldo.txt", "w")
    arq_saldo.write("0")

  saldo = float(arq_saldo.read())

  arq_saldo.close()
  #Fechamento do arquivo de saldo


  #Abertura do arquivo de historico de vendas e armazenamento das vendas no vetor EstoqueLivros
  try:
    arq_historico = open("db/historico.txt", "r")
  except FileNotFoundError:
    arq_historico = open("db/historico.txt", "w")

  contador = 0
  temp = []
  for linha in arq_historico:
    contador+=1
    if (contador != 1):
      temp.append(linha.rstrip().replace("\t", ""))
      if contador == 4:
        livro = getLivroByTitulo(temp[0])
        venderLivro(livro['ISBN'], int(temp[1]))
        temp = []
        contador = 0
  
  arq_historico.close()
  #Fechamento do arquivo de historico



def salvarDados():
  ''' Funcao para a atualização dos arquivos de database com os dados preenchidos nos vetores.'''
  #Chamada da variavel global saldo, EstoqueLivros, HistoricoVendas
  global saldo;
  global EstoqueLivros
  global HistoricoVendas

  #Abertura do arquivo estoque.txt e armazenamento dentro deste de todos os livros presentes no vetor EstoqueLivros
  arq_estoque = open("db/estoque.txt", "w")
  contador = 1
  for livro in EstoqueLivros:
    arq_estoque.write("Livro "+format(contador)+":\n")
    arq_estoque.write("\t"+livro['Titulo']+"\n")
    arq_estoque.write("\t"+format(livro['ISBN'])+"\n")
    arq_estoque.write("\t"+"{:.2f}".format(livro['Valor'])+"\n")
    arq_estoque.write("\t"+format(livro['QuantidadeEstoque'])+"\n")
    contador+=1

  arq_estoque.close()
  #Fechamento do arquivo estoque.txt

  #Abertura do arquivo saldo.txt e armazenamento dentro deste do saldo informado pela variavel saldo.
  arq_saldo = open("db/saldo.txt", "w")
  arq_saldo.write("{:.2f}".format(saldo))
  arq_saldo.close()
  #Fechamento do arquivos saldo.txt

  #Abertura do arquivo historico.txt e armazenamento dentro deste de todas as vendas presentes no vetor HistoricoVendas
  arq_historico = open("db/historico.txt", "w")
  contador = 1
  for venda in HistoricoVendas:
    arq_historico.write("Venda "+format(contador)+":\n")
    arq_historico.write("\t"+venda[0]+"\n")
    arq_historico.write("\t"+format(venda[1])+"\n")
    arq_historico.write("\t"+"{:.2f}".format(venda[2])+"\n")
    contador+=1
  arq_historico.close()
  #Fechamento do arquivos historico.txt

  print("Os dados foram salvos no banco de dados!\n")
  #Volta ao menu principal
  menu(0)



def usuario_cadastraLivro():
  ''' Funcao para que usuario insira os dados do livro para fazer o cadastro.'''

  #Pede para o usuario inserir o ISBN e procura se existe um livro com o mesmo.
  print("##Cadastra Livro##")
  isbn = int(input("Digite o ISBN do livro: "))

  Livro = getLivroByISBN(isbn);
  #Verifica se o livro é encontrado
  if (Livro != None):
    #Caso sim, pede para digitar a quantidade a ser adicionada.
    print("\nLivro com esse ISBN já cadastrado! \nTitulo: "+Livro['Titulo']+ "\n")
    qtd = int(input("Digite a quantidade a ser adicionada ao estoque: "))
    cadastrarLivro(Livro['Titulo'], isbn, Livro['Valor'], qtd)
  else:
    #Caso não, pede para usuario inserir os dados do livro e chama a funcao de cadastro.
    titulo = input("Digite o Titulo do livro: ")
    valor = float(input("Digite o Valor unitário: "))
    qtd = int(input("Digite a quantidade em estoque: "))
    cadastrarLivro(titulo, isbn, valor, qtd)

  #Limpa a tela e retorna mensagem de sucesso!
  clear()
  print("\nLivro cadastrado com sucesso!\n")
  menu(0)



def usuario_vendeLivro():
  ''' Funcao para que usuario insira os dados da venda para ser registrada.'''
  #Chamada da variavel global saldo
  global saldo

  #Pede para o usuario inserir o ISBN do livro e a quantidade a ser vendida
  print("##Venda de Livro##")
  isbn = int(input("Digite o ISBN do livro: "))
  qtd = int(input("Digite a quantidade a ser vendida: "))

  Venda = venderLivro(isbn, qtd)
  if (Venda == None):
    #Caso a venda retorne None, printa ao usuario que o livro não foi encontrado.
    clear()
    print("Livro não encontrado!\n")
  elif (not Venda):
    #Caso a venda não seja realizada, printa ao usuario que a quantidade de livros em estoque é insuficiente
    clear()
    print("Quantidade em estoque insuficiente!\n")
  else:
    #Caso a venda seja realizada, adiciona o valor da venda ao saldo da loja e printa ao usurario.
    clear()
    saldo+=Venda
    print("Venda realizada! Valor total: R$ " + "{:.2f}".format(Venda)+ "\n")
  #Retorona ao menu principal.
  menu(0)



def consultaEstoqueTitulo():
  ''' Funcao para retornar o usuario um livro dependendo de seu titulo informado.'''

  #Limpa o terminal e pede para usuario inserir o titulo do livro e busca no vetor EstoqueLivros.
  clear()
  Livro = getLivroByTitulo(input("Insira o nome do livro: "))
  clear()

  if (Livro != None):
    #Caso o livro não retorne None, printa os dados do livro
    print("Titulo: "+Livro['Titulo'])
    print("ISBN: "+format(Livro['ISBN']))
    print("Valor: "+"{:.2f}".format(Livro['Valor']))
    print("Quantidade em estoque: "+format(Livro['QuantidadeEstoque'])+"\n")
  else:
    #Caso contrario, printa ao usuario que o livro não foi encontrado.
    print("Livro não encontrado!\n")
  #Volta ao menu principal
  menu(0)



def consultaEstoqueISBN():
  ''' Funcao para retornar o usuario um livro dependendo de seu ISBN informado.'''
  #Limpa o terminal e pede para usuario inserir o ISBN do livro e busca no vetor EstoqueLivros.
  clear()
  Livro = getLivroByISBN(int(input("Insira o ISBN do livro: ")))
  clear()

  if (Livro != None):
    #Caso o livro não retorne None, printa os dados do livro
    print("Titulo: "+Livro['Titulo'])
    print("ISBN: "+format(Livro['ISBN']))
    print("Valor: "+"{:.2f}".format(Livro['Valor']))
    print("Quantidade em estoque: "+format(Livro['QuantidadeEstoque'])+"\n")
  else:
    #Caso contrario, printa ao usuario que o livro não foi encontrado.
    print("Livro não encontrado!\n")
  #Volta ao menu principal
  menu(0)



def consultaSaldo():
  ''' Funcao para printar ao usuario o saldo da loja.'''
  print("O saldo da loja é: R$ "+"{:.2f}".format(saldo)+"\n")
  menu(0)

def imprimeHistorico():
  ''' Funcao para imprimir o historico de vendas da loja.'''
  #Chamada da variavel global HistoricoVendas
  global HistoricoVendas
  #Pede para o usuario inserir a quantidade das ultimas vendas a serem printadas
  qtd = int(input("Insira a quantidade de vendas a serem mostradas: "))
  #Limpa o terminal
  clear()
  #Procura dentro do vetor HistoricoVendas a quantidade de vendas informadas e printa no terminal
  for i in range (qtd):
    print("Venda "+format(len(HistoricoVendas)-i)+ ":")
    print("\tTitulo: "+HistoricoVendas[-i][0])
    print("\tQuantidade: "+format(HistoricoVendas[-i][1]))
    print("\tValor total: "+"{:.2f}\n".format(HistoricoVendas[-i][2]))
  #Retorna ao menu principal
  menu(0)



def menu(escolha: int):
  ''' Funcao responsavel por mostrar o menu de opcoes para o usuario
    :param escolha: Escolha do usuario do menu.'''

  #Caso a escolha seja 0, mostra todas as opcoes do menu e pede para o usuario escolher uma.
  if (escolha == 0):
    opcoes = int(input("1. Cadastrar Livro\n2. Consulta Estoque (Busca por Título)\n3. Consulta Estoque (Busca por ISBN)\n4. Vender um Livro\n5. Consultar Saldo da loja\n6. Mostrar histórico de vendas\n7. Salvar Dados\n9. Sair\n"))
    menu(opcoes)
  #Caso a escolha seja 1, pede ao usuario cadastrar o livro.
  elif (escolha == 1):
    clear()
    usuario_cadastraLivro()
  #Caso a escolha seja 2, pede ao usuario um titulo do livro e printa suas informacoes.
  elif (escolha == 2):
    clear()
    consultaEstoqueTitulo()
  #Caso a escolha seja 3, pede ao usuario um ISBN do livro e printa suas informacoes.
  elif (escolha == 3):
    clear()
    consultaEstoqueISBN()
  #Caso a escolha seja 4, pede ao usuario um ISBN de um livro e realiza a venda deste.
  elif (escolha == 4):
    clear()
    usuario_vendeLivro()
  #Caso a escolha seja 5, printa ao usuario o saldo da loja.
  elif (escolha == 5):
    clear()
    consultaSaldo()
  #Caso a escolha seja 6, pede ao usuario quantas vendas ele deseja que sejam mostradas e as printa no terminal.
  elif (escolha == 6):
    clear()
    imprimeHistorico()
  #Caso a escolha seja 7, salva todos os dados inseridos na execucao do programa nos arquivos da pasta DB.
  elif (escolha == 7):
    clear()
    salvarDados()
  #Caso a escolha seja 9, finaliza a livraria.
  elif (escolha == 9):
    clear()
    print("Livraria finalizada!")
  #Caso a escolha seja qualquer outra, limpa o terminal e retorna ao menu principal.
  else:
    clear()
    menu(0)


#Execucao do programa ->
#Limpa o terminal
clear()
#Faz a leitura de todos arquivos de DB
lerArquivos()
#Printa o menu inicial
menu(0)
