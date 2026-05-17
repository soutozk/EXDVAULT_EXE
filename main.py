import os
import json
import customtkinter as ctk
import re
import hashlib
import requests
from tkinter import messagebox

from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ctk.set_appearance_mode("dark")

VAULT_FILE = "vault.enc"
SALT_FILE = "salt.bin"  

# ----------------------------
# API: SENHAS VAZADAS (HIBP)
# ----------------------------

def check_password_pwned(password: str) -> bool:
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return False

        hashes = (line.split(":") for line in res.text.splitlines())
        return any(h == suffix for h, _ in hashes)

    except:
        return False
# ----------------------------
# CRIPTOGRAFIA
# ----------------------------

# gera a chave de criptografia (Essa função transforma a senha do usuário em uma chave criptográfica forte, utilizando argon2)
# password.encode() = transforma a senha em bytes
# time_cost=3 = quantas vezes o algoritimo roda 
# memory_cost=65536 = quantidade de memoria usada em kb (65536 kb = 64 mb)
# parallelism=4 = Número de threads usadas do processador 
#hash_len=32 = tamanho da chave gerada, 32 = 256 bits (tamanho de bits usados no AES-256)
def derive_key(password, salt):
    return hash_secret_raw(
        password.encode(),
        salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )


def encrypt(data, key):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aes.encrypt(nonce, data.encode(), None)
    return nonce + ciphertext


def decrypt(blob, key):
    aes = AESGCM(key)
    nonce = blob[:12]
    ciphertext = blob[12:]
    return aes.decrypt(nonce, ciphertext, None).decode()


# ----------------------------
# PRIMEIRO SETUP
# ----------------------------

def first_setup():

    result = {"key": None, "vault": None}

    def criar_senha():

        password = entry.get()

        if len(password) < 8:
            status.configure(text="Senha mínima 8 caracteres")
            return

        if not re.search(r"[A-Z]", password):
            status.configure(text="Senha deve ter pelo menos uma letra maiúscula")
            return
        if not re.search(r"[a-z]", password):
            status.configure(text="Senha deve ter pelo menos uma letra minúscula")
            return
        if not re.search(r"[0-9]", password):
            status.configure(text="Senha deve ter pelo menos um número")
            return
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            status.configure(text="Senha deve ter pelo menos um caractere especial")
            return
       #API CHECK AQUI
        status.configure(text="Verificando vazamentos...")
        root.update()

        if check_password_pwned(password):
            status.configure(text="Senha vazada em leaks! escolha outra")
            return
            
        salt = os.urandom(16)

        with open(SALT_FILE, "wb") as f:
            f.write(salt)

        key = derive_key(password, salt)

        vault = {
            "Redes_sociais": {},
            "Apps": {},
            "Sites": {},
            "Bancos_de_dados": {},
            "Faculdade": {},
            "Outros": {}
        }

        encrypted = encrypt(json.dumps(vault), key)

        with open(VAULT_FILE, "wb") as f:
            f.write(encrypted)

        result["key"] = key
        result["vault"] = vault

        root.destroy()

    
    root = ctk.CTk()
    root.title("ExdVault - Primeiro Acesso")
    root.geometry("450x300")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(
        frame,
        text="ExdVault",
        font=("Arial", 24, "bold")
    )
    titulo.pack(pady=(20,5))

    subtitulo = ctk.CTkLabel(
        frame,
        text="Crie sua senha mestre",
        font=("Arial", 14)
    )
    subtitulo.pack(pady=(0,20))

    entry = ctk.CTkEntry(
        frame,
        placeholder_text="Digite sua senha",
        show="*",
        width=270,
        height=40,
    )
    entry.pack(padx=40)

    botao = ctk.CTkButton(
        frame,
        text="Criar Vault",
        width=270,
        height=40,
        font=("Arial", 16, "bold"),
        fg_color="#5E00AA",
        hover_color="#420079",
        command=criar_senha
    )
    botao.pack(pady=15)

    status = ctk.CTkLabel(frame, text="", text_color="red")
    status.pack(pady=5)

    root.mainloop()

    return result["key"], result["vault"]


# ----------------------------
# LOGIN
# ----------------------------

def open_vault():

    result = {"key": None, "vault": None}

    def login():

        password = entry.get()

        with open(SALT_FILE, "rb") as f:
            salt = f.read()

        key = derive_key(password, salt)

        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()

        try:

            data = decrypt(encrypted, key)
            vault = json.loads(data)

            result["key"] = key
            result["vault"] = vault

            root.destroy()

        except:
            status.configure(text="Senha incorreta")

    root = ctk.CTk()
    root.title("ExdVault - Login")
    root.geometry("450x280")
    root.resizable(False, False)

    frame = ctk.CTkFrame(root, corner_radius=15)
    frame.pack(expand=True, padx=30, pady=30)

    titulo = ctk.CTkLabel(
        frame,
        text="ExdVault",
        font=("Arial", 24, "bold")
    )
    titulo.pack(pady=(20,5))

    subtitulo = ctk.CTkLabel(
        frame,
        text="Digite sua senha mestre",
        font=("Arial", 14)
    )
    subtitulo.pack(pady=(0,20))

    entry = ctk.CTkEntry(
        frame,
        placeholder_text="Senha mestre",
        show="*",
        width=270,
        height=40
    )
    entry.pack(padx=40)

    botao = ctk.CTkButton(
        frame,
        text="Abrir Vault",
        width=270,
        height=40,
        font=("Arial", 16, "bold"),
        fg_color="#5E00AA",
        hover_color="#420079",
        command=login
    )
    botao.pack(pady=15)

    status = ctk.CTkLabel(frame, text="", text_color="red")
    status.pack()

    root.mainloop()

    return result["key"], result["vault"]


# ----------------------------
# SALVAR
# ----------------------------

def save_vault(vault, key):

    encrypted = encrypt(json.dumps(vault), key)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)


# ----------------------------
# INTERFACE PRINCIPAL
# ----------------------------

class VaultGUI:

    def __init__(self, key, vault):

        self.key = key
        self.vault = vault

        self.root = ctk.CTk()
        self.root.title("ExdVault")
        self.root.geometry("520x420")

        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, padx=20, pady=20, fill="both")

        ctk.CTkLabel(frame, text="ExdVault", font=("Arial", 26, "bold")).pack(pady=10)

        self.category = ctk.StringVar(value="Redes_sociais")

        self.menu = ctk.CTkOptionMenu(
        frame,
    values=list(vault.keys()),
    variable=self.category,
    font=("Arial", 14, "bold"),
    fg_color="#5E00AA",
    button_color="#5E00AA",
    button_hover_color="#420079",
    dropdown_fg_color="#2b2b2b",
    dropdown_hover_color="#420079",
    text_color="white",
    width=200,
    height=35
)

        self.menu.pack(pady=10)

        

        self.textbox = ctk.CTkTextbox(
        frame,
        width=420,
        height=200,
        state="disabled"
        )
        self.textbox.pack(pady=10)

        buttons = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.pack()

        ctk.CTkButton(
        buttons, 
        text="Ver", 
        font=("Arial", 14, "bold"),
        fg_color="#5E00AA",
        hover_color="#420079",
        command=self.view
        ).grid(row=0, column=0, padx=5)

        ctk.CTkButton(
        buttons,
        text="Adicionar",
        font=("Arial", 14, "bold"),
        fg_color="#5E00AA",
        hover_color="#420079", 
        command=self.add
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(
        buttons, 
        text="Salvar", 
        font=("Arial", 14, "bold"),
        fg_color="#5E00AA",
        hover_color="#420079",
        command=self.save
        ).grid(row=0, column=2, padx=5)

        self.root.mainloop()

    def view(self):

        cat = self.category.get()
        self.textbox.configure(state="normal")  
        self.textbox.delete("1.0", "end")

        items = self.vault.get(cat, {})

        if not items:
            self.textbox.insert("end", "Categoria vazia")
            return
        else:
         for name, data in items.items():

            self.textbox.insert(
                "end",
                f"{name}\nUsuário: {data['usuario']}\nSenha: {data['senha']}\n\n"
            )
        self.textbox.configure(state="disabled")

    def add(self):

        window = ctk.CTkToplevel(self.root)
        window.title("Adicionar")
        window.geometry("300x230")

        cat = self.category.get()

        ctk.CTkLabel(window, text="Serviço").pack()
        name = ctk.CTkEntry(window)
        name.pack(pady=5)

        ctk.CTkLabel(window, text="Usuário").pack()
        user = ctk.CTkEntry(window)
        user.pack(pady=5)

        ctk.CTkLabel(window, text="Senha").pack()
        pwd = ctk.CTkEntry(window)
        pwd.pack(pady=5)

        def salvar():

            n = name.get()

            if not n:
                return

            self.vault[cat][n] = {
                "usuario": user.get(),
                "senha": pwd.get()
            }

            window.destroy()

        ctk.CTkButton(window, text="Salvar", command=salvar).pack(pady=10)

    def save(self):

        save_vault(self.vault, self.key)
        messagebox.showinfo("ExdVault", "Vault salvo")


# ----------------------------
# MAIN
# ----------------------------

if not os.path.exists(VAULT_FILE):

    key, vault = first_setup()

else:

    key, vault = open_vault()

VaultGUI(key, vault)