# Instruções do Jogo THE RESISTANCE

## Funcionalidades Implementadas

### 1. Botão de Iniciar Rodada
- O botão "Iniciar Jogo" no lobby agora funciona corretamente
- Após iniciar, o jogo THE RESISTANCE começa automaticamente
- O líder pode propor um time clicando nos jogadores
- Use o botão "Confirmar Time" para propor o time selecionado

### 2. Controles de Redimensionamento da Tela
- **ESC**: Abre menu de configurações (em qualquer tela do jogo)
- **Menu Principal**: Botão "CONFIGURAÇÕES" para acessar opções
- **Disponível em**: Menu principal, Lobby, Durante o jogo
- **Opções disponíveis**:
  - Pequeno (800x600)
  - Médio (1200x800) - padrão
  - Grande (1600x1000)
  - Extra Grande (1920x1080)
  - Tela Cheia

### 3. Fluxo Completo do Jogo

#### Fase 1: Proposta do Time
1. O líder atual (destacado em dourado) seleciona jogadores clicando neles
2. O número de jogadores selecionados deve corresponder ao tamanho necessário da missão
3. Clique em "Confirmar Time" para propor o time

#### Fase 2: Votação do Time
1. Todos os jogadores votam para aprovar ou rejeitar o time proposto
2. Use os botões "Aprovar" (verde) ou "Rejeitar" (vermelho)
3. Se aprovado, a missão inicia automaticamente
4. Se rejeitado, o próximo jogador se torna líder

#### Fase 3: Execução da Missão
1. Apenas os membros do time proposto participam
2. Cada membro vota "Sucesso" ou "Falha"
3. Apenas espiões podem votar "Falha"
4. A missão é concluída quando todos votam

#### Fase 4: Resultado
1. O sistema calcula automaticamente o resultado
2. A missão avança para a próxima
3. O jogo termina quando uma equipe atinge 3 vitórias

### 4. Chat
- Use o painel de chat à direita para comunicação
- Clique no campo de texto para digitar
- Pressione Enter para enviar mensagem
- O chat funciona em todas as telas do jogo

### 5. Informações do Jogo
- **Papéis**: Cada jogador tem um papel (Resistência ou Espião)
- **Líder**: Rotaciona a cada rodada
- **Missões**: 5 missões no total
- **Vitória**: Resistência precisa de 3 sucessos, Espiões precisam de 3 falhas

### 6. Dicas de Jogo
- Apenas espiões sabem quem são os outros espiões
- A Resistência deve tentar identificar espiões através do comportamento
- Espiões devem tentar sabotar missões sem serem descobertos
- Use o chat para discussões e estratégias

## Como Testar
1. Execute `python main.py`
2. Escolha "THE RESISTANCE"
3. Selecione o número de jogadores (5-10)
4. **Na tela de lobby**: Pressione ESC para testar configurações
5. Clique em "Iniciar"
6. **Durante o jogo**: Pressione ESC para acessar configurações
7. Teste diferentes tamanhos de tela nas configurações
8. **Teste o chat**: Digite mensagens no painel à direita
9. **Verifique responsividade**: O chat deve estar sempre visível em todos os tamanhos

## Controles Resumidos
- **Mouse**: Clicar em botões e selecionar jogadores
- **Teclado**: Digitar no chat
- **ESC**: Abrir configurações (em qualquer tela)
- **Menu Principal**: Acessar configurações via botão "CONFIGURAÇÕES"
