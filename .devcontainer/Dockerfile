FROM alpine:3.20

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependências do sistema
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    curl \
    bash \
    zsh \
    openssh-client \
    ca-certificates \
    build-base \
    python3-dev

# Criar symlink para python
RUN ln -sf /usr/bin/python3 /usr/local/bin/python && \
    ln -sf /usr/bin/python3 /usr/bin/python

# Criar usuário não-root para desenvolvimento
RUN addgroup -g 1000 vscode && \
    adduser -D -u 1000 -G vscode vscode && \
    mkdir -p /home/vscode/.vscode-server && \
    chown -R vscode:vscode /home/vscode

# Instalar ferramentas de desenvolvimento Python
RUN pip install --upgrade pip setuptools wheel --break-system-packages

# Mudar para o usuário vscode
USER vscode

# Instalar Oh My Zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Instalar Powerlevel10k
RUN git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Configurar Zsh como shell padrão e tema
RUN sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="powerlevel10k\/powerlevel10k"/g' ~/.zshrc && \
    echo 'export PATH=$PATH:/home/vscode/.local/bin' >> ~/.zshrc

# Definir Zsh como shell padrão
USER root
RUN sed -i 's|/bin/ash|/bin/zsh|g' /etc/passwd
USER vscode

WORKDIR /workspace
