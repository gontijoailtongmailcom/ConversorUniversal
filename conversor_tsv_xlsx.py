# -*- coding: utf-8 -*-
import subprocess
import sys
 
def instalar_pacotes(pacotes):
    for pacote in pacotes:
        try:
            __import__(pacote)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
 
instalar_pacotes(["pandas", "openpyxl"])
 
 
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
 
def converter():
    escolha = opcao.get()
 
    config = {
        "1": {"in": ".csv", "out": ".xlsx", "sep_in": ",", "func_in": pd.read_csv, "func_out": "to_excel"},
        "2": {"in": ".tsv", "out": ".xlsx", "sep_in": "\t", "func_in": pd.read_csv, "func_out": "to_excel"},
        "3": {"in": ".tsv", "out": ".csv", "sep_in": "\t", "func_in": pd.read_csv, "func_out": "to_csv", "sep_out": ","},
        "4": {"in": ".csv", "out": ".tsv", "sep_in": ",", "func_in": pd.read_csv, "func_out": "to_csv", "sep_out": "\t"},
        "5": {"in": ".xlsx", "out": ".csv", "func_in": pd.read_excel, "func_out": "to_csv", "sep_out": ","},
        "6": {"in": ".xlsx", "out": ".tsv", "func_in": pd.read_excel, "func_out": "to_csv", "sep_out": "\t"},
    }
 
    if escolha not in config:
        messagebox.showerror("Erro", "Escolha uma opção de conversão.")
        return
 
    c = config[escolha]
 
    arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=[("Arquivos suportados", "*" + c["in"])]
    )
 
    if not arquivo:
        return
 
    try:
        if c["in"] == ".xlsx":
            df = c["func_in"](arquivo)
        else:
            df = c["func_in"](arquivo, sep=c["sep_in"])
 
        nome_base = os.path.splitext(arquivo)[0]
        nome_saida = nome_base + c["out"]
 
        if c["func_out"] == "to_excel":
            df.to_excel(nome_saida, index=False, engine="openpyxl")
        else:
            df.to_csv(nome_saida, index=False, sep=c.get("sep_out", ","))
 
        messagebox.showinfo("Sucesso", f"Arquivo convertido!\n\n{nome_saida}")
 
    except Exception as e:
        messagebox.showerror("Erro", str(e))
 
 
# Criar janela
janela = tk.Tk()
janela.title("Conversor Universal de Arquivos")
janela.geometry("420x320")
janela.resizable(False, False)
 
titulo = tk.Label(janela, text="🛠️ Conversor de Arquivos", font=("Arial", 16))
titulo.pack(pady=15)
 
opcao = tk.StringVar()
 
opcoes = [
    ("CSV ➜ XLSX", "1"),
    ("TSV ➜ XLSX", "2"),
    ("TSV ➜ CSV", "3"),
    ("CSV ➜ TSV", "4"),
    ("XLSX ➜ CSV", "5"),
    ("XLSX ➜ TSV", "6"),
]
 
for texto, valor in opcoes:
    tk.Radiobutton(
        janela,
        text=texto,
        variable=opcao,
        value=valor,
        font=("Arial", 11)
    ).pack(anchor="w", padx=80)
 
botao = tk.Button(
    janela,
    text="Selecionar arquivo e converter",
    command=converter,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12),
    padx=10,
    pady=5
)
 
botao.pack(pady=20)
 
janela.mainloop()