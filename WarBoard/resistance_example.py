"""
Exemplo de uso do módulo The Resistance
Demonstra como usar todas as funcionalidades implementadas
"""

from resistance_game import ResistanceGame, PlayerRole, MissionResult, Vote


def exemplo_jogo_completo():
    """
    Exemplo completo de como usar o jogo The Resistance
    """
    
    # Criar jogo com 7 jogadores
    num_jogadores = 7
    game = ResistanceGame(num_jogadores)
    
    # Lista de jogadores
    jogadores = [f"Jogador{i+1}" for i in range(num_jogadores)]
    
    # PARTE 2: Alocar papéis dos jogadores
    print("=== ALOCANDO PAPÉIS ===")
    game.alocar_papeis_jogadores(jogadores)
    
    # PARTE 1: Verificar quem é resistência e quem é espião
    print("\n=== PAPÉIS DOS JOGADORES ===")
    for jogador in jogadores:
        papel = game.definir_papel_jogador(jogador)
        tipo = "Espião" if game.eh_espiao(jogador) else "Resistência"
        print(f"{jogador}: {tipo}")
    
    print(f"\nEspiões: {game.obter_espioes()}")
    print(f"Resistência: {game.obter_resistencia()}")
    
    # PARTE 4: Verificar líder atual
    print(f"\n=== LÍDER ATUAL ===")
    print(f"Líder: {game.obter_lider_atual()}")
    
    # Simular ciclo de jogo
    print("\n=== INICIANDO MISSÃO 1 ===")
    lider = game.obter_lider_atual()
    print(f"Líder propõe time: {lider}")
    
    # PARTE 3: Selecionar time para missão
    mission_config = game.mission_config[0]
    print(f"Tamanho necessário do time: {mission_config['mission_size']}")
    
    # Líder seleciona time
    time_proposto = jogadores[:mission_config['mission_size']]
    game.selecionar_time_missao(lider, time_proposto)
    print(f"Time proposto: {time_proposto}")
    
    # PARTE 5: Todos votam na proposta
    print("\n=== VOTAÇÃO DO TIME ===")
    for jogador in jogadores:
        # Simulação: cada jogador vota aleatoriamente aprovar ou rejeitar
        voto = Vote.APPROVE if random.random() > 0.3 else Vote.REJECT
        game.votar_proposta_time(jogador, voto)
        print(f"{jogador}: {voto.value}")
    
    # Calcular resultado
    resultado_votacao = game.gerenciar_ciclo_votacao_time()
    print(f"\nResultado: {resultado_votacao['status']}")
    print(f"Mensagem: {resultado_votacao['message']}")
    
    if resultado_votacao['status'] == 'time_aprovado':
        # PARTE 3: Executar missão
        print("\n=== EXECUTANDO MISSÃO ===")
        time_missao = resultado_votacao['time']
        
        for jogador in time_missao:
            # Resistência sempre vota sucesso, espiões podem votar falha
            if game.eh_espiao(jogador):
                resultado = MissionResult.FAILURE if random.random() > 0.5 else MissionResult.SUCCESS
            else:
                resultado = MissionResult.SUCCESS
            
            game.executar_missao(jogador, resultado)
            print(f"{jogador} ({'Espião' if game.eh_espiao(jogador) else 'Resistência'}): {resultado.value}")
        
        # Calcular resultado da missão
        resultado_missao = game.calcular_resultado_missao()
        if resultado_missao:
            print(f"\nResultado da Missão: {resultado_missao[0].value}")
            print(f"Falhas: {resultado_missao[1]['fail_count']}/{resultado_missao[1]['fails_needed']}")
            
            # Avançar para próxima missão
            game.avancar_missao()
            print(f"\nPróxima missão: {game.mission_number}")
            print(f"Novo líder: {game.obter_lider_atual()}")
    
    # Mostrar estado do jogo
    print("\n=== ESTADO DO JOGO ===")
    estado = game.obter_estado_jogo()
    for chave, valor in estado.items():
        print(f"{chave}: {valor}")


if __name__ == "__main__":
    import random
    exemplo_jogo_completo()

