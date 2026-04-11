<img width="861" height="269" alt="image" src="https://github.com/user-attachments/assets/357dcdbd-5c50-484e-942e-b9c7c30fc0fb" />

## 📌 Sobre o Projeto

O **ExdVault** é uma aplicação desktop desenvolvida em Python que permite o armazenamento seguro de credenciais (usuários e senhas) por meio de criptografia forte.

A aplicação utiliza uma **senha mestre** para proteger todos os dados armazenados, garantindo que apenas o usuário autorizado consiga acessá-los.

---

## 🚨 Problema

Muitas pessoas armazenam suas senhas de forma insegura, como:

- Bloco de notas
- Planilhas sem proteção
- Anotações físicas
- Reutilização de senhas simples

Isso expõe dados sensíveis a riscos como:

- Vazamento de informações
- Acesso indevido a contas pessoais
- Roubo de identidade digital

---

## 💡 Solução Proposta

O ExdVault resolve esse problema oferecendo:

- Armazenamento local criptografado
- Proteção por senha mestre
- Organização por categorias
- Interface gráfica simples e intuitiva

Todos os dados são criptografados utilizando algoritmos modernos antes de serem salvos no disco.

---

## 👥 Público-Alvo

- Usuários que desejam armazenar senhas com segurança
- Estudantes e profissionais de tecnologia
- Pessoas que buscam uma alternativa simples a gerenciadores de senha complexos

---

## ✨ Funcionalidades

- 🔐 Criação de cofre seguro (vault)
- 🔑 Autenticação via senha mestre
- 📂 Organização por categorias:

  - Redes sociais
  - Apps
  - Sites
  - Bancos de dados
  - Faculdade
  - Outros

- ➕ Adição de credenciais (serviço, usuário e senha)
- 👁️ Visualização das credenciais
- 💾 Salvamento criptografado em arquivo local

---

## 🔒 Segurança

O projeto utiliza práticas modernas de segurança:

- **Argon2** para derivação de chave (proteção contra brute force)
- **AES-GCM (256 bits)** para criptografia autenticada
- Uso de **salt aleatório**
- Armazenamento seguro em arquivo binário

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- customtkinter
- cryptography
- argon2-cffi
- json

---

## 📦 Estrutura do Projeto

```
ExdVault/
├── main.py
├── requirements.txt
├── VERSION
├── README.md
├── tests/
│   └── test_crypto.py
└── .github/
    └── workflows/
        └── ci.yml
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```
git clone https://github.com/seu-usuario/exdvault.git
cd exdvault
```

### 2. Instale as dependências

```
pip install -r requirements.txt
```

---

## ▶️ Execução

```
python main.py
```

---

## 🧪 Testes Automatizados

Execute os testes com:

```
pytest
```

---

## 🧹 Análise de Código (Lint)

Execute o lint com:

```
ruff .
```

---

## 🔄 Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para:

- Instalar dependências automaticamente
- Executar lint
- Rodar testes automatizados

A pipeline é executada a cada:

- push
- pull request

---

## 📊 Versionamento

Este projeto segue **Versionamento Semântico (SemVer)**:

```
MAJOR.MINOR.PATCH
```

Versão atual:

```
1.0.0
```

---

## 📁 Armazenamento de Dados

Os dados são armazenados localmente em:

- `vault.enc` → dados criptografados
- `salt.bin` → salt utilizado na derivação da chave

⚠️ Importante:
Sem a senha mestre correta, os dados não podem ser recuperados.

---

## 📸 Exemplo de Uso

1. Criar senha mestre
2. Selecionar categoria
3. Adicionar credenciais
4. Visualizar dados salvos
5. Salvar cofre

---

## ⚠️ Limitações

- Armazenamento apenas local
- Não possui backup automático
- Não há recuperação de senha mestre

---

## 🚀 Melhorias Futuras

- Exportação criptografada
- Backup em nuvem
- Gerador de senhas seguras
- Autopreenchimento
- Interface mais avançada

---

## 👨‍💻 Autor

<h1>João Gabriel Souto</h1>

<div>
  <a href="https://www.linkedin.com/in/gabrielsouto01/" target="_blank">
    <img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white">
  </a>
  <a href="https://github.com/soutozk" target="_blank">
    <img src="https://img.shields.io/badge/-GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
  </a>
</div>

---

## 📄 Licença

Este projeto é livre para fins educacionais.
