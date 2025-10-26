"""
The Resistance - Jogo de Tabuleiro
Implementação completa das regras do jogo The Resistance
"""

import random
from enum import Enum
from typing import List, Dict, Set, Optional, Tuple


class PlayerRole(Enum):
    """Define os papéis dos jogadores no jogo"""
    RESISTANCE = "Resistência"
    SPY = "Espião"


class MissionResult(Enum):
    """Resultado de uma missão"""
    SUCCESS = "Sucesso"
    FAILURE = "Falha"


class Vote(Enum):
    """Voto de aprovação/rejeição"""
    APPROVE = "Aprovar"
    REJECT = "Rejeitar"


class ResistanceGame:
    """
    Classe principal que gerencia o jogo The Resistance
    """
    
    def __init__(self, num_players: int):
        """
        Inicializa o jogo com número de jogadores
        
        Args:
            num_players: Número de jogadores (5-10)
        """
        if not (5 <= num_players <= 10):
            raise ValueError("O jogo requer entre 5 e 10 jogadores")
        
        self.num_players = num_players
        self.players: List[str] = []
        self.player_roles: Dict[str, PlayerRole] = {}
        self.current_leader_index = 0
        self.mission_number = 1
        self.failed_vote_count = 0
        self.game_over = False
        self.winner: Optional[PlayerRole] = None
        
        # Histórico de resultados das missões
        self.mission_results: List[MissionResult] = []
        self.success_count = 0
        self.failure_count = 0
        
        # Configuração de missões baseada no número de jogadores
        self.mission_config = self._obter_configuracao_missoes()
        self.current_mission_team: List[str] = []
        self.current_mission_votes: Dict[str, MissionResult] = {}
        self.leader_votes: Dict[str, Vote] = {}
        
    # ============ PARTE 1: DEFINIÇÃO DE ALIADOS E ESPIÕES ============
    
    def definir_papel_jogador(self, player_name: str) -> PlayerRole:
        """
        Define se um jogador é Resistência ou Espião
        
        Args:
            player_name: Nome do jogador
            
        Returns:
            PlayerRole do jogador
        """
        return self.player_roles.get(player_name, PlayerRole.RESISTANCE)
    
    def eh_resistencia(self, player_name: str) -> bool:
        """
        Verifica se um jogador é da Resistência
        
        Args:
            player_name: Nome do jogador
            
        Returns:
            True se for da Resistência, False caso contrário
        """
        return self.player_roles.get(player_name) == PlayerRole.RESISTANCE
    
    def eh_espiao(self, player_name: str) -> bool:
        """
        Verifica se um jogador é Espião
        
        Args:
            player_name: Nome do jogador
            
        Returns:
            True se for Espião, False caso contrário
        """
        return self.player_roles.get(player_name) == PlayerRole.SPY
    
    def obter_espioes(self) -> List[str]:
        """
        Retorna lista de todos os espiões no jogo
        
        Returns:
            Lista com nomes dos espiões
        """
        return [player for player, role in self.player_roles.items() if role == PlayerRole.SPY]
    
    def obter_resistencia(self) -> List[str]:
        """
        Retorna lista de todos os membros da Resistência
        
        Returns:
            Lista com nomes dos membros da Resistência
        """
        return [player for player, role in self.player_roles.items() if role == PlayerRole.RESISTANCE]
    
    # ============ PARTE 2: ALOCAÇÃO DE FUNÇÕES BASEADA NO NÚMERO DE JOGADORES ============
    
    def alocar_papeis_jogadores(self, player_names: List[str]) -> None:
        """
        Aloca os papéis de Resistência e Espião baseado no número de jogadores.
        A quantidade de espiões segue a regra padrão do jogo The Resistance.
        
        Args:
            player_names: Lista com nomes de todos os jogadores
        """
        if len(player_names) != self.num_players:
            raise ValueError(f"Esperado {self.num_players} jogadores, recebido {len(player_names)}")
        
        self.players = player_names.copy()
        
        # Determinar número de espiões baseado no número de jogadores
        num_spies = self._calcular_numero_espioes()
        
        # Selecionar espiões aleatoriamente
        spies = random.sample(player_names, num_spies)
        
        # Atribuir papéis
        self.player_roles = {}
        for player in player_names:
            if player in spies:
                self.player_roles[player] = PlayerRole.SPY
            else:
                self.player_roles[player] = PlayerRole.RESISTANCE
    
    def _calcular_numero_espioes(self) -> int:
        """
        Calcula o número de espiões baseado no número total de jogadores.
        Regras padrão do The Resistance:
        - 5 jogadores: 2 espiões
        - 6 jogadores: 2 espiões
        - 7 jogadores: 3 espiões
        - 8 jogadores: 3 espiões
        - 9 jogadores: 3 espiões
        - 10 jogadores: 4 espiões
        
        Returns:
            Número de espiões para este jogo
        """
        spy_count = {
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            9: 3,
            10: 4
        }
        return spy_count.get(self.num_players, 2)
    
    # ============ PARTE 3: SISTEMA DE MISSÕES ============
    
    def _obter_configuracao_missoes(self) -> List[Dict]:
        """
        Retorna a configuração de missões baseada no número de jogadores.
        Cada missão especifica quantos jogadores devem participar e quantas
        falhas são necessárias para a missão falhar.
        
        Returns:
            Lista de dicionários com configuração de cada missão
        """
        configs = {
            5: [
                {"mission_size": 2, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 2, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1}
            ],
            6: [
                {"mission_size": 2, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1}
            ],
            7: [
                {"mission_size": 2, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 2},
                {"mission_size": 4, "fails_needed": 1}
            ],
            8: [
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 5, "fails_needed": 2},
                {"mission_size": 5, "fails_needed": 1}
            ],
            9: [
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 5, "fails_needed": 2},
                {"mission_size": 5, "fails_needed": 1}
            ],
            10: [
                {"mission_size": 3, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 4, "fails_needed": 1},
                {"mission_size": 5, "fails_needed": 2},
                {"mission_size": 5, "fails_needed": 1}
            ]
        }
        return configs.get(self.num_players, configs[5])
    
    def selecionar_time_missao(self, leader_name: str, team_members: List[str]) -> bool:
        """
        Líder seleciona o time para a missão atual
        
        Args:
            leader_name: Nome do líder atual
            team_members: Lista de nomes dos jogadores selecionados para a missão
            
        Returns:
            True se a seleção é válida, False caso contrário
        """
        if self.game_over:
            return False
        
        if self._obter_lider_atual() != leader_name:
            return False
        
        if self.mission_number > len(self.mission_config):
            return False
        
        mission_config = self.mission_config[self.mission_number - 1]
        required_size = mission_config["mission_size"]
        
        if len(team_members) != required_size:
            return False
        
        if not all(player in self.players for player in team_members):
            return False
        
        self.current_mission_team = team_members.copy()
        return True
    
    def votar_missao(self, player_name: str, vote: Vote) -> bool:
        """
        Jogador vota para aprovar ou rejeitar o time proposto
        
        Args:
            player_name: Nome do jogador votando
            vote: Voto (APPROVE ou REJECT)
            
        Returns:
            True se o voto foi registrado, False caso contrário
        """
        if player_name not in self.players:
            return False
        
        if not self.current_mission_team:
            return False
        
        self.leader_votes[player_name] = vote
        return True
    
    def calcular_resultado_votacao_time(self) -> Optional[bool]:
        """
        Calcula se o time proposto foi aprovado pela maioria
        
        Returns:
            True se aprovado, False se rejeitado, None se ainda faltam votos
        """
        if len(self.leader_votes) < self.num_players:
            return None
        
        approve_count = sum(1 for vote in self.leader_votes.values() if vote == Vote.APPROVE)
        reject_count = sum(1 for vote in self.leader_votes.values() if vote == Vote.REJECT)
        
        return approve_count > reject_count
    
    def executar_missao(self, player_name: str, mission_result: MissionResult) -> bool:
        """
        Jogador executa a missão (sucesso ou falha)
        Espiões podem votar falha, Resistência sempre vota sucesso
        
        Args:
            player_name: Nome do jogador executando
            mission_result: Resultado escolhido pelo jogador
            
        Returns:
            True se o voto foi registrado, False caso contrário
        """
        if player_name not in self.current_mission_team:
            return False
        
        # Resistência sempre vota sucesso
        if self.eh_resistencia(player_name) and mission_result == MissionResult.FAILURE:
            return False
        
        self.current_mission_votes[player_name] = mission_result
        return True
    
    def calcular_resultado_missao(self) -> Optional[Tuple[MissionResult, Dict]]:
        """
        Calcula o resultado final da missão baseado nos votos
        
        Returns:
            Tupla com (resultado da missão, detalhes dos votos) ou None se ainda faltam votos
        """
        mission_config = self.mission_config[self.mission_number - 1]
        
        if len(self.current_mission_votes) < len(self.current_mission_team):
            return None
        
        fails_needed = mission_config["fails_needed"]
        fail_count = sum(1 for vote in self.current_mission_votes.values() 
                         if vote == MissionResult.FAILURE)
        
        mission_result = MissionResult.SUCCESS if fail_count < fails_needed else MissionResult.FAILURE
        
        # Registrar resultado da missão
        self.mission_results.append(mission_result)
        if mission_result == MissionResult.SUCCESS:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        # Verificar vitória após registrar resultado
        self._verificar_condicao_vitoria()
        
        return (mission_result, {
            "fail_count": fail_count,
            "fails_needed": fails_needed,
            "votes": self.current_mission_votes.copy()
        })
    
    def avancar_missao(self) -> None:
        """
        Avança para a próxima missão e limpa dados da missão atual
        """
        if self.game_over:
            return
        
        self.mission_number += 1
        self.current_mission_team = []
        self.current_mission_votes = {}
        self.leader_votes = {}
        self._avancar_lider()
    
    def _verificar_condicao_vitoria(self) -> None:
        """
        Verifica se o jogo terminou e define o vencedor.
        Chamado automaticamente após cada missão completada.
        """
        # Se já há um vencedor definido, não verifica novamente
        if self.winner:
            return
        
        # Vitória da Resistência: 3 missões bem-sucedidas
        if self.success_count >= 3:
            self.winner = PlayerRole.RESISTANCE
            self.game_over = True
            return
        
        # Vitória dos Espiões: 3 missões falhadas
        if self.failure_count >= 3:
            self.winner = PlayerRole.SPY
            self.game_over = True
            return
    
    def verificar_vitoria(self) -> Optional[PlayerRole]:
        """
        Verifica se o jogo terminou e quem ganhou
        
        Returns:
            PlayerRole do vencedor ou None se o jogo continua
        """
        return self.winner
    
    # ============ PARTE 4: PAPEL DE LÍDER ============
    
    def _obter_lider_atual(self) -> str:
        """
        Retorna o nome do líder atual
        
        Returns:
            Nome do líder atual
        """
        return self.players[self.current_leader_index]
    
    def obter_lider_atual(self) -> str:
        """
        Método público para obter o líder atual
        
        Returns:
            Nome do líder atual
        """
        return self._obter_lider_atual()
    
    def _avancar_lider(self) -> None:
        """
        Avança o líder para o próximo jogador na ordem
        """
        self.current_leader_index = (self.current_leader_index + 1) % self.num_players
    
    def selecionar_proximo_lider(self) -> str:
        """
        Seleciona o próximo líder (avança automaticamente após rejeição ou missão)
        
        Returns:
            Nome do novo líder
        """
        self._avancar_lider()
        return self._obter_lider_atual()
    
    def pode_selecionar_time(self, player_name: str) -> bool:
        """
        Verifica se um jogador pode selecionar o time (é o líder atual)
        
        Args:
            player_name: Nome do jogador
            
        Returns:
            True se o jogador é o líder atual
        """
        return self._obter_lider_atual() == player_name
    
    # ============ PARTE 5: ESCOLHA DO LÍDER E ALGORITMO DE APROVAÇÃO/REJEIÇÃO ============
    
    def rejeitar_time_e_avancar(self) -> str:
        """
        Rejeita o time proposto e avança para o próximo líder.
        Se 5 propostas consecutivas forem rejeitadas, os espiões ganham.
        
        Returns:
            Nome do novo líder
        """
        self.failed_vote_count += 1
        
        # Se 5 votações consecutivas falharem, espiões ganham
        if self.failed_vote_count >= 5:
            self.winner = PlayerRole.SPY
            self.game_over = True
            return self._obter_lider_atual()
        
        # Limpar votos e time atual
        self.current_mission_team = []
        self.leader_votes = {}
        
        # Avançar líder
        return self.selecionar_proximo_lider()
    
    def aprovar_time(self) -> None:
        """
        Time foi aprovado, agora os membros votam na missão
        Reseta o contador de falhas de votação
        """
        self.failed_vote_count = 0
        # Os votos do líder já estão registrados, agora os membros da missão votam
    
    def votar_proposta_time(self, player_name: str, vote: Vote) -> Optional[bool]:
        """
        Sistema completo de votação para aprovar/rejeitar o time proposto
        
        Args:
            player_name: Nome do jogador votando
            vote: Voto do jogador (APPROVE ou REJECT)
            
        Returns:
            True se aprovado, False se rejeitado, None se ainda faltam votos
        """
        if not self.votar_missao(player_name, vote):
            return None
        
        return self.calcular_resultado_votacao_time()
    
    def gerenciar_ciclo_votacao_time(self) -> Dict:
        """
        Gerencia o ciclo completo de votação do time:
        1. Líder propõe time
        2. Todos votam
        3. Se aprovado, missão começa
        4. Se rejeitado, próximo líder propõe
        
        Returns:
            Dicionário com status da votação e ações necessárias
        """
        resultado = self.calcular_resultado_votacao_time()
        
        if resultado is None:
            return {
                "status": "aguardando_votos",
                "message": "Aguardando todos os jogadores votarem"
            }
        
        if resultado:
            self.aprovar_time()
            return {
                "status": "time_aprovado",
                "message": "Time aprovado! Missão pode começar.",
                "time": self.current_mission_team.copy()
            }
        else:
            novo_lider = self.rejeitar_time_e_avancar()
            return {
                "status": "time_rejeitado",
                "message": f"Time rejeitado. Novo líder: {novo_lider}",
                "novo_lider": novo_lider,
                "contador_falhas": self.failed_vote_count
            }
    
    def obter_estado_jogo(self) -> Dict:
        """
        Retorna o estado atual completo do jogo
        
        Returns:
            Dicionário com todas as informações do estado atual
        """
        return {
            "num_players": self.num_players,
            "mission_number": self.mission_number,
            "current_leader": self._obter_lider_atual(),
            "failed_vote_count": self.failed_vote_count,
            "current_mission_team": self.current_mission_team.copy(),
            "leader_votes": {k: v.value for k, v in self.leader_votes.items()},
            "mission_votes": {k: v.value for k, v in self.current_mission_votes.items()},
            "mission_results": [r.value for r in self.mission_results],
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "game_over": self.game_over,
            "winner": self.winner.value if self.winner else None,
            "mission_config": self.mission_config[self.mission_number - 1] if self.mission_number <= len(self.mission_config) else None
        }
