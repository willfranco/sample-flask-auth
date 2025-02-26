# API de Autenticação em Flask

Esta é uma API de autenticação desenvolvida com Flask, Flask-Login e Flask-Migrate, utilizando SQLite como banco de dados.

## Tecnologias Utilizadas
- Python 3
- Flask
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Bcrypt
- SQLite

## Configuração e Execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-repositorio.git
cd seu-repositorio
```

### 2. Criar e Ativar um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate  # Para Windows
```

### 3. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar a Base de Dados
```bash
flask db init
flask db migrate -m "Inicialização do banco"
flask db upgrade
```

### 5. Executar a API
```bash
python app.py
```

A API estará rodando em `http://127.0.0.1:5000/`

## Endpoints

### 1. Testar se a API está funcionando
**GET /**
```json
{
    "message": "API Flask funcionando!"
}
```

### 2. Criar um Usuário
**POST /user**
#### Requisição
```json
{
    "username": "usuario",
    "password": "senha123"
}
```
#### Resposta
```json
{
    "message": "Usuário cadastrado com sucesso"
}
```

### 3. Login
**POST /login**
#### Requisição
```json
{
    "username": "usuario",
    "password": "senha123"
}
```
#### Resposta
```json
{
    "message": "Autenticação realizada com sucesso"
}
```

### 4. Logout
**GET /logout**
#### Resposta
```json
{
    "message": "Logout realizado com sucesso!"
}
```

### 5. Obter Dados do Usuário
**GET /user/{id_user}** *(Requer Autenticação)*
#### Resposta
```json
{
    "username": "usuario",
    "role": "user"
}
```

### 6. Atualizar Senha do Usuário
**PUT /user/{id_user}** *(Requer Autenticação)*
#### Requisição
```json
{
    "password": "novaSenha123"
}
```
#### Resposta
```json
{
    "message": "Usuário {id_user} atualizado com sucesso"
}
```

### 7. Deletar Usuário
**DELETE /user/{id_user}** *(Apenas Admin)*
#### Resposta
```json
{
    "message": "Usuário {id_user} deletado com sucesso"
}
```

## Autenticação e Permissões
- Apenas usuários autenticados podem acessar seus próprios dados e atualizar sua senha.
- Apenas administradores podem deletar outros usuários.

