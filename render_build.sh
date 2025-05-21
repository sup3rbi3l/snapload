#!/bin/bash
set -e # Sai imediatamente se um comando sair com status diferente de zero.
set -x # Imprime os comandos e seus argumentos à medida que são executados (bom para depuração).

echo "--- Iniciando render_build.sh ---"

# Instala o Nixpacks
echo "--- Instalando Nixpacks ---"
if curl -sSL https://nixpacks.com/install.sh | sh; then
    echo "Nixpacks script de instalação executado."
else
    echo "ERRO: Falha ao executar o script de instalação do Nixpacks."
    exit 1
fi

# Adiciona o Nixpacks ao PATH da sessão atual
# Este export precisa estar aqui para que os comandos subsequentes neste script encontrem nixpacks
echo "--- Exportando Nixpacks para o PATH ---"
export PATH="$HOME/.nixpacks/bin:$PATH"
echo "PATH atual: $PATH"

# Verifica a versão do Nixpacks
echo "--- Verificando versão do Nixpacks ---"
if command -v nixpacks &> /dev/null; then
    echo "Nixpacks Version: $(nixpacks --version)"
else
    echo "ERRO: Nixpacks não encontrado no PATH após a tentativa de instalação!"
    ls -la "$HOME/.nixpacks/bin" # Lista o conteúdo do diretório para depuração
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
# É importante verificar se o diretório de origem existe
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
    # Você pode querer que o build falhe aqui se os artefatos são essenciais
    # exit 1
    # Ou apenas avisar e continuar, dependendo da sua lógica
    echo "AVISO: Continuando sem copiar artefatos do Nixpacks pois o diretório de saída não foi encontrado."
fi

echo "--- Conteúdo do diretório raiz (após cp) ---"
ls -R . || echo "AVISO: Falha ao listar diretório raiz."

echo "--- render_build.sh concluído com sucesso ---"
