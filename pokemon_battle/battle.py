import random
from typing import Tuple, List
from .pokemon import Pokemon

class BattleSystem:
    """Clase que maneja la lógica de las batallas Pokémon."""
    
    SPECIAL_ATTACK_TYPES = {
        'water', 'fire', 'grass', 'electric', 'psychic',
        'ice', 'dragon', 'dark', 'fairy'
    }
    
    @classmethod
    def calculate_damage(cls, attacker: Pokemon, defender: Pokemon, move_type: str = None) -> int:
        """
        Calcula el daño de un ataque entre dos Pokémon.
        
        """
        # Determinar tipo de movimiento si no se especifica
        if not move_type:
            move_type = attacker.type1.lower()
        
        # Determinar si es ataque especial o físico
        is_special = move_type.lower() in cls.SPECIAL_ATTACK_TYPES
        
        # Obtener estadísticas relevantes
        attack_stat = attacker.sp_attack if is_special else attacker.attack
        defense_stat = defender.sp_defense if is_special else defender.defense
        
        # Calcular efectividad
        effectiveness = defender.get_effectiveness(move_type)
        
        # Fórmula de daño simplificada (similar a los juegos principales)
        level_factor = 50  # Nivel fijo para simplificar
        power = 80        # Poder base fijo para simplificar
        modifier = random.uniform(0.85, 1.0) * effectiveness
        
        damage = (((2 * level_factor / 5 + 2) * power * attack_stat / defense_stat) / 50 + 2) * modifier
        
        return int(max(1, damage))
    
    @classmethod
    def battle(cls, pokemon1: Pokemon, pokemon2: Pokemon) -> Tuple[Pokemon, List[str]]:
        """
        Simula una batalla entre dos Pokémon.
        
        """
        # Preparar Pokémon para la batalla
        pokemon1.reset_hp()
        pokemon2.reset_hp()
        
        # Determinar orden de ataque (por velocidad)
        if pokemon1.speed == pokemon2.speed:
            first, second = (pokemon1, pokemon2) if random.random() > 0.5 else (pokemon2, pokemon1)
        else:
            first, second = (pokemon1, pokemon2) if pokemon1.speed > pokemon2.speed else (pokemon2, pokemon1)
        
        battle_log = [
            f"¡Comienza la batalla entre {pokemon1.name} y {pokemon2.name}!",
            f"{first.name} (Velocidad: {first.speed}) ataca primero!"
        ]
        
        turn = 1
        while True:
            battle_log.append(f"\n--- Turno {turn} ---")
            
            # Primer Pokémon ataca
            damage = cls.calculate_damage(first, second)
            fainted = second.receive_damage(damage)
            battle_log.append(
                f"{first.name} ataca a {second.name} por {damage} de daño! "
                f"(HP: {second.current_hp}/{second.hp})"
            )
            
            if fainted:
                battle_log.append(f"\n¡{second.name} se ha debilitado!")
                battle_log.append(f"¡{first.name} gana la batalla!")
                return first, battle_log
            
            # Segundo Pokémon ataca
            damage = cls.calculate_damage(second, first)
            fainted = first.receive_damage(damage)
            battle_log.append(
                f"{second.name} ataca a {first.name} por {damage} de daño! "
                f"(HP: {first.current_hp}/{first.hp})"
            )
            
            if fainted:
                battle_log.append(f"\n¡{first.name} se ha debilitado!")
                battle_log.append(f"¡{second.name} gana la batalla!")
                return second, battle_log
            
            turn += 1