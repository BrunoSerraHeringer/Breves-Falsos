"""
Sistema de repetição de teclas para THE RESISTANCE
"""

import pygame
import time


class KeyRepeatSystem:
    """
    Sistema que gerencia repetição de teclas com delay inicial
    """
    
    def __init__(self):
        # Configurações de timing
        self.initial_delay = 0.8  # 800ms de delay inicial (maior)
        self.repeat_delay = 0.05  # 50ms entre repetições (mais rápido)
        
        # Estado das teclas
        self.pressed_keys = {}  # {key: {'start_time': float, 'last_repeat': float}}
        self.repeat_events = []  # Eventos de repetição para processar
        
    def update(self):
        """Atualiza o sistema de repetição de teclas"""
        current_time = time.time()
        self.repeat_events.clear()
        
        # Verificar teclas pressionadas
        keys = pygame.key.get_pressed()
        
        for key in range(len(keys)):
            if keys[key]:  # Tecla está pressionada
                if key not in self.pressed_keys:
                    # Primeira vez pressionando a tecla
                    self.pressed_keys[key] = {
                        'start_time': current_time,
                        'last_repeat': current_time
                    }
                    # Criar evento inicial
                    self.repeat_events.append(pygame.event.Event(
                        pygame.KEYDOWN, {'key': key, 'repeat': False}
                    ))
                else:
                    # Tecla já estava pressionada, verificar se deve repetir
                    key_data = self.pressed_keys[key]
                    time_since_start = current_time - key_data['start_time']
                    time_since_last_repeat = current_time - key_data['last_repeat']
                    
                    # Se passou o delay inicial e o delay de repetição
                    if (time_since_start >= self.initial_delay and 
                        time_since_last_repeat >= self.repeat_delay):
                        
                        # Criar evento de repetição
                        self.repeat_events.append(pygame.event.Event(
                            pygame.KEYDOWN, {'key': key, 'repeat': True}
                        ))
                        
                        # Atualizar último tempo de repetição
                        key_data['last_repeat'] = current_time
            else:
                # Tecla não está mais pressionada, remover do estado
                if key in self.pressed_keys:
                    del self.pressed_keys[key]
    
    def get_repeat_events(self):
        """Retorna os eventos de repetição para processar"""
        return self.repeat_events.copy()
    
    def is_key_pressed(self, key):
        """Verifica se uma tecla está sendo pressionada"""
        return key in self.pressed_keys
    
    def get_key_press_duration(self, key):
        """Retorna há quanto tempo uma tecla está sendo pressionada"""
        if key in self.pressed_keys:
            return time.time() - self.pressed_keys[key]['start_time']
        return 0
    
    def clear(self):
        """Limpa o estado de todas as teclas"""
        self.pressed_keys.clear()
        self.repeat_events.clear()
