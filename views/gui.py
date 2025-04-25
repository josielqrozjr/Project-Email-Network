"""
Interface gráfica usando tkinter para o projeto de Redes de Email
Tema elegante com cores neutras e sofisticadas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font, Entry, StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import os
import sys
import time

# Adicionar o diretório raiz ao path para importações corretas
# quando executado diretamente
if __name__ == "__main__":
    # Adiciona o diretório pai ao path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.grafo import Grafo
from controller.one_controller import gerar_grafo
from controller.two_controller import (
    get_numero_vertices, 
    get_numero_arestas, 
    get_vertices_isolados, 
    get_vertices_com_loops,
    get_maiores_graus_entrada,
    get_maiores_graus_saida,
    grafo
)
# Importando os novos controllers
from controller.third_controller import grafo_euleriano_direcionado
from controller.four_controller import vertices_ate_distancia
from controller.five_controller import calcular_diametro, calcular_diametro_paralelo

class GUI:
    def __init__(self, root=None):
        # Cores do tema
        self.cores = {
            "bg_principal": "#F5F5F5",  # Cinza muito claro
            "bg_frame": "#FFFFFF",      # Branco
            "bg_text": "#FAFAFA",       # Branco ligeiramente acinzentado
            "texto": "#2E2E2E",         # Cinza escuro
            "titulo": "#1A1A1A",        # Quase preto
            "destaque": "#3F51B5",      # Azul índigo
            "destaque_hover": "#303F9F", # Azul índigo mais escuro
            "botao_texto": "#FFFFFF",   # Branco
            "borda": "#E0E0E0",         # Cinza claro
            "header_bg": "#3F51B5",     # Cor de fundo do header
            "header_text": "#FFFFFF"    # Cor de texto do header
        }
        
        if root is None:
            self.root = tk.Tk()
            self.root.title("Análise de Rede de Emails - Enron")
            self.root.geometry("1200x800")
            self.root.configure(bg=self.cores["bg_principal"])
            # Ícone para a aplicação (se tiver um disponível)
            # self.root.iconbitmap("caminho/para/icone.ico")
        else:
            self.root = root
            self.root.configure(bg=self.cores["bg_principal"])
            
        # Configuração de estilo
        self.configurar_estilo()
        self.criar_widgets()
        
    def configurar_estilo(self):
        # Configurar estilo do ttk
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')  # Usando clam como base para personalização
        
        # Configurando fonte principal
        fonte_padrao = font.nametofont("TkDefaultFont")
        fonte_padrao.configure(family="Segoe UI", size=10)
        
        # Estilo para os botões (bordas arredondadas)
        self.estilo.configure('TButton', 
                          background=self.cores["destaque"],
                          foreground=self.cores["botao_texto"],
                          font=("Segoe UI", 10, "bold"),
                          borderwidth=0,
                          focusthickness=3,
                          focuscolor=self.cores["destaque"],
                          relief="flat")
        
        self.estilo.map('TButton',
                    background=[('active', self.cores["destaque_hover"])],
                    relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Estilo para os frames
        self.estilo.configure('TFrame', background=self.cores["bg_frame"])
        
        # Estilo para os frames arredondados
        self.estilo.configure('Rounded.TFrame', 
                          background=self.cores["bg_frame"])
        
        # Estilo para os notebooks (abas)
        self.estilo.configure('TNotebook', background=self.cores["bg_principal"])
        self.estilo.configure('TNotebook.Tab', 
                          background=self.cores["bg_frame"],
                          foreground=self.cores["texto"],
                          padding=[12, 6],
                          font=("Segoe UI", 10))
        
        self.estilo.map('TNotebook.Tab',
                    background=[('selected', self.cores["destaque"])],
                    foreground=[('selected', self.cores["botao_texto"])])
        
        # Estilo para os LabelFrames (bordas arredondadas)
        self.estilo.configure('Rounded.TLabelframe', 
                          background=self.cores["bg_frame"],
                          foreground=self.cores["texto"],
                          borderwidth=2,
                          relief="groove")
        
        self.estilo.configure('Rounded.TLabelframe.Label', 
                          background=self.cores["bg_frame"],
                          foreground=self.cores["titulo"],
                          font=("Segoe UI", 11, "bold"))
                          
        # Estilo para o header
        self.estilo.configure('Header.TFrame',
                          background=self.cores["header_bg"])
        
        # Estilo para painel vertical
        self.estilo.configure('TSeparator', 
                          background=self.cores["borda"])
    
    def criar_widgets(self):
        # Frame principal para centralizar o conteúdo
        self.frame_principal = ttk.Frame(self.root, style='TFrame')
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header da aplicação
        self.header_frame = ttk.Frame(self.frame_principal, style='Header.TFrame')
        self.header_frame.pack(fill='x', pady=(0, 20))
        
        # Conteúdo do header
        titulo_label = tk.Label(self.header_frame, 
                             text="Análise de Rede de Emails",
                             font=("Segoe UI", 18, "bold"),
                             background=self.cores["header_bg"],
                             foreground=self.cores["header_text"])
        titulo_label.pack(side='left', padx=20, pady=15)
        
        # Subtítulo no header
        subtitulo_label = tk.Label(self.header_frame, 
                                text="Dataset Enron | Visualizador de Grafo de Comunicações",
                                font=("Segoe UI", 11),
                                background=self.cores["header_bg"],
                                foreground=self.cores["header_text"])
        subtitulo_label.pack(side='left', padx=10, pady=15)
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba Principal
        self.tab_principal = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_principal, text="Principal")
        
        # Aba de Informações
        self.tab_info = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_info, text="Informações do Grafo")
        
        # Aba de Visualização
        self.tab_visualizacao = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_visualizacao, text="Visualização")
        
        # Novas abas para os novos controllers
        # Aba para o controller 3 - Verificação de grafo euleriano
        self.tab_euleriano = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_euleriano, text="Grafo Euleriano")
        
        # Aba para o controller 4 - Distância entre vértices
        self.tab_distancia = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_distancia, text="Distância entre Vértices")
        
        # Aba para o controller 5 - Diâmetro do grafo
        self.tab_diametro = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(self.tab_diametro, text="Diâmetro do Grafo")
        
        # Conteúdo da Aba Principal
        # Frame para as ações
        self.frame_acoes = ttk.LabelFrame(self.tab_principal, text="Ações", style='Rounded.TLabelframe')
        self.frame_acoes.pack(fill='x', expand=False, padx=15, pady=15)
        
        # Container para os botões
        self.frame_botoes = ttk.Frame(self.frame_acoes, style='TFrame')
        self.frame_botoes.pack(pady=15)
        
        # Função para criar botões arredondados personalizados
        def criar_botao_arredondado(parent, texto, comando, largura=20):
            frame = tk.Frame(parent, bg=self.cores["destaque"], bd=0, highlightthickness=0)
            frame.bind("<Enter>", lambda e: frame.config(bg=self.cores["destaque_hover"]))
            frame.bind("<Leave>", lambda e: frame.config(bg=self.cores["destaque"]))
            
            # Criando um Canvas para desenhar a borda arredondada
            canvas = tk.Canvas(frame, bg=self.cores["destaque"], highlightthickness=0, 
                            width=largura*8, height=32)
            canvas.pack(side='left', fill='both', expand=True)
            
            # Criando o botão
            btn = tk.Button(canvas, text=texto, command=comando,
                         bg=self.cores["destaque"], fg=self.cores["botao_texto"],
                         activebackground=self.cores["destaque_hover"],
                         activeforeground=self.cores["botao_texto"],
                         font=("Segoe UI", 10, "bold"),
                         bd=0, padx=10, pady=0)
            
            btn_window = canvas.create_window(largura*4, 16, window=btn)
            btn.bind("<Enter>", lambda e: frame.config(bg=self.cores["destaque_hover"]))
            btn.bind("<Leave>", lambda e: frame.config(bg=self.cores["destaque"]))
            
            return frame
        
        # Botões com cantos arredondados
        self.btn_gerar = criar_botao_arredondado(self.frame_botoes, "Gerar Grafo", self.executar_gerar_grafo)
        self.btn_gerar.pack(side='left', padx=10)
        
        self.btn_info = criar_botao_arredondado(self.frame_botoes, "Mostrar Informações", self.mostrar_informacoes)
        self.btn_info.pack(side='left', padx=10)
        
        self.btn_visualizar = criar_botao_arredondado(self.frame_botoes, "Visualizar Grafo", self.visualizar_grafo)
        self.btn_visualizar.pack(side='left', padx=10)
        
        # Layout dividido horizontalmente para o painel principal
        self.painel_principal = ttk.PanedWindow(self.tab_principal, orient=tk.HORIZONTAL)
        self.painel_principal.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Frame para a área de log (lado esquerdo)
        self.frame_log = ttk.LabelFrame(self.painel_principal, text="Log de Operações", style='Rounded.TLabelframe')
        
        # Frame para visualização do grafo (lado direito)
        self.frame_preview = ttk.LabelFrame(self.painel_principal, text="Pré-visualização do Grafo", style='Rounded.TLabelframe')
        
        # Adicionar ambos os painéis à janela principal
        self.painel_principal.add(self.frame_log, weight=1)
        self.painel_principal.add(self.frame_preview, weight=2)
        
        # Área de log com estilo personalizado
        self.log_area = scrolledtext.ScrolledText(self.frame_log, 
                                             width=50, 
                                             height=20,
                                             background=self.cores["bg_text"],
                                             foreground=self.cores["texto"],
                                             font=("Consolas", 10),
                                             borderwidth=1,
                                             relief="solid")
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Área para pré-visualização do grafo
        self.fig = plt.Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_preview)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()
        
        # Conteúdo da Aba de Informações
        # Frame para as estatísticas do grafo
        self.frame_info = ttk.LabelFrame(self.tab_info, text="Estatísticas e Dados do Grafo", style='Rounded.TLabelframe')
        self.frame_info.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Área para mostrar informações do grafo
        self.info_area = scrolledtext.ScrolledText(self.frame_info, 
                                              width=70, 
                                              height=30,
                                              background=self.cores["bg_text"],
                                              foreground=self.cores["texto"],
                                              font=("Consolas", 10),
                                              borderwidth=1,
                                              relief="solid")
        self.info_area.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Conteúdo da Aba de Visualização
        self.frame_visualizacao = ttk.LabelFrame(self.tab_visualizacao, text="Visualização do Grafo", style='Rounded.TLabelframe')
        self.frame_visualizacao.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Controles para a visualização
        self.frame_controles = ttk.Frame(self.frame_visualizacao, style='TFrame')
        self.frame_controles.pack(fill='x', padx=5, pady=5)
        
        # Slider para número de nós a exibir
        ttk.Label(self.frame_controles, text="Número de nós:").pack(side='left', padx=(0, 5))
        
        # Variável para armazenar o valor atual do slider
        self.var_num_nos = tk.IntVar(value=30)
        
        # Label para mostrar o valor atual do slider
        self.lbl_num_nos = ttk.Label(self.frame_controles, 
                                   text="30", 
                                   font=("Segoe UI", 10, "bold"),
                                   foreground=self.cores["destaque"])
        self.lbl_num_nos.pack(side='left', padx=(0, 5))
        
        # Slider com callback para atualização em tempo real
        self.slider_nos = ttk.Scale(self.frame_controles, 
                                 from_=10, 
                                 to=100, 
                                 orient='horizontal', 
                                 length=200,
                                 variable=self.var_num_nos,
                                 command=self.atualizar_valor_slider)
        self.slider_nos.set(30)
        self.slider_nos.pack(side='left', padx=(0, 20))
        
        # Botão para atualizar a visualização
        self.btn_atualizar_vis = criar_botao_arredondado(self.frame_controles, "Atualizar", self.atualizar_visualizacao, 15)
        self.btn_atualizar_vis.pack(side='left')
        
        # Área para visualização do grafo
        self.frame_vis_grafo = ttk.Frame(self.frame_visualizacao, style='TFrame')
        self.frame_vis_grafo.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.fig_vis = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax_vis = self.fig_vis.add_subplot(111)
        self.canvas_vis = FigureCanvasTkAgg(self.fig_vis, master=self.frame_vis_grafo)
        self.canvas_vis.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas_vis.draw()
        
        # Configurar as novas abas
        self.configurar_aba_euleriano()
        self.configurar_aba_distancia()
        self.configurar_aba_diametro()
        
        # Barra de status no rodapé
        self.barra_status = tk.Label(self.root, 
                                 text="Pronto", 
                                 bd=1, 
                                 relief=tk.SUNKEN, 
                                 anchor=tk.W, 
                                 background=self.cores["destaque"],
                                 foreground=self.cores["botao_texto"],
                                 font=("Segoe UI", 9),
                                 padx=10,
                                 pady=3)
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X)
    
    def configurar_aba_euleriano(self):
        """Configura a aba de verificação de grafo euleriano (Controller 3)"""
        frame_euleriano = ttk.LabelFrame(self.tab_euleriano, text="Verificação de Grafo Euleriano", style='Rounded.TLabelframe')
        frame_euleriano.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Botão para verificar se é euleriano
        frame_btn = ttk.Frame(frame_euleriano, style='TFrame')
        frame_btn.pack(pady=15)
        
        btn_verificar = self.criar_botao_arredondado(frame_btn, "Verificar se o Grafo é Euleriano", self.verificar_euleriano)
        btn_verificar.pack()
        
        # Área de resultados
        self.euleriano_area = scrolledtext.ScrolledText(frame_euleriano, 
                                                   width=70, 
                                                   height=25,
                                                   background=self.cores["bg_text"],
                                                   foreground=self.cores["texto"],
                                                   font=("Consolas", 10),
                                                   borderwidth=1,
                                                   relief="solid")
        self.euleriano_area.pack(fill='both', expand=True, padx=5, pady=5)
    
    def configurar_aba_distancia(self):
        """Configura a aba de cálculo de distância entre vértices (Controller 4)"""
        frame_distancia = ttk.LabelFrame(self.tab_distancia, text="Vértices até uma Distância Máxima", style='Rounded.TLabelframe')
        frame_distancia.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Frame para entrada de dados
        frame_entrada = ttk.Frame(frame_distancia, style='TFrame')
        frame_entrada.pack(fill='x', padx=5, pady=15)
        
        # Entrada para vértice de origem
        ttk.Label(frame_entrada, text="Vértice de origem:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_origem = ttk.Entry(frame_entrada, width=30)
        self.entrada_origem.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Entrada para distância máxima
        ttk.Label(frame_entrada, text="Distância máxima:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entrada_distancia = ttk.Entry(frame_entrada, width=10)
        self.entrada_distancia.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Botão para calcular
        btn_calcular = self.criar_botao_arredondado(frame_entrada, "Calcular", self.calcular_distancia)
        btn_calcular.grid(row=2, column=0, columnspan=2, padx=5, pady=15)
        
        # Área de resultados
        self.distancia_area = scrolledtext.ScrolledText(frame_distancia, 
                                                   width=70, 
                                                   height=20,
                                                   background=self.cores["bg_text"],
                                                   foreground=self.cores["texto"],
                                                   font=("Consolas", 10),
                                                   borderwidth=1,
                                                   relief="solid")
        self.distancia_area.pack(fill='both', expand=True, padx=5, pady=5)
    
    def configurar_aba_diametro(self):
        """Configura a aba de cálculo do diâmetro do grafo (Controller 5)"""
        frame_diametro = ttk.LabelFrame(self.tab_diametro, text="Cálculo do Diâmetro do Grafo", style='Rounded.TLabelframe')
        frame_diametro.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Frame para os botões
        frame_btns = ttk.Frame(frame_diametro, style='TFrame')
        frame_btns.pack(fill='x', padx=5, pady=15)
        
        # Botões para cálculo sequencial e paralelo
        btn_seq = self.criar_botao_arredondado(frame_btns, "Calcular Diâmetro (Sequencial)", self.calcular_diametro_seq)
        btn_seq.pack(side='left', padx=10)
        
        btn_par = self.criar_botao_arredondado(frame_btns, "Calcular Diâmetro (Paralelo)", self.calcular_diametro_par)
        btn_par.pack(side='left', padx=10)
        
        # Área de resultados
        self.diametro_area = scrolledtext.ScrolledText(frame_diametro, 
                                                  width=70, 
                                                  height=20,
                                                  background=self.cores["bg_text"],
                                                  foreground=self.cores["texto"],
                                                  font=("Consolas", 10),
                                                  borderwidth=1,
                                                  relief="solid")
        self.diametro_area.pack(fill='both', expand=True, padx=5, pady=5)
    
    def criar_botao_arredondado(self, parent, texto, comando, largura=20):
        """Função para criar botões arredondados personalizados"""
        frame = tk.Frame(parent, bg=self.cores["destaque"], bd=0, highlightthickness=0)
        frame.bind("<Enter>", lambda e: frame.config(bg=self.cores["destaque_hover"]))
        frame.bind("<Leave>", lambda e: frame.config(bg=self.cores["destaque"]))
        
        # Criando um Canvas para desenhar a borda arredondada
        canvas = tk.Canvas(frame, bg=self.cores["destaque"], highlightthickness=0, 
                        width=largura*8, height=32)
        canvas.pack(side='left', fill='both', expand=True)
        
        # Criando o botão
        btn = tk.Button(canvas, text=texto, command=comando,
                     bg=self.cores["destaque"], fg=self.cores["botao_texto"],
                     activebackground=self.cores["destaque_hover"],
                     activeforeground=self.cores["botao_texto"],
                     font=("Segoe UI", 10, "bold"),
                     bd=0, padx=10, pady=0)
        
        btn_window = canvas.create_window(largura*4, 16, window=btn)
        btn.bind("<Enter>", lambda e: frame.config(bg=self.cores["destaque_hover"]))
        btn.bind("<Leave>", lambda e: frame.config(bg=self.cores["destaque"]))
        
        return frame
    
    def atualizar_valor_slider(self, event=None):
        """Atualiza o valor exibido do slider em tempo real"""
        valor = int(self.slider_nos.get())
        self.lbl_num_nos.config(text=str(valor))
    
    def executar_gerar_grafo(self):
        self.log_area.delete(1.0, tk.END)
        self.log_area.insert(tk.END, "🔄 Gerando grafo... Por favor, aguarde.\n")
        self.barra_status.config(text="Gerando grafo...")
        self.root.update()
        
        try:
            resultado = gerar_grafo()
            self.log_area.insert(tk.END, "✅ " + resultado + "\n")
            
            # Atualizar a pré-visualização do grafo
            self.atualizar_preview_grafo()
            
            self.barra_status.config(text="Grafo gerado com sucesso!")
            messagebox.showinfo("Sucesso", "Grafo gerado com sucesso!")
        except Exception as e:
            self.log_area.insert(tk.END, f"❌ Erro: {str(e)}\n")
            self.barra_status.config(text="Erro ao gerar grafo")
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o grafo: {str(e)}")
    
    def atualizar_preview_grafo(self):
        """Atualiza a pré-visualização do grafo na página principal"""
        try:
            # Limpar a visualização anterior
            self.ax.clear()
            
            # Criar um grafo do NetworkX a partir dos dados do grafo atual
            G = nx.DiGraph()
            
            # Selecionar apenas os 20 principais vértices para melhor visualização
            top_vertices = [v for v, _ in get_maiores_graus_saida(20)]
            
            # Adicionar vértices e arestas
            for origem in top_vertices:
                if origem in grafo.adj_list:
                    for destino, peso in grafo.adj_list[origem]:
                        if destino in top_vertices:
                            G.add_edge(origem, destino, weight=peso)
            
            # Posicionar os nós
            pos = nx.spring_layout(G, k=0.5)  # Ajuste k para mudar a distância entre os nós
            
            # Desenhar nós e arestas
            nx.draw_networkx_nodes(G, pos, node_size=300, node_color=self.cores["destaque"], alpha=0.8, ax=self.ax)
            nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=self.ax)
            
            # Adicionar os nomes dos vértices (apenas os primeiros 8 caracteres)
            labels = {node: node[:8] + '...' if len(node) > 8 else node for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black', ax=self.ax)
            
            # Configurar a visualização
            self.ax.set_title("Pré-visualização dos 20 Principais Nós", fontsize=10)
            self.ax.axis('off')
            
            # Atualizar o canvas
            self.fig.tight_layout()
            self.canvas.draw()
            
            self.log_area.insert(tk.END, "✅ Pré-visualização do grafo atualizada.\n")
        except Exception as e:
            self.log_area.insert(tk.END, f"❌ Erro ao atualizar a pré-visualização: {str(e)}\n")
    
    def visualizar_grafo(self):
        """Visualiza o grafo na aba de visualização"""
        self.notebook.select(self.tab_visualizacao)
        self.atualizar_visualizacao()
    
    def atualizar_visualizacao(self):
        """Atualiza a visualização completa do grafo"""
        try:
            self.barra_status.config(text="Atualizando visualização do grafo...")
            self.root.update()
            
            # Limpar a visualização anterior
            self.ax_vis.clear()
            
            # Obter o número de nós a exibir
            num_nos = int(self.slider_nos.get())
            
            # Criar um grafo do NetworkX
            G = nx.DiGraph()
            
            # Selecionar os vértices com maiores graus
            top_vertices = [v for v, _ in get_maiores_graus_saida(num_nos)]
            
            # Adicionar vértices e arestas
            for origem in top_vertices:
                if origem in grafo.adj_list:
                    for destino, peso in grafo.adj_list[origem]:
                        if destino in top_vertices:
                            G.add_edge(origem, destino, weight=peso)
            
            # Posicionar os nós
            pos = nx.spring_layout(G, k=0.3, seed=42)  # Usando seed para consistência entre visualizações
            
            # Pesos das arestas para determinar a largura das linhas
            weights = [G[u][v]['weight'] for u, v in G.edges()]
            max_weight = max(weights) if weights else 1
            normalized_weights = [w / max_weight * 3 for w in weights]
            
            # Desenhar nós
            nx.draw_networkx_nodes(G, pos, 
                               node_size=350, 
                               node_color=self.cores["destaque"], 
                               alpha=0.8, 
                               ax=self.ax_vis)
            
            # Desenhar arestas com largura proporcional ao peso
            nx.draw_networkx_edges(G, pos, 
                               width=normalized_weights,
                               edge_color='gray', 
                               alpha=0.5, 
                               arrowsize=15,
                               ax=self.ax_vis)
            
            # Adicionar os nomes dos vértices (apenas os primeiros 8 caracteres)
            labels = {node: node[:8] + '...' if len(node) > 8 else node for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black', ax=self.ax_vis)
            
            # Configurar a visualização
            self.ax_vis.set_title(f"Visualização dos {num_nos} Principais Nós", fontsize=12)
            self.ax_vis.axis('off')
            
            # Atualizar o canvas
            self.fig_vis.tight_layout()
            self.canvas_vis.draw()
            
            self.barra_status.config(text=f"Visualização atualizada com {num_nos} nós")
        except Exception as e:
            self.barra_status.config(text="Erro ao gerar visualização")
            messagebox.showerror("Erro", f"Ocorreu um erro ao visualizar o grafo: {str(e)}")
    
    def mostrar_informacoes(self):
        try:
            self.barra_status.config(text="Carregando informações do grafo...")
            self.root.update()
            
            self.info_area.delete(1.0, tk.END)
            self.info_area.tag_configure("titulo", foreground=self.cores["destaque"], font=("Consolas", 11, "bold"))
            self.info_area.tag_configure("subtitulo", foreground=self.cores["destaque"], font=("Consolas", 10, "bold"))
            self.info_area.tag_configure("normal", foreground=self.cores["texto"], font=("Consolas", 10))
            self.info_area.tag_configure("destaque", foreground=self.cores["destaque_hover"], font=("Consolas", 10, "bold"))
            
            # Informações básicas
            self.info_area.insert(tk.END, "=== INFORMAÇÕES DO GRAFO ===\n\n", "titulo")
            self.info_area.insert(tk.END, f"Número de vértices (ordem): ", "normal")
            self.info_area.insert(tk.END, f"{get_numero_vertices()}\n", "destaque")
            self.info_area.insert(tk.END, f"Número de arestas (tamanho): ", "normal")
            self.info_area.insert(tk.END, f"{get_numero_arestas()}\n\n", "destaque")
            
            # Vértices isolados
            vertices_isolados, num_isolados = get_vertices_isolados()
            self.info_area.insert(tk.END, f"Número de vértices isolados: ", "normal")
            self.info_area.insert(tk.END, f"{num_isolados}\n", "destaque")
            if num_isolados > 0:
                self.info_area.insert(tk.END, "Exemplos de vértices isolados:\n", "normal")
                for i, v in enumerate(vertices_isolados[:5], 1):
                    self.info_area.insert(tk.END, f"  {i}. ", "normal")
                    self.info_area.insert(tk.END, f"{v}\n", "destaque")
                if num_isolados > 5:
                    self.info_area.insert(tk.END, f"  ... e mais {num_isolados - 5} vértices\n\n", "normal")
            
            # Vértices com loops
            vertices_com_loops, num_loops = get_vertices_com_loops()
            self.info_area.insert(tk.END, f"\nNúmero de vértices com loops (auto-arestas): ", "normal")
            self.info_area.insert(tk.END, f"{num_loops}\n", "destaque")
            if num_loops > 0:
                self.info_area.insert(tk.END, "Exemplos de vértices com loops:\n", "normal")
                for i, v in enumerate(vertices_com_loops[:5], 1):
                    self.info_area.insert(tk.END, f"  {i}. ", "normal")
                    self.info_area.insert(tk.END, f"{v}\n", "destaque")
                if num_loops > 5:
                    self.info_area.insert(tk.END, f"  ... e mais {num_loops - 5} vértices\n\n", "normal")
            
            # Top vértices com maior grau de saída
            self.info_area.insert(tk.END, "\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE SAÍDA ===\n", "subtitulo")
            for i, (vertice, grau) in enumerate(get_maiores_graus_saida(20), 1):
                self.info_area.insert(tk.END, f"{i}. ", "normal")
                self.info_area.insert(tk.END, f"{vertice}: ", "destaque")
                self.info_area.insert(tk.END, f"{grau}\n", "normal")
            
            # Top vértices com maior grau de entrada
            self.info_area.insert(tk.END, "\n=== TOP 20 VÉRTICES COM MAIOR GRAU DE ENTRADA ===\n", "subtitulo")
            for i, (vertice, grau) in enumerate(get_maiores_graus_entrada(20), 1):
                self.info_area.insert(tk.END, f"{i}. ", "normal")
                self.info_area.insert(tk.END, f"{vertice}: ", "destaque")
                self.info_area.insert(tk.END, f"{grau}\n", "normal")
                
            # Mudar para a aba de informações
            self.notebook.select(self.tab_info)
            self.barra_status.config(text="Informações do grafo carregadas com sucesso")
            
        except Exception as e:
            self.barra_status.config(text="Erro ao carregar informações")
            messagebox.showerror("Erro", f"Ocorreu um erro ao mostrar informações: {str(e)}")
    
    def verificar_euleriano(self):
        """Verifica se o grafo é euleriano e mostra o resultado"""
        try:
            self.barra_status.config(text="Verificando se o grafo é euleriano...")
            self.root.update()
            
            self.euleriano_area.delete(1.0, tk.END)
            self.euleriano_area.tag_configure("titulo", foreground=self.cores["destaque"], font=("Consolas", 11, "bold"))
            self.euleriano_area.tag_configure("resultado", foreground=self.cores["texto"], font=("Consolas", 10))
            self.euleriano_area.tag_configure("positivo", foreground="green", font=("Consolas", 10, "bold"))
            self.euleriano_area.tag_configure("negativo", foreground="red", font=("Consolas", 10, "bold"))
            
            # Verificar se o grafo é euleriano
            eh_euleriano, mensagem = grafo_euleriano_direcionado()
            
            # Exibir resultado
            self.euleriano_area.insert(tk.END, "=== VERIFICAÇÃO DE GRAFO EULERIANO ===\n\n", "titulo")
            
            if eh_euleriano:
                self.euleriano_area.insert(tk.END, "O grafo É euleriano!\n\n", "positivo")
                self.euleriano_area.insert(tk.END, mensagem + "\n", "resultado")
            else:
                self.euleriano_area.insert(tk.END, "O grafo NÃO é euleriano!\n\n", "negativo")
                self.euleriano_area.insert(tk.END, "Condições não satisfeitas:\n", "resultado")
                for condicao in mensagem:
                    self.euleriano_area.insert(tk.END, f"- {condicao}\n", "resultado")
            
            self.barra_status.config(text="Verificação de grafo euleriano concluída")
        except Exception as e:
            self.barra_status.config(text="Erro na verificação")
            messagebox.showerror("Erro", f"Ocorreu um erro na verificação: {str(e)}")
    
    def calcular_distancia(self):
        """Calcula os vértices alcançáveis a partir de uma origem até uma distância máxima"""
        try:
            origem = self.entrada_origem.get().strip()
            
            # Verificar se a origem existe no grafo
            if not origem or origem not in grafo.adj_list:
                messagebox.showerror("Erro", "Vértice de origem não encontrado no grafo!")
                return
            
            # Verificar se a distância é válida
            try:
                distancia_maxima = int(self.entrada_distancia.get().strip())
                if distancia_maxima < 0:
                    messagebox.showerror("Erro", "A distância máxima deve ser um inteiro não negativo!")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Entrada inválida! Digite um número inteiro para a distância.")
                return
            
            self.barra_status.config(text=f"Calculando vértices até distância {distancia_maxima}...")
            self.root.update()
            
            # Calcular vértices até a distância
            vertices = vertices_ate_distancia(origem, distancia_maxima)
            
            # Exibir resultado
            self.distancia_area.delete(1.0, tk.END)
            self.distancia_area.tag_configure("titulo", foreground=self.cores["destaque"], font=("Consolas", 11, "bold"))
            self.distancia_area.tag_configure("subtitulo", foreground=self.cores["destaque"], font=("Consolas", 10, "bold"))
            self.distancia_area.tag_configure("normal", foreground=self.cores["texto"], font=("Consolas", 10))
            
            self.distancia_area.insert(tk.END, "=== VÉRTICES ALCANÇÁVEIS ATÉ UMA DISTÂNCIA MÁXIMA ===\n\n", "titulo")
            self.distancia_area.insert(tk.END, f"Origem: {origem}\n", "subtitulo")
            self.distancia_area.insert(tk.END, f"Distância máxima: {distancia_maxima}\n\n", "subtitulo")
            
            if vertices:
                self.distancia_area.insert(tk.END, f"Total de vértices encontrados: {len(vertices)}\n\n", "normal")
                self.distancia_area.insert(tk.END, "Vértices alcançáveis:\n", "subtitulo")
                for i, v in enumerate(vertices, 1):
                    self.distancia_area.insert(tk.END, f"{i}. {v}\n", "normal")
            else:
                self.distancia_area.insert(tk.END, "Nenhum vértice encontrado para essa distância.\n", "normal")
            
            self.barra_status.config(text="Cálculo de distância concluído")
        except Exception as e:
            self.barra_status.config(text="Erro no cálculo de distância")
            messagebox.showerror("Erro", f"Ocorreu um erro no cálculo: {str(e)}")
    
    def calcular_diametro_seq(self):
        """Calcula o diâmetro do grafo usando o método sequencial"""
        try:
            self.barra_status.config(text="Calculando o diâmetro do grafo (sequencial)...")
            self.root.update()
            
            self.diametro_area.delete(1.0, tk.END)
            self.diametro_area.tag_configure("titulo", foreground=self.cores["destaque"], font=("Consolas", 11, "bold"))
            self.diametro_area.tag_configure("subtitulo", foreground=self.cores["destaque"], font=("Consolas", 10, "bold"))
            self.diametro_area.tag_configure("normal", foreground=self.cores["texto"], font=("Consolas", 10))
            self.diametro_area.tag_configure("destaque", foreground=self.cores["destaque_hover"], font=("Consolas", 10, "bold"))
            
            self.diametro_area.insert(tk.END, "=== CÁLCULO DO DIÂMETRO DO GRAFO (SEQUENCIAL) ===\n\n", "titulo")
            self.diametro_area.insert(tk.END, "Calculando...\n", "normal")
            self.root.update()
            
            # Medir o tempo de execução
            inicio = time.time()
            diametro, caminho = calcular_diametro(grafo)
            fim = time.time()
            tempo = fim - inicio
            
            # Exibir resultados
            self.diametro_area.delete(1.0, tk.END)
            self.diametro_area.insert(tk.END, "=== CÁLCULO DO DIÂMETRO DO GRAFO (SEQUENCIAL) ===\n\n", "titulo")
            self.diametro_area.insert(tk.END, f"Diâmetro: ", "subtitulo")
            self.diametro_area.insert(tk.END, f"{diametro}\n\n", "destaque")
            
            self.diametro_area.insert(tk.END, "Caminho correspondente:\n", "subtitulo")
            self.diametro_area.insert(tk.END, " -> ".join(caminho) + "\n\n", "normal")
            
            self.diametro_area.insert(tk.END, f"Tempo de execução: {tempo:.2f} segundos\n", "normal")
            
            self.barra_status.config(text="Cálculo do diâmetro concluído")
        except Exception as e:
            self.barra_status.config(text="Erro no cálculo do diâmetro")
            messagebox.showerror("Erro", f"Ocorreu um erro no cálculo: {str(e)}")
    
    def calcular_diametro_par(self):
        """Calcula o diâmetro do grafo usando o método paralelo"""
        try:
            self.barra_status.config(text="Calculando o diâmetro do grafo (paralelo)...")
            self.root.update()
            
            self.diametro_area.delete(1.0, tk.END)
            self.diametro_area.tag_configure("titulo", foreground=self.cores["destaque"], font=("Consolas", 11, "bold"))
            self.diametro_area.tag_configure("subtitulo", foreground=self.cores["destaque"], font=("Consolas", 10, "bold"))
            self.diametro_area.tag_configure("normal", foreground=self.cores["texto"], font=("Consolas", 10))
            self.diametro_area.tag_configure("destaque", foreground=self.cores["destaque_hover"], font=("Consolas", 10, "bold"))
            
            self.diametro_area.insert(tk.END, "=== CÁLCULO DO DIÂMETRO DO GRAFO (PARALELO) ===\n\n", "titulo")
            self.diametro_area.insert(tk.END, "Calculando...\n", "normal")
            self.root.update()
            
            # Medir o tempo de execução
            inicio = time.time()
            diametro, caminho = calcular_diametro_paralelo(grafo)
            fim = time.time()
            tempo = fim - inicio
            
            # Exibir resultados
            self.diametro_area.delete(1.0, tk.END)
            self.diametro_area.insert(tk.END, "=== CÁLCULO DO DIÂMETRO DO GRAFO (PARALELO) ===\n\n", "titulo")
            self.diametro_area.insert(tk.END, f"Diâmetro: ", "subtitulo")
            self.diametro_area.insert(tk.END, f"{diametro}\n\n", "destaque")
            
            self.diametro_area.insert(tk.END, "Caminho correspondente:\n", "subtitulo")
            self.diametro_area.insert(tk.END, " -> ".join(caminho) + "\n\n", "normal")
            
            self.diametro_area.insert(tk.END, f"Tempo de execução: {tempo:.2f} segundos\n", "normal")
            
            self.barra_status.config(text="Cálculo do diâmetro concluído")
        except Exception as e:
            self.barra_status.config(text="Erro no cálculo do diâmetro")
            messagebox.showerror("Erro", f"Ocorreu um erro no cálculo: {str(e)}")
    
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.iniciar()
