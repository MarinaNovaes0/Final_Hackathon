from tkinter import * # Para a interface gráfica
from tkinter import ttk, messagebox # Para criar widgets e janelas de erro ou sucesso
from tkinter import Toplevel # Para criar novas janelas
from tkcalendar import Calendar # Inclui a interface do calendário interativo 
import calendar # Serve para obter informações como número de dias do mês ou verificar anos bissextos.
from PIL import Image, ImageTk # Para abrir, manipular e exibir imagens.
import services  # Importar o módulo que faz a interação com o banco de dados
import re # Para trabalhar com validação de strings.
import datetime # Para manipular e formatar datas e horas.

# Mudar a cor do botão das janelas para evitar erro
def on_enter(button, hover_color):
    button.configure(bg=hover_color)

def on_leave(button, default_color):
    button.configure(bg=default_color)

# Mudar a cor dos botões cinzas
class BotaoComHover(Button):
    def __init__(self, master=None, hover_bg="lightgray", normal_bg="gray", **kwargs):
        super().__init__(master, **kwargs)
        self.hover_bg = hover_bg       # Cor ao passar o mouse
        self.normal_bg = normal_bg     # Cor normal do botão
        self['background'] = self.normal_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self['background'] = self.hover_bg

    def on_leave(self, event):
        self['background'] = self.normal_bg

# Mudar a cor dos botões
class BotaoComHover2(Button):
    def __init__(self, master=None, hover_bg="#a62828", normal_bg="#5b1717", **kwargs):
        super().__init__(master, **kwargs)
        self.hover_bg = hover_bg       # Cor ao passar o mouse
        self.normal_bg = normal_bg     # Cor normal do botão
        self['background'] = self.normal_bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self['background'] = self.hover_bg

    def on_leave(self, event):
        self['background'] = self.normal_bg
        
# Interface do caledário na janela principal
def mostrar_calendario(event=None):
    global janela_principal, janela, data_atual
    data_atual = datetime.date.today()
    calendario_janela = Toplevel(janela_principal)
    calendario_janela.overrideredirect(True)
    calendario_janela.geometry("250x250")
    
    calendario = Calendar(calendario_janela, selectmode='day', year=data_atual.year, month=data_atual.month, day=data_atual.day,
                          foreground='black', background='gray', selectbackground='red',
                          headersbackground='gray', bordercolor='gray', showweeknumbers=False)
    calendario.pack(pady=5)
    
    selecionar_button = Button(calendario_janela, text="Selecionar",
                               command=lambda: selecionar_data(calendario, calendario_janela))
    selecionar_button.pack(pady=5)
    
    # Posição da janela
    x = data_entry.winfo_rootx() + data_entry.winfo_width() + 10
    y = data_entry.winfo_rooty()
    calendario_janela.geometry(f"+{x}+{y}")

# Para aparecer a data selecionada e quando clicar no botão o calendário sumir
def selecionar_data(calendario, janela):
    data_selecionada = calendario.get_date()
    data_formatada = datetime.datetime.strptime(data_selecionada, '%d/%m/%Y').strftime(f'%d/%m/{data_atual.year}')
    data_entry.config(state='normal')
    data_entry.delete(0, "end")
    data_entry.insert(0, data_formatada)
    data_entry.config(state='readonly')
    janela.destroy()

# Para quando clicar no campo data a mensagem padrão suma e apenas a data apareça
def on_entry_click_data(event):
    if data_entry.get() == "Clique para selecionar":
        data_entry.delete(0, "end")  
        data_entry.config(state='readonly') 
 
# Interface do caledário na janela listar
def mostrar_calendario2(event=None):
    global data_atual2
    data_atual2 = datetime.date.today()
    calendario_janela_listar = Toplevel(janela_listar)
    calendario_janela_listar.overrideredirect(True) 
    calendario_janela_listar.geometry("250x250") 

    calendario2 = Calendar(calendario_janela_listar, selectmode='day', year=data_atual2.year, month=data_atual2.month, day=data_atual2.day, 
                          foreground='black', background='gray', selectbackground='red', 
                          headersbackground='gray', bordercolor='gray', showweeknumbers=False)
    calendario2.pack(pady=5) 

    selecionar_button2 = Button(calendario_janela_listar, text="Selecionar", 
                               command=lambda: selecionar_data2(calendario2, calendario_janela_listar))
    selecionar_button2.pack(pady=5) 
    
    # Posição da janela
    x = data_entry_listar.winfo_rootx() + data_entry_listar.winfo_width() + 10 
    y = data_entry_listar.winfo_rooty()
    calendario_janela_listar.geometry(f"+{x}+{y}")

# Para aparecer a data selecionada e quando clicar no botão o calendário sumir
def selecionar_data2(calendario, janela):
    data_selecionada2 = calendario.get_date()
    data_formatada2 = datetime.datetime.strptime(data_selecionada2, '%d/%m/%Y').strftime(f'%d/%m/{data_atual2.year}')
    data_entry_listar.config(state='normal') 
    data_entry_listar.delete(0, 'end')
    data_entry_listar.insert(0, data_formatada2)
    data_entry_listar.config(state='readonly')
    janela.destroy() 

# Para quando clicar no campo data a mensagem padrão suma e apenas a data apareça
def on_entry_click_data_listar(event):
    if data_entry_listar.get() == "Clique para selecionar":
        data_entry_listar.delete(0, "end") 
        data_entry_listar.config(state='readonly')

# Para no campo valor aparecer o R$ e automáticamente formatar o valor para 0,00
def formatar_valor(event=None):
    # Obtém o valor atual do campo
    valor = valor_entry.get().replace("R$", "").replace(".", "").replace(",", "").strip()
    
    # Filtra para manter apenas dígitos
    valor = ''.join(filter(str.isdigit, valor))

    # Se o campo estiver vazio, não faz nada
    if valor == "":
        valor_entry.delete(0, END)
        valor_entry.insert(0, "R$ ")
        return

    # Formata o valor como "R$ x.xx"
    valor_float = float(valor) / 100 if valor else 0  # Converte centavos em reais
    valor_formatado = f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    valor_entry.delete(0, END) 
    valor_entry.insert(0, valor_formatado)

# Apenas números são permitido no campo valor
def apenas_numeros(char):
    return char.isdigit()  # Retorna True se o caractere for um dígito

# Quando clicar no campo valor a mensagem padrão se apagar
def on_entry_click_valor(event):
    if valor_entry.get() == "R$ 0,00":
        valor_entry.delete(0, "end") 

# Para quando clicar em sair todas as janelas serem fechadas
def destruir_todas_as_janelas():
    for window in janela.winfo_children():
        window.destroy()  
        janela.quit()

''' Verifica se há despesas cadastradas no banco de dados, senão houver não
 dá pra entrar na janela listar nem na de cálculo '''  
def verificar_despesas_cadastradas():
    despesas = services.listar_despesas()

    if not despesas:
        messagebox.showerror("Erro", "Nenhuma despesa cadastrada.", parent=janela_principal)
        return False 

    return True

# Campo para verificação de dados na hora de cadastrar despesas
def inserir_dados():
    categoria = categoria_combobox.get().strip()
    data = data_entry.get().strip()
    valor = valor_entry.get().strip()
    
    # Verifica se algum campo está vazio
    if not categoria or not data or not valor:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.", parent=janela_principal)
        return
    
    # Verifica se os campos só estão com as mensagens padrão
    if categoria == "Clique para selecionar" or data == "Clique para selecionar" or valor == "R$ 0,00":
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.", parent=janela_principal)
        return
    
    # Remove o "R$" e converte o valor para float
    try:
        valor_num = float(re.sub(r"[^\d,]", "", valor).replace(',', '.')) 
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Por favor, insira um valor numérico.", parent=janela_principal)
        return

    # Para inserir no banco de dados
    if services.inserir_dados(categoria, data, valor_num): 
        messagebox.showinfo("Sucesso", "Despesa cadastrada com sucesso!", parent=janela_principal)

        # Resetando os campos com as mensagens padrão
        categoria_combobox.set("Clique para selecionar")  

        data_entry.config(state='normal')
        data_entry.delete(0, END) 
        data_entry.insert(0, "Clique para selecionar")  
        
        valor_entry.delete(0, END)  
        valor_entry.insert(0, "R$ 0,00")

    # Se algum outro erro aparecer
    else:
        messagebox.showerror("Erro", "Erro ao cadastrar despesa!", parent=janela_principal)

# Para trocar de janela
def mostrar_janela(janela):
    janela.deiconify()  # Mostra a janela caso esteja escondida
    janela.lift()       # Traz a janela para a frente

# Categorias para as combobox
categorias = ["Moradia", "Alimentação", "Transporte", "Saúde", "Lazer", "Educação", "Vestuário", "Outros"] 

# Meses para as combobox
meses = ["Clique para selecionar", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    
# Logo quando iniciar todas as janelas são criadas, para deixar mais suave a passagem entre elas
def criar_janelas():
    global janela, janela_principal, janela_listar, janela_despesas, nova_janela, categoria_combobox, data_entry, valor_entry, data_entry_listar, categorias, meses
    
    # ANCHOR Criação da Janela inicial de boas vindas
    janela = Tk()
    janela.title("Bem-vindo ao Skynet Hackathon 2024")
    janela.attributes('-fullscreen', True)
    janela.configure(bg="black")

    try:
        img = Image.open("terminator_image.jpg")
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        img = img.resize((largura_tela, altura_tela), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        label = Label(janela, image=img_tk)
        label.place(relwidth=1, relheight=1)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar a imagem: {str(e)}", parent=janela)

    subtitulo_label = Label(janela, text="Hackathon 2024", font=('Arial', 60), bg="black", fg="gray")
    subtitulo_label.place(relx=0.5, rely=0.5, anchor=CENTER)  

    try:
        img2 = Image.open('logo.jpg') 
        img2 = img2.resize((900, 300), Image.LANCZOS) 
        img2_tk = ImageTk.PhotoImage(img2)

        label2 = Label(janela, image=img2_tk, background='black')
        label2.place(relx=0.6, rely=0.18, anchor=CENTER)  
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao carregar a segunda imagem: {str(e)}", parent=janela)

    btn_frame = Frame(janela, bg="black")
    btn_frame.place(relx=0.5, rely=0.65, anchor=CENTER)  

    entrar_button = BotaoComHover(btn_frame, text="Entrar", width=20, command=lambda: mostrar_janela(janela_principal), bg="gray", fg="black", height=2, font=('Arial', 20, 'bold'))
    entrar_button.grid(row=0, column=0, padx=10, pady=15)

    sair_button = BotaoComHover2(btn_frame, text="Sair", width=20, command=destruir_todas_as_janelas, bg="#5b1717", height=2, fg="white", font=('Arial', 20, 'bold'))
    sair_button.grid(row=0, column=1, padx=10, pady=15)

    # Lista de nomes na parte inferior da janela
    lista_nomes_frame = Frame(janela, bg="black")
    lista_nomes_frame.pack(side=BOTTOM, pady=20)

    nomes = [
        "Feito por:",
        "Rafael Carvalho",
        "Philipi José",
        "Marina Novaes"
        ]

    for nome in nomes:
        Label(lista_nomes_frame, text=nome, font=('Arial', 17), bg="black", fg="gray").pack(pady=2) 

   
    # ANCHOR Criação da Janela principal
    janela_principal = Toplevel()
    janela_principal.withdraw()  # Esconde a janela principal até que o usuário clique em "Entrar"
    janela_principal.title("Gerenciador de Despesas")
    janela_principal.attributes('-fullscreen', True)
    janela_principal.configure(bg="black")

    imagem_fundo = Image.open("fundo.jpg") 
    imagem_fundo = imagem_fundo.resize((janela_principal.winfo_screenwidth(), janela_principal.winfo_screenheight()))
    bg_image = ImageTk.PhotoImage(imagem_fundo)

    background_label = Label(janela_principal, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    titulo = Label(janela_principal, text='Gerenciador de Despesas', font=('Orbitron', 60, 'bold'), bg="black", fg="white")
    titulo.place(relx=0.5, rely=0.1, anchor=CENTER)

    form_frame = Frame(janela_principal, bg="black")
    form_frame.place(relx=0.5, rely=0.35, anchor=CENTER)

    Label(form_frame, text="Categoria:", font=('Arial', 20), bg="black", fg="white").grid(row=0, column=0, sticky=W, padx=10, pady=10)
    categoria_combobox = ttk.Combobox(form_frame, width=28, values=categorias, font=('Arial', 20), state="readonly")
    categoria_combobox.grid(row=0, column=1, padx=10, pady=10) 
    categoria_combobox.set("Clique para selecionar")
    categoria_combobox.configure(foreground="black") 
    
    Label(form_frame, text="Data da Despesa:", font=('Arial', 20), bg="black", fg="white").grid(row=1, column=0, sticky=W, padx=10, pady=10)
    data_entry = Entry(form_frame, width=30, font=('Arial', 20), fg='black', state='normal')
    data_entry.insert(0, "Clique para selecionar")
    data_entry.grid(row=1, column=1, padx=10, pady=10)
    data_entry.bind("<Button-1>", mostrar_calendario)
    data_entry.bind("<FocusIn>", on_entry_click_data)
        
    Label(form_frame, text="Valor:", font=('Arial', 20), bg="black", fg="white").grid(row=2, column=0, sticky=W, padx=10, pady=10)
    valor_entry = Entry(form_frame, width=30, font=('Arial', 20), fg='black')
    valor_entry.insert(0, "R$ 0,00")  # Texto padrão
    valor_entry.grid(row=2, column=1, padx=10, pady=10)
    valor_entry.bind("<KeyRelease>", formatar_valor)
    valor_entry.bind("<FocusIn>", on_entry_click_valor)


    buttons_frame = Frame(janela_principal, bg="black")
    buttons_frame.place(relx=0.5, rely=0.65, anchor=CENTER)

    # Criação dos botões
    cadastrar_button2 = BotaoComHover(buttons_frame, text="Cadastrar Despesa", width=20, command=inserir_dados, bg="gray", height=2, font=('Arial', 20, 'bold'))
    cadastrar_button2.grid(row=0, column=0, padx=10, pady=5)

   # Botão "Cálculo Despesas" usando a classe BotaoComHover
    calcular_button = BotaoComHover(buttons_frame, text="Cálculo Despesas", width=20,
                            command=lambda: (verificar_despesas_cadastradas() and mostrar_janela(nova_janela)), 
                            bg="gray", height=2, font=('Arial', 20, 'bold'))

    calcular_button.grid(row=1, column=0, padx=10, pady=5)

    listar_button = BotaoComHover(buttons_frame, text='Listar Despesas', width=20, 
                        command=lambda: (verificar_despesas_cadastradas() and mostrar_janela(janela_listar)), 
                        bg="gray", height=2, font=('Arial', 20, 'bold'))
    listar_button.grid(row=0, column=1, padx=10, pady=5)

    sair_button2 = Button(buttons_frame, text="Sair", width=20, command=destruir_todas_as_janelas, bg="#5b1717", height=2, fg="white", font=('Arial', 20, 'bold'))
    sair_button2.grid(row=1, column=1, padx=10, pady=15)

    # Bind dos eventos para o botão "Sair". Não sei porque aplicar neste botão dá erro
    sair_button2.bind("<Enter>", lambda e: on_enter(sair_button2, "#a62828"))
    sair_button2.bind("<Leave>", lambda e: on_leave(sair_button2, "#5b1717"))
    
    # ANCHOR Criação da janela de listagem
    janela_listar = Toplevel(janela_principal)
    janela_listar.title("Listar Despesas")
    janela_listar.attributes('-fullscreen', True)
    janela_listar.configure(bg="black")
    background_label = Label(janela_listar)
    background_label.place(relwidth=1, relheight=1)

    def atualizar_imagem():
        background_image = Image.open("fundo.jpg")  
        background_image = background_image.resize((janela_listar.winfo_width(), janela_listar.winfo_height()))
        background_photo = ImageTk.PhotoImage(background_image)
            
        background_label.configure(image=background_photo)
        background_label.image = background_photo 

    janela_listar.update()
    atualizar_imagem()
            
    titulo = Label(janela_listar, text='Listar Despesas', font=('Orbitron', 60, 'bold'), bg="black", fg="white")
    titulo.place(relx=0.5, rely=0.05, anchor=CENTER)  

    # Frame para o formulário
    form_frame = Frame(janela_listar, bg="black")
    form_frame.place(relx=0.5, rely=0.5, anchor=CENTER) 

    # Função se clicar no botão "Listar todas as Despesas"
    def listar_todas_despesas():
    
        despesas = services.listar_despesas()
        mostrar_despesas(despesas)
        
    # Botão "Listar Todas as Despesas"
    listar_todas_button = BotaoComHover(form_frame, text='Listar Todas as Despesas', width=30, command=listar_todas_despesas, bg="gray", height=2, font=('Arial', 15, 'bold'))
    listar_todas_button.pack(pady=10)
    
    
    # Labels e campos para filtrar por categoria e data
    Label(form_frame, text="Filtrar por Categoria:", font=('Arial', 20), bg="black", fg="white").pack(pady=10)
    categoria_combobox_listar = ttk.Combobox(form_frame, width=28, values=categorias, font=('Arial', 20), state="readonly")
    categoria_combobox_listar.pack(padx=10, pady=10) 
    categoria_combobox_listar.set("Clique para selecionar")
    categoria_combobox_listar.configure(foreground="black")  

    Label(form_frame, text="Filtrar por Data:", font=('Arial', 20), bg="black", fg="white").pack(pady=10)
    data_entry_listar = Entry(form_frame, width=30, font=('Arial', 20), fg='black', state='normal')
    data_entry_listar.insert(0, "Clique para selecionar")
    data_entry_listar.pack(pady=10)
    data_entry_listar.bind("<Button-1>", mostrar_calendario2)
    data_entry_listar.bind("<FocusIn>", on_entry_click_data_listar)

    Label(form_frame, text="Filtrar por Mês:", font=('Arial', 20), bg="black", fg="white").pack(pady=10)
    mes_combobox_listar = ttk.Combobox(form_frame, width=28, values=meses, font=('Arial', 20), state="readonly")
    mes_combobox_listar.pack(padx=10, pady=10) 
    mes_combobox_listar.set("Clique para selecionar")
    mes_combobox_listar.configure(foreground="black")

    # Botão "Listar Despesas Filtradas"
    listar_filtradas_button = Button(form_frame, text='Listar Despesas Filtradas', width=30, command=lambda: listar_despesas_filtradas(), bg="gray", height=2, font=('Arial', 15, 'bold'))
    listar_filtradas_button.pack(pady=10)
  
    # Botão "Voltar"
    voltar_button = BotaoComHover2(form_frame, text='Voltar', width=20, command=lambda: mostrar_janela(janela_principal), bg="#5b1717", height=2, fg="white", font=('Arial', 15, 'bold'))
    voltar_button.pack(pady=15)
    
    # Bind dos eventos para "Listar Despesas Filtradas"
    listar_filtradas_button.bind("<Enter>", lambda e: on_enter(listar_filtradas_button, "lightgray"))
    listar_filtradas_button.bind("<Leave>", lambda e: on_leave(listar_filtradas_button, "gray"))
    

    # Criação da janela para mostrar as despesas
    def mostrar_despesas(despesas):   
        janela_despesas = Toplevel()  
        janela_despesas.title("Todas as Despesas")  
        janela_despesas.attributes('-fullscreen', True) 
        janela_despesas.configure(bg="black") 

        Label(janela_despesas, text="Despesas Cadastradas", font=('Orbitron', 24, 'bold'), bg="black", fg="white").pack(pady=20)

        table_frame = Frame(janela_despesas, bg="black") 
        table_frame.pack(pady=10, padx=20, fill=BOTH, expand=True)  

        # Cria a tabela (Treeview) para exibir as despesas
        tree = ttk.Treeview(table_frame, columns=('Categoria', 'Data', 'Valor'), show='headings') 
        tree.heading('Categoria', text='Categoria') 
        tree.heading('Data', text='Data') 
        tree.heading('Valor', text='Valor')  

        # Estilizando a tabela
        style = ttk.Style()  
        style.configure("Treeview",
                        font=('Arial', 16),  
                        background="gray", 
                        foreground="black", 
                        rowheight=30, 
                        fieldbackground="black")  

        style.configure("Treeview.Heading",
                        background="black", 
                        foreground="#5b1717",  
                        font=('Arial', 20, 'bold')) 

        # Preenche a tabela com os dados das despesas
        for despesa in despesas: 
            categoria = despesa[1]  # Extrai a categoria da despesa (presumivelmente a segunda posição)
            data = despesa[2] if despesa[2] else "N/A"  # Se houver data, usa-a; senão, coloca "N/A"
            valor = f"R$ {despesa[3]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  # Formata o valor com vírgula como separador decimal
            tree.insert('', END, values=(categoria, data, valor))  # Insere os dados na tabela

        # Cria a barra de rolagem para a tabela
        scrollbar = Scrollbar(table_frame, orient="vertical", command=tree.yview, bg="#a00")  
        tree.configure(yscrollcommand=scrollbar.set) 
        scrollbar.pack(side="right", fill="y") 

        # Exibe a tabela na tela
        tree.pack(fill=BOTH, expand=True) 

        def voltar():
            # Limpa os campos e reseta as seleções de categoria, data e mês
            data_entry_listar.config(state='normal')  
            data_entry_listar.delete(0, END)  
            data_entry_listar.insert(0, "Clique para selecionar")  
            data_entry_listar.config(state='readonly') 
            categoria_combobox_listar.set("Clique para selecionar") 
            mes_combobox_listar.set("Clique para selecionar")  

            mostrar_janela(janela_listar)

        # Cria o botão "Voltar"
        voltar_button = BotaoComHover2(janela_despesas, text='Voltar', width=20, command=voltar, bg="#5b1717", fg="white", height=2, font=('Arial', 12, 'bold'))
        voltar_button.pack(pady=15)  

    # Função para listar despesas filtradas
    def listar_despesas_filtradas():
        categoria = categoria_combobox_listar.get().strip()
        data = data_entry_listar.get().strip()
        mes = mes_combobox_listar.get().strip()

        despesas = services.listar_despesas()

        # Verifica se o usuário selecionou tanto mês quanto data
        if mes != "Clique para selecionar" and data != "Clique para selecionar":
            messagebox.showerror("Erro", "Escolha se vai querer filtrar por dia ou por mês, não ambos.", parent=janela_listar)
            data_entry_listar.config(state='normal')
            data_entry_listar.delete(0, END) 
            data_entry_listar.insert(0, "Clique para selecionar")
            data_entry_listar.config(state='readonly')
            mes_combobox_listar.set("Clique para selecionar")
            categoria_combobox_listar.set("Clique para selecionar") 
            return

        # Verifica se pelo menos um critério foi preenchido
        if categoria == "Clique para selecionar" and mes == "Clique para selecionar" and data == "Clique para selecionar":
            messagebox.showerror("Erro", "Por favor, preencha pelo menos um dos campos de filtro.", parent=janela_listar)
            return

        # Filtrar por categoria
        if categoria and categoria != "Clique para selecionar":
            despesas = [d for d in despesas if d[1] == categoria]

        # Filtrar por mês
        if mes != "Clique para selecionar":
            mes_num = meses.index(mes)   # Mapeamento do mês selecionado para número (1 a 12)
            despesas = [d for d in despesas if d[2] and d[2].month == mes_num]

         # Filtrar por dia
        if data and data != "Clique para selecionar":
            try:
                # Formato esperado é 'dd/mm/yyyy'
                data_formatada = datetime.datetime.strptime(data, '%d/%m/%Y').date()  # Converter a string em um objeto date
                despesas = [d for d in despesas if d[2] and d[2] == data_formatada]
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use o formato dd/mm/aaaa.", parent=janela_listar)
                return


        # Verificação se não encontrou despesas
        if not despesas:
            messagebox.showerror("Erro", "Nenhuma despesa encontrada com os critérios selecionados.", parent=janela_listar)
            data_entry_listar.config(state='normal')
            data_entry_listar.delete(0, END) 
            data_entry_listar.insert(0, "Clique para selecionar")
            data_entry_listar.config(state='readonly')
            mes_combobox_listar.set("Clique para selecionar")
            categoria_combobox_listar.set("Clique para selecionar") 
            return

        # Mostrar despesas filtradas
        mostrar_despesas(despesas)


    # ANCHOR Criação da janela para cálculo de despesas
    nova_janela = Toplevel()
    nova_janela.title("Cálculo de Despesas")
    nova_janela.attributes('-fullscreen', True)
    nova_janela.configure(bg="black")

    background_label = Label(nova_janela)
    background_label.place(relwidth=1, relheight=1)

    def atualizar_imagem():
        background_image = Image.open("fundo.jpg")
        background_image = background_image.resize((nova_janela.winfo_width(), nova_janela.winfo_height()))
        background_photo = ImageTk.PhotoImage(background_image)

        background_label.configure(image=background_photo)
        background_label.image = background_photo 
    
    nova_janela.update()
    atualizar_imagem()

    titulo = Label(nova_janela, text='Cálculo de Despesas', font=('Orbitron', 60, 'bold'), bg="black", fg="white")
    titulo.place(relx=0.5, rely=0.05, anchor=CENTER)

    form_frame = Frame(nova_janela, bg="black")
    form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Combobox para selecionar o mês
    Label(form_frame, text="Selecione o Mês:", font=('Arial', 20), bg="black", fg="white").pack(pady=10)
    mes_combobox = ttk.Combobox(form_frame, values=meses, font=('Arial', 20), state="readonly")
    mes_combobox.pack(pady=10)
    mes_combobox.set("Clique para selecionar") 

    # Combobox para selecionar a categoria
    Label(form_frame, text="Selecione a Categoria (opcional):", font=('Arial', 20), bg="black", fg="white").pack(pady=10)
    categorias = ["Moradia", "Alimentação", "Transporte", "Saúde", "Lazer", "Educação", "Vestuário", "Outros"]
    categoria2_combobox = ttk.Combobox(form_frame, values=categorias, font=('Arial', 20), state="readonly")
    categoria2_combobox.pack(pady=10)
    categoria2_combobox.set("Clique para selecionar") 

    # Exibir resultados
    resultado_label = Label(form_frame, text="", font=('Arial', 16), bg="black", fg="white")
    resultado_label.pack(pady=20)

    # Para calcular segundo oque o usuário escolheu
    def calcular():
        ano_atual = 2024
        mes_selecionado = mes_combobox.get().strip()
        categoria2_selecionada = categoria2_combobox.get().strip()

        # Tratar "Clique para selecionar" como não selecionado
        if mes_selecionado == "Clique para selecionar":
            mes_selecionado = ""
        if categoria2_selecionada == "Clique para selecionar":
            categoria2_selecionada = ""

        total_gasto = 0
        contador = 0
        total_gasto_categoria = 0
        contador_categoria = 0
        media_diaria = 0

        despesas_cadastradas = services.listar_despesas()  # Chama a função do services.py para listar despesas

        # Verifique se a categoria foi selecionada sem um mês
        if categoria2_selecionada and not mes_selecionado:
            messagebox.showerror("Erro", "Por favor, selecione um mês ao filtrar por categoria.", parent=nova_janela)
            return 

        # Loop para calcular os totais baseados no filtro de mês e categoria
        for despesa in despesas_cadastradas:
            categoria = despesa[1]
            data = despesa[2]
            valor = despesa[3]

            if data is not None:
                try:
                    mes_despesa = data.month

                    # Aplica o filtro de mês e categoria conforme seleção
                    if mes_selecionado and categoria2_selecionada:
                        if mes_despesa == (meses.index(mes_selecionado) ) and categoria == categoria2_selecionada:
                            total_gasto_categoria += valor
                            contador_categoria += 1

                    elif mes_selecionado:
                        if mes_despesa == (meses.index(mes_selecionado) ):
                            total_gasto += valor
                            contador += 1

                    elif categoria2_selecionada:
                        if categoria == categoria2_selecionada:
                            total_gasto_categoria += valor
                            contador_categoria += 1

                except AttributeError:
                    continue

        # Calcular média diária para o mês selecionado, com num_dias definido apenas quando necessário
        if mes_selecionado:
            num_dias = calendar.monthrange(ano_atual, meses.index(mes_selecionado) )[1]
            if contador > 0:
                media_diaria = total_gasto / num_dias if num_dias > 0 else 0

        # Exibir resultados para somente mês selecionado
        if mes_selecionado and not categoria2_selecionada:
            if total_gasto == 0:
                messagebox.showerror("Erro", f"Não há despesas registradas para o mês de {mes_selecionado}.", parent=nova_janela)
                mes_combobox.set("Clique para selecionar")
                return

            resultado_texto = f"Total gasto em {mes_selecionado}: R$ {total_gasto:,.2f}\n"
            resultado_texto += f"Média de gasto diário em {mes_selecionado}: R$ {media_diaria:,.2f}\n"
            resultado_label.config(text=resultado_texto)
            mes_combobox.set("Clique para selecionar")
        
        # Exibir resultados para mês e categoria selecionados
        elif categoria2_selecionada and mes_selecionado:
            if total_gasto_categoria == 0:
                messagebox.showerror("Erro", f"Não há despesas registradas para a categoria {categoria2_selecionada} no mês de {mes_selecionado}.", parent=nova_janela)
                mes_combobox.set("Clique para selecionar")
                categoria2_combobox.set("Clique para selecionar")
                return
            else:
                media_gasto_categoria = total_gasto_categoria / num_dias if num_dias > 0 else 0

                resultado_texto = f"\nTotal gasto em {categoria2_selecionada} no mês de {mes_selecionado}: R$ {total_gasto_categoria:,.2f}\n"
                resultado_texto += f"Média de gasto diário em {categoria2_selecionada} no mês de {mes_selecionado}: R$ {media_gasto_categoria:,.2f}"
                resultado_label.config(text=resultado_texto)
                mes_combobox.set("Clique para selecionar")
                categoria2_combobox.set("Clique para selecionar")

        else:
            messagebox.showerror("Erro", "Por favor, selecione um mês ou uma categoria para calcular.", parent=nova_janela)
            mes_combobox.set("Clique para selecionar")
            categoria2_combobox.set("Clique para selecionar")
        
    def voltar_e_apagar():  
        resultado_label.config(text= " ")
        mostrar_janela(janela_principal)  


    # Botão "Calcular"
    calcular_button = BotaoComHover(form_frame, text='Calcular', width=30, command=calcular, bg="gray", height=2, font=('Arial', 16, 'bold'))
    calcular_button.pack(pady=10)

    # Botão "Voltar"
    voltar_button = BotaoComHover2(form_frame, text='Voltar', width=20, command=lambda: voltar_e_apagar(), bg="#5b1717", height=2, fg="white", font=('Arial', 15, 'bold'))
    voltar_button.pack(pady=15)

    # Define a primeira janela para aparecer
    mostrar_janela(janela)
    
    # Para ficar em loop até ser interrompido
    janela.mainloop()   

# Cria todas as janelas  
criar_janelas()
    
    