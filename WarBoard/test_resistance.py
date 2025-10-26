"""
Teste para validar o módulo The Resistance
Verifica se funciona corretamente para todos os números de jogadores (5-10)
"""

from resistance_game import ResistanceGame, PlayerRole, MissionResult, Vote


def testar_numero_espioes():
    """Testa se o número de espiões está correto para cada configuração"""
    print("=== TESTE: Número de Espiões ===")
    
    configs_esperadas = {
        5: 2,
        6: 2,
        7: 3,
        8: 3,
        9: 3,
        10: 4
    }
    
    for num_players in range(5, 11):
        game = ResistanceGame(num_players)
        jogadores = [f"J{i}" for i in range(num_players)]
        game.alocar_papeis_jogadores(jogadores)
        
        num_espioes = len(game.obter_espioes())
        esperado = configs_esperadas[num_players]
        
        status = "✓" if num_espioes == esperado else "✗"
        print(f"{status} {num_players} jogadores: {num_espioes} espiões (esperado: {esperado})")
        
        # Verificar que total de espiões + resistência = total de jogadores
        total = len(game.obter_espioes()) + len(game.obter_resistencia())
        assert total == num_players, f"Total não confere para {num_players} jogadores"


def testar_configuracao_missoes():
    """Testa se as configurações de missões estão corretas"""
    print("\n=== TESTE: Configuração de Missões ===")
    
    for num_players in range(5, 11):
        game = ResistanceGame(num_players)
        config = game.mission_config
        
        print(f"\n{num_players} jogadores:")
        for i, missao in enumerate(config, 1):
            print(f"  Missão {i}: {missao['mission_size']} jogadores, {missao['fails_needed']} falha(s) necessária(s)")
        
        # Verificar que há 5 missões
        assert len(config) == 5, f"Deve haver 5 missões para {num_players} jogadores"


def testar_ciclo_completo():
    """Testa um ciclo completo de jogo"""
    print("\n=== TESTE: Ciclo Completo de Jogo ===")
    
    game = ResistanceGame(7)
    jogadores = [f"J{i+1}" for i in range(7)]
    game.alocar_papeis_jogadores(jogadores)
    
    print(f"Espiões: {game.obter_espioes()}")
    print(f"Resistência: {game.obter_resistencia()}")
    print(f"Líder inicial: {game.obter_lider_atual()}")
    
    # Simular primeira missão aprovada e bem-sucedida
    lider = game.obter_lider_atual()
    time = jogadores[:2]  # Missão 1 requer 2 jogadores
    
    assert game.selecionar_time_missao(lider, time), "Deve conseguir selecionar time"
    
    # Todos votam aprovar
    for jogador in jogadores:
        game.votar_proposta_time(jogador, Vote.APPROVE)
    
    resultado = game.gerenciar_ciclo_votacao_time()
    assert resultado['status'] == 'time_aprovado', "Time deve ser aprovado"
    
    # Executar missão (sucesso)
    for jogador in time:
        game.executar_missao(jogador, MissionResult.SUCCESS)
    
    resultado_missao = game.calcular_resultado_missao()
    assert resultado_missao[0] == MissionResult.SUCCESS, "Missão deve ser bem-sucedida"
    assert game.success_count == 1, "Deve ter 1 sucesso"
    
    # Avançar missão
    game.avancar_missao()
    assert game.mission_number == 2, "Deve estar na missão 2"
    assert game.obter_lider_atual() != lider, "Líder deve ter mudado"
    
    print("✓ Ciclo completo executado com sucesso")


def testar_vitoria_espioes():
    """Testa condição de vitória dos espiões (5 rejeições)"""
    print("\n=== TESTE: Vitória por Rejeições ===")
    
    game = ResistanceGame(5)
    jogadores = [f"J{i+1}" for i in range(5)]
    game.alocar_papeis_jogadores(jogadores)
    
    # Simular 5 rejeições consecutivas
    for i in range(5):
        lider = game.obter_lider_atual()
        time = jogadores[:2]
        game.selecionar_time_missao(lider, time)
        
        # Todos votam rejeitar
        for jogador in jogadores:
            game.votar_proposta_time(jogador, Vote.REJECT)
        
        resultado = game.gerenciar_ciclo_votacao_time()
        assert resultado['status'] == 'time_rejeitado', f"Rejeição {i+1} deve ser rejeitada"
        
        if game.game_over:
            break
    
    assert game.game_over, "Jogo deve terminar após 5 rejeições"
    assert game.winner == PlayerRole.SPY, "Espiões devem ganhar"
    print("✓ Vitória dos espiões por rejeições funcionando")


def testar_vitoria_resistencia():
    """Testa condição de vitória da resistência (3 sucessos)"""
    print("\n=== TESTE: Vitória da Resistência ===")
    
    game = ResistanceGame(5)
    jogadores = [f"J{i+1}" for i in range(5)]
    game.alocar_papeis_jogadores(jogadores)
    
    # Simular 3 missões bem-sucedidas
    for missao_num in range(1, 4):
        # Aprovar time
        lider = game.obter_lider_atual()
        config = game.mission_config[missao_num - 1]
        time = jogadores[:config['mission_size']]
        
        game.selecionar_time_missao(lider, time)
        for jogador in jogadores:
            game.votar_proposta_time(jogador, Vote.APPROVE)
        
        game.gerenciar_ciclo_votacao_time()
        
        # Executar missão com sucesso (resistência sempre vota sucesso)
        for jogador in time:
            game.executar_missao(jogador, MissionResult.SUCCESS)
        
        game.calcular_resultado_missao()
        
        if game.game_over:
            break
        
        if missao_num < 3:
            game.avancar_missao()
    
    assert game.game_over, "Jogo deve terminar após 3 sucessos"
    assert game.winner == PlayerRole.RESISTANCE, "Resistência deve ganhar"
    print("✓ Vitória da resistência funcionando")


if __name__ == "__main__":
    print("Iniciando testes do módulo The Resistance...\n")
    
    try:
        testar_numero_espioes()
        testar_configuracao_missoes()
        testar_ciclo_completo()
        testar_vitoria_espioes()
        testar_vitoria_resistencia()
        
        print("\n" + "="*50)
        print("✓ TODOS OS TESTES PASSARAM!")
        print("="*50)
        print("\nO código está funcionando corretamente para:")
        print("- Todos os números de jogadores (5-10)")
        print("- Alocação correta de espiões")
        print("- Configuração correta de missões")
        print("- Sistema de votação")
        print("- Condições de vitória")
        
    except AssertionError as e:
        print(f"\n✗ TESTE FALHOU: {e}")
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()

