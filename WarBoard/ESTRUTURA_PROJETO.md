# Estrutura do Projeto THE RESISTANCE

## 📁 Organização dos Módulos

### 🎮 **Sistema Principal**
- **`game_manager.py`** - Gerenciador principal que coordena todos os sistemas
- **`main.py`** - Ponto de entrada do jogo (chama GameManager)

### 🖥️ **Sistema de Interface (UI)**
- **`ui_system.py`** - Coordena todas as telas de interface
- **`main_menu.py`** - Menu principal do jogo
- **`room_menu_screen.py`** - Menu de salas (criar/entrar)
- **`create_room_screen.py`** - Tela de criação de sala
- **`player_name_screen.py`** - Tela de seleção de nome
- **`lobby_screen.py`** - Tela de lobby
- **`game_screen.py`** - Tela principal do jogo
- **`settings_screen.py`** - Tela de configurações
- **`ui_components.py`** - Componentes reutilizáveis (botões, etc.)

### 🏠 **Sistema de Salas**
- **`room_system.py`** - Gerencia criação, códigos e dados das salas
- **Funcionalidades:**
  - Criação de salas com códigos únicos
  - Entrada em salas existentes
  - Gerenciamento de jogadores
  - Validação de capacidade

### 🎲 **Sistema do Jogo**
- **`resistance_system.py`** - Gerencia toda a lógica do THE RESISTANCE
- **`resistance_game.py`** - Lógica base do jogo (regras, missões, etc.)
- **Funcionalidades:**
  - Inicialização de partidas
  - Gerenciamento de turnos
  - Sistema de votação
  - Execução de missões
  - Verificação de vitória

### ⚙️ **Sistema de Configurações**
- **`settings_system.py`** - Gerencia configurações do jogo
- **Funcionalidades:**
  - Tamanho de tela
  - Modo tela cheia
  - Volume e outras opções
  - Persistência de configurações

### 🔧 **Utilitários e Constantes**
- **`constants.py`** - Constantes do jogo (cores, dimensões, etc.)
- **`game_states.py`** - Estados possíveis do jogo
- **`resistance_example.py`** - Exemplo de uso do sistema

## 🔄 **Fluxo de Dados**

```
GameManager (Coordenador)
    ↓
UI System (Interface)
    ↓
Room System (Salas) ← → Resistance System (Jogo)
    ↓
Settings System (Configurações)
```

## 📋 **Responsabilidades de Cada Sistema**

### **GameManager**
- ✅ Coordena todos os sistemas
- ✅ Gerencia estados do jogo
- ✅ Roteia eventos para sistemas apropriados
- ✅ Controla loop principal

### **UISystem**
- ✅ Gerencia todas as telas
- ✅ Processa eventos de interface
- ✅ Coordena navegação entre telas
- ✅ Atualiza layouts responsivos

### **RoomSystem**
- ✅ Cria códigos únicos de sala
- ✅ Gerencia jogadores conectados
- ✅ Valida entrada em salas
- ✅ Controla capacidade das salas

### **ResistanceSystem**
- ✅ Executa lógica do jogo
- ✅ Gerencia turnos e missões
- ✅ Processa votos e ações
- ✅ Determina vencedores

### **SettingsSystem**
- ✅ Gerencia configurações
- ✅ Aplica mudanças de tela
- ✅ Salva/carrega preferências
- ✅ Valida configurações

## 🎯 **Vantagens da Separação**

1. **Modularidade**: Cada sistema tem responsabilidade específica
2. **Manutenibilidade**: Fácil de modificar partes isoladas
3. **Testabilidade**: Sistemas podem ser testados independentemente
4. **Reutilização**: Componentes podem ser reutilizados
5. **Escalabilidade**: Fácil adicionar novas funcionalidades

## 🚀 **Como Adicionar Novas Funcionalidades**

1. **Nova Tela**: Adicionar em `ui_system.py` e criar arquivo da tela
2. **Nova Lógica**: Adicionar em sistema apropriado ou criar novo
3. **Novo Estado**: Adicionar em `game_states.py` e rotear em `GameManager`
4. **Nova Configuração**: Adicionar em `settings_system.py`

## 📝 **Padrões Utilizados**

- **MVC**: Separação entre lógica (Model), interface (View) e controle (Controller)
- **Observer**: Sistemas notificam mudanças de estado
- **Factory**: Criação de componentes de UI
- **State Machine**: Gerenciamento de estados do jogo
