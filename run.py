
import sys
import os

# Añadir el directorio raíz al path para que se pueda importar utils correctamente
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from bot.main import run_bot

if __name__ == "__main__":
    run_bot()
