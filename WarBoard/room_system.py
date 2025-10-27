"""
Sistema de Salas
Gerencia criação, códigos e dados das salas
"""

import random
import string
from typing import Dict, List, Optional


class RoomSystem:
    """
    Sistema responsável por gerenciar salas de jogo
    """
    
    def __init__(self):
        """Inicializa o sistema de salas"""
        self.current_room = None
        self.room_code = ""
        self.rooms = {}  # Dicionário de salas ativas
    
    def create_room(self, num_players: int) -> str:
        """
        Cria uma nova sala
        
        Args:
            num_players: Número de jogadores da sala
            
        Returns:
            Código da sala criada
        """
        # Gerar código único
        self.room_code = self._generate_room_code()
        
        # Criar dados da sala
        self.current_room = {
            'code': self.room_code,
            'num_players': num_players,
            'players': [],
            'status': 'waiting',  # waiting, playing, finished
            'created_at': self._get_timestamp()
        }
        
        # Adicionar à lista de salas
        self.rooms[self.room_code] = self.current_room
        
        return self.room_code
    
    def join_room(self, room_code: str, player_name: str) -> bool:
        """
        Entra em uma sala existente
        
        Args:
            room_code: Código da sala
            player_name: Nome do jogador
            
        Returns:
            True se conseguiu entrar, False caso contrário
        """
        if room_code not in self.rooms:
            return False
        
        room = self.rooms[room_code]
        if len(room['players']) >= room['num_players']:
            return False
        
        if room['status'] != 'waiting':
            return False
        
        # Adicionar jogador
        room['players'].append({
            'name': player_name,
            'ready': False,
            'joined_at': self._get_timestamp()
        })
        
        return True
    
    def get_room_code(self) -> str:
        """Retorna o código da sala atual"""
        return self.room_code
    
    def get_room_data(self) -> Optional[Dict]:
        """Retorna os dados da sala atual"""
        return self.current_room
    
    def get_players(self) -> List[Dict]:
        """Retorna lista de jogadores da sala atual"""
        if self.current_room:
            return self.current_room['players']
        return []
    
    def is_room_full(self) -> bool:
        """Verifica se a sala atual está cheia"""
        if not self.current_room:
            return False
        
        return len(self.current_room['players']) >= self.current_room['num_players']
    
    def can_start_game(self) -> bool:
        """Verifica se o jogo pode ser iniciado"""
        if not self.current_room:
            return False
        
        return (len(self.current_room['players']) >= 5 and 
                self.current_room['status'] == 'waiting')
    
    def start_game(self):
        """Inicia o jogo na sala atual"""
        if self.current_room:
            self.current_room['status'] = 'playing'
    
    def _generate_room_code(self) -> str:
        """Gera um código de sala único de 5 caracteres"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            if code not in self.rooms:
                return code
    
    def _get_timestamp(self) -> str:
        """Retorna timestamp atual"""
        import time
        return str(int(time.time()))
    
    def cleanup_old_rooms(self):
        """Remove salas antigas (para limpeza)"""
        # TODO: Implementar limpeza de salas antigas
        pass
