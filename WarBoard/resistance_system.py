"""
Sistema do Jogo THE RESISTANCE
Gerencia toda a lógica do jogo The Resistance
"""

from resistance_game import ResistanceGame, PlayerRole, MissionResult, Vote
from typing import Dict, List, Optional, Tuple


class ResistanceSystem:
    """
    Sistema responsável por gerenciar o jogo The Resistance
    """
    
    def __init__(self):
        """Inicializa o sistema do jogo"""
        self.game = None
        self.player_names = []
        self.current_mission_team = []
        self.selected_team = []
        self.game_state = {
            'is_active': False,
            'mission_number': 1,
            'current_leader': '',
            'game_over': False,
            'winner': None
        }
    
    def start_game(self, num_players: int, player_names: List[str] = None):
        """
        Inicia um novo jogo
        
        Args:
            num_players: Número de jogadores
            player_names: Lista de nomes dos jogadores
        """
        try:
            self.game = ResistanceGame(num_players)
            
            if player_names:
                self.player_names = player_names
            else:
                self.player_names = [f"Jogador {i+1}" for i in range(num_players)]
            
            # Alocar papéis
            self.game.alocar_papeis_jogadores(self.player_names)
            
            # Atualizar estado
            self.game_state['is_active'] = True
            self.game_state['mission_number'] = 1
            self.game_state['current_leader'] = self.game.obter_lider_atual()
            self.game_state['game_over'] = False
            self.game_state['winner'] = None
            
            return True
        except Exception as e:
            print(f"Erro ao iniciar jogo: {e}")
            return False
    
    def propose_team(self, leader_name: str, team_members: List[str]) -> bool:
        """
        Líder propõe um time para a missão
        
        Args:
            leader_name: Nome do líder
            team_members: Lista de membros do time
            
        Returns:
            True se a proposta foi aceita, False caso contrário
        """
        if not self.game or not self.game_state['is_active']:
            return False
        
        return self.game.selecionar_time_missao(leader_name, team_members)
    
    def vote_on_team(self, player_name: str, vote: Vote) -> Dict:
        """
        Jogador vota na proposta do time
        
        Args:
            player_name: Nome do jogador
            vote: Voto (APPROVE ou REJECT)
            
        Returns:
            Resultado da votação
        """
        if not self.game:
            return {'status': 'error', 'message': 'Jogo não iniciado'}
        
        # Registrar voto
        self.game.votar_proposta_time(player_name, vote)
        
        # Calcular resultado
        result = self.game.gerenciar_ciclo_votacao_time()
        
        if result['status'] == 'time_aprovado':
            self.current_mission_team = result['time']
            return {
                'status': 'approved',
                'message': 'Time aprovado! Missão pode começar.',
                'team': result['time']
            }
        elif result['status'] == 'time_rejeitado':
            return {
                'status': 'rejected',
                'message': f"Time rejeitado. Novo líder: {result['novo_lider']}",
                'new_leader': result['novo_lider']
            }
        else:
            return {
                'status': 'waiting',
                'message': 'Aguardando mais votos...'
            }
    
    def execute_mission(self, player_name: str, result: MissionResult) -> Dict:
        """
        Jogador executa a missão
        
        Args:
            player_name: Nome do jogador
            result: Resultado da missão (SUCCESS ou FAILURE)
            
        Returns:
            Resultado da execução
        """
        if not self.game:
            return {'status': 'error', 'message': 'Jogo não iniciado'}
        
        # Verificar se é espião (apenas espiões podem votar falha)
        if result == MissionResult.FAILURE and not self.game.eh_espiao(player_name):
            return {'status': 'error', 'message': 'Apenas espiões podem votar falha!'}
        
        # Executar missão
        success = self.game.executar_missao(player_name, result)
        if not success:
            return {'status': 'error', 'message': 'Erro ao executar missão'}
        
        # Verificar se missão foi completada
        mission_result = self.game.calcular_resultado_missao()
        if mission_result:
            mission_outcome, details = mission_result
            
            # Avançar para próxima missão
            self.game.avancar_missao()
            
            # Atualizar estado
            self.game_state['mission_number'] = self.game.mission_number
            self.game_state['current_leader'] = self.game.obter_lider_atual()
            
            # Verificar vitória
            winner = self.game.verificar_vitoria()
            if winner:
                self.game_state['game_over'] = True
                self.game_state['winner'] = winner.value
                return {
                    'status': 'game_over',
                    'winner': winner.value,
                    'mission_result': mission_outcome.value,
                    'details': details
                }
            
            return {
                'status': 'mission_complete',
                'result': mission_outcome.value,
                'details': details,
                'next_mission': self.game.mission_number,
                'new_leader': self.game.obter_lider_atual()
            }
        
        return {'status': 'waiting', 'message': 'Aguardando outros jogadores...'}
    
    def get_game_state(self) -> Dict:
        """Retorna o estado atual do jogo"""
        if not self.game:
            return self.game_state
        
        # Obter estado do jogo
        state = self.game.obter_estado_jogo()
        
        # Combinar com estado interno
        self.game_state.update({
            'mission_number': state['mission_number'],
            'current_leader': state['current_leader'],
            'game_over': state['game_over'],
            'winner': state['winner'],
            'mission_config': state.get('mission_config'),
            'current_mission_team': state.get('current_mission_team', []),
            'mission_results': state.get('mission_results', []),
            'success_count': state.get('success_count', 0),
            'failure_count': state.get('failure_count', 0)
        })
        
        return self.game_state
    
    def get_player_role(self, player_name: str) -> str:
        """Retorna o papel de um jogador"""
        if not self.game:
            return "Desconhecido"
        
        role = self.game.definir_papel_jogador(player_name)
        return role.value
    
    def is_spy(self, player_name: str) -> bool:
        """Verifica se um jogador é espião"""
        if not self.game:
            return False
        
        return self.game.eh_espiao(player_name)
    
    def get_mission_team(self) -> List[str]:
        """Retorna o time da missão atual"""
        return self.current_mission_team
    
    def can_propose_team(self, player_name: str) -> bool:
        """Verifica se um jogador pode propor time"""
        if not self.game:
            return False
        
        return self.game.pode_selecionar_time(player_name)
    
    def reset_game(self):
        """Reseta o jogo"""
        self.game = None
        self.player_names = []
        self.current_mission_team = []
        self.selected_team = []
        self.game_state = {
            'is_active': False,
            'mission_number': 1,
            'current_leader': '',
            'game_over': False,
            'winner': None
        }
