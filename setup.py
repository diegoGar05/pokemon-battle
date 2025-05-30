from setuptools import setup, find_packages

setup(
    name="pokemon-battle",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'pokemon-battle=pokemon_battle.cli:main',
        ],
    },
    package_data={
        'pokemon_battle': ['pokemon_battle\data\pokemon.csv'],
    },
    author="Diego Armando Garcia Castañeda",
    description="Sistema de batallas Pokémon con datos completos de la Pokédex",
    python_requires='>=3.6',
)
