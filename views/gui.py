"""
Interface gráfica usando tkinter para o projeto de Redes de Email
Tema elegante com cores neutras e sofisticadas
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import os
import sys

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
            "borda": "#E0E0E0"          # Cinza claro
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
        
        # Estilo para os botões
        self.estilo.configure('TButton', 
                          background=self.cores["destaque"],
                          foreground=self.cores["botao_texto"],
                          font=("Segoe UI", 10, "bold"),
                          borderwidth=0,
                          focusthickness=3,
                          focuscolor=self.cores["destaque"])
        
        self.estilo.map('TButton',
                    background=[('active', self.cores["destaque_hover"])],
                    relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Estilo para os frames
        self.estilo.configure('TFrame', background=self.cores["bg_frame"])
        
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
        
        # Estilo para os LabelFrames
        self.estilo.configure('TLabelframe', 
                          background=self.cores["bg_frame"],
                          foreground=self.cores["texto"],
                          borderwidth=1,
                          relief="solid")
        
        self.estilo.configure('TLabelframe.Label', 
                          background=self.cores["bg_frame"],
                          foreground=self.cores["titulo"],
                          font=("Segoe UI", 11, "bold"))
    
    def criar_widgets(self):
        # Frame principal para centralizar o conteúdo
        self.frame_principal = ttk.Frame(self.root, style='TFrame')
        self.frame_principal.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título da aplicação
        titulo_label = tk.Label(self.frame_principal, 
                             text="Análise de Rede de Emails - Dataset Enron",
                             font=("Segoe UI", 16, "bold"),
                             background=self.cores["bg_frame"],
                             foreground=self.cores["titulo"])
        titulo_label.pack(pady=(0, 20))
        
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
        
        # Conteúdo da Aba Principal
        # Frame para as ações
        self.frame_acoes = ttk.LabelFrame(self.tab_principal, text="Ações", style='TLabelframe')
        self.frame_acoes.pack(fill='x', expand=False, padx=15, pady=15)
        
        # Container para os botões
        self.frame_botoes = ttk.Frame(self.frame_acoes, style='TFrame')
        self.frame_botoes.pack(pady=15)
        
        # Botões com ícones
        self.btn_gerar = ttk.Button(self.frame_botoes, text="Gerar Grafo", 
                                 command=self.executar_gerar_grafo,
                                 width=20)
        self.btn_gerar.pack(side='left', padx=10)
        
        self.btn_info = ttk.Button(self.frame_botoes, text="Mostrar Informações", 
                               command=self.mostrar_informacoes,
                               width=20)
        self.btn_info.pack(side='left', padx=10)
        
        self.btn_visualizar = ttk.Button(self.frame_botoes, text="Visualizar Grafo", 
                                  command=self.visualizar_grafo,
                                  width=20)
        self.btn_visualizar.pack(side='left', padx=10)
        
        # Layout dividido horizontalmente para o painel principal
        self.painel_principal = ttk.PanedWindow(self.tab_principal, orient=tk.HORIZONTAL)
        self.painel_principal.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Frame para a área de log (lado esquerdo)
        self.frame_log = ttk.LabelFrame(self.painel_principal, text="Log de Operações", style='TLabelframe')
        
        # Frame para visualização do grafo (lado direito)
        self.frame_preview = ttk.LabelFrame(self.painel_principal, text="Pré-visualização do Grafo", style='TLabelframe')
        
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
        self.frame_info = ttk.LabelFrame(self.tab_info, text="Estatísticas e Dados do Grafo", style='TLabelframe')
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
        self.frame_visualizacao = ttk.LabelFrame(self.tab_visualizacao, text="Visualização do Grafo", style='TLabelframe')
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
        self.btn_atualizar_vis = ttk.Button(self.frame_controles, text="Atualizar", 
                                       command=self.atualizar_visualizacao)
        self.btn_atualizar_vis.pack(side='left')
        
        # Área para visualização do grafo
        self.frame_vis_grafo = ttk.Frame(self.frame_visualizacao, style='TFrame')
        self.frame_vis_grafo.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.fig_vis = plt.Figure(figsize=(10, 8), dpi=100)
        self.ax_vis = self.fig_vis.add_subplot(111)
        self.canvas_vis = FigureCanvasTkAgg(self.fig_vis, master=self.frame_vis_grafo)
        self.canvas_vis.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas_vis.draw()
        
        # Barra de status no rodapé
        self.barra_status = tk.Label(self.root, 
                                 text="Pronto", 
                                 bd=1, 
                                 relief=tk.SUNKEN, 
                                 anchor=tk.W, 
                                 background=self.cores["destaque"],
                                 foreground=self.cores["botao_texto"],
                                 font=("Segoe UI", 9))
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X)
    
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
    
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GUI()
    app.iniciar()
