# The Resistance - Documentação do Módulo

Este módulo implementa completamente o jogo de tabuleiro **The Resistance** seguindo as regras clássicas.

## Estrutura do Módulo

O módulo está organizado em 5 partes principais, cada uma com funções claramente nomeadas:

### PARTE 1: Definição de Aliados e Espiões

Funções que definem e verificam os papéis dos jogadores:

- `definir_papel_jogador(player_name)` - Retorna o papel de um jogador
- `eh_resistencia(player_name)` - Verifica se é da Resistência
- `eh_espiao(player_name)` - Verifica se é Espião
- `obter_espioes()` - Lista todos os espiões
- `obter_resistencia()` - Lista todos os membros da Resistência

### PARTE 2: Alocação de Funções Baseada no Número de Jogadores

Sistema que distribui papéis automaticamente conforme o número de jogadores (5-10):

- `alocar_papeis_jogadores(player_names)` - Distribui papéis de forma aleatória
- `_calcular_numero_espioes()` - Calcula quantos espiões deve haver:
  - 5 jogadores: 2 espiões
  - 6 jogadores: 2 espiões
  - 7 jogadores: 3 espiões
  - 8 jogadores: 3 espiões
  - 9 jogadores: 3 espiões
  - 10 jogadores: 4 espiões

### PARTE 3: Sistema de Missões

Gerencia todas as missões do jogo:

- `_obter_configuracao_missoes()` - Configura tamanho do time e falhas necessárias por missão
- `selecionar_time_missao(leader_name, team_members)` - Líder seleciona o time
- `executar_missao(player_name, mission_result)` - Jogador vota na missão
- `calcular_resultado_missao()` - Calcula se a missão foi bem-sucedida
- `avancar_missao()` - Passa para a próxima missão

**Regras importantes:**
- Resistência sempre vota **Sucesso**
- Espiões podem votar **Sucesso** ou **Falha**
- Missão falha se houver número suficiente de votos de falha (varia por missão)

### PARTE 4: Papel de Líder

Gerencia a rotação e poder do líder:

- `obter_lider_atual()` - Retorna o líder atual
- `selecionar_proximo_lider()` - Avança para o próximo líder
- `pode_selecionar_time(player_name)` - Verifica se pode propor time
- `_avancar_lider()` - Rotaciona o líder automaticamente

### PARTE 5: Escolha do Líder e Algoritmo de Aprovação/Rejeição

Sistema completo de votação para aprovar/rejeitar times propostos:

- `votar_proposta_time(player_name, vote)` - Jogador vota na proposta
- `calcular_resultado_votacao_time()` - Calcula resultado da votação
- `rejeitar_time_e_avancar()` - Rejeita time e avança líder
- `aprovar_time()` - Aprova time para execução
- `gerenciar_ciclo_votacao_time()` - Gerencia todo o ciclo de votação

**Regras importantes:**
- Se 5 propostas consecutivas forem rejeitadas, **Espiões ganham automaticamente**
- Maioria simples decide aprovação/rejeição
- Após rejeição, próximo líder propõe novo time

## Como Usar

```python
from resistance_game import ResistanceGame, PlayerRole, MissionResult, Vote

# Criar jogo
game = ResistanceGame(num_players=7)

# Definir jogadores
jogadores = ["Alice", "Bob", "Carol", "David", "Eve", "Frank", "Grace"]
game.alocar_papeis_jogadores(jogadores)

# Verificar papéis
for jogador in jogadores:
    if game.eh_espiao(jogador):
        print(f"{jogador} é espião!")

# Líder propõe time
lider = game.obter_lider_atual()
time = ["Alice", "Bob", "Carol"]
game.selecionar_time_missao(lider, time)

# Todos votam
for jogador in jogadores:
    game.votar_proposta_time(jogador, Vote.APPROVE)

# Verificar resultado
resultado = game.gerenciar_ciclo_votacao_time()
if resultado['status'] == 'time_aprovado':
    # Executar missão
    for jogador in time:
        game.executar_missao(jogador, MissionResult.SUCCESS)
    
    # Calcular resultado
    resultado_missao = game.calcular_resultado_missao()
```

## Estados do Jogo

Use `obter_estado_jogo()` para obter informações completas:

```python
estado = game.obter_estado_jogo()
# Retorna:
# {
#     "num_players": 7,
#     "mission_number": 1,
#     "current_leader": "Alice",
#     "failed_vote_count": 0,
#     "current_mission_team": [...],
#     "leader_votes": {...},
#     "mission_votes": {...},
#     "game_over": False,
#     "winner": None,
#     "mission_config": {...}
# }
```

## Condições de Vitória

- **Resistência vence:** Quando 3 missões são bem-sucedidas
- **Espiões vencem:** Quando 3 missões falham OU quando 5 propostas consecutivas são rejeitadas

## Exemplo Completo

Veja `resistance_example.py` para um exemplo completo de uso do módulo.

