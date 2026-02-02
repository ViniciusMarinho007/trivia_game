import json
import os
from tkinter import messagebox

JSON_FILE = "perguntas_esportes.json"

def carregar_perguntas_local(arquivo=JSON_FILE):
    if not os.path.exists(arquivo):
        messagebox.showerror("Erro", f"O arquivo {arquivo} não foi encontrado!")
        return []
    with open(arquivo, "r", encoding="utf-8") as f:
        perguntas = json.load(f)
    return perguntas
