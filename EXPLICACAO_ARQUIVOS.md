# 📚 Explicação dos Arquivos do Sistema

## 🎯 Visão Geral do Sistema

O sistema segue a arquitetura **cliente-servidor** solicitada no trabalho, com 3 componentes principais:

1. **Cliente** - Coleta dados do hardware
2. **Servidor** - Recebe e armazena dados
3. **Interface Web** - Visualiza os dados

---

## 📁 Estrutura de Pastas e Arquivos

```
~/monitor/
├── venv/                    # Ambiente virtual Python
├── client/                  # Módulo Cliente
├── server/                  # Módulo Servidor
├── web/                     # Módulo Interface Web
├── sql/                     # Scripts de banco de dados
├── .gitignore              # Controle de versionamento
└── README.md               # Documentação
```

---

## 🔵 1. VENV (Ambiente Virtual)

### O que é?
Uma **máquina virtual Python** isolada para o projeto.

### Para que serve?
- Isola as bibliotecas do projeto das bibliotecas do sistema
- Evita conflitos de versões
- Facilita distribuição (outras pessoas instalam as mesmas versões)

### Como funciona?
Quando você ativa com `source venv/bin/activate`, o Python passa a usar apenas as bibliotecas instaladas dentro dessa pasta, não as do sistema.

### Arquivos principais:
- `venv/bin/python3` - Interpretador Python isolado
- `venv/lib/` - Bibliotecas instaladas (psutil, flask, etc)

**📌 NÃO deve ser commitado no Git** (é muito grande e cada máquina cria o seu próprio)

---

## 🟢 2. CLIENT/ (Módulo Cliente)

### Função Geral
**Coleta informações de hardware do sistema e envia para o servidor via UDP.**

---

### `client/client.py` - Script Principal do Cliente

**O que faz:**
- Coleta dados do sistema operacional a cada X segundos
- Monta um pacote JSON com as informações
- Envia o pacote via protocolo UDP para o servidor

**Principais funções:**

```python
def obter_ip_local()
    # Descobre o IP da máquina atual

def coletar_uso_memoria()
    # Usa psutil.virtual_memory() para pegar uso de RAM

def coletar_uso_cpu()
    # Usa psutil.cpu_percent() para pegar uso do processador

def coletar_uso_disco()
    # Usa psutil.disk_io_counters() para calcular I/O do disco
    # Mede bytes lidos/escritos por segundo e converte para %

def coletar_processos()
    # Usa psutil.process_iter() para listar processos
    # Ordena por uso de CPU e pega os top 10

def montar_pacote()
    # Junta todos os dados coletados em um dicionário Python

def enviar_pacote()
    # Serializa o dicionário em JSON
    # Envia via socket UDP para o servidor
```

**Bibliotecas usadas:**
- `psutil` - Coleta informações do sistema (CPU, memória, disco, processos)
- `socket` - Comunicação de rede via UDP
- `json` - Serialização dos dados

**Loop principal:**
```python
while True:
    coletar dados → montar pacote → enviar UDP → aguardar 5 segundos
```

---

### `client/config.py` - Configurações do Cliente

**O que contém:**
```python
SERVER_IP = '127.0.0.1'      # Para onde enviar os dados
SERVER_PORT = 5000           # Porta UDP do servidor
INTERVALO_COLETA = 5         # Intervalo entre coletas (segundos)
IP_DESTINO = '127.0.0.1'     # IP de destino (mesmo do servidor)
```

**Por que separar configurações?**
- Facilita alterar sem mexer no código
- Pode ter valores diferentes por máquina
- Segurança (não commitar senhas)

---

## 🔴 3. SERVER/ (Módulo Servidor)

### Função Geral
**Recebe pacotes UDP dos clientes e armazena no banco de dados MySQL.**

---

### `server/server.py` - Script Principal do Servidor

**O que faz:**
- Cria um socket UDP e escuta na porta 5000
- Recebe pacotes dos clientes
- Deserializa o JSON
- Chama funções para gravar no banco de dados

**Principais funções:**

```python
def iniciar_servidor()
    # Cria socket UDP
    # Faz bind na porta 5000
    # Loop infinito esperando pacotes
    # Quando recebe: decodifica JSON e chama inserir_dados()
```

**Fluxo:**
```
Cliente envia UDP → Servidor recebe → Extrai JSON → Grava no MySQL
```

**Bibliotecas usadas:**
- `socket` - Recebe pacotes UDP
- `json` - Deserializa os dados recebidos

---

### `server/database.py` - Funções de Banco de Dados

**O que faz:**
Concentra todas as operações com MySQL em um único arquivo (organização).

**Principais funções:**

```python
def conectar_bd()
    # Cria conexão com MySQL usando mysql.connector
    # Retorna objeto de conexão

def inserir_dados(pacote)
    # Recebe o dicionário com os dados
    # Monta query SQL INSERT
    # Executa a inserção na tabela monitoring_data
    # Commit para salvar

def obter_ultimos_registros(limite=50)
    # SELECT dos últimos N registros
    # Usado pela interface web

def obter_estatisticas()
    # SELECT com funções agregadas (AVG, MAX, MIN, COUNT)
    # Calcula médias e totais
    # Usado pela interface web
```

**Por que separar database.py do server.py?**
- **Organização**: Cada arquivo tem uma responsabilidade
- **Reutilização**: A interface web também usa database.py
- **Manutenção**: Fácil mudar banco sem mexer no servidor

**Bibliotecas usadas:**
- `mysql.connector` - Driver oficial do MySQL para Python

---

### `server/config.py` - Configurações do Servidor

**O que contém:**
```python
SERVER_PORT = 5000           # Porta UDP para escutar

DB_CONFIG = {                # Credenciais do MySQL
    'host': 'localhost',
    'user': 'monitor_user',
    'password': 'senha123',   # ⚠️ NÃO commitar com senha real!
    'database': 'monitoring_db'
}
```

**Por que não colocar direto no código?**
- **Segurança**: Não expor senhas no GitHub
- **Flexibilidade**: Fácil mudar sem alterar código

---

## 🟣 4. WEB/ (Módulo Interface Web)

### Função Geral
**Fornece uma interface visual para visualizar os dados coletados.**

---

### `web/app.py` - Aplicação Flask

**O que faz:**
- Cria um servidor web HTTP com Flask
- Define rotas (URLs) que retornam dados ou páginas HTML
- Consulta o banco de dados e retorna em formato JSON

**Principais rotas:**

```python
@app.route('/')
    # Retorna a página HTML (index.html)

@app.route('/api/dados')
    # Consulta MySQL: últimos 50 registros
    # Retorna JSON para a tabela

@app.route('/api/estatisticas')
    # Consulta MySQL: médias, totais, etc
    # Retorna JSON para os cards de estatísticas

@app.route('/api/grafico')
    # Consulta MySQL: dados dos últimos 5 minutos
    # Retorna JSON para o gráfico Chart.js
```

**Arquitetura:**
```
Navegador → Flask (porta 8080) → MySQL → JSON → Navegador
```

**Bibliotecas usadas:**
- `flask` - Framework web Python
- `mysql.connector` - Acessa o banco de dados

---

### `web/templates/index.html` - Interface Visual

**O que faz:**
Página HTML/CSS/JavaScript que o usuário vê no navegador.

**Estrutura:**

1. **HTML** - Estrutura da página
   - Cards de estatísticas (Total, Média CPU, etc)
   - Container do gráfico
   - Tabela de registros

2. **CSS** - Estilo visual
   - Cores da UFSM (azul #003366)
   - Layout responsivo (Grid CSS)
   - Cards com sombras e bordas arredondadas

3. **JavaScript** - Lógica e interatividade
   ```javascript
   carregarEstatisticas()  // Busca dados em /api/estatisticas
   carregarGrafico()       // Busca dados em /api/grafico
   carregarDados()         // Busca dados em /api/dados
   ```

**Bibliotecas JavaScript:**
- `Chart.js` - Cria o gráfico de linhas interativo

**Fluxo de atualização:**
```
1. Página carrega
2. JavaScript faz fetch('/api/dados')
3. Servidor retorna JSON
4. JavaScript preenche a tabela HTML
5. A cada 3 segundos, atualiza só o gráfico
```

---

### `web/static/` - Arquivos Estáticos

```
static/
└── images/
    └── logo.png    # Logo da UFSM
```

**O que são arquivos estáticos?**
Arquivos que não mudam (imagens, CSS, JS externos). O Flask os serve diretamente sem processar.

---

### `web/config.py` - Configurações Web

**O que contém:**
```python
WEB_PORT = 8080              # Porta HTTP do servidor web

DB_CONFIG = {                # Mesmas credenciais do server
    'host': 'localhost',
    'user': 'monitor_user',
    'password': 'senha123',
    'database': 'monitoring_db'
}

DEBUG = True                 # Modo debug (mostra erros detalhados)
```

---

## 🗄️ 5. SQL/ (Scripts de Banco de Dados)

### `sql/create_tables.sql` - Criação da Tabela

**O que faz:**
Script SQL que cria a estrutura do banco de dados.

**Conteúdo:**
```sql
CREATE TABLE monitoring_data (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- ID único de cada registro
    ip_origem VARCHAR(45) NOT NULL,           -- IP do cliente
    ip_destino VARCHAR(45) NOT NULL,          -- IP do servidor
    uso_memoria FLOAT NOT NULL,               -- % de memória
    uso_cpu FLOAT NOT NULL,                   -- % de CPU
    uso_disco FLOAT NOT NULL,                 -- % de disco
    processos TEXT NOT NULL,                  -- Lista de processos
    tempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- Horário automático
    INDEX idx_tempo (tempo),                  -- Índice para buscar por data
    INDEX idx_ip_origem (ip_origem)           -- Índice para buscar por IP
);
```

**Por que usar índices?**
- Aceleram as consultas (SELECT) por tempo e IP
- Importante quando há muitos registros

**Tipos de dados:**
- `INT` - Números inteiros (id)
- `VARCHAR(45)` - Texto até 45 caracteres (IPs IPv4/IPv6)
- `FLOAT` - Números decimais (porcentagens)
- `TEXT` - Texto longo (lista de processos)
- `TIMESTAMP` - Data e hora

---

## 📄 6. Arquivos de Documentação

### `README.md`
- Visão geral do projeto
- Como executar
- Estrutura básica

### `INSTALACAO.md` (wiki)
- Passo a passo completo de instalação
- Troubleshooting
- Configuração para máquinas diferentes

### `.gitignore`
- Lista de arquivos que o Git deve ignorar
- Exemplos: venv/, __pycache__, config.py (com senhas)

---

## 🔄 Fluxo Completo do Sistema

```
┌─────────────────────────────────────────────────────────────┐
│  1. CLIENTE (client.py)                                     │
│     - Coleta: CPU, Memória, Disco, Processos, IP           │
│     - Monta JSON: {"ip_origem": "...", "uso_cpu": 15, ...} │
│     - Envia via UDP para porta 5000                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ UDP (Protocolo solicitado)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SERVIDOR (server.py)                                    │
│     - Recebe pacote UDP                                     │
│     - Deserializa JSON                                      │
│     - Chama database.py                                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL INSERT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. MYSQL (monitoring_db)                                   │
│     - Armazena na tabela monitoring_data                    │
│     - Adiciona timestamp automático                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ SQL SELECT
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. INTERFACE WEB (app.py)                                  │
│     - Rotas Flask retornam JSON                             │
│     - /api/dados → últimos 50 registros                     │
│     - /api/grafico → últimos 5 minutos                      │
│     - /api/estatisticas → médias e totais                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP JSON
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  5. NAVEGADOR (index.html)                                  │
│     - JavaScript faz fetch das APIs                         │
│     - Chart.js desenha gráfico                              │
│     - Tabela HTML mostra registros                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tecnologias Utilizadas por Arquivo

| Arquivo | Linguagem/Tecnologia | Bibliotecas Principais |
|---------|---------------------|------------------------|
| `client.py` | Python 3 | psutil, socket, json |
| `server.py` | Python 3 | socket, json |
| `database.py` | Python 3 | mysql.connector |
| `app.py` | Python 3 | flask, mysql.connector |
| `index.html` | HTML5 + CSS3 + JavaScript | Chart.js |
| `create_tables.sql` | SQL | MySQL |

---

## 📊 Por que essa Arquitetura?

### Separação de Responsabilidades
Cada módulo tem uma função específica:
- **Cliente** - Só coleta
- **Servidor** - Só recebe e armazena
- **Web** - Só visualiza

### Escalabilidade
- Pode ter **N clientes** monitorando várias máquinas
- **1 servidor central** recebendo tudo
- **1 interface web** mostrando dados de todos

### Manutenibilidade
- Trocar banco de dados? Só mexe em `database.py`
- Mudar interface? Só mexe em `index.html`
- Adicionar métrica? Só adiciona função no cliente

### Reutilização
- `database.py` é usado tanto pelo servidor quanto pela web
- `config.py` centraliza configurações

---

## 💡 Conceitos de Redes Aplicados

| Conceito | Onde foi usado |
|----------|----------------|
| **Protocolo UDP** | Comunicação cliente→servidor |
| **Sockets** | client.py e server.py |
| **Cliente/Servidor** | Arquitetura geral |
| **Serialização (JSON)** | Formato dos pacotes |
| **Endereço IP** | Identificação dos clientes |
| **Portas** | 5000 (UDP), 8080 (HTTP) |
| **Camada de Aplicação** | Protocolo customizado sobre UDP |

---

## ✅ Resumo para o Professor

**"Professor, o sistema tem 3 componentes principais:**

1. **venv/** - Ambiente virtual Python para isolar dependências

2. **client/** - Coleta informações do hardware (CPU, memória, disco, processos) usando a biblioteca `psutil` e envia via protocolo UDP para o servidor a cada 5 segundos

3. **server/** - Recebe os pacotes UDP, extrai os campos conforme solicitado e insere no banco de dados MySQL com timestamp automático

4. **web/** - Interface Flask que consulta o MySQL e exibe os dados em gráficos e tabelas para visualização

5. **sql/** - Scripts de criação da estrutura do banco de dados

**Todos os requisitos do trabalho foram atendidos: arquitetura cliente/servidor, protocolo UDP, coleta das 5 métricas solicitadas, pacotes com os campos especificados e armazenamento em banco de dados com timestamp."**
