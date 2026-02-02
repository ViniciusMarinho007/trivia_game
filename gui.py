import tkinter as tk
from tkinter import messagebox, simpledialog
from trivia import TriviaGameLogic
from ranking import criar_banco, salvar_pontuacao, ler_ranking
from perguntas import carregar_perguntas_local

class RoundedButton(tk.Canvas):
    """Botão arredondado estilo card com hover"""
    def __init__(self, master, text="", command=None, width=250, height=50,
                 bg="#ff1d8e", fg="#000000", font=("Arial", 12, "bold"), radius=25):
        super().__init__(master, width=width, height=height, highlightthickness=0, bg=master["bg"])
        self.bg = bg
        self.fg = fg
        self.radius = radius
        self.command = command
        self.font = font
        self.text = text

        self.rect = self.create_rounded_rect(0, 0, width, height, radius, fill=bg)
        self.label = self.create_text(width//2, height//2, text=text, fill=fg, font=font)

        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def create_rounded_rect(self, x1, y1, x2, y2, r=25, **kwargs):
        points = [
            x1+r, y1,
            x1+r, y1,
            x2-r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y1+r,
            x2, y2-r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x2-r, y2,
            x1+r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y2-r,
            x1, y1+r,
            x1, y1+r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.rect, fill="#e6007a")  # hover rosa escuro

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg)

    def set_text(self, text):
        self.itemconfig(self.label, text=text)

    def set_bg(self, color):
        self.itemconfig(self.rect, fill=color)


class TriviaGameGUI:
    def __init__(self):
        criar_banco()
        self.root = tk.Tk()
        self.root.title("Trivia de Esportes")
        self.root.geometry("750x550")
        self.root.configure(bg="#000000")

        self.tempo = 20
        self.timer_id = None

        # Carregar perguntas e lógica
        perguntas = carregar_perguntas_local()
        if not perguntas:
            self.root.destroy()
            return
        self.game = TriviaGameLogic(perguntas)

        # Label da pergunta
        self.label_pergunta = tk.Label(
            self.root, text="", wraplength=700,
            font=("Arial", 16, "bold"), fg="#ff1d8e", bg="#000000"
        )
        self.label_pergunta.pack(pady=30)

        # Botões de respostas estilo card
        self.buttons = []
        for i in range(4):
            btn = RoundedButton(
                self.root, text="", width=400, height=60,
                bg="#ff1d8e", fg="#000000",
                font=("Arial", 14, "bold"),
                command=lambda i=i: self.responder(i)
            )
            self.buttons.append(btn)

        # Timer
        self.label_timer = tk.Label(self.root, text="", font=("Arial", 16, "bold"), fg="#ff1d8e", bg="#000000")
        self.label_timer.pack(pady=15)

        # Botão iniciar
        self.botao_start = RoundedButton(
            self.root, text="Start", width=300, height=60,
            bg="#ff1d8e", fg="#000000",
            font=("Arial", 16, "bold"),
            command=self.start_game
        )
        self.botao_start.pack(pady=25)

        self.root.mainloop()

    def start_game(self):
        self.botao_start.pack_forget()
        self.proxima()

    def proxima(self):
        self.tempo = 20
        self.atualizar_timer()
        self.pergunta_atual = self.game.proxima_pergunta()
        if not self.pergunta_atual:
            self.fim_jogo()
            return

        self.label_pergunta.config(text=self.pergunta_atual['pergunta'])
        for i, opcao in enumerate(self.pergunta_atual['opcoes_embaralhadas']):
            self.buttons[i].set_text(opcao)
            self.buttons[i].set_bg("#ff1d8e")
            self.buttons[i].pack(pady=12)

    def atualizar_timer(self):
        self.label_timer.config(text=f"Tempo: {self.tempo} s")
        if self.tempo <= 0:
            messagebox.showinfo("Tempo esgotado!", "Você não respondeu a tempo!")
            self.proxima()
        else:
            self.tempo -= 1
            self.timer_id = self.root.after(1000, self.atualizar_timer)

    def responder(self, i):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)

        escolhida = self.pergunta_atual['opcoes_embaralhadas'][i]
        if self.game.verificar_resposta(self.pergunta_atual, escolhida):
            self.game.pontuacao += 10
            self.buttons[i].set_bg("#00ff00")
            messagebox.showinfo("Correto!", "Resposta correta!")
        else:
            self.buttons[i].set_bg("#ff0000")
            # mostrar correta
            for j, opcao in enumerate(self.pergunta_atual['opcoes_embaralhadas']):
                if opcao == self.pergunta_atual['correta']:
                    self.buttons[j].set_bg("#00ff00")
            messagebox.showinfo("Errado!", f"Resposta correta: {self.pergunta_atual['correta']}")
        self.proxima()

    def fim_jogo(self):
        nome = simpledialog.askstring("Fim de jogo", f"Sua pontuação: {self.game.pontuacao}\nDigite seu nome para o ranking:")
        if nome:
            salvar_pontuacao(nome, self.game.pontuacao)
        top10 = ler_ranking()
        resultado = "🏆 Ranking Top 10 🏆\n\n"
        for i, (nome, pts) in enumerate(top10, start=1):
            resultado += f"{i}. {nome} - {pts} pts\n"
        messagebox.showinfo("Ranking", resultado)
        self.botao_start.pack(pady=25)
        for btn in self.buttons:
            btn.pack_forget()
        self.label_pergunta.config(text="")
        self.label_timer.config(text="")
