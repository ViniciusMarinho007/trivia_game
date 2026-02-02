# Trivia Game - Esportes 🏆

**Trivia Game** é um jogo de perguntas e respostas sobre esportes, desenvolvido em **Python** com interface **Tkinter**.  
O jogo possui design moderno rosa/preto, botões arredondados estilo card e embaralhamento das respostas.

---

 Funcionalidades

- Perguntas em **Português** carregadas de um arquivo JSON.
- Interface **moderna** com botões arredondados e efeito hover.
- **Timer** de 20 segundos para cada pergunta.
- **Ranking** local com pontuação usando SQLite.
- Feedback visual para respostas corretas (**verde**) e erradas (**vermelho**).
- Perguntas e respostas **embaralhadas** a cada partida.

---

 Estrutura do projeto

trivia_game/
│
├─ main.py # Executa o jogo
├─ gui.py # Interface Tkinter
├─ trivia.py # Lógica do jogo
├─ ranking.py # Banco de dados SQLite
├─ perguntas.py # Carregar perguntas JSON
├─ perguntas_esportes.json # Perguntas em português
└─ README.md # Este arquivo



---

 Tecnologias

- Python 3.x
- Tkinter (GUI)
- SQLite (ranking local)
- JSON (perguntas)

---

 Como executar

1. Clone o repositório:

```bash
git clone https://github.com/ViniciusMarinho007/trivia_game.git
cd trivia_game
Execute o jogo:
python main.py
Certifique-se de ter o Python 3 instalado.

Observações

As perguntas estão no arquivo perguntas_esportes.json.

Você pode adicionar novas perguntas mantendo o mesmo formato JSON:
