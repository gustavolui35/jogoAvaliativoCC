import pygame
import random
import pyttsx3

voz = pyttsx3.init()
voz.setProperty("rate", 180)

from recursos.trabalho import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import gerar_passageiro

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada, horaJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Taxi GTA")
icone  = pygame.image.load("bases/Icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 215, 0)


fundo = pygame.image.load("bases/Fundo.png")
fundo = pygame.transform.scale(fundo, (1129,700))
fundoDead = pygame.image.load("bases/FimDeJogo.png")
fundoStart = pygame.image.load("bases/TelaInicial.png")

taxi = pygame.image.load("bases/Personagem.png")
taxi = pygame.transform.scale(taxi, (180, 90))
carro = pygame.image.load("bases/Azul.png")
carro = pygame.transform.scale(carro, (160,80))
passaro = pygame.image.load("bases/Passaro.png")
passaro = pygame.transform.scale(passaro, (50,40))
explosaoSound = pygame.mixer.Sound("bases/Batida.mp3")
pygame.mixer.music.load("bases/TrilhaSonora.mp3")
fonteMenu = pygame.font.SysFont("arial", 24, bold=True)


def jogar():
    fundoMov1 = 0
    fundoMov2 = fundo.get_width()

    raioSol = 30
    aumentando = True

    posicaoXPersona = 0
    posicaoXPassaro = 1000
    posicaoYPassaro = random.randint(20,150)
    posicaoYPersona = 60

    movimentoXPersona = 0
    movimentoYPersona = 0

    velocidadeMovPersona = 5

    pistas = [180, 240, 300, 360, 420]

    posicaoXcarro = 800
    posicaoYcarro = random.choice(pistas)
    velocidadecarro = 2


    pontos = 0

    pausado = False

    pygame.mixer.music.play(-1)
    
    voz.say(f"Bem vindo {nome}. Prepare-se para dirigir. Boa sorte!")
    voz.runAndWait()



    dificuldade = 20

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                elif evento.key == pygame.K_SPACE:
                    pausado = not pausado

                elif evento.key == pygame.K_UP:
                    movimentoYPersona = -velocidadeMovPersona

                elif evento.key == pygame.K_DOWN:
                    movimentoYPersona = velocidadeMovPersona

            elif evento.type == pygame.KEYUP:

                if evento.key == pygame.K_UP:
                    movimentoYPersona = 0

                elif evento.key == pygame.K_DOWN:
                    movimentoYPersona = 0

        if pausado:

            tela.fill(branco)
            tela.blit(fundo,(fundoMov1,0))
            tela.blit(fundo,(fundoMov2,0))

            textoPause = fonteMenu.render("PAUSE",True,branco)
            tela.blit(textoPause,(450,320))

            pygame.display.update()
            relogio.tick(60)
            continue

        # SOL PULSANTE

        if aumentando:
            raioSol += 1
        else:
            raioSol -= 1

        if raioSol >= 40:
            aumentando = False

        if raioSol <= 30:
            aumentando = True

        # MOVIMENTO PERSONAGEM

        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona

        if posicaoXPersona < 180:
            posicaoXPersona = 180
        elif posicaoXPersona > 685:
            posicaoXPersona = 685

# Limita o táxi à pista
        if posicaoYPersona < 170:
         posicaoYPersona = 170

        elif posicaoYPersona > 420:
         posicaoYPersona = 420
        # PASSARO

        posicaoXPassaro -= 2

        if posicaoXPassaro < -50:
            posicaoXPassaro = 1000
            posicaoYPassaro = random.randint(20,150)

        # carro

        posicaoXcarro -= velocidadecarro

        if posicaoXcarro < -125:
            posicaoXcarro = 800
            pontos += 1
            
            if pontos == 20:
             voz.say("Parabéns! Você sobreviveu ao trânsito até agora.")
             voz.runAndWait()


            velocidadecarro += 1
            pistas = [180, 240, 300, 360, 420]
            posicaoYcarro = random.choice(pistas)


        # DESENHAR

        tela.fill(branco)

        tela.blit(fundo,(fundoMov1,0))
        tela.blit(fundo,(fundoMov2,0))

        pygame.draw.circle(tela,(255,255,0),(900,80),raioSol)

        fundoMov1 -= 1
        fundoMov2 -= 1

        if fundoMov1 <= -1129:
            fundoMov1 = 1129

        elif fundoMov2 <= -1129:
            fundoMov2 = 1129

        tela.blit(passaro,(posicaoXPassaro,posicaoYPassaro))
        tela.blit(taxi,(posicaoXPersona,posicaoYPersona))
        tela.blit(carro,(posicaoXcarro,posicaoYcarro))

        texto = fonteMenu.render("Pontos: " + str(pontos),True,branco)
        tela.blit(texto,(700,15))
        
        textoAjuda = fonteMenu.render("Press Space to Pause Game", True, branco)
        tela.blit(textoAjuda, (10, 15))

        pixelsPersonaX = list(range(posicaoXPersona,posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona,posicaoYPersona+51))

        pixelscarroX = list(range(posicaoXcarro,posicaoXcarro+125))
        pixelscarroY = list(range(posicaoYcarro,posicaoYcarro+25))

        if len(list(set(pixelscarroY).intersection(set(pixelsPersonaY)))) > dificuldade:

            if len(list(set(pixelscarroX).intersection(set(pixelsPersonaX)))) > dificuldade:

                escreverDados(nome,pontos)
                dead(pontos)

        pygame.display.update()
        relogio.tick(60)


def dead(pontos):
    
    voz.say(f"Fim de jogo {nome}. Até a próxima!")
    voz.runAndWait()

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        
        textoPontos = fonteMenu.render(f"Pontuacao: {pontos}", True, branco)
        tela.blit(textoPontos, (10, 120))

        textoRecorde = fonteMenu.render(f"Recorde: {nome_maior} - {maior_pontos}", True, branco)
        tela.blit(textoRecorde, (10, 150))

        # Botões invisíveis sobre a imagem
        startButton = pygame.Rect(370, 520, 270, 60)
        quitButton = pygame.Rect(370, 600, 270, 60)

        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
while True:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif evento.type == pygame.MOUSEBUTTONUP:

            if startButton.collidepoint(evento.pos):
                jogar()

            if quitButton.collidepoint(evento.pos):
                pygame.quit()
                quit()

    # Desenha a tela
    tela.fill(branco)
    tela.blit(fundoStart, (0,0))

    # Retângulos para testar a posição
    startButton = pygame.Rect(380, 360, 250, 65)
    quitButton = pygame.Rect(380, 440, 250, 60)

    # Nome do jogador
# Sombra
    textoNome = fonteMenu.render(f"Jogador: {nome}", True, preto)
    tela.blit(textoNome, (12,525))

# Texto
    textoNome = fonteMenu.render(f"Jogador: {nome}", True, amarelo)
    tela.blit(textoNome, (410, 525 ))
# Instruções
    texto1 = fonteMenu.render("Desvie dos carros para sobreviver.", True, amarelo)
    tela.blit(texto1, (15, 15))

    texto2 = fonteMenu.render("Use as setas para mover o taxi.", True, amarelo)
    tela.blit(texto2, (15, 35))

# Melhor jogador
    textoRecorde = fonteMenu.render(
    f"The Best - {nome_maior} - {maior_pontos} - {dataJogada} - {horaJogada}",
    True,
    amarelo
)
    tela.blit(textoRecorde, (480, 15))
    
    pygame.display.update()
    relogio.tick(60)


    start()