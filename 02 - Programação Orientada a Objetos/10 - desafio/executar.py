import os
import sys
import subprocess
from tkinter import messagebox

def executar_programa():
    try:
        # Obtém o diretório atual
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        
        # Esconde a janela do terminal
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            # Executa o programa principal
            subprocess.Popen(['python', 'interface_bancaria.py'],
                           startupinfo=startupinfo,
                           creationflags=subprocess.CREATE_NO_WINDOW,
                           cwd=diretorio_atual)
        else:
            subprocess.Popen(['python3', 'interface_bancaria.py'],
                           cwd=diretorio_atual)
        
        # Fecha o executável
        sys.exit(0)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar o programa: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    executar_programa() 