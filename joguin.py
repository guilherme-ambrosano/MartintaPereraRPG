from random import randint, choice
from collections import OrderedDict
import itertools

greetings = ["ola", "oi", "oie", "oiee", "oieee", "eae", "iaee", "falae", "iae", "iai", "opa", "eaee"]
ofensas = ["vsf", "vai toma no cu", "me chupa", "vai toma no meio do seu cu sua piranha do caralho", "vtnc", "vai se fude"]

inventario = ["lanterna"]

em_combate = 0

vida_player = 5
ataque_player = 1

jogo = 0

pontos = 0

interacoes = {
        "andar" : "Posso me locomover até algum lugar que posso ver.\nUso: andar local",
        "olhar": "Posso olhar um objeto especifico ou meus arredores.\nUso: olhar [objeto]",
        "atacar": "Posso atacar alguma coisa.\nUso: atacar algo",
        "status": "Posso ver minha vida, meus pontos de ataque e meu inventário",
        "voltar": "Posso voltar de onde eu vim",
        "abrir": "Posso abrir alguma coisa.\nUso: abrir algo",
        "dizer": "Posso dizer alguma coisa.\nUso: dizer algo",
        "acender": "Posso acender minha lanterna",
        "sair": "Para sair do jogo",
        "ajuda": "Para obter ajuda sobre os comandos do jogo\nUso: ajuda [comando]"
        }


def get_input():
    global vida_player
    comando = input("\n: ")
    comando = comando.split()
#  try:
    ordem = comando[0]
    if ordem in verbos:
      verbo = verbos[ordem]
      if em_combate == 1 and (verbo == voltar or verbo == andar or verbo == abrir):
        print("Tento sair do combate, mas levo um golpe e sofro 1 de dano")
        vida_player -= 1
        return None
    else:
      print('Comando "{}" desconhecido'.format(" ".join(comando)))
      return None
    if len(comando) >= 2:
      substantivo = "_".join(comando[1:])
      verbo(substantivo)
    else:
      verbo("nada")
#  except:
#    print('Comando desconhecido')

def comecar_fase(fase, condicoes_extra = None):
    global vida_player, jogo, pontos
    while jogo == fase:
      if vida_player == 1 and randint(0, 3) == 0:
        print("Estou com muita dor")
      elif vida_player == 1 and randint(0, 3) == 0:
        print("Preciso me recuperar...")
      if vida_player <= 0:
        print("Minha visão escurece e eu caio no chão, desacordado")
        jogo = 666
        break
      if condicoes_extra is not None:
        try:
          condicoes_extra()
        except Acabou:
          break
      get_input()

def fim_do_jogo():
    global pontos
    global jogo
    global vida_player
    global ataque_player

    if jogo == 666:
      pontos += vida_player - 5
      pontos += ataque_player - 1
      print("Fim do jogo\nPontuação: {}".format(pontos))
      jogo = 616


def dizer(substantivo):
  global zumbi_atento
  global ofereceu_chave
  global vida_player

  substantivo = substantivo.replace("_", " ")

  if substantivo == "nada":
    print("Preciso de algo para dizer")
    return None

  print('Eu disse "{}"'.format(substantivo))

  acentos = {
          "á": "a",
          "à": "a",
          "ã": "a",
          "é": "e",
          "í": "i",
          "ó": "o",
          "õ": "o",
          "ú": "u"
          }
  
  for acento, normal in acentos.items():
      substantivo = substantivo.replace(acento, normal)

  pontuacoes = [",", ".", ";", ":", "[", "]", "{", "}", "(", ")", "_", "-", "'", '"', "+", "="]

  for pontuacao in pontuacoes:
      substantivo = substantivo.replace(pontuacao, " ")

  substantivo = substantivo.lower()

   
  personagens_presentes = [x for x in eval(lugar) if x in personagens]
  
  for x in personagens_presentes:
    eval(x).conversar(substantivo)

def olhar(substantivo):
  global lugar
  if substantivo == "nada":
    if len(eval(lugar)) <= 1:
      print("Não vejo nada")
      return None
    print("Eu vejo:")
    for i in (range(len(eval(lugar)) - 1)):
      print("- {}".format(eval(lugar)[i].replace("_", " ")))
  elif substantivo in eval(lugar):
    try:
      print(manual[substantivo])
    except:
      if substantivo in eval(lugar):
        print('Eu observo "{}" atentamente'.format(substantivo.replace("_", " ")))
      else:
        print('Não posso olhar para "{}"'.format(substantivo.replace("_", " ")))
  else:
      print('Não posso olhar para "{}"'.format(substantivo.replace("_", " ")))

def voltar(substantivo):
    global lugar
    if eval(lugar)[-1] == "fim":
      print("Não é possível voltar mais")
    else:
      print('Eu saio de "{}"'.format(lugar.replace("_", " ")))
      lugar = str(eval(lugar)[-1])
      triggers(lugar)

def respawn(local, coisa, vida = None):
    if isinstance(eval(coisa), objeto):
        eval(coisa).aberto = False
        return None
    elif isinstance(eval(coisa), personagem):
        local.insert(0, coisa)
        eval(coisa).morto = 0
        eval(coisa).vida = vida


def andar(substantivo):
  global condicoes_triggers, triggers
  global lugar
  global vida_player

  if substantivo == "nada":
    print("Preciso de um local para onde andar")
    return None

  if substantivo not in andavel:
    print('Não posso andar até "{}"'.format(substantivo.replace("_", " ")))
    return None

  if substantivo in eval(lugar):
    print('Eu ando até "{}"'.format(substantivo.replace("_", " ")))
    lugar = str(substantivo)
    triggers(substantivo)
  else:
    print('Não posso andar até "{}"'.format(substantivo.replace("_", " ")))

    
def sair(substantivo):
    global jogo
    jogo = 666

def ajuda(substantivo):
    if substantivo == "nada":
      print("Posso utilizar os seguintes comandos:")
      for i in range(len(list(verbos))):
        print("- {}".format(list(verbos)[i].replace("_", " ")))
    else:
      if substantivo not in list(interacoes):
        print('Comando "{}" desconhecido'.format(substantivo.replace("_", " ")))
      else:
        print(interacoes[substantivo])


def atacar(substantivo):
    global em_combate
    global ataque_player
    global vida_player
    global lugar
    global pontos

    if substantivo == "nada":
      print("Preciso de algo para atacar")
      return None

    if substantivo not in eval(lugar):
      print('Não posso atacar "{}"'.format(substantivo.replace("_", " ")))
      return None

    try:
      morto = eval(substantivo).atacar(ataque_player)
      if morto == 1:
        eval(lugar).remove(substantivo)
        pontos += 10
    except:
      print('Não posso atacar "{}"'.format(substantivo.replace("_", " ")))

def status(substantivo):
  global vida_player
  global ataque_player
  if em_combate == 1:
    print("Estou em combate")
  print("Minha vida é igual a {}".format(vida_player))
  print("Meu ataque é igual a {}".format(ataque_player))
  print("No meu inventário, eu tenho:")
  inventario_unico = list(set(inventario))
  for i in range(len(inventario_unico)):
    print("- {0} {1}".format(inventario.count(inventario_unico[i]), inventario_unico[i].replace("_", " ")))

def acender(substantivo):
    if substantivo != "nada":
       print('Não posso acender "{}"'.format(substantivo.replace("_", " ")))
       return None
    print("Tento acender minha lanterna, mas ela está sem pilhas")


class objeto:
  itens = {}
  extra = []
  precisa_de_chave = False
  aberto = False
  chave = "chave"

  def __init__(self, itens, prop, extra, precisa_de_chave, chave = "chave"):
    self.itens = itens
    self.prop = prop
    self.precisa_de_chave = precisa_de_chave
    self.extra = extra
    self.chave = chave

  def pegar_item(self):
    if self.itens is None:
        if self.extra is not None:
            for funcao in self.extra:
                funcao()
        self.aberto = True
        return None
    if self.aberto == True:
        if self.extra is not None:
            for funcao in self.extra:
                funcao()
        print("Está vazio...")
        return None 
    if self.prop is not None:
        vetor = []
        for i in range(len(self.prop)):
            for j in range(self.prop[i]):
                vetor.append(i)
        item = choice(vetor)
    else:
        item = randint(0, len(list(self.itens))-1)
    self.aberto = True
    if self.extra is not None:
        for funcao in self.extra:
            funcao()
    return self.itens[list(self.itens)[item]]
    

def abrir(substantivo):
  global inventario

  if substantivo not in objetos:
    print('Não é possível abrir "{}"'.format(substantivo.replace("_", " ")))
    return None

  if substantivo == "nada":
    print("Preciso de algo para abrir")
    return None

  if substantivo not in eval(lugar):
    print('Não vejo "{}" para abrir'.format(substantivo.replace("_", " ")))
    return None

  if eval(substantivo).chave not in inventario and eval(substantivo).precisa_de_chave == True and eval(substantivo).aberto == False:
    print('Eu preciso de "{}" para abrir'.format(eval(substantivo).chave))
    return None

  efeito = eval(substantivo).pegar_item()

  if eval(substantivo).precisa_de_chave == True and eval(substantivo).chave in inventario:
      inventario.remove(eval(substantivo).chave)
  
  if efeito is not None:
      efeito()

class personagem:
  nome= ""
  tem_loot = True
  ataque = 0
  vida = 0
  morto = 0
  extra = []
  morte = []
  dialogo = {}
  esquiva = 4
  esquiva_player = 3
  especial = 2
  prende_combate = True
  qual_loot = None
  chance_loot = 0
  frase_padrao = None
  
  def __init__(self, nome, ataque, vida, extra = None, dialogo = None, esquiva = 4, esquiva_player = 3,
          especial = 2, morte = None, tem_loot = True, qual_loot = None, chance_loot = 0,
          prende_combate = True, frase_padrao = None):
    self.morto = 0
    self.nome = nome
    self.ataque = ataque
    self.vida = vida
    self.extra = extra
    self.dialogo = dialogo
    self.especial = especial
    self.morte = morte
    self.esquiva = esquiva
    self.esquiva_player = esquiva_player
    self.tem_loot = tem_loot
    self.prende_combate = prende_combate
    self.qual_loot = qual_loot
    self.chance_loot = chance_loot
    self.frase_padrao = frase_padrao
  
  def get_desc(self):
    return self.nome + "\n" + self.desc
  
  def atacar(self, golpe):
      global em_combate
      global vida_player, ataque_player
      global inventario
      esquivou = randint(0, self.esquiva)

      if esquivou == 0: 
        print("{} esquivou do meu ataque".format(self.nome))
      else:
         self.vida = self.vida - golpe 
         if self.vida <= 0:
           self.morto = 1
         #print("Eu causei {0} de dano em {1}.\nA vida dele agora eh {2}".format(ataque_player, self.nome, self.vida))
         print("Eu causei {0} de dano em {1}.".format(ataque_player, self.nome))
      if randint(0,1) == 1 and self.prende_combate == True:
         em_combate = 1
      if self.morto == 0:
         player_esquivou = randint(0, self.esquiva_player)
         if player_esquivou == 0:
           print("Consigo me esquivar do ataque de {}".format(self.nome))
           return None
         if self.extra is not None:
            if randint(0, self.especial) == 0:
                qual = randint(0, len(self.extra) -1)
                self.extra[qual]()
                return None
         vida_player -= self.ataque 
         print("{0} causou {1} de dano em mim".format(self.nome, self.ataque))
      else:
         print("{} veio a falecer".format(self.nome))
         if self.morte is not None:
            for magia in range(len(self.morte)):
                self.morte[magia]()
         loot = randint(self.chance_loot, 1)
         if self.tem_loot == False:
             loot = 0
         if loot == 1:
             print("Eu procuro no corpo de {}...".format(self.nome))
             if self.qual_loot is None:
                print("Eu encontrei uma chave!")
                inventario.append("chave")
             elif self.qual_loot is not None:
                efeito = self.qual_loot.pegar_item()
                if efeito is not None:
                  efeito()
         em_combate = 0
      return self.morto

      
  def conversar(self, frase):
      if self.dialogo is None:
        return None

      chave = None
      combinacoes = []
      for i in range(1, len(frase.split()) + 1):
          for j in list(map(" ".join, itertools.combinations(frase.split(), i))):
              combinacoes.append(j)

      for palavra in combinacoes:
          if palavra in list(self.dialogo):
              chave = palavra

      chave_greetings = None
      for palavra in combinacoes:
          if palavra in greetings:
              chave_greetings = palavra

      chave_ofensas = None
      for palavra in combinacoes:
          if palavra in ofensas:
              chave_ofensas = palavra

      if chave is not None:
        if callable(self.dialogo[chave]):
            self.dialogo[chave]()
        else:
            print(self.dialogo[chave])
      elif chave_greetings is not None:
        if callable(self.dialogo["oi"]):
            self.dialogo["oi"]()
        else:
            print(self.dialogo["oi"])
      elif chave_ofensas is not None:
        if callable(self.dialogo["vsf"]):
            self.dialogo["vsf"]()
        else:
            print(self.dialogo["vsf"])
      elif self.frase_padrao is not None:
        print(self.frase_padrao)

verbos = OrderedDict([
     ("ajuda", ajuda),
     ("status", status),
     ("dizer", dizer),
     ("olhar", olhar),
     ("acender", acender),
     ("andar", andar),
     ("voltar", voltar),
     ("atacar", atacar),
     ("abrir", abrir),
     ("sair", sair)
     ])
 
def primeira_fase():
  try:
    global jogo
    global lugar
    global nome_player
    global rua, casa, predio, quarto, cozinha, hall, escada, quartinho
    global andavel
    global cadaver_aguardando, zumbi_atento, ofereceu_chave, em_combate
    global personagens, dialogo_matinta, cafe_pra_matinta, dialogo_cadaver, sanduba_pro_cadaver
    global dialogo_zumbi, oi_pro_zumbi, ajuda_pro_zumbi, sim_pro_zumbi, nao_pro_zumbi, deu_chave
    global matinta, zumbi, boss, cadaver, murcego
    global condicoes_triggers, triggers
    global objetos
    global porta, bau, cofre, geladeira
    global item_chave, item_nada, item_duas_chaves, item_power_up, item_vida, item_cafe
    global porta_boss, cadaver_no_aguardo
    global manual
    global pontos
    global itens_loot, loot


    condicoes_triggers = {
            "primeira_vez_predio": True,
            "primeira_vez_hall": True
            }

    manual = {
        "quartinho" : "Um quartinho escuro, preciso me abaixar para passar pela porta.\nO chão parece ter sido destruido, a queda parece ir além do primeiro andar do prédio...\nEu claramente não sobreviveria",
        "mesa" : "Uma mesa de madeira escura, emanando um cheiro nauseante de mofo",
        "cadeira" : "Uma cadeira antiga, mas parece estar em boas condições...",
        "cozinha" : "Uma cozinha",
        "geladeira": "Uma geladeira muito antiga e suja está no canto da cozinha. Deve estar vazia",
        "porta" : "Vejo uma porta no fundo da sala. Pode ser aberta com uma chave",
        "bau": "Pode ser aberto com uma chave",
        "cofre": "Sinto algo estranho neste hall... Parece estar vindo daquele cofre. Acho que tem algum tipo de magia aqui.\nO cofre pode ser aberto com uma chave",
        "escadas": "Em um canto escuro, vejo as escadas que dão para o andar de cima... Não parece ser seguro subir ali",
        "hall": "Um hall vazio com um cofre no centro... Me pergunto para que este lugar era utilizado",
        "cadaver": "Um cadáver começando a apodrecer. Não parece estar aqui há tanto tempo",
        "matinta": "Uma velha esquisita, sentada na sarjeta. Esta bebendo alguma coisa. Melhor nao incomodar",
        "zumbi": "Um cadáver em decomposição. Mas... Está se mexendo?",
        "casa": "Uma casa bem antiga... Parece abandonada há muito tempo",
        "predio": "Um prédio em ruínas, pode ser perigoso entrar ai",
        "sala": "Posso ver a sala de estar, mas uma viga desabou do teto. Não consigo entrar ali",
        "quarto": "Um quarto da casa",
        "boss": "Uma criatura enorme me impede de passar pela porta no fundo da sala"
        }

    lugar = "rua"

    rua = ["matinta", "casa", "predio", "fim"]
    casa = ["sala", "cozinha", "quarto", "rua"]
    predio = ["hall", "escada", "rua"] 
    quarto = ["zumbi", "escrivaninha", "cadeira", "cama", "bau", "casa"]
    cozinha = ["mesa", "cadeira", "cadeira", "geladeira", "cadaver", "casa"]
    hall = ["cofre", "predio"]
    escada = ["porta", "boss", "quartinho", "predio"]
    quartinho = ["predio"]
    
    andavel = ["rua", "casa", "predio", "quarto", "quartinho", "cozinha", "hall", "escada"]
    
    cadaver_aguardando = 0
    zumbi_atento = 0
    ofereceu_chave = 0
    deu_chave = 0

    def item_chave():
       global inventario
       inventario.append("chave")
       print("Eu encontrei uma chave!")

    def item_nada():
       global inventario
       print("Está vazio...")

    def item_duas_chaves():
        global inventario
        inventario.append("chave")
        inventario.append("chave")
        print("Eu encontrei duas chaves!")

    def item_power_up():
        global inventario
        global ataque_player
        ataque_player += randint(1, 2)
        print("Eu encontrei um power-up, meu ataque agora é {}".format(ataque_player))

    def item_vida():
        global inventario
        global vida_player
        if vida_player >= 5:
            vida_player += randint(1, 2)
        else:
            vida_player = 5
        print("Eu encontrei um bonus de vida, minha vida agora é {}".format(vida_player))

    def item_armadilha():
        global vida_player
        if randint(0, 1) == 0:
            print("Ao abrir o cofre, disparei uma armadilha, mas consegui me esquivar e saí ileso")
            return None
        print ("Ao abrir o cofre, disparei uma armadilha e fui atingido. Levei 1 de dano")
        vida_player -= 1
    
    itens_bau = OrderedDict([
            ("chave", item_chave),
            ("nada", item_nada),
            ("duas_chaves", item_duas_chaves),
            ("power-up", item_power_up),
            ("vida", item_vida)
            ])

    def cadaver_no_aguardo():
        global cadaver_aguardando
        global vida_player
        if cadaver_aguardando == 1:
          print("Não tem nenhum sanduba aqui.\nO cadáver provavelmente está louco de droga.\nAo perceber que não tem sanduba, o cadáver me ataca e eu sofro 1 de dano")
          vida_player -= 1
          cadaver_aguardando = 0

    itens_cofre = OrderedDict([
            ("armadilha", item_armadilha),
            ("chave", item_chave),
            ("nada", item_nada),
            ("duas_chaves", item_duas_chaves),
            ("power-up", item_power_up),
            ("vida", item_vida)
            ])


    def item_cafe():
        global inventario
        inventario.append("cafe")
        print("Encontrei café!")
    
    itens_geladeira = OrderedDict([
            ("duas chaves", item_duas_chaves),
            ("cafe", item_cafe)
            ])

    def porta_boss():
        global jogo
        if "boss" in escada:
            print("Eu preciso derrotar o boss antes de entrar aqui")
            return None
        jogo = 1
        return None
    
    bau = objeto(itens_bau, [1, 1, 1, 4, 3], None, True)
    geladeira = objeto(itens_geladeira, None, [cadaver_no_aguardo], False)
    cofre = objeto(itens_cofre, [2, 1, 1, 1, 4, 3], None, True)
    porta = objeto(None, None, [porta_boss], True)
     
    objetos = ["bau", "geladeira", "cofre", "porta"]

    itens_loot_murcego = OrderedDict([
        ("power-up", item_power_up),
        ("vida", item_vida)
        ])
    
    loot_murcego = objeto(itens_loot_murcego, None, None, False)
    
    itens_loot_boss = OrderedDict([
        ("chave", item_chave),
        ])

    loot_boss = objeto(itens_loot_boss, None, None, False)
    
    itens_loot = OrderedDict([
        ("chave", item_chave),
        ("duas_chaves", item_duas_chaves),
        ("power-up", item_power_up),
        ("vida", item_vida)
        ])

    loot = objeto(itens_loot, None, None, False)

    def triggers(local):
      global primeira_vez_predio, primeira_vez_hall
      global vida_player, ataque_player
      global em_combate
      global condicoes_triggers

      if randint(0, 5) == 0:
          em_combate = 1
          print('Surge um Murcego em {} e me ataca.\nEu consigo me esquivar, mas não posso fugir dele.'.format(local))
          respawn(eval(local), "murcego", vida = 1)
 
      if local == "quartinho":
        print('O chão do quartinho havia sido destruído.\nEu caio por mais de 15 metros, até bem abaixo do andar térreo.\nSinto os ossos das minhas pernas se quebrando e o sangue quente espirrando assim que atinjo o chão.')
        vida_player = 0

      elif local == "predio" and condicoes_triggers["primeira_vez_predio"] == True:
        print("Consigo escutar sons vindos da escadaria que dá para o andar de cima.\nO hall neste andar parece vazio, mas sinto algo me puxando na direcao dele...")
        condicoes_triggers["primeira_vez_predio"] = False

      elif local == "hall" and condicoes_triggers["primeira_vez_hall"] == True:
        print("Apesar de o hall estar vazio, consigo sentir uma presença.\nAlgo me diz que há algum tipo de magia naquele cofre")
        condicoes_triggers["primeira_vez_hall"] = False
 
      elif local == "hall" and cofre.aberto == True:
        print ("Ao entrar no hall, escuto o som de um objeto atingindo uma superfície metálica...\nO som parece ter vindo do interior do cofre")
        respawn(hall, "cofre")
        
      if inventario.count("chave") == 0 and "matinta" not in rua and "zumbi" not in quarto:
        boss.vida += randint(0,2)
        boss.ataque += randint(0,2)
        if local != "quarto" and local != "rua":
          respawn(quarto, "zumbi", vida = 3*ataque_player)
          zumbi.ataque = max(vida_player//3, 1)
          respawn(rua, "matinta", vida = 3*ataque_player)
          matinta.ataque = max(vida_player//3, 1)
        if "boss" not in escada and lugar != "escada":
          print("O Boss ressurgiu no prédio... Ele parece estar mais forte do que antes")
          respawn(escada, "boss", vida = 4*ataque_player)
   


    def cafe_pra_matinta():
       global inventario
       global vida_player
       if "cafe" in inventario:
           print('A Matinta Perera agradece o café. Em troca ela me oferece duas chaves')
           inventario.append("chave")
           inventario.append("chave")
           inventario.remove("cafe")
       elif "cafe" not in inventario:
           print("A Matinta Perera não recebe o seu café e fica irritada. Ela me ataca e eu sofro 1 de dano")
           vida_player -= 1

    dialogo_matinta = {
        "oi": 'A Matinta Perera responde "eae {} caralho vc tem café aí meu campeão?"\nDiga "me ajuda" para pedir ajuda'.format(nome_player),
        "vsf": 'A Matinta Perera parece se ofender. Ela diz: "mas vc é um arrombadão mesmo hein"',
        "sacipereredacumbedacumbe": 'A Matinta Perera responde "que porra é essa querido, vc tá retardado?"',
        "me ajuda": 'A Matinta Perera me olha desconfiada e diz: "só se tu me der o café o seu porra."\nSe voce tiver café, diga "toma aí o café" para oferecer café para a Matinta Perera.\nDigite "status" para olhar seu inventário.',
        "toma ai o cafe": cafe_pra_matinta
        }

    def sanduba_pro_cadaver():
        global cadaver_aguardando
        cadaver_aguardando = 1
        print('O cadáver claramente se move ao me escutar.\nParece estar esperando algo')

    dialogo_cadaver = {
        "oi": 'O cadáver parece se mover ao ouvir minha voz.\nUm som bem baixo parece ser emitido dele, semelhante uma voz rouca distante, dizendo:\n"aí, meu companheiro, vê se me dá um toro do sanduba que tá nessa geladera"\nDiga "calma aí que eu vou pegar o sanduba" para oferecer o sanduba ao cadáver',
        "vsf": 'Percebo o cadáver se mover. Acho que não gostou do que eu disse',
        "calma ai que eu vou pegar o sanduba": sanduba_pro_cadaver 
        }

    def oi_pro_zumbi():
        global zumbi_atento
        zumbi_atento = 1
        print('O zumbi reage ao som da minha voz.\nSua cabeca vira em minha direção, apesar de seus olhos já estarem em decomposição há muito tempo.\nDiga "me ajuda" para pedir ajuda ao Zumbi')

    def ajuda_pro_zumbi():
        global ofereceu_chave
        global zumbi_atento
        global deu_chave
        if zumbi_atento == 1:
            if deu_chave < 3:
              ofereceu_chave = 1
              zumbi_atento = 0
              print('O zumbi retira uma chave do bolso em sua camiseta, e me oferece\nDiga "sim" para aceitar a chave e "não" para recusar')
            else:
              print('O zumbi não tem mais nenhuma chave para me dar...')

    def nao_pro_zumbi():
        global ofereceu_chave
        if ofereceu_chave == 1:
          print('O zumbi guarda novamente a chave em seu bolso')
          ofereceu_chave = 0

    def sim_pro_zumbi():
        global ofereceu_chave
        global vida_player
        global inventario
        global deu_chave
        if ofereceu_chave == 1:
          print('Eu pego a chave')
          ofereceu_chave = 0
          deu_chave += 1
          if randint(0, 1) == 0:
            print('Inalar o hálito podre do zumbi me faz sentir um mal-estar imediatamente.\nLevei 1 de dano')
            vida_player -= 1
          if deu_chave < 3:
            print('Algo me diz que o zumbi tem mais chaves com ele')
          inventario.append("chave")

    dialogo_zumbi = {
        "oi": oi_pro_zumbi,
        "vsf": 'O zumbi parece se ofender com o que eu disse.\nEle me da 1 de dano', 
        "ao zumbiziao": 'O zumbi emite um grunhido. Ele parece ter entendido o que eu disse',
        "me ajuda": ajuda_pro_zumbi,
        "sim": sim_pro_zumbi,
        "nao": nao_pro_zumbi
        }

    personagens = ["matinta", "zumbi", "boss", "cadaver", "murcego"]

    matinta = personagem("Matinta Perera", 1, 5, None, dialogo_matinta, qual_loot = loot)
    cadaver = personagem("Cadaver", 1, 5, None, dialogo_cadaver, qual_loot = loot)
    zumbi = personagem("Zumbi", 1, 5, None, dialogo_zumbi, qual_loot = loot)
    murcego = personagem("Murcego", 1, 1, None, None, qual_loot = loot_murcego)
    
    def abalo_sismico():
        global vida_player
        print("O Boss ergue os braços e dá um pulo.\n Ao aterrissar, o choque do seu corpo com o chão faz com que toda a sala trema.\nEu levo 3 pontos de dano.")
        vida_player -= 3

    def heal():
        global ataque_player
        print("O Boss secreta uma gosma esverdeada debaixo de sua axila esquerda.\nEle pega um bocado da gosma com sua mão direita e esfrega sobre seus ferimentos.\nEle parece se recuperar imediatamente")
        boss.vida += ataque_player

    def fogo():
        global vida_player
        print("Sob um comando do Boss, labaredas consomem o chão onde eu estava.\nAs chamas somem com a mesma velocidade com que surgiram.\nEu levo 3 de dano.")
        vida_player -= 3

    boss = personagem("Boss", 2, 10, [abalo_sismico, heal, fogo], None, chance_loot = 1, esquiva_player = 10, qual_loot = loot_boss)

  

    if jogo == 0:
        print("Me vejo em uma rua escura e fria... Melhor procurar abrigo")

    comecar_fase(0)
    fim_do_jogo()

    
    del rua, casa, predio, quarto, cozinha, hall, escada
    del cadaver_aguardando, zumbi_atento, ofereceu_chave
    del dialogo_matinta, cafe_pra_matinta, dialogo_cadaver, sanduba_pro_cadaver
    del dialogo_zumbi, oi_pro_zumbi, ajuda_pro_zumbi, sim_pro_zumbi, nao_pro_zumbi
    del matinta, zumbi, boss, cadaver
    del porta, bau, cofre, geladeira
    del item_chave, item_nada, item_duas_chaves, item_power_up, item_vida, item_cafe
    del porta_boss, cadaver_no_aguardo

  except KeyboardInterrupt:
    pass
  

def segunda_fase():
    global vida_player, ataque_player, nome_player
    global condicoes_triggers, triggers 
    global objetos, personagens, lugar, andavel, jogo, em_combate, manual
    global corredor, primeiro_quarto, segunda_porta, terceira_porta, quarta_porta, porta
    global segundo_quarto, terceiro_quarto, quarto_quarto
    global arvore, cauboi, satanas_de_vestido, bando_de_morcegos
    global bau_da_direita, bau_da_esquerda, fogo
    global pontos, controle_morcegos, dialogo_morcegos
    global charada, charada_proposta, charadas


    condicoes_triggers = {"primeira_vez_no_primeiro_quarto": True}

    manual = {"primeiro_quarto": "O primeiro quarto do corredor. O único que não está trancado",
            "segunda_porta": "Uma das portas do corredor. Preciso de uma chave para abrir",
            "terceira_porta": "Uma das portas do corredor. Preciso de uma chave para abrir",
            "quarta_porta": "Uma das portas do corredor. Preciso de uma chave para abrir",
            "fogo": "O fogo se ergue do chão em dois buracos nos cantos do quarto, como duas fontes. As chamas chegam à minha altura.",
            "trono": "Um trono de madeira negra com detalhes em ouro e um tecido vermelho",
            "satanas_de_vestido": "O Satanás à minha frente, com um vestido comprido verde claro com flores brancas",
            "arvore": "Uma árvore está plantada no meio do quarto. Ela se movimenta, como um humano",
            "porta": "Tem uma porta em um dos cantos da sala... Preciso derrotar todos os inimigos para abrir",
            "cauboi": "Um caubói que saiu da copa da árvore, que está plantada neste quarto",
            "bando_de_morcegos": "Os morcegos voam em círculo sobre mim. Nada parece fazê-los parar",
            "bau_da_direita": "Pode ser aberto com uma chave",
            "bau_da_esquerda": "Pode ser aberto com uma chave",
            "corredor": "Um corredor comprido"
            }

    def triggers(local):
        global vida_player
        if local == "primeiro_quarto" and condicoes_triggers["primeira_vez_no_primeiro_quarto"] == True:
            print("Vejo um quarto vazio, com dois baús no chão, um à esquerda da porta e um à direita")
        if local == "fogo":
            print("Sinto, por alguns instantes, uma dor horrível enquanto o fogo queima meu corpo.")
            vida_player = 0

        

    em_combate = 0

    controle_morcegos = 0
    charada_proposta = False

    objetos = ["bau_da_direita", "bau_da_esquerda", "segunda_porta", "terceira_porta", "quarta_porta", "porta"]
    personagens = ["arvore", "cauboi", "satanas_de_vestido", "bando_de_morcegos"]

    def porta_boss():
        global jogo
        global pontos
        if "arvore" in quarto_quarto or "cauboi" in quarto_quarto:
            print("Eu preciso derrotar todos os inimigos antes de entrar aqui")
            return None
        jogo = 2
        pontos += 90
        return None
    
    porta = objeto(None, None, [porta_boss], True)

    def item_chave_segunda_porta():
        global inventario
        global vida_player
        vida_player += randint(3,5)
        print("Encontrei a chave para a segunda porta!\nEncontrei um bônus de vida! Minha vida agora é {}".format(vida_player))
        inventario.append("chave da segunda porta")

    itens_bau_da_direita = OrderedDict([
        ("chave da segunda porta", item_chave_segunda_porta)
        ])


    def item_chave_bau_direita():
        global inventario
        global ataque_player
        ataque_player += randint(3,5)
        print("Encontrei a chave para o baú da direita!\nEncontrei um power-up! Meu ataque agora é {}".format(ataque_player))
        inventario.append("chave do baú")

    itens_bau_da_esquerda = OrderedDict([
        ("chave do bau da direita", item_chave_bau_direita)
        ])

    def entrar_segunda_porta():
        global lugar
        global segundo_quarto
        lugar = "segundo_quarto"
        if "satanas_de_vestido" in segundo_quarto:
            print("A porta se abre e eu entro no segundo quarto do corredor.\nEste quarto tem paredes de mármore e colunas imitando um templo antigo. Existem dois buracos no chão, um em cada canto do quarto, por onde dançam labaredas da minha altura. Ao centro, vejo um trono em madeira preta com detalhes em ouro e um tecido vermelho.\nNo trono, está sentado o Satanás de vestido.")
        else:
            print("Eu entro no segundo quarto")

    def entrar_terceira_porta():
        global lugar
        global inventario
        global quarta_porta
        lugar = "terceiro_quarto"
        if "chave da quarta porta" not in inventario and quarta_porta.aberto == False:
            print("Consigo destrancar a porta e entro no terceiro quarto. As paredes deste quarto são completamente negras, e ele é muito mais escuro que os outros.\nNo teto, vejo um bando de morcegos repousando. Quando abro a porta de modo que a luz do corredor atinge o quarto, os morcegos decolam e começam a voar em círculos sobre minha cabeça.")
        else:
            print("Eu entro no terceiro quarto")

    def entrar_quarta_porta():
        global lugar
        global quarto_quarto
        lugar = "quarto_quarto"
        if "arvore" in quarto_quarto or "cauboi" in quarto_quarto:
            print("Eu abro a porta lentamente e entro no quarto quarto do corredor.\nEste quarto tem papeis de parede com desenhos de floresta. Passando os olhos pelo papel de parede, vejo várias figuras de cavalos e touros sendo montados, em meio à floresta. Há também uma porta em um dos cantos\nNo centro do quarto, está plantada uma árvore. No entanto, vejo esta árvore se mexer, como um humano. Ela mexia em alguma coisa no interior de sua copa, mas assim que entro no quarto, ela se coloca em uma posição agressiva.")
        else:
            print("Eu entro no quarto quarto")


    segunda_porta = objeto(None, None, [entrar_segunda_porta], True, chave = "chave da segunda porta")
    terceira_porta = objeto(None, None, [entrar_terceira_porta], True, chave = "chave da terceira porta")
    quarta_porta = objeto(None, None, [entrar_quarta_porta], True, chave = "chave da quarta porta")

    bau_da_direita = objeto(itens_bau_da_direita, None, None, True, chave = "chave do baú")
    bau_da_esquerda = objeto(itens_bau_da_esquerda, None, None, False)

    lugar = "corredor"
    corredor = ["primeiro_quarto", "segunda_porta", "terceira_porta", "quarta_porta", "fim"]
    primeiro_quarto = ["bau_da_direita", "bau_da_esquerda", "corredor"]
    segundo_quarto = ["satanas_de_vestido", "fogo", "trono", "corredor"]
    fogo = ["segundo_quarto"]
    terceiro_quarto = ["bando_de_morcegos", "corredor"]
    quarto_quarto = ["arvore", "porta", "corredor"]
    andavel = ['primeiro_quarto', 'fogo']

    def arremessar_cauboi():
        global quarto_quarto
        global vida_player
        if "cauboi" in quarto_quarto:
            print("O caubói me ataca junto com a árvore. Ambos me dão {} pontos de dano".format(arvore.ataque + cauboi.ataque))
            vida_player -= arvore.ataque + cauboi.ataque 
        else:
            print("A árvore coloca um de seus galhos dentro de sua copa e retira um caubói.\nEla arremessa o caubói ao seu lado, e este se prepara para batalhar junto dela")
            respawn(quarto_quarto, "cauboi", vida = 1)

    def chuva_de_meteoros():
        global vida_player
        print("O Satanás de Vestido dá um comando, e meteoros em chamas passam a cair do teto, à minha volta. Eu levo 3 de dano")
        vida_player -= 3

    def loot_satanas():
        global inventario
        global vida_player
        vida_player += randint(3, 5)
        print("O corpo de Satanás de vestido atinge o chão com força. No impacto, percebo que algo caiu de seu bolso.\nEncontrei a chave para a terceira porta!\nEncontrei um bônus de vida! Minha vida agora é {}".format(vida_player))
        inventario.append("chave da terceira porta")

    def loot_arvore():
        global inventario
        print("A árvore estala e cai até o chão, o que parece durar vários instantes. A queda termina com um baque, que ecoa pelo prédio.\nVejo algo brilhando entre as folhas da árvore caída.\nEncontrei uma chave!")
        inventario.append("chave")

    def chave_morcegos():
        global inventario
        global charada, charada_proposta
        global pontos
        global controle_morcegos
        if controle_morcegos == 0 and charada_proposta == True:
          print('Os morcegos param de voar por um instante e dizem, em coro:\n"parabéns, você desvendou a nossa charada!". Eles me entregam a chave do quarto quarto e voltam a voar em círculos')
          inventario.append("chave da quarta porta")
          controle_morcegos = 1
          redefinir_charada()
          charada_proposta = False
          pontos += 1
        elif controle_morcegos == 1 and charada_proposta == True:
          print('Os morcegos param de voar por um instante e dizem, em coro:\n"parabéns, você desvendou a nossa charada!".')
          redefinir_charada()
          charada_proposta = False
          pontos += 1
        elif charada_proposta == False:
          print("Os morcegos começam a voar mais rápido. Parece que eu não disse o que eles esperavam")
    
    def oi_morcegos():
        global charada, nome_player, charadas
        global charada_proposta
        print('Enquanto voam em círculos, os morcegos me propõem uma charada, eles gritam em coro:\n"atenção, {0}! responda com apenas uma palavra!\no que é o que é: {1}?"'.format(nome_player, charadas[charada]))
        charada_proposta = True
        
    charadas = ["foi feito pra andar, mas não anda",
            "dá muitas voltas, mas não sai do lugar", 
            "tem duas letras, um buraco no meio e começa com a letra C", 
            "não se come, mas é bom para comer",
            "anda com os pés na cabeça",
            "quanto mais se tira, mais aumenta",
            "o que tem no meio do ovo",
            "o que tem no meio da rua",
            "cai de pé e corre deitado"]
    respostas = ["rua", "relogio", "CD", "garfo", "piolho", "buraco", "v", "u", "chuva"]


    def redefinir_charada():
        global charada, dialogo_morcegos
        global bando_de_morcegos
        charada = randint(0, 8)
        dialogo_morcegos = {
                "oi": oi_morcegos,
                "vsf": "Nada parece fazer os morcegos pararem de voar em círculos",
                respostas[charada]: chave_morcegos
                }
        bando_de_morcegos = personagem(nome = "Bando de morcegos", ataque = 1, vida = 50*(ataque_player + 5),
                dialogo = dialogo_morcegos, esquiva = 0,
                esquiva_player = 10, prende_combate = False,
                frase_padrao = "Os morcegos começam a voar mais rápido. Parece que eu não disse o que eles esperavam")

    charada = 9
    dialogo_morcegos = {}
    redefinir_charada()
    
    arvore = personagem("Árvore", (vida_player + randint(3, 5))//5 + 1, 5*(ataque_player + randint(3, 5)), [arremessar_cauboi], None, esquiva = 5, esquiva_player = 5, morte = [loot_arvore], especial = 1, tem_loot = False)
    cauboi = personagem("Caubói", 1, 1, None, None, esquiva_player = 10, esquiva = 2, tem_loot = False)
    satanas_de_vestido = personagem("Satanás de Vestido", vida_player//5 + 1, 3*(ataque_player + 2), None, None, morte = [loot_satanas], tem_loot = False)
    
    if jogo == 1:
        print("Eu subi ao nível 2!")
        print("A porta se abre com um estalo e um longo rangido. Ao atravessá-la, me deparo com um longo corredor, com quatro portas")
        pontos += 90

    comecar_fase(1)
    fim_do_jogo()

    del corredor, primeiro_quarto, segunda_porta, terceira_porta, quarta_porta, porta
    del segundo_quarto, terceiro_quarto, quarto_quarto
    del arvore, cauboi, satanas_de_vestido, bando_de_morcegos
    del bau_da_direita, bau_da_esquerda, fogo



def terceira_fase():
    global nome_player
    global vida_player, ataque_player
    global condicoes_triggers, triggers 
    global objetos, personagens, lugar, andavel, jogo, em_combate, manual
    global pontos
    global casa_do_bruno, quarto, quarto_do_bruno, cama_de_viuvo
    global laura, wander, denis, marcia, daniel, luis, leandro, bruno, raquel
    global dialogo_individuo, dialogo_bruno, oi_pro_bruno, individuos
    global Acabou
    global fim
    global controle, controle2

    controle = 0
    controle2 = 0

    class Acabou(Exception): pass

    manual = {
            "cama_de_viuvo": "Uma cama de viúvo onde casais costumam copular. Posso andar até ela para vê-la melhor"}

    andavel = ["casa_do_bruno", "quarto", "quarto_do_bruno", "cama_de_viuvo"]
    objetos = []
    personagens = ["laura", "wander", "denis", "bruno", "luis", "daniel", "raquel", "marcia", "leandro"]

    lugar = "casa_do_bruno"

    condicoes_triggers = {"primeira_vez_quarto_do_bruno": True}

    def triggers(local):
        if local == "quarto_do_bruno" and condicoes_triggers["primeira_vez_quarto_do_bruno"] == True:
            print("Eu entro no quarto do Bruno e me deparo com dois indivíduos acasalando em uma cama de viúvo")
            condicoes_triggers["primeira_vez_quarto_do_bruno"] = False

    def fim():
        global lugar
        global jogo
        global cama_de_viuvo
        if lugar == "cama_de_viuvo" and cama_de_viuvo == ["quarto_do_bruno"]:
            print("\nParabéns! Você ganhou!\n")
            jogo = 666
            raise Acabou

    casa_do_bruno = ["bruno", "quarto_do_bruno", "quarto", "fim"]
    quarto = ["laura", "casa_do_bruno"]
    quarto_do_bruno = ["cama_de_viuvo","casa_do_bruno"]

    cama_de_viuvo = ["quarto_do_bruno"]
    individuos = ["wander", "denis", "marcia", "daniel", "luis", "leandro", "raquel"]

    for i in range(2):
        individuo = individuos[randint(0,len(individuos)-1)]
        cama_de_viuvo.insert(0, individuo)
        individuos.remove(individuo)

    def oi_pro_bruno():
        global vida_player, ataque_player, inventario
        global nome_player, cama_de_viuvo
        print("Olá, {0}!\nVocê está procurando por {1}? Da última vez que eu vi, estava entrando no meu quarto...\nTome, isto vai te ajudar em sua jornada".format(nome_player, eval(cama_de_viuvo[0]).nome))
        aleatorio = randint(0,2)
        if aleatorio == 0:
            ataque_player += randint(1,3)
            print("Bruno me deu um power-up! Meu ataque agora é {}".format(ataque_player))
        elif aleatorio == 1:
            vida_player += randint(1,3)
            print("Bruno me deu um bonus de vida! Minha vida agora é {}".format(vida_player))
        elif aleatorio == 2:
            inventario.append("chave")
            print("Bruno me deu uma chave!")

    dialogo_bruno = {"oi": oi_pro_bruno,
            "vsf": "O Bruno me olha bravo"}

    def oi_pros_individuos():
        global cama_de_viuvo
        global controle
        if len(cama_de_viuvo) != 3:
            controle = 1
        if controle == 0:
            print('{0} se levanta e diz "Olá, {1}! Eu estava te esperando!"\n{2} também se levanta, e diz: "Junte-se a nós!"'.format(eval(cama_de_viuvo[0]).nome, nome_player, eval(cama_de_viuvo[1]).nome))
            controle = 1

    def vsf_pros_individuos():
        global cama_de_viuvo
        global controle2
        if controle2 == 0:
          print('{} se levanta e me diz "Pau no seu cu, arrombado".\nE volta a se deitar'.format(eval(cama_de_viuvo[0]).nome))
          controle2 = 1
        elif controle2 == 1:
            controle2 = 0

    dialogo_individuo = {"oi": oi_pros_individuos,
             "vsf": vsf_pros_individuos}

    laura = personagem(vida = 5, ataque = 1, nome = "Laura")
    denis = personagem(vida = 2, ataque = 1, nome = "Dênis", dialogo = dialogo_individuo)
    marcia = personagem(vida = 2, ataque = 1, nome = "Márcia", dialogo = dialogo_individuo)
    daniel = personagem(vida = 2, ataque = 1, nome = "Daniel", dialogo = dialogo_individuo)
    luis = personagem(vida = 2, ataque = 1, nome = "Luis", dialogo = dialogo_individuo)
    leandro = personagem(vida = 2, ataque = 1, nome = "Leandro", dialogo = dialogo_individuo)
    raquel = personagem(vida = 2, ataque = 1, nome = "Raquel", dialogo = dialogo_individuo)
    wander = personagem(vida = 2, ataque = 1, nome = "Wander", dialogo = dialogo_individuo)

    bruno = personagem(nome = "Bruno", vida = 10, ataque = 2, dialogo = dialogo_bruno)

    if jogo == 2:
        print("Eu subi ao nível 3!")
        print("A porta na verdade era um portal para a casa do Bruno.\nEu pulo o muro e entro na casa.")

    comecar_fase(2, condicoes_extra = fim)
    fim_do_jogo()

print("Bem-vindo ao joguin")
print("Para obter ajuda, digite 'ajuda [comando]'")
print()

nome_player = input("Digite seu nome: ")
print()

primeira_fase()
segunda_fase()
terceira_fase()
