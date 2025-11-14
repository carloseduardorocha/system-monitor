# 🖥️ Sistema de Monitoramento de Hardware

Sistema cliente/servidor para monitoramento de recursos de hardware (CPU, Memória, Disco e Processos) com interface web para visualização dos dados.

## 📋 Descrição

O sistema é composto por três componentes:

1. **Cliente** - Coleta informações do sistema a cada 5 segundos e envia via UDP
2. **Servidor** - Recebe os pacotes UDP e armazena no banco de dados MySQL
3. **Interface Web** - Dashboard para visualização dos dados em tempo real

---

## 🛠️ Tecnologias Utilizadas

- **Python 3** - Linguagem principal
- **MySQL** - Banco de dados
- **Flask** - Framework web
- **psutil** - Coleta de informações do sistema
- **Chart.js** - Gráficos interativos
- **UDP Sockets** - Comunicação cliente/servidor

---

## 📁 Estrutura do Projeto

```
~/monitor/
├── venv/                    # Ambiente virtual Python
├── client/                  # Módulo cliente
│   ├── client.py           # Script principal do cliente
│   └── config.py           # Configurações do cliente
├── server/                  # Módulo servidor
│   ├── server.py           # Script principal do servidor
│   ├── database.py         # Funções de banco de dados
│   └── config.py           # Configurações do servidor
├── web/                     # Interface web
│   ├── app.py              # Aplicação Flask
│   ├── config.py           # Configurações web
│   └── templates/
│       └── index.html      # Template HTML
├── sql/
│   └── create_tables.sql   # Script de criação das tabelas
└── README.md               # Este arquivo
```

---

## ⚙️ Pré-requisitos

- Ubuntu/Linux
- Python 3
- MySQL Server
- pip3

---

## 🚀 Como Executar o Projeto

### 1️⃣ Ativar o Ambiente Virtual

Sempre que for trabalhar no projeto, você precisa ativar o ambiente virtual:

```bash
cd ~/monitor
source venv/bin/activate
```

✅ Quando ativado, você verá `(venv)` no início da linha do terminal.

---

### 2️⃣ Executar o Sistema

Você precisa abrir **3 terminais separados** e executar cada componente:

#### **Terminal 1 - Servidor UDP**

```bash
cd ~/monitor
source venv/bin/activate
cd server
python3 server.py
```

Você deve ver:
```
============================================================
SERVIDOR DE MONITORAMENTO
============================================================
Escutando na porta UDP 5000
Aguardando pacotes... (Ctrl+C para parar)
============================================================
```

---

#### **Terminal 2 - Cliente (Monitoramento)**

Abra um **novo terminal**:

```bash
cd ~/monitor
source venv/bin/activate
cd client
python3 client.py
```

Você deve ver:
```
============================================================
CLIENTE DE MONITORAMENTO
============================================================
Servidor: 127.0.0.1:5000
Intervalo de coleta: 5 segundos
============================================================
✓ Pacote enviado - CPU: 15.2% | MEM: 45.8% | DISCO: 67.3%
```

---

#### **Terminal 3 - Interface Web**

Abra um **novo terminal**:

```bash
cd ~/monitor
source venv/bin/activate
cd web
python3 app.py
```

Você deve ver:
```
============================================================
INTERFACE WEB DE MONITORAMENTO
============================================================
Acesse: http://localhost:8080
============================================================
```

---

### 3️⃣ Acessar a Interface Web

Abra seu navegador e acesse:

```
http://localhost:8080
```

A página exibe:
- 📊 **Estatísticas gerais** (total de registros, médias)
- 📈 **Gráfico** com dados dos últimos 5 minutos
- 📋 **Tabela** com os últimos 50 registros

Para atualizar os dados, pressione **F5** ou clique no botão **🔄 Atualizar**.

---

## 🛑 Como Parar o Sistema

Para parar cada componente, pressione **Ctrl+C** no respectivo terminal:

1. Terminal do Servidor → `Ctrl+C`
2. Terminal do Cliente → `Ctrl+C`
3. Terminal da Web → `Ctrl+C`

---

## 🔧 Desativar o Ambiente Virtual

Quando terminar de trabalhar no projeto:

```bash
deactivate
```

O `(venv)` desaparecerá do terminal.

---

## ⚙️ Configurações

### Intervalo de Coleta

Para mudar o intervalo de coleta (padrão: 5 segundos):

```bash
nano ~/monitor/client/config.py
```

Altere a linha:
```python
INTERVALO_COLETA = 5  # Mude para o valor desejado em segundos
```

### Credenciais do Banco de Dados

Se precisar alterar usuário/senha do MySQL:

1. **Servidor**:
```bash
nano ~/monitor/server/config.py
```

2. **Interface Web**:
```bash
nano ~/monitor/web/config.py
```

Altere a seção `DB_CONFIG`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'monitor'
}
```

---

## 🗄️ Banco de Dados

### Acessar o MySQL via Terminal

```bash
mysql -u root -p
```

Depois digite a senha: `root`

### Comandos Úteis

```sql
-- Ver banco de dados
USE monitor;

-- Ver total de registros
SELECT COUNT(*) FROM monitoring_data;

-- Ver últimos 10 registros
SELECT * FROM monitoring_data ORDER BY tempo DESC LIMIT 10;

-- Limpar todos os dados (cuidado!)
DELETE FROM monitoring_data;

-- Sair
EXIT;
```

### Acessar via PHPMyAdmin

Se você tem PHPMyAdmin instalado:

```
http://localhost/phpmyadmin
```

**Login:**
- Usuário: `root`
- Senha: `root`
- Banco: `monitor`

---

## 🐛 Resolução de Problemas

### Erro: "Can't connect to MySQL server"

Verifique se o MySQL está rodando:
```bash
sudo systemctl status mysql
sudo systemctl start mysql
```

### Erro: "Address already in use"

Algum processo já está usando a porta. Mate o processo:
```bash
# Para porta 5000 (servidor UDP)
sudo lsof -t -i:5000 | xargs kill -9

# Para porta 8080 (web)
sudo lsof -t -i:8080 | xargs kill -9
```

### Dados não aparecem na interface web

1. Verifique se o servidor está rodando (Terminal 1)
2. Verifique se o cliente está enviando dados (Terminal 2)
3. Verifique se há dados no banco:
```bash
mysql -u root -proot -e "SELECT COUNT(*) FROM monitor.monitoring_data;"
```

---

## 📝 Informações Adicionais

### Protocolo de Comunicação

- **Protocolo**: UDP
- **Porta**: 5000
- **Formato**: JSON

### Exemplo de Pacote UDP

```json
{
    "ip_origem": "127.0.0.1",
    "ip_destino": "127.0.0.1",
    "uso_memoria": 45.2,
    "uso_cpu": 23.5,
    "uso_disco": 67.8,
    "processos": "python:1234, firefox:5678, systemd:1"
}
```