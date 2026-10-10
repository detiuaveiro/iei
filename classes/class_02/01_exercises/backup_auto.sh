#!/bin/bash
# backup_auto.sh — Cria arquivo .tar.gz com timestamp e exclui temporarios
set -euo pipefail

# 1. Validar se a pasta de origem foi indicada e se existe
if [ "$#" -eq 0 ]; then
    echo "Uso: $0 <diretorio_origem> [diretorio_destino]" >&2
    exit 1
fi

ORIGEM="$1"
DESTINO="${2:-.}"

if [ ! -d "$ORIGEM" ]; then
    echo "Erro: O diretorio '$ORIGEM' nao existe!" >&2
    exit 1
fi

NOME_BASE=$(basename "$ORIGEM")

# 2. Gerar timestamp e nome do ficheiro de saida
# TODO [Desafio 1]: Guarde em TIMESTAMP a data atual no formato YYYYMMDD_HHMMSS (use o comando date).
# De seguida, construa o caminho completo do ficheiro de destino em NOME_ARQUIVO:
# "${DESTINO}/backup_${NOME_BASE}_${TIMESTAMP}.tar.gz"

# (Defina aqui as variaveis TIMESTAMP e NOME_ARQUIVO)


echo "A empacotar '$ORIGEM' para '$NOME_ARQUIVO'..."

# 3. Criar arquivo comprimido (.tar.gz) excluindo temporarios
# TODO [Desafio 2]: Execute o utilitario tar para criar o arquivo comprimido
# no caminho "$NOME_ARQUIVO" com o conteudo de "$ORIGEM".
# Requisitos:
#  - Comprimir com gzip (-czf)
#  - Excluir ficheiros com extensao .tmp (--exclude="*.tmp")
#  - Excluir ficheiros com extensao .log (--exclude="*.log")

# (Escreva aqui o seu comando tar)


# 4. Exibir relatorio de sucesso e contagem de ficheiros preservados
TOTAL_FICH=$(tar -tf "$NOME_ARQUIVO" | wc -l | tr -d ' ')
TAMANHO=$(ls -lh "$NOME_ARQUIVO" | awk '{print $5}')

echo "Backup concluido com sucesso!"
echo " - Ficheiro: $NOME_ARQUIVO"
echo " - Tamanho: $TAMANHO"
echo " - Ficheiros preservados: $TOTAL_FICH"
