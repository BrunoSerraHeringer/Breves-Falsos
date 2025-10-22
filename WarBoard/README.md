# War Board - Jogo de Estratégia de Guerra

Um jogo de tabuleiro de estratégia de guerra desenvolvido em Python com Pygame.

## Instalação

1. Certifique-se de ter Python instalado
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

```bash
python main.py
```

## Servidor de Socket Local (somente local)

Para habilitar comunicação local simples entre clientes (chat/broadcast), rode o servidor TCP incluso:

```bash
python server.py
```

Detalhes:
- Por padrão o servidor escuta em `127.0.0.1:8765` (apenas esta máquina)
- Você pode conectar via `telnet 127.0.0.1 8765` para testar
- Comando `/quit` desconecta o cliente

## Controles

- **Mouse**: Navegação pelos menus e interação com o jogo
- **ESC**: Voltar ao menu (quando implementado)

## Recursos Implementados

- ✅ Menu principal com design moderno
- ✅ Botões interativos com efeitos hover
- ✅ Background com gradiente
- ⏳ Sistema de jogo (em desenvolvimento)
- ⏳ Configurações (em desenvolvimento)

## Estrutura do Projeto

- `main.py`: Arquivo principal com toda a lógica do jogo
- `requirements.txt`: Dependências do projeto

## Próximas Funcionalidades

- Tela de jogo com tabuleiro
- Sistema de turnos
- Unidades militares
- Sistema de combate
- Configurações de jogo





