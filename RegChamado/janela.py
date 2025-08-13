# janela.py

import tkinter as tk
from tkinter import messagebox
import threading

# Importa as funções de lógica do outro arquivo
# O 'as robo' cria um apelido para facilitar a chamada das funções
import automacao_hospital as robo

def iniciar_navegador_thread(status_label, botoes):
    """Chama a função de login em uma thread para não travar a interface."""
    def run():
        # A função de login agora está no módulo 'robo'
        robo.iniciar_navegador(status_label, botoes)
    
    threading.Thread(target=run, daemon=True).start()

def preencher_formulario_thread(status_label):
    """Chama a função de preenchimento em uma thread."""
    threading.Thread(target=lambda: robo.preencher_formulario(status_label), daemon=True).start()

def reiniciar_processo_thread(status_label):
    """Chama a função de reinício em uma thread."""
    threading.Thread(target=lambda: robo.reiniciar_processo(status_label), daemon=True).start()

def criar_interface():
    root = tk.Tk()
    root.title("Automador de Chamados")
    root.geometry("350x220")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    botoes = {}

    botoes['iniciar'] = tk.Button(main_frame, text="1. Iniciar Navegador e Login", command=lambda: iniciar_navegador_thread(status_label, botoes), font=("Segoe UI", 10, "bold"), bg="#0078D7", fg="white", relief="flat", padx=10, pady=5)
    botoes['iniciar'].pack(pady=5, ipady=4, fill="x")

    botoes['preencher'] = tk.Button(main_frame, text="2. Preencher Formulário", command=lambda: preencher_formulario_thread(status_label), font=("Segoe UI", 10, "bold"), bg="#2a75bb", fg="white", relief="flat", padx=10, pady=5, state=tk.DISABLED)
    botoes['preencher'].pack(pady=5, ipady=4, fill="x")
    
    botoes['reiniciar'] = tk.Button(main_frame, text="3. Iniciar Novo Chamado", command=lambda: reiniciar_processo_thread(status_label), font=("Segoe UI", 10, "bold"), bg="#107C10", fg="white", relief="flat", padx=10, pady=5, state=tk.DISABLED)
    botoes['reiniciar'].pack(pady=5, ipady=4, fill="x")
    
    status_label = tk.Label(main_frame, text="Status: Aguardando início...", bd=1, relief="sunken", anchor="w", padx=5)
    status_label.pack(side="bottom", fill="x", pady=(10, 0))
    
    root.mainloop()

# Este é o ponto de entrada do programa
if __name__ == "__main__":
    criar_interface()
