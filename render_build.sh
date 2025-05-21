#!/bin/bash
set -e # Sai imediatamente se um comando sair com status diferente de zero.
set -x # Imprime os comandos e seus argumentos à medida que são executados (bom para depuração).

echo "--- Iniciando render_build.sh ---"

# Instala o Nixpacks (baixando primeiro)
echo "--- Instalando Nixpacks (baixando primeiro) ---"
if curl -sSL -o nixpacks_install.sh https://nixpacks.com/install.sh; then
    echo "Script de instalação do Nixpacks baixado como nixpacks_install.sh."
    # Dê permissão de execução
    chmod +x nixpacks_install.sh
    # Execute o script baixado
    # O script de instalação do Nixpacks pode precisar de argumentos se você quiser evitar o daemon,
    # mas geralmente ele se instala no diretório do usuário sem problemas.
    # A documentação do Nixpacks sugere: bash -s -- --no-daemon
    # Vamos tentar executar diretamente primeiro, e se necessário, invocar com bash.
    if ./nixpacks_install.sh; then
        echo "Script nixpacks_install.sh executado com sucesso."
    else
        echo "ERRO: Falha ao executar ./nixpacks_install.sh. Tentando com 'bash nixpacks_install.sh'..."
        # Segunda tentativa, invocando explicitamente com bash
        if bash ./nixpacks_install.sh; then
            echo "Script nixpacks_install.sh executado com sucesso via 'bash'."
        else
            echo "ERRO: Falha ao executar nixpacks_install.sh mesmo com 'bash'."
            exit 1
        fi
    fi
else
    echo "ERRO: Falha ao baixar o script de instalação do Nixpacks."
    exit 1
fi

# Adiciona o Nixpacks ao PATH da sessão atual
echo "--- Exportando Nixpacks para o PATH ---"
export PATH="$HOME/.nixpacks/bin:$PATH"
echo "PATH atual: $PATH"

# Verifica a versão do Nixpacks
echo "--- Verificando versão do Nixpacks ---"
if command -v nixpacks &> /dev/null; then
    echo "Nixpacks Version: $(nixpacks --version)"
else
    echo "ERRO: Nixpacks não encontrado no PATH após a tentativa de instalação!"
    echo "Conteúdo de $HOME/.nixpacks/bin:"
    ls -la "$HOME/.nixpacks/bin" || echo "AVISO: Não foi possível listar $HOME/.nixpacks/bin"
    exit 1
fi

# Rode seu comando de build original
echo "--- Rodando nixpacks build . --name meuapp-python ---"
if nixpacks build . --name meuapp-python; then
    echo "Nixpacks build concluído com sucesso."
else
    echo "ERRO: Falha no comando 'nixpacks build'."
    exit 1
fi

echo "--- Conteúdo de _nixpacks/meuapp-python/out (antes do cp) ---"
if [ -d "./_nixpacks/meuapp-python/out" ]; then
    ls -R ./_nixpacks/meuapp-python/out
    echo "--- Copiando artefatos do Nixpacks para a raiz ---"
    if cp -R ./_nixpacks/meuapp-python/out/. .; then
        echo "Cópia dos artefatos concluída."
    else
        echo "ERRO: Falha ao copiar artefatos do Nixpacks."
        exit 1
    fi
else
    echo "ERRO: Diretório de saída do Nixpacks ./_nixpacks/meuapp-python/out não encontrado!"
    # Se os artefatos do Nixpacks são cruciais (e são, neste caso), o build deve falhar.
    exit 1
fi

echo "--- Conteúdo do diretório raiz (após cp) ---"
ls -R . || echo "AVISO: Falha ao listar diretório raiz."

echo "--- render_build.sh concluído com sucesso ---"