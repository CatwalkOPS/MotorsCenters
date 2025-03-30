# Loja de Peças de Moto

Um sistema web para gerenciamento de vendas de peças de moto com área administrativa.

## Funcionalidades

- Sistema de login e registro de usuários
- Área administrativa para gerenciamento de produtos
- Upload de imagens para produtos
- Visualização de produtos na página inicial
- Interface responsiva e moderna

## Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
SECRET_KEY=sua_chave_secreta_aqui
```

## Executando o Projeto

1. Inicie o servidor Flask:
```bash
python app.py
```

2. Acesse o site no navegador:
```
http://localhost:5000
```

## Credenciais do Administrador

- Email: admin@admin.com
- Senha: admin123

## Estrutura do Projeto

```
.
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências do projeto
├── static/            # Arquivos estáticos
│   ├── css/          # Arquivos CSS
│   └── uploads/      # Imagens enviadas
└── templates/         # Templates HTML
    ├── base.html
    ├── index.html
    ├── login.html
    ├── registro.html
    └── admin_produtos.html
```

## Tecnologias Utilizadas

- Flask (Framework web)
- SQLite (Banco de dados)
- Bootstrap 5 (Framework CSS)
- Flask-Login (Autenticação)
- Flask-SQLAlchemy (ORM) 