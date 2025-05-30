from typing import Optional
from .manager import PokemonManager
from .battle import BattleSystem
from .pokemon import Pokemon

##Módulo de interfaz de línea de comandos para el sistema de batallas Pokémon.
class PokemonCLI:
    """Clase que maneja la interfaz de usuario por línea de comandos."""
    
    def __init__(self):
        """Inicializa el CLI con un PokemonManager."""
        self.manager = PokemonManager()
    
    def start(self) -> None:
        """Inicia la interfaz de usuario."""
        print("\n¡Bienvenido al Sistema de Batallas Pokémon!")
        print(f"Cargados {len(self.manager.list_pokemons())} Pokémon.\n")
        
        while True:
            self._display_main_menu()
            choice = input("\nSeleccione una opción (1-7): ")
            
            if choice == '1':
                self._list_pokemons()
            elif choice == '2':
                self._show_pokemon_details()
            elif choice == '3':
                self._add_pokemon()
            elif choice == '4':
                self._update_pokemon()
            elif choice == '5':
                self._delete_pokemon()
            elif choice == '6':
                self._battle_pokemons()
            elif choice == '7':
                print("\n¡Gracias por usar el Sistema de Batallas Pokémon!")
                break
            else:
                print("\nOpción no válida. Por favor seleccione 1-7.")
    
    def _display_main_menu(self) -> None:
        """Muestra el menú principal."""
        print("\n--- Menú Principal ---")
        print("1. Listar todos los Pokémons")
        print("2. Ver detalles de un Pokémon")
        print("3. Agregar nuevo Pokémon")
        print("4. Modificar Pokémon existente")
        print("5. Eliminar Pokémon")
        print("6. Realizar una batalla")
        print("7. Salir")
    
    def _list_pokemons(self) -> None:
        """Lista todos los Pokémon disponibles."""
        print("\n--- Pokémons Disponibles ---")
        for i, name in enumerate(self.manager.list_pokemons(), 1):
            pokemon = self.manager.get_pokemon(name)
            print(f"{i:3d}. #{pokemon.pokedex_number:03d} {pokemon.name}")
        print(f"\nTotal: {len(self.manager.list_pokemons())} Pokémons")
    
    def _show_pokemon_details(self) -> None:
        """Muestra los detalles de un Pokémon específico."""
        name = input("\nIngrese el nombre del Pokémon: ")
        pokemon = self.manager.get_pokemon(name)
        
        if not pokemon:
            print("\n¡Pokémon no encontrado!")
            return
        
        print("\n--- Detalles del Pokémon ---")
        print(f"ID: #{pokemon.pokedex_number}")
        print(f"Nombre: {pokemon.name} (Alemán: {pokemon.german_name}, Japonés: {pokemon.japanese_name})")
        print(f"Generación: {pokemon.generation} - Especie: {pokemon.species}")
        print(f"Tipos: {pokemon.type1}" + (f"/{pokemon.type2}" if pokemon.type2 else ""))
        print(f"Altura: {pokemon.height}m - Peso: {pokemon.weight}kg")
        
        print("\nHabilidades:")
        print(f"- {pokemon.ability1}")
        if pokemon.ability2:
            print(f"- {pokemon.ability2}")
        if pokemon.hidden_ability:
            print(f"- Habilidad Oculta: {pokemon.hidden_ability}")
        
        print("\nEstadísticas:")
        print(f"HP: {pokemon.hp}")
        print(f"Ataque: {pokemon.attack}")
        print(f"Defensa: {pokemon.defense}")
        print(f"Ataque Especial: {pokemon.sp_attack}")
        print(f"Defensa Especial: {pokemon.sp_defense}")
        print(f"Velocidad: {pokemon.speed}")
        
        print("\nDatos de Entrenamiento:")
        print(f"Ratio de Captura: {pokemon.catch_rate}")
        print(f"Amistad Base: {pokemon.base_friendship}")
        print(f"Experiencia Base: {pokemon.base_experience}")
        print(f"Ratio de Crecimiento: {pokemon.growth_rate}")
    
    def _add_pokemon(self) -> None:
        """Interfaz para agregar un nuevo Pokémon."""
        print("\n--- Agregar Nuevo Pokémon ---")
        print("Complete los datos del nuevo Pokémon (deje vacío para cancelar):")
        
        name = input("Nombre: ").strip()
        if not name:
            print("\nOperación cancelada.")
            return
        
        if self.manager.get_pokemon(name):
            print("\n¡Ya existe un Pokémon con ese nombre!")
            return
        
        try:
            # Datos básicos
            pokedex_number = int(input("Número en la Pokédex: "))
            type1 = input("Tipo primario: ").strip().capitalize()
            type2 = input("Tipo secundario (opcional): ").strip().capitalize() or None
            
            # Estadísticas
            hp = int(input("HP: "))
            attack = int(input("Ataque: "))
            defense = int(input("Defensa: "))
            sp_attack = int(input("Ataque Especial: "))
            sp_defense = int(input("Defensa Especial: "))
            speed = int(input("Velocidad: "))
            
            # Crear Pokémon (simplificado para el ejemplo)
            # En una implementación real, pediríamos todos los campos
            pokemon = Pokemon(
                pokedex_number=pokedex_number,
                name=name,
                german_name="",
                japanese_name="",
                generation=1,
                status="Normal",
                species="Custom Pokémon",
                type1=type1,
                type2=type2,
                height=1.0,
                weight=1.0,
                ability1="Custom Ability",
                ability2=None,
                hidden_ability=None,
                hp=hp,
                attack=attack,
                defense=defense,
                sp_attack=sp_attack,
                sp_defense=sp_defense,
                speed=speed,
                catch_rate=45,
                base_friendship=50,
                base_experience=64,
                growth_rate="Medium Slow",
                against_types={t: 1.0 for t in ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 
                                              'fight', 'poison', 'ground', 'flying', 'psychic', 'bug',
                                              'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']}
            )
            
            if self.manager.add_pokemon(pokemon):
                print(f"\n¡{name} ha sido agregado exitosamente!")
            else:
                print("\nError al agregar el Pokémon.")
                
        except ValueError:
            print("\nError: Los valores numéricos deben ser enteros.")
    
    def _update_pokemon(self) -> None:
        """Interfaz para modificar un Pokémon existente."""
        name = input("\nIngrese el nombre del Pokémon a modificar: ")
        pokemon = self.manager.get_pokemon(name)
        
        if not pokemon:
            print("\n¡Pokémon no encontrado!")
            return
        
        print(f"\nModificando a {pokemon.name} (#{pokemon.pokedex_number})")
        print("Ingrese los nuevos valores (deje vacío para mantener el actual):")
        
        try:
            updates = {}
            
            # Ejemplo de campos modificables
            new_hp = input(f"HP [{pokemon.hp}]: ").strip()
            if new_hp:
                updates['hp'] = int(new_hp)
                
            new_attack = input(f"Ataque [{pokemon.attack}]: ").strip()
            if new_attack:
                updates['attack'] = int(new_attack)
                
            new_defense = input(f"Defensa [{pokemon.defense}]: ").strip()
            if new_defense:
                updates['defense'] = int(new_defense)
            
            if updates and self.manager.update_pokemon(name, **updates):
                print(f"\n¡{pokemon.name} ha sido actualizado!")
            else:
                print("\nNo se realizaron cambios.")
                
        except ValueError:
            print("\nError: Los valores deben ser números enteros.")
    
    def _delete_pokemon(self) -> None:
        """Interfaz para eliminar un Pokémon."""
        name = input("\nIngrese el nombre del Pokémon a eliminar: ")
        
        if self.manager.delete_pokemon(name):
            print(f"\n¡{name} ha sido eliminado exitosamente!")
        else:
            print("\n¡Pokémon no encontrado!")
    
    def _battle_pokemons(self) -> None:
        """Interfaz para realizar una batalla entre Pokémon."""
        print("\n--- Batalla Pokémon ---")
        print("Seleccione el modo de batalla:")
        print("1. Batalla manual (elegir Pokémon)")
        print("2. Batalla aleatoria")
        
        mode = input("Seleccione (1-2): ").strip()
        
        if mode == '1':
            self._manual_battle()
        elif mode == '2':
            self._random_battle()
        else:
            print("\nOpción no válida.")
    
    def _manual_battle(self) -> None:
        """Batalla donde el usuario elige los Pokémon."""
        self._list_pokemons()
        
        pokemon1 = None
        while not pokemon1:
            name = input("\nNombre del primer Pokémon: ").strip()
            pokemon1 = self.manager.get_pokemon(name)
            if not pokemon1:
                print("¡Pokémon no encontrado! Intente nuevamente.")
        
        pokemon2 = None
        while not pokemon2:
            name = input("Nombre del segundo Pokémon: ").strip()
            pokemon2 = self.manager.get_pokemon(name)
            if not pokemon2:
                print("¡Pokémon no encontrado! Intente nuevamente.")
            elif pokemon2.name == pokemon1.name:
                print("¡No puede elegir el mismo Pokémon! Intente nuevamente.")
                pokemon2 = None
        
        self._start_battle(pokemon1, pokemon2)
    
    def _random_battle(self) -> None:
        """Batalla con Pokémon seleccionados aleatoriamente."""
        pokemon1 = self.manager.get_random_pokemon()
        pokemon2 = self.manager.get_random_pokemon()
        
        # Asegurarse de que sean diferentes
        while pokemon2.name == pokemon1.name:
            pokemon2 = self.manager.get_random_pokemon()
        
        print(f"\n¡Batalla aleatoria entre {pokemon1.name} y {pokemon2.name}!")
        self._start_battle(pokemon1, pokemon2)
    
    def _start_battle(self, pokemon1: Pokemon, pokemon2: Pokemon) -> None:
        """Inicia y muestra una batalla main dos Pokémon."""
        input("\nPresione Enter para comenzar la batalla...")
        
        winner, battle_log = BattleSystem.battle(pokemon1, pokemon2)
        
        print("\n--- Resumen de la Batalla ---")
        for line in battle_log:
            print(line)
        
        print(f"\n¡El ganador es {winner.name} (#{winner.pokedex_number})!")
        input("\nPresione Enter para continuar...")


def main():
    """Punto de entrada principal para el comando pokemon-battle"""
    cli = PokemonCLI()
    cli.start()

if __name__ == "__main__":
    main()