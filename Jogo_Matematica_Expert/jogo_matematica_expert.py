# Bibliotecas Necessárias
import os
import pygame
import random

class Jogo: # Classe principal do programa
    def __init__(self): # Definindo todas as variáveis necessárias para esta classe 
        self.largura_tela = 1024
        self.altura_tela = 704
        self.contador_pontos = 0
        self.numero_pergunta = 0
        self.resultado = 0
        self.primeiro_valor = 0
        self.segundo_valor = 0
        self.tempo = 0
        self.contador_tempo = 0 
        self.tempo_escolhido = 0
        self.operacao = ""
        self.tela_inicial = ""
        self.caminho_relativo_imagem_inicial = ""
        self.caminho_relativo_som_fundo = ""
        self.janela = ""
        self.janela_de_inicio_aberta = True
        self.janela_de_jogo_aberta = False
        self.janela_de_reinicio_aberta = False
        self.caminho_atual = os.path.abspath(os.path.dirname(__file__)) # Caminho atual dos arquivos
        self.mouse = ""


        # Inicia o pygame
        pygame.init()

    def ajustes_iniciais(self): # Faz os ajustes iniciais do jogo(tela, título, música, etc...)
        self.caminho_relativo_imagem_inicial = os.path.join(self.caminho_atual, "tela_fundo_jogo_matematica.jpg")
        self.tela_inicial = pygame.image.load(self.caminho_relativo_imagem_inicial)
        # Ajusta o modo do tamanho da janela
        self.janela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        self.botao = Botao(self)
        # Coloca o título do jogo
        pygame.display.set_caption("Matemática Expert")
        self.caminho_relativo_som_fundo = os.path.join(self.caminho_atual, 'SomFundo_Dark_Electro_Rock.mp3')
        pygame.mixer.music.load(self.caminho_relativo_som_fundo)
        pygame.mixer.music.play(loops=-1)


    def texto_na_tela(self, mensagem, tamanho, x, y): # Facilita a chamada da classe "Texto"
        texto = Texto(self)
        texto.formatacao_texto(mensagem, tamanho)
        texto.posicao_texto(x, y)

    def janela_inicial_aberta(self): # Janela inicial(Onde é escolhida a dificuldade) 
        self.janela_de_reinicio_aberta = False
        while self.janela_de_inicio_aberta: # Loop enquanto a janela estiver aberta
            self.janela.blit(self.tela_inicial, (0, 0))
            for evento in pygame.event.get(): # Detecta todos os eventos que ocorrem(mouse, teclado, etc...)
                if evento.type == pygame.QUIT:
                    self.janela_de_inicio_aberta = False

                if self.botao.verificar_clique_dificuldade(evento) == False:
                    self.janela_jogo_aberta()
                    
            self.mouse = pygame.mouse.get_pos()
            self.texto_na_tela("Olá, mundo!!", 60, 380, 250)
            self.texto_na_tela("Escolha um dos níveis de dificuldade abaixo: ", 40, 220, 350)

            self.botao.cria_botoes_dificuldade()
            pygame.display.update() # Atualiza a tela a cada loop

    def janela_jogo_aberta(self): #  Janela onde o usuário joga
        self.janela_de_inicio_aberta = False
        self.janela_de_jogo_aberta = True
        while self.janela_de_jogo_aberta: # Loop enquanto a janela estiver aberta
            self.janela.blit(self.tela_inicial, (0, 0))
            for evento in pygame.event.get(): # Detecta todos os eventos que ocorrem(mouse, teclado, etc...)
                if evento.type == pygame.QUIT:
                    self.janela_de_jogo_aberta = False
                
                self.botao.verificar_clique_resposta(evento)
            
            if self.tempo > 0:
                self.temporizador()

            else:
                self.janela_reiniciar_aberta()

            if self.contador_pontos < self.numero_pergunta-1:
                self.numero_pergunta = 1
                self.janela_reiniciar_aberta()

            self.texto_na_tela(f"{self.numero_pergunta}) Resolva a seguinte operação: {self.primeiro_valor} {self.operacao} {self.segundo_valor}",\
                           40, 100, 250)
            
            self.mensagem_pontuacao = f"PONTUAÇÃO: {self.contador_pontos}"
            self.texto_na_tela(self.mensagem_pontuacao, 30, 820, 20)

            self.botao.cria_botoes_respostas()
            pygame.display.update() # Atualiza a tela a cada loop

    def janela_reiniciar_aberta(self): # Janela para reiniciar o jogo
        self.janela_de_jogo_aberta = False
        self.janela_de_reinicio_aberta = True
        while self.janela_de_reinicio_aberta: # Loop enquanto a janela estiver aberta
            self.janela.blit(self.tela_inicial, (0, 0))
            for evento in pygame.event.get(): # Detecta todos os eventos que ocorrem(mouse, teclado, etc...)
                if evento.type == pygame.QUIT:
                    self.janela_de_reinicio_aberta = False

                if self.botao.verificar_clique_reiniciar(evento) == False:
                    self.contador_pontos = 0
                    self.janela_de_inicio_aberta = True
                    self.janela_inicial_aberta()

            self.mouse = pygame.mouse.get_pos()

            self.texto_na_tela("GAME OVER!!!", 60, 380, 250)
            self.texto_na_tela(f"SUA PONTUAÇÃO: {self.contador_pontos}", 40, 220, 350)
            
            self.botao.cria_botao_reiniciar()
            pygame.display.update() # Atualiza a tela a cada loop

    def operacoes_aleatorias(self): # Gera operações matemáticas de forma aleátoria
        lista_numeros_grandes = []
        lista_numeros_pequenos = []
        lista_operacoes = ["+", "-", "*", "/"]
        self.operacao = random.choice(lista_operacoes)
        for i in range(1, 100+1):
            lista_numeros_grandes.append(i)
        
        for i in range(1, 30+1):
            lista_numeros_pequenos.append(i)

        if self.operacao == "*" or self.operacao == "/":
            self.primeiro_valor = random.choice(lista_numeros_pequenos)
            self.segundo_valor = random.choice(lista_numeros_pequenos)
        
        else:
            self.primeiro_valor = random.choice(lista_numeros_grandes)
            self.segundo_valor = random.choice(lista_numeros_grandes)
        
        while self.operacao == "/" and self.primeiro_valor % self.segundo_valor != 0:
            self.operacao = random.choice(lista_operacoes)
        
        if self.operacao == "+":
            resultado = self.primeiro_valor + self.segundo_valor
        elif self.operacao == "-":
            resultado = self.primeiro_valor - self.segundo_valor
        elif self.operacao == "*":
            resultado = self.primeiro_valor * self.segundo_valor
        elif self.operacao == "/":
            resultado = self.primeiro_valor / self.segundo_valor

        return resultado
    
    def lista_possibilidades(self): # Gera alternativas incorretas a partir do resultado correto
        self.resultado = self.operacoes_aleatorias()
        self.numero_pergunta += 1
        modifica_resultado_correto = []
        resultados_possiveis = [self.resultado]
        operacoes_modifica_resposta = ["+", "-"]
        for i in range(1, 31):
            modifica_resultado_correto.append(i)
        for _ in range(3):
            operacao = random.choice(operacoes_modifica_resposta)
            if operacao == "+":
                resultados_possiveis.append(self.resultado + random.choice(modifica_resultado_correto))
            if operacao == "-":
                resultados_possiveis.append(self.resultado - random.choice(modifica_resultado_correto))
        random.shuffle(resultados_possiveis)
        return resultados_possiveis

    def temporizador(self): # Temporizador que contabiliza a partir do nível de processamento do pc
        # Mostra o tempo na tela
        self.texto_na_tela(f"TEMPO: {self.tempo}", 30, 465, 600)
        # Contador de tempo para resetar o jogo(equivalente a 1 minuto)
        self.contador_tempo += 7
        if self.contador_tempo > 1000:
            self.contador_tempo = 0
            self.tempo -= 1
    

class Texto:
    def __init__(self, jogo): # Iniciando as variáveis necessárias para essa classe
        self.jogo = jogo
        self.fonte = ""
        self.formatacao = ""

    def formatacao_texto(self, texto, tamanho): # Formata texto(cor, tamanho e fonte)
        self.fonte = pygame.font.SysFont(None, tamanho)
        self.formatacao = self.fonte.render(texto, True, (255, 255, 255, 255))

    def posicao_texto(self, x, y): # Posiciona o texto na tela
        self.jogo.janela.blit(self.formatacao, (x, y))


class Botao:
    def __init__(self, jogo): # Iniciando as variáveis necessárias para essa classe
        self.jogo = jogo
        self.botoes_dificuldades = ["FÁCIL", "MÉDIO", "DIFÍCIL", "EXPERT", "NIGHTMARE"]
        self.botoes_possibilidade_respostas = jogo.lista_possibilidades()
        self.botao_cor_normal = (0, 0, 80)
        self.botao_cor_mouse_em_cima = (0, 0, 150)
        self.fonte = pygame.font.SysFont(None, 40)
        self.largura_total_botoes_dificuldade = 0
        self.largura_total_botoes_resposta = 0
        self.contador_pontos = 0
        self.mensagem_pontuacao = ""

    def desenhar_botao(self, mensagem, x, y, largura, cor): # Desenha o botão na tela
        retangulo = pygame.Rect(x, y, largura, 40)
        pygame.draw.rect(self.jogo.janela, cor, retangulo)
        texto = self.fonte.render(mensagem, True, (255, 255, 255))
        texto_retangulo = texto.get_rect()
        texto_retangulo.center = retangulo.center
        self.jogo.janela.blit(texto, texto_retangulo)

    def cria_botoes_dificuldade(self): # Desenha os botões de dificuldades com interatividade e larguras proporcionais
        total_botoes_dificuldades = len(self.botoes_dificuldades)
        self.largura_total_botoes_dificuldade = sum([self.fonte.size(texto)[0] for texto in self.botoes_dificuldades]) + (total_botoes_dificuldades - 1) * 20
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_dificuldade // 2 -50
        posicao_y = self.jogo.altura_tela // 2 +100

        for texto in self.botoes_dificuldades: # Define a largura dos botões de acordo com o tamanho do texto
            largura = self.fonte.size(texto)[0] + 20
            self.desenhar_botao(texto, posicao_x, posicao_y, largura, self.botao_cor_normal)
            posicao_x += largura + 20
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_dificuldade // 2 -50
        for texto in self.botoes_dificuldades: # Faz o mesmo que o loop anterior, porém a cor do botão muda com o mouse
            largura = self.fonte.size(texto)[0] + 20
            if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
                self.desenhar_botao(texto, posicao_x, posicao_y, largura, self.botao_cor_mouse_em_cima)
                break
            posicao_x += largura + 20
        
    def verificar_clique_dificuldade(self, evento): # Captura e verifica o evento de clique do botão
        mouse_x, mouse_y = pygame.mouse.get_pos()
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_dificuldade // 2 - 50
        posicao_y = self.jogo.altura_tela // 2 + 100

        for texto in self.botoes_dificuldades:
            largura = self.fonte.size(texto)[0] + 20
            if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
                if evento.type == pygame.MOUSEBUTTONDOWN: # Se o botão do mouse for clicado, será verficado se...
                    if texto == "FÁCIL":
                        self.jogo.tempo = 60
                    elif texto == "MÉDIO":
                        self.jogo.tempo = 30
                    elif texto == "DIFÍCIL":
                        self.jogo.tempo = 15
                    elif texto == "EXPERT":
                        self.jogo.tempo = 10
                    elif texto == "NIGHTMARE":
                        self.jogo.tempo = 5
                    self.jogo.tempo_escolhido = self.jogo.tempo
                    self.jogo.temporizador()
                    return False
                break
            posicao_x += largura + 20

    def cria_botoes_respostas(self): # Desenha os botões de resposta com interatividade e larguras proporcionais
        total_botoes_respostas = len(self.botoes_possibilidade_respostas)
        # Aqui você pode ajustar para que o tamanho dos botões seja baseado na quantidade de números possíveis
        self.largura_total_botoes_resposta = total_botoes_respostas * (self.fonte.size("0")[0] + 100) + (total_botoes_respostas - 1) * 20
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_resposta // 2 - 50
        posicao_y = self.jogo.altura_tela // 2 + 100

        for numero in self.botoes_possibilidade_respostas: # Define a largura dos botões de acordo com o tamanho do texto
            texto = str(numero)  # Convertendo o número em string
            largura = self.fonte.size(texto)[0] + 50
            self.desenhar_botao(texto, posicao_x, posicao_y, largura, self.botao_cor_normal)
            posicao_x += largura + 20
            
        mouse_x, mouse_y = pygame.mouse.get_pos()
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_resposta // 2 - 50
        for numero in self.botoes_possibilidade_respostas:# O mesmo do loop anterior,porém a cor do botão muda com o mouse
            texto = str(numero)  # Convertendo o número em string
            largura = self.fonte.size(texto)[0] + 50
            if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
                self.desenhar_botao(texto, posicao_x, posicao_y, largura, self.botao_cor_mouse_em_cima)
                break
            posicao_x += largura + 20

    def verificar_clique_resposta(self, evento): # Captura e verifica o evento de clique do botão
        mouse_x, mouse_y = pygame.mouse.get_pos()
        posicao_x = self.jogo.largura_tela // 2 - self.largura_total_botoes_resposta // 2 - 50
        posicao_y = self.jogo.altura_tela // 2 + 100

        for numero in self.botoes_possibilidade_respostas:
            texto = str(numero)
            largura = self.fonte.size(texto)[0] + 50
            if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
                if evento.type == pygame.MOUSEBUTTONDOWN: # Se o botão do mouse for clicado, será verficado se...
                    if numero == self.jogo.resultado:
                        self.jogo.contador_pontos += 1
                        self.jogo.tempo = self.jogo.tempo_escolhido
                    # Atualiza os valores da operação e da lista de possibilidades
                    self.jogo.operacoes_aleatorias()
                    self.botoes_possibilidade_respostas = self.jogo.lista_possibilidades()
                    return False
                break
            posicao_x += largura + 20

    def cria_botao_reiniciar(self): # Desenha os botões de resposta com interatividade e larguras proporcionais
        mouse_x, mouse_y = pygame.mouse.get_pos()
        largura = 230
        posicao_x = self.jogo.largura_tela // 2  -105
        posicao_y = self.jogo.altura_tela // 2 + 100
        self.desenhar_botao("REINICIAR", posicao_x, posicao_y, largura, self.botao_cor_normal)
        if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
            self.desenhar_botao("REINICIAR", posicao_x, posicao_y, largura, self.botao_cor_mouse_em_cima)

    def verificar_clique_reiniciar(self, evento): # Captura e verifica o evento de clique do botão
        mouse_x, mouse_y = pygame.mouse.get_pos()
        largura = 230
        posicao_x = self.jogo.largura_tela // 2  -105
        posicao_y = self.jogo.altura_tela // 2 + 100
        if posicao_x <= mouse_x <= posicao_x + largura and posicao_y <= mouse_y <= posicao_y + 40:
            if evento.type == pygame.MOUSEBUTTONDOWN: # Se o botão do mouse for clicado...
                return False


if __name__ == "__main__":
    jogo = Jogo()
    jogo.ajustes_iniciais()
    jogo.janela_inicial_aberta()
    pygame.quit()
