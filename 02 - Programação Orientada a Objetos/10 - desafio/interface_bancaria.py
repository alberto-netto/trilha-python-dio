import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Esconde a janela do terminal
if sys.platform == 'win32':
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.CloseHandle(whnd)

def resource_path(relative_path):
    """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
    try:
        # PyInstaller cria um temp folder e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Importa as classes do desafio_v1
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from desafio_v1 import (
    PessoaFisica,
    ContaCorrente,
    Deposito,
    Saque
)

from datetime import datetime

class InterfaceBancaria:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu_Banco")
        self.root.geometry("800x600")
        
        # Centralizar a janela principal
        self.centralizar_janela(self.root)
        
        # Inicialização das listas de clientes e contas
        self.clientes = []
        self.contas = []
        
        # Configuração do estilo
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        self.titulo = ttk.Label(self.main_frame, text="Meu_Banco", font=("Helvetica", 16, "bold"))
        self.titulo.grid(row=0, column=0, columnspan=2, pady=20)
        
        # Frame para operações
        self.operacoes_frame = ttk.LabelFrame(self.main_frame, text="Operações", padding="10")
        self.operacoes_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Botões de operações
        ttk.Button(self.operacoes_frame, text="Novo Cliente", command=self.criar_cliente).grid(row=0, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(self.operacoes_frame, text="Nova Conta", command=self.criar_conta).grid(row=1, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(self.operacoes_frame, text="Depositar", command=self.depositar).grid(row=2, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(self.operacoes_frame, text="Sacar", command=self.sacar).grid(row=3, column=0, pady=5, padx=5, sticky="ew")
        ttk.Button(self.operacoes_frame, text="Extrato", command=self.exibir_extrato).grid(row=4, column=0, pady=5, padx=5, sticky="ew")
        
        # Frame para listagem
        self.listagem_frame = ttk.LabelFrame(self.main_frame, text="Listagem", padding="10")
        self.listagem_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Treeview para listar contas
        self.tree = ttk.Treeview(self.listagem_frame, columns=("Agência", "Conta", "Titular"), show="headings")
        self.tree.heading("Agência", text="Agência")
        self.tree.heading("Conta", text="Conta")
        self.tree.heading("Titular", text="Titular")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar para a Treeview
        scrollbar = ttk.Scrollbar(self.listagem_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Configuração do grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        self.listagem_frame.columnconfigure(0, weight=1)
        self.listagem_frame.rowconfigure(0, weight=1)

    def centralizar_janela(self, janela):
        janela.update_idletasks()
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        x = (janela.winfo_screenwidth() // 2) - (largura // 2)
        y = (janela.winfo_screenheight() // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_cliente(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Novo Cliente")
        dialog.geometry("400x300")
        self.centralizar_janela(dialog)
        
        # Campos de entrada
        ttk.Label(dialog, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        nome_entry = ttk.Entry(dialog)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Data de Nascimento:").grid(row=1, column=0, padx=5, pady=5)
        data_entry = ttk.Entry(dialog)
        data_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="CPF:").grid(row=2, column=0, padx=5, pady=5)
        cpf_entry = ttk.Entry(dialog)
        cpf_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Endereço:").grid(row=3, column=0, padx=5, pady=5)
        endereco_entry = ttk.Entry(dialog)
        endereco_entry.grid(row=3, column=1, padx=5, pady=5)
        
        def salvar():
            try:
                cliente = PessoaFisica(
                    nome=nome_entry.get(),
                    data_nascimento=data_entry.get(),
                    cpf=cpf_entry.get(),
                    endereco=endereco_entry.get()
                )
                self.clientes.append(cliente)
                messagebox.showinfo("Sucesso", "Cliente criado com sucesso!")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar cliente: {str(e)}")
        
        ttk.Button(dialog, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2, pady=20)

    def criar_conta(self):
        # Criar janela de diálogo para solicitar CPF
        dialog = tk.Toplevel(self.root)
        dialog.title("Criar Nova Conta")
        dialog.geometry("300x150")
        
        # Centralizar a janela
        self.centralizar_janela(dialog)
        dialog.grab_set()
        
        # Frame para o conteúdo
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Label e Entry para CPF
        ttk.Label(frame, text="Informe o CPF do cliente:").grid(row=0, column=0, pady=10)
        cpf_entry = ttk.Entry(frame)
        cpf_entry.grid(row=1, column=0, pady=5)
        
        def criar():
            cpf = cpf_entry.get()
            cliente = self.filtrar_cliente(cpf)
            
            if not cliente:
                messagebox.showerror("Erro", "Cliente não encontrado!")
                return
            
            try:
                numero_conta = len(self.contas) + 1
                conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
                self.contas.append(conta)
                cliente.contas.append(conta)
                
                # Atualizar Treeview
                self.tree.insert("", "end", values=(conta.agencia, conta.numero, conta.cliente.nome))
                
                # Fechar a janela de diálogo
                dialog.destroy()
                
                # Criar janela com os dados da conta
                info_dialog = tk.Toplevel(self.root)
                info_dialog.title("Conta Criada")
                info_dialog.geometry("300x200")
                
                # Centralizar a janela
                self.centralizar_janela(info_dialog)
                info_dialog.grab_set()
                
                # Frame para as informações
                info_frame = ttk.Frame(info_dialog, padding="20")
                info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
                
                # Exibir informações da conta
                ttk.Label(info_frame, text="Conta criada com sucesso!", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=10)
                ttk.Label(info_frame, text=f"Titular: {conta.cliente.nome}").grid(row=1, column=0, pady=5)
                ttk.Label(info_frame, text=f"Agência: {conta.agencia}").grid(row=2, column=0, pady=5)
                ttk.Label(info_frame, text=f"Conta: {conta.numero}").grid(row=3, column=0, pady=5)
                
                ttk.Button(info_frame, text="OK", command=info_dialog.destroy).grid(row=4, column=0, pady=20)
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar conta: {str(e)}")
        
        ttk.Button(frame, text="Criar Conta", command=criar).grid(row=2, column=0, pady=20)

    def criar_dialog_cpf(self, titulo, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("300x150")
        self.centralizar_janela(dialog)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Informe o CPF do cliente:").grid(row=0, column=0, pady=10)
        cpf_entry = ttk.Entry(frame)
        cpf_entry.grid(row=1, column=0, pady=5)
        
        def confirmar():
            cpf = cpf_entry.get()
            cliente = self.filtrar_cliente(cpf)
            if not cliente:
                messagebox.showerror("Erro", "Cliente não encontrado!")
                return
            callback(cliente)
            dialog.destroy()
        
        ttk.Button(frame, text="Confirmar", command=confirmar).grid(row=2, column=0, pady=20)

    def criar_dialog_valor(self, titulo, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("300x150")
        self.centralizar_janela(dialog)
        
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Informe o valor:").grid(row=0, column=0, pady=10)
        valor_entry = ttk.Entry(frame)
        valor_entry.grid(row=1, column=0, pady=5)
        
        def confirmar():
            try:
                valor = float(valor_entry.get())
                callback(valor)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        ttk.Button(frame, text="Confirmar", command=confirmar).grid(row=2, column=0, pady=20)

    def depositar(self):
        def operacao_deposito(cliente):
            def executar_deposito(valor):
                try:
                    conta = self.recuperar_conta_cliente(cliente)
                    if not conta:
                        messagebox.showerror("Erro", "Cliente não possui conta!")
                        return
                    
                    transacao = Deposito(valor)
                    cliente.realizar_transacao(conta, transacao)
                    messagebox.showinfo("Sucesso", "Depósito realizado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao realizar depósito: {str(e)}")
            
            self.criar_dialog_valor("Depósito", executar_deposito)
        
        self.criar_dialog_cpf("Depósito", operacao_deposito)

    def sacar(self):
        def operacao_saque(cliente):
            def executar_saque(valor):
                try:
                    conta = self.recuperar_conta_cliente(cliente)
                    if not conta:
                        messagebox.showerror("Erro", "Cliente não possui conta!")
                        return
                    
                    transacao = Saque(valor)
                    cliente.realizar_transacao(conta, transacao)
                    messagebox.showinfo("Sucesso", "Saque realizado com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao realizar saque: {str(e)}")
            
            self.criar_dialog_valor("Saque", executar_saque)
        
        self.criar_dialog_cpf("Saque", operacao_saque)

    def exibir_extrato(self):
        def mostrar_extrato(cliente):
            conta = self.recuperar_conta_cliente(cliente)
            if not conta:
                messagebox.showerror("Erro", "Cliente não possui conta!")
                return
            
            extrato_window = tk.Toplevel(self.root)
            extrato_window.title("Extrato")
            extrato_window.geometry("400x500")
            
            extrato_text = tk.Text(extrato_window, wrap=tk.WORD)
            extrato_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            extrato_text.insert(tk.END, "================ EXTRATO ================\n\n")
            
            transacoes = conta.historico.transacoes
            if not transacoes:
                extrato_text.insert(tk.END, "Não foram realizadas movimentações.\n")
            else:
                for transacao in transacoes:
                    extrato_text.insert(tk.END, f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}\n")
            
            extrato_text.insert(tk.END, f"\nSaldo:\t\tR$ {conta.saldo:.2f}\n")
            extrato_text.insert(tk.END, "==========================================")
            
            extrato_text.config(state=tk.DISABLED)
        
        self.criar_dialog_cpf("Extrato", mostrar_extrato)

    def filtrar_cliente(self, cpf):
        clientes_filtrados = [cliente for cliente in self.clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None

    def recuperar_conta_cliente(self, cliente):
        if not cliente.contas:
            return None
        return cliente.contas[0]

def main():
    root = tk.Tk()
    app = InterfaceBancaria(root)
    root.mainloop()
    sys.exit()

if __name__ == "__main__":
    main() 