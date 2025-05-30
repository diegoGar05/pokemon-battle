import pandas as pd
import os
from typing import Dict, Optional, List
from .pokemon import Pokemon

class PokemonManager:
    """Clase que gestiona la colección de Pokémon y carga los datos del CSV."""
    
    def __init__(self, csv_path=None):
        self.pokemons: Dict[str, Pokemon] = {}  # Inicialización explícita
        # Obtiene la ruta absoluta al archivo CSV
        if csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(base_dir, 'pokemon_battle', 'data', 'pokemon.csv')
        self._load_from_csv(csv_path)
    
    def _load_from_csv(self, csv_path: str) -> None:
        """Carga los datos de Pokémon desde un archivo CSV."""
        try:
            print(f"Intentando cargar CSV desde: {csv_path}")  
            print(f"El archivo existe: {os.path.exists(csv_path)}") 
            
            if not os.path.exists(csv_path):
                raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
            
            data = pd.read_csv(csv_path)
            
            # Limpiar diccionario existente
            self.pokemons = {}
            
            for _, row in data.iterrows():
                # Preparamos el diccionario de efectividades
                against_types = {
                    'normal': row['against_normal'],
                    'fire': row['against_fire'],
                    'water': row['against_water'],
                    'electric': row['against_electric'],
                    'grass': row['against_grass'],
                    'ice': row['against_ice'],
                    'fight': row['against_fight'],
                    'poison': row['against_poison'],
                    'ground': row['against_ground'],
                    'flying': row['against_flying'],
                    'psychic': row['against_psychic'],
                    'bug': row['against_bug'],
                    'rock': row['against_rock'],
                    'ghost': row['against_ghost'],
                    'dragon': row['against_dragon'],
                    'dark': row['against_dark'],
                    'steel': row['against_steel'],
                    'fairy': row['against_fairy']
                }
                
                # Creamos el Pokémon
                pokemon = Pokemon(
                    pokedex_number=row['pokedex_number'],
                    name=row['name'],
                    german_name=row['german_name'],
                    japanese_name=row['japanese_name'],
                    generation=row['generation'],
                    status=row['status'],
                    species=row['species'],
                    type1=row['type_1'],
                    type2=row['type_2'] if pd.notna(row['type_2']) else None,
                    height=row['height_m'],
                    weight=row['weight_kg'],
                    ability1=row['ability_1'],
                    ability2=row['ability_2'] if pd.notna(row['ability_2']) else None,
                    hidden_ability=row['ability_hidden'] if pd.notna(row['ability_hidden']) else None,
                    hp=row['hp'],
                    attack=row['attack'],
                    defense=row['defense'],
                    sp_attack=row['sp_attack'],
                    sp_defense=row['sp_defense'],
                    speed=row['speed'],
                    catch_rate=row['catch_rate'],
                    base_friendship=row['base_friendship'],
                    base_experience=row['base_experience'],
                    growth_rate=row['growth_rate'],
                    against_types=against_types
                )
                
                self.pokemons[pokemon.name.lower()] = pokemon
                
        except FileNotFoundError as e:
            print(f"Error crítico: {str(e)}")
            self.pokemons = {}  # Asegurar diccionario vacío
            raise
        except Exception as e:
            print(f"Error procesando CSV: {str(e)}")
            self.pokemons = {}  # Asegurar diccionario vacío
            raise ValueError(f"Error al procesar el CSV: {str(e)}")
        
    def get_pokemon(self, name: str) -> Optional[Pokemon]:
        """
        Obtiene un Pokémon por nombre (case insensitive).
            
        """
        return self.pokemons.get(name.lower())
    
    def _save_to_csv(self, csv_path: str = None) -> None:
        """Guarda todos los Pokémon en el archivo CSV"""
        if csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(base_dir, 'pokemon_battle', 'data', 'pokemon.csv')
        
        try:
            # Convertir todos los Pokémon a diccionarios
            pokemon_data = []
            for pokemon in self.pokemons.values():
                pokemon_dict = {
                    'pokedex_number': pokemon.pokedex_number,
                    'name': pokemon.name,
                    'german_name': pokemon.german_name,
                    'japanese_name': pokemon.japanese_name,
                    'generation': pokemon.generation,
                    'status': pokemon.status,
                    'species': pokemon.species,
                    'type_1': pokemon.type1,
                    'type_2': pokemon.type2 if pokemon.type2 else None,
                    'height_m': pokemon.height,
                    'weight_kg': pokemon.weight,
                    'ability_1': pokemon.ability1,
                    'ability_2': pokemon.ability2 if hasattr(pokemon, 'ability2') and pokemon.ability2 else None,
                    'ability_hidden': pokemon.hidden_ability if hasattr(pokemon, 'hidden_ability') and pokemon.hidden_ability else None,
                    'hp': pokemon.hp,
                    'attack': pokemon.attack,
                    'defense': pokemon.defense,
                    'sp_attack': pokemon.sp_attack,
                    'sp_defense': pokemon.sp_defense,
                    'speed': pokemon.speed,
                    'catch_rate': pokemon.catch_rate,
                    'base_friendship': pokemon.base_friendship,
                    'base_experience': pokemon.base_experience,
                    'growth_rate': pokemon.growth_rate,
                    **pokemon.against_types 
                }
                pokemon_data.append(pokemon_dict)
            
            # Crear DataFrame y guardar
            df = pd.DataFrame(pokemon_data)
            df.to_csv(csv_path, index=False)
            
        except Exception as e:
            print(f"Error al guardar el CSV: {str(e)}")
            raise
        
    def add_pokemon(self, pokemon: Pokemon) -> bool:
        """Agrega nuevo Pokémon y guarda en CSV"""
        if pokemon.name.lower() in self.pokemons:
            return False
            
        self.pokemons[pokemon.name.lower()] = pokemon
        self._save_to_csv()  # Guarda los cambios
        return True

    def update_pokemon(self, name: str, **kwargs) -> bool:
        """Actualiza Pokémon y guarda en CSV"""
        pokemon = self.get_pokemon(name)
        if not pokemon:
            return False
            
        for attr, value in kwargs.items():
            if hasattr(pokemon, attr):
                setattr(pokemon, attr, value)
        
        self._save_to_csv()  # Guarda los cambios
        return True

    def delete_pokemon(self, name: str) -> bool:
        """Elimina Pokémon y guarda en CSV"""
        if name.lower() not in self.pokemons:
            return False
            
        del self.pokemons[name.lower()]
        self._save_to_csv()  # Guarda los cambios
        return True
        
    def list_pokemons(self) -> List[str]:
        """
        Lista los nombres de todos los Pokémon disponibles.
            
        """
        return sorted(self.pokemons.keys(), key=lambda x: self.pokemons[x].pokedex_number)
        
    def get_random_pokemon(self) -> Pokemon:
        """
        Obtiene un Pokémon aleatorio de la colección.
            
        """
        import random
        return random.choice(list(self.pokemons.values()))