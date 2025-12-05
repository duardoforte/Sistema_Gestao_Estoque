#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# JSON com os dados de estoque iniciais
dados_json = '''
{
    "estoque": [
        {
            "codigoProduto": 101,
            "descricaoProduto": "Caneta Azul",
            "estoque": 150
        },
        {
            "codigoProduto": 102,
            "descricaoProduto": "Caderno Universitário",
            "estoque": 75
        },
        {
            "codigoProduto": 103,
            "descricaoProduto": "Borracha Branca",
            "estoque": 200
        },
        {
            "codigoProduto": 104,
            "descricaoProduto": "Lápis Preto HB",
            "estoque": 320
        },
        {
            "codigoProduto": 105,
            "descricaoProduto": "Marcador de Texto Amarelo",
            "estoque": 90
        }
    ]
}
'''

class SistemaEstoque:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Estoque")
        # Janela grande
        self.root.geometry("1200x800")
        self.root.configure(bg='#ecf0f1')
        
        # Carregar dados
        self.dados = json.loads(dados_json)
        self.produtos = {p['codigoProduto']: p for p in self.dados['estoque']}
        self.movimentacoes = []
        self.proximo_id = 1
        
        # Criar interface
        self.criar_interface()
        
    def gerar_id_movimentacao(self):
        """Gera um ID único para a movimentação."""
        id_mov = self.proximo_id
        self.proximo_id += 1
        return id_mov
        
    def criar_interface(self):
        # Container principal
        container = tk.Frame(self.root, bg='#ecf0f1')
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ==================== CABEÇALHO ====================
        header = tk.Frame(container, bg='#2c3e50', height=90)
        header.pack(fill=tk.X, pady=(0, 15))
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="📦 SISTEMA DE CONTROLE DE ESTOQUE",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=(15, 5))
        
        subtitle = tk.Label(
            header,
            text=f"Gerenciamento de Movimentações | {datetime.now().strftime('%d/%m/%Y')}",
            font=('Arial', 11),
            bg='#2c3e50',
            fg='#bdc3c7'
        )
        subtitle.pack()
        
        # ==================== PAINEL PRINCIPAL ====================
        main_panel = tk.Frame(container, bg='#ecf0f1')
        main_panel.pack(fill=tk.BOTH, expand=True)
         
        # ==================== FRAME ESQUERDO (Menor Agora) ====================
        left_frame = tk.Frame(main_panel, bg='white', relief=tk.RAISED, borderwidth=2)
        # Reduzi a largura fixa aqui para 310
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0, expand=False)
        left_frame.configure(width=310) 
        left_frame.pack_propagate(False) # Garante que ele respeite os 310px
        
        # Título do formulário
        form_title = tk.Label(
            left_frame,
            text="Nova Movimentação",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            pady=10
        )
        form_title.pack(fill=tk.X)
        
        # Frame interno do formulário
        form_inner = tk.Frame(left_frame, bg='white')
        form_inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Produto
        tk.Label(form_inner, text="Produto:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
        
        self.combo_produto = ttk.Combobox(form_inner, font=('Arial', 10), state='readonly')
        produtos_lista = [f"{p['codigoProduto']} - {p['descricaoProduto']}" for p in self.dados['estoque']]
        self.combo_produto.configure(values=produtos_lista)
        self.combo_produto.pack(fill=tk.X, pady=(0, 10))
        self.combo_produto.bind('<<ComboboxSelected>>', self.atualizar_estoque_atual)
        
        # Estoque atual (exibição)
        tk.Label(form_inner, text="Estoque Atual:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
        
        self.label_estoque_atual = tk.Label(
            form_inner,
            text="Selecione um produto",
            font=('Arial', 12),
            bg='#ecf0f1',
            fg='#2c3e50',
            relief=tk.SUNKEN,
            padx=10,
            pady=8
        )
        self.label_estoque_atual.pack(fill=tk.X, pady=(0, 10))
        
        # Tipo de movimentação
        tk.Label(form_inner, text="Tipo de Movimentação:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
        
        self.tipo_var = tk.StringVar(value="ENTRADA")
        
        radio_frame = tk.Frame(form_inner, bg='white')
        radio_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Radiobutton(
            radio_frame,
            text="📥 Entrada",
            variable=self.tipo_var,
            value="ENTRADA",
            font=('Arial', 10),
            bg='white',
            activebackground='white',
            selectcolor='#2ecc71'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Radiobutton(
            radio_frame,
            text="📤 Saída",
            variable=self.tipo_var,
            value="SAIDA",
            font=('Arial', 10),
            bg='white',
            activebackground='white',
            selectcolor='#e74c3c'
        ).pack(side=tk.LEFT)
        
        # Quantidade
        tk.Label(form_inner, text="Quantidade:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
        
        self.entry_quantidade = tk.Entry(form_inner, font=('Arial', 12), relief=tk.SOLID, borderwidth=1)
        self.entry_quantidade.pack(fill=tk.X, pady=(0, 10))
        
        # Descrição
        tk.Label(form_inner, text="Descrição:", font=('Arial', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
        
        self.text_descricao = scrolledtext.ScrolledText(
            form_inner,
            font=('Arial', 10),
            height=3, 
            relief=tk.SOLID,
            borderwidth=1,
            wrap=tk.WORD
        )
        self.text_descricao.pack(fill=tk.X, pady=(0, 15))
        
        # ==================== BOTÕES ====================
        btn_frame = tk.Frame(form_inner, bg='white')
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.btn_lancar = tk.Button(
            btn_frame,
            text="✓ CONFIRMAR", 
            command=self.lancar_movimentacao,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            pady=10
        )
        self.btn_lancar.pack(fill=tk.X, pady=(0, 8))
        
        btn_limpar = tk.Button(
            btn_frame,
            text="🔄 Limpar",
            command=self.limpar_formulario,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            pady=8
        )
        btn_limpar.pack(fill=tk.X)
        
        # ==================== FRAME DIREITO (Maior Agora) ====================
        right_frame = tk.Frame(main_panel, bg='#ecf0f1')
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tabela de estoque atual
        estoque_frame = tk.Frame(right_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        estoque_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        estoque_title = tk.Label(
            estoque_frame,
            text="📊 Estoque Atual",
            font=('Arial', 13, 'bold'),
            bg='#16a085',
            fg='white',
            pady=10
        )
        estoque_title.pack(fill=tk.X)
        
        # Treeview Estoque
        columns_estoque = ('Código', 'Produto', 'Estoque')
        self.tree_estoque = ttk.Treeview(estoque_frame, columns=columns_estoque, show='headings', height=6)
        
        self.tree_estoque.heading('Código', text='Código')
        self.tree_estoque.heading('Produto', text='Produto')
        self.tree_estoque.heading('Estoque', text='Estoque')
        
        self.tree_estoque.column('Código', width=100, anchor='center')
        self.tree_estoque.column('Produto', width=300, anchor='w')
        self.tree_estoque.column('Estoque', width=120, anchor='center')
        
        scroll_estoque = ttk.Scrollbar(estoque_frame, orient=tk.VERTICAL, command=self.tree_estoque.yview)
        self.tree_estoque.configure(yscroll=scroll_estoque.set)
        
        self.tree_estoque.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scroll_estoque.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        self.atualizar_tabela_estoque()
        
        # Tabela de movimentações
        mov_frame = tk.Frame(right_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        mov_frame.pack(fill=tk.BOTH, expand=True)
        
        mov_title = tk.Label(
            mov_frame,
            text="📝 Histórico de Movimentações",
            font=('Arial', 13, 'bold'),
            bg='#8e44ad',
            fg='white',
            pady=10
        )
        mov_title.pack(fill=tk.X)
        
        # ============================================================
        # AJUSTE FINO DAS COLUNAS PARA APROVEITAR O ESPAÇO NOVO
        # ============================================================
        columns_mov = ('ID', 'Data/Hora', 'Produto', 'Tipo', 'Qtd', 'Est. Final', 'Descrição')
        self.tree_mov = ttk.Treeview(mov_frame, columns=columns_mov, show='headings', height=10)
        
        self.tree_mov.heading('ID', text='ID')
        self.tree_mov.heading('Data/Hora', text='Data/Hora')
        self.tree_mov.heading('Produto', text='Produto')
        self.tree_mov.heading('Tipo', text='Tipo')
        self.tree_mov.heading('Qtd', text='Qtd')
        self.tree_mov.heading('Est. Final', text='Est. Final')
        self.tree_mov.heading('Descrição', text='Descrição', anchor='w')
        
        # Diminuí as colunas numéricas para sobrar espaço para Descrição
        self.tree_mov.column('ID', width=30, anchor='center')
        self.tree_mov.column('Data/Hora', width=130, anchor='center')
        self.tree_mov.column('Produto', width=200, anchor='w')
        self.tree_mov.column('Tipo', width=80, anchor='center')
        self.tree_mov.column('Qtd', width=50, anchor='center')
        self.tree_mov.column('Est. Final', width=70, anchor='center')
        
        # Coluna Descrição agora tem mais espaço
        self.tree_mov.column('Descrição', width=300, anchor='w')
        
        scroll_mov = ttk.Scrollbar(mov_frame, orient=tk.VERTICAL, command=self.tree_mov.yview)
        self.tree_mov.configure(yscroll=scroll_mov.set)
         
        self.tree_mov.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scroll_mov.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Estilo
        self.configurar_estilo()
        
    def configurar_estilo(self):
        """Configura o estilo das tabelas."""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Treeview',
                       background='white',
                       foreground='black',
                       rowheight=28,
                       fieldbackground='white',
                       font=('Arial', 10))
        
        style.configure('Treeview.Heading',
                       background='#34495e',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       relief=tk.FLAT)
        
        style.map('Treeview',
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
    def atualizar_estoque_atual(self, event=None):
        """Atualiza o label com o estoque atual do produto selecionado."""
        selecao = self.combo_produto.get()
        if selecao:
            codigo = int(selecao.split(' - ')[0])
            produto = self.produtos[codigo]
            self.label_estoque_atual.configure(
                text=f"{produto['estoque']} unidades",
                font=('Arial', 14, 'bold'),
                fg='#16a085'
            )
        
    def atualizar_tabela_estoque(self):
        """Atualiza a tabela de estoque."""
        # Limpar tabela
        for item in self.tree_estoque.get_children():
            self.tree_estoque.delete(item)
        
        # Adicionar dados
        for produto in sorted(self.produtos.values(), key=lambda x: x['codigoProduto']):
            self.tree_estoque.insert('', tk.END, values=(
                produto['codigoProduto'],
                produto['descricaoProduto'],
                produto['estoque']
            ))
            
    def lancar_movimentacao(self):
        """Lança uma nova movimentação de estoque."""
        try:
            # Validações
            if not self.combo_produto.get():
                messagebox.showwarning("Atenção", "Selecione um produto!")
                return
                
            codigo = int(self.combo_produto.get().split(' - ')[0])
            
            try:
                quantidade = int(self.entry_quantidade.get())
                if quantidade <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Atenção", "Informe uma quantidade válida (número inteiro positivo)!")
                return
            
            descricao = self.text_descricao.get("1.0", tk.END).strip()
            if not descricao:
                messagebox.showwarning("Atenção", "Informe uma descrição para a movimentação!")
                return
            
            tipo = self.tipo_var.get()
            produto = self.produtos[codigo]
            
            # Validar estoque para saída
            if tipo == "SAIDA" and quantidade > produto['estoque']:
                messagebox.showerror(
                    "Erro",
                    f"Estoque insuficiente!\nEstoque atual: {produto['estoque']}\nQuantidade solicitada: {quantidade}"
                )
                return
            
            # Calcular novo estoque
            if tipo == "ENTRADA":
                novo_estoque = produto['estoque'] + quantidade
            else:
                novo_estoque = produto['estoque'] - quantidade
            
            # Gerar ID único
            id_movimentacao = self.gerar_id_movimentacao()
            
            # Atualizar estoque
            produto['estoque'] = novo_estoque
            
            # Registrar movimentação
            movimentacao = {
                'id': id_movimentacao,
                'data_hora': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                'codigo_produto': codigo,
                'descricao_produto': produto['descricaoProduto'],
                'tipo': tipo,
                'quantidade': quantidade,
                'estoque_final': novo_estoque,
                'descricao': descricao
            }
            self.movimentacoes.append(movimentacao)
            
            # Atualizar interface
            self.atualizar_tabela_estoque()
            self.atualizar_estoque_atual()
            self.adicionar_movimentacao_tabela(movimentacao)
            
            # Mostrar confirmação
            cor_tipo = '#27ae60' if tipo == 'ENTRADA' else '#e74c3c'
            simbolo = '📥' if tipo == 'ENTRADA' else '📤'
            
            msg = f"""{simbolo} Movimentação realizada com sucesso!
ID: {id_movimentacao}
Produto: {produto['descricaoProduto']}
Tipo: {tipo}
Qtd: {quantidade}
Estoque Final: {novo_estoque}"""
            
            messagebox.showinfo("Sucesso", msg)
            
            # Limpar formulário
            self.limpar_formulario()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar: {str(e)}")
            
    def adicionar_movimentacao_tabela(self, mov):
        """Adiciona uma movimentação na tabela."""
        cor_tag = 'entrada' if mov['tipo'] == 'ENTRADA' else 'saida'
        
        self.tree_mov.insert('', 0, values=(
            mov['id'],
            mov['data_hora'],
            mov['descricao_produto'],
            mov['tipo'],
            mov['quantidade'],
            mov['estoque_final'],
            mov['descricao'] 
        ), tags=(cor_tag,))
        
        # Cores para os tipos
        self.tree_mov.tag_configure('entrada', background='#d5f4e6')
        self.tree_mov.tag_configure('saida', background='#fadbd8')
        
    def limpar_formulario(self):
        """Limpa todos os campos do formulário."""
        self.combo_produto.set('')
        self.entry_quantidade.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        self.tipo_var.set("ENTRADA")
        self.label_estoque_atual.configure(
            text="Selecione um produto",
            font=('Arial', 12),
            fg='#2c3e50'
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEstoque(root)
    root.mainloop()