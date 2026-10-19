# ❤️ Medidor de Pressão (Django)

Hackathon: CRUD básico com autenticação de usuário em Django.
Cada usuário cadastra, lista, edita e exclui **apenas as suas** medições de pressão arterial,
com classificação automática e médias.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations pressao
python manage.py migrate
python manage.py runserver
```

Acesse http://127.0.0.1:8000 e crie uma conta em "Cadastrar".
(Opcional: `python manage.py createsuperuser` para usar o /admin.)

## Funcionalidades
- Cadastro, login e logout
- **C**reate: registrar medição (sistólica, diastólica, pulso, data/hora, observação)
- **R**ead: lista com média, pulso médio e classificação colorida
- **U**pdate: editar medição
- **D**elete: excluir com confirmação
- Isolamento por usuário (ninguém vê dados de outro)

> Projeto acadêmico. Não substitui orientação médica.
