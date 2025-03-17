import PyInstaller.__main__
import os

# Obtém o diretório atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# Configuração do PyInstaller
PyInstaller.__main__.run([
    'interface_bancaria.py',
    '--onefile',
    '--windowed',
    '--name=Meu_Banco',
    '--add-data=desafio_v1.py;.',
    '--clean',
    '--noconfirm',
    f'--distpath={os.path.join(diretorio_atual, "dist")}',
    f'--workpath={os.path.join(diretorio_atual, "build")}',
    f'--specpath={diretorio_atual}',
]) 