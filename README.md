# Águas para Viver — POC

Mapeamento e acompanhamento de nascentes em **Pará de Minas/MG**.

O Águas para Viver tem como objetivo contribuir para a identificação, o mapeamento, a preservação e o acompanhamento das nascentes existentes no município de Pará de Minas/MG, por meio de uma plataforma web colaborativa.

A proposta é disponibilizar um ambiente no qual a população possa contribuir ativamente com a identificação de nascentes, realizando seus cadastros e compartilhando informações, imagens e localizações. Essas contribuições passam por um processo de análise e validação realizado por administradores responsáveis, garantindo maior organização e confiabilidade às informações disponibilizadas.

Dessa forma, o projeto busca aproximar a comunidade das iniciativas de preservação dos recursos hídricos locais, facilitando o acesso às informações sobre as nascentes identificadas e oferecendo uma ferramenta de apoio ao monitoramento e à gestão ambiental do município.

Além disso, a plataforma pretende servir como uma base inicial para a construção de um inventário geográfico das nascentes de Pará de Minas, incentivando a conscientização ambiental e a participação da sociedade na proteção dos recursos naturais.

> **Escopo restrito:** o projeto é voltado à realidade do município de Pará de Minas. O mapa é centrado na cidade e a lógica de cadastro/validação foi pensada para esse contexto local.

## Sobre o projeto

Esta seção será complementada manualmente com o contexto institucional, os objetivos gerais, o público-atendido e os critérios de uso da plataforma.

Como base inicial: o Águas para Viver é uma aplicação web para registrar nascentes, visualizá-las em um mapa interativo e permitir que uma equipe responsável analise, valide e acompanhe as informações cadastradas pela comunidade. Cada nascente possui status de validação, histórico de visitas e documentos associados.

## Funcionalidades

- **Mapa interativo:** visualização das nascentes com marcadores coloridos por status, legenda, controles de navegação, localização do usuário e link para abrir o ponto no Google Maps.
- **Cadastro de nascente:** usuário autenticado escolhe a coordenada no mapa e informa endereço, foto e descrição. O registro entra com status `PENDENTE`.
- **Listagem pública:** página inicial com as nascentes cadastradas.
- **Painel administrativo:** listagem de nascentes pendentes e aprovadas, com acesso a detalhes e edição.
- **Validação e edição:** o administrador pode validar uma nascente, atualizar endereço, coordenadas, descrição e imagem, ou excluir o registro.
- **Histórico de visitas:** cada atualização feita pelo administrador registra uma visita com imagem e descrição, permitindo consultar o histórico da nascente.
- **Documentos:** anexar, listar, abrir e excluir arquivos PDF por nascente.
- **Autenticação:** login, cadastro de novos membros, logout e controle de acesso por sessão.

Os status utilizados no fluxo são `PENDENTE` e `APROVADA`; a legenda do mapa também prevê `DESAPROVADA`.

## Divisão de tipos de usuários

| Perfil | Como é obtido | Permissões |
| --- | --- | --- |
| **Visitante** | Acesso sem login | Visualizar a página inicial e o mapa, consultar a legenda e se cadastrar como membro. Não cadastra nascentes nem acessa o painel administrativo. |
| **MEMBRO** | Cadastro público ou usuário padrão | Tudo o que o visitante pode fazer, mais o cadastro de novas nascentes. Não acessa rotas administrativas. |
| **ADMINISTRADOR** | Usuário padrão criado no bootstrap | Tudo o que o membro pode fazer, mais o painel de nascentes, validação/edição/exclusão, histórico de visitas e gerenciamento de documentos. |

O tipo fica armazenado no campo `tipoUsuario` do model `Usuario`. O visitante é um estado implícito (sem sessão), não um tipo persistido no banco.

## Tecnologias principais

| Camada | Tecnologias |
| --- | --- |
| **Frontend** | HTML, Jinja2 (templates do Flask), CSS e JavaScript puros, MapLibre GL JS `4.7.1` via CDN, tiles do OpenFreeMap e Google Fonts. |
| **Backend** | Python e Flask, com renderização server-side, sessões para autenticação e camada DAO para acesso aos dados. |
| **Banco de dados** | SQLite, acessado via SQLAlchemy / Flask-SQLAlchemy com models ORM. |
| **Bibliotecas Python** | `flask`, `flask_sqlalchemy`, `sqlalchemy` e `werkzeug` (este último usado para uploads seguros). |

Ainda não há `requirements.txt` ou `package.json` versionados; as dependências Python precisam ser instaladas manualmente e as bibliotecas de front são carregadas por CDN.

## Arquivos principais

- `app/app.py`: aplicação Flask, rotas, autenticação, uploads de imagem/PDF e inicialização do banco.
- `app/extensions.py`: instância do SQLAlchemy compartilhada pelos models e DAOs.
- `app/models/`: entidades `Usuario`, `Nascente`, `VisitaNascente` e `DocumentoNascente`.
- `app/dao/`: operações de criação, leitura, atualização e exclusão organizadas por entidade.
- `app/seed.py`: criação dos usuários padrão (`ADMINISTRADOR` e `MEMBRO`).
- `app/templates/`: páginas Jinja2, incluindo `base.html`, `login.html`, `register.html`, `mapa.html`, `nascentes.html`, `cadastrarNascente.html`, `dashboardNascentes.html`, `detalhesNascente.html`, `editarNascente.html`, `historicoVisitas.html` e `documentosNascente.html`.
- `app/static/css/style.css`: estilos da aplicação.
- `app/static/js/main.js`: comportamentos compartilhados do front (senha, confirmação, prévia de imagem, carrossel e modais).
- `app/static/img/` e `app/static/uploads/`: imagens do projeto e arquivos enviados pelos usuários.
- `app/database.db` e `database/database.db`: arquivos SQLite do projeto.

## Execução local

Com as dependências instaladas, execute a aplicação de dentro da pasta `app` (os imports são relativos a essa pasta):

```bash
pip install flask flask-sqlalchemy
cd app
python app.py
```

Na primeira execução, `db.create_all()` cria as tabelas e `criarUsuariosPadrao()` cria os usuários padrão. A chave da sessão pode ser definida pela variável de ambiente `SECRET_KEY`.
