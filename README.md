# ADR Reviewer

Projeto para análise de Architecture Decision Records (ADRs).

## Configuração do Ambiente de Desenvolvimento

Este projeto usa Dev Containers para fornecer um ambiente de desenvolvimento consistente.

### Como usar

1. Abra o projeto no VS Code
2. Quando solicitado, clique em "Reopen in Container" ou use o comando `Dev Containers: Reopen in Container`
3. O container será construído automaticamente com Python 3.12 e todas as dependências

### Extensões Recomendadas

Após abrir no container, instale manualmente estas extensões do VS Code:

- **Python** (`ms-python.python`) - Suporte completo para Python
- **Black Formatter** (`ms-python.black-formatter`) - Formatação automática de código
- **isort** (`ms-isort.isort`) - Organização automática de imports

### Configurações Automáticas

O dev container já configura automaticamente:
- Formatação com Black ao salvar
- Organização de imports com isort
- Linting com Pylint
- Testes com pytest
- Interpretador Python padrão

### SSH Keys

Suas chaves SSH do host são automaticamente montadas no container. Certifique-se de que as permissões estejam corretas no host (chmod 600 para chaves privadas, 700 para ~/.ssh).

### Instalação das Dependências

Após abrir no container, as dependências Python são instaladas automaticamente. Se por algum motivo não forem instaladas, execute manualmente:

```bash
pip install -e .[dev]
```

### Estrutura do Projeto

```
.
├── .devcontainer/          # Configuração do dev container
│   ├── devcontainer.json
│   └── Dockerfile
├── pyproject.toml          # Configuração do projeto Python
└── src/                    # Código fonte
```
