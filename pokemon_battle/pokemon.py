"""
Módulo que contiene la clase Pokémon con todos sus atributos y métodos.
Basado en la estructura del CSV proporcionado.
"""

class Pokemon:
    """Clase que representa un Pokémon con todas sus características."""
    
    def __init__(self, pokedex_number: int, name: str, german_name: str, japanese_name: str, 
                 generation: int, status: str, species: str, type1: str, type2: str, 
                 height: float, weight: float, ability1: str, ability2: str, 
                 hidden_ability: str, hp: int, attack: int, defense: int, 
                 sp_attack: int, sp_defense: int, speed: int, catch_rate: int, 
                 base_friendship: int, base_experience: int, growth_rate: str, 
                 against_types: dict):
        """
        Inicializa un Pokémon con todos sus atributos.
        
        """
        # Identificación
        self.pokedex_number = pokedex_number
        self.name = name
        self.german_name = german_name
        self.japanese_name = japanese_name
        self.generation = generation
        
        # Clasificación
        self.status = status
        self.species = species
        
        # Tipos
        self.type1 = type1
        self.type2 = type2 if type2 and type2 != "None" else None
        
        # Características físicas
        self.height = height
        self.weight = weight
        
        # Habilidades
        self.ability1 = ability1
        self.ability2 = ability2
        self.hidden_ability = hidden_ability
        
        # Estadísticas de combate
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
        self.current_hp = hp  # Para seguimiento durante batallas
        
        # Datos de captura/entrenamiento
        self.catch_rate = catch_rate
        self.base_friendship = base_friendship
        self.base_experience = base_experience
        self.growth_rate = growth_rate
        
        # Efectividad contra tipos
        self.against_types = against_types
    
    def __str__(self) -> str:
        """Representación en string del Pokémon."""
        types = f"{self.type1}/{self.type2}" if self.type2 else self.type1
        return f"#{self.pokedex_number:03d} {self.name} ({types}) - HP: {self.hp}"
    
    def receive_damage(self, damage: int) -> bool:
        """
        Reduce los puntos de salud del Pokémon.
        
        """
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp == 0
    
    def get_effectiveness(self, move_type: str) -> float:
        """
        Obtiene la efectividad de un tipo de ataque contra este Pokémon.
        
        """
        return self.against_types.get(move_type.lower(), 1.0)
    
    def reset_hp(self) -> None:
        """Restablece los puntos de salud al máximo."""
        self.current_hp = self.hp