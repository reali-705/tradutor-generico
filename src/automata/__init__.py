"""
Este arquivo __init__.py transforma o diretório 'automata' em um pacote Python.

Ele também "promove" as classes principais dos módulos internos para o nível do pacote,
facilitando as importações em outras partes do projeto.

Com este arquivo, em vez de:
from src.automata.transdutor_finito import TransdutorFinito

Podemos usar a importação mais curta e limpa:
from src.automata import TransdutorFinito
"""

from .transdutor_finito import TransdutorFinito
from .transdutor_pilha import *
