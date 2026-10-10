---
title: "Linux II: Gestão de Ambiente, Automação & IA na Engenharia de Software"
subtitle: Introdução à Engenharia Informática
institute: Universidade de Aveiro
date: September 28, 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
header-includes:
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guião Prático de Laboratório

Este guião foi desenhado para uma sessão de **3 horas** e está dividido em duas partes fundamentais e uma secção de extensão autónoma:

* **Parte I — Gestão de Ambiente e Cópias de Segurança (Exercícios 1 e 2):** Consolidação de variáveis de sistema, fronteiras de processos e empacotamento com `tar`.
* **Parte II — Engenharia de IA, Contexto e Agentes na CLI (Exercícios 3 a 8):** Chamadas a APIs na linha de comandos, boas práticas de segurança de segredos, Engenharia de Contexto, criação de ficheiros `AGENTS.md`, desenho de uma *Skill* modular (`safe-cli`), automação com o assistente `ask_ai.sh` e desafio integrador de diagnóstico de erros (`ai_fix.sh`).
* **Exercícios Opcionais de Extensão (Exercícios 9 a 11):** Automação avançada de cópias com carimbo temporal dinâmico (`backup_auto.sh`), ponte preparatória para Git com gerador inteligente de *Conventional Commits* (`skills/git-commit`) e personalização de arranque da *shell* com painel de boas-vindas e atalhos globais (`welcome.sh` no `~/.bashrc` / `~/.zshrc`).

\vspace{1em}

> **Dicas de Sobrevivência no Terminal:**
>
> * **Autocompletar com `<Tab>`:** Escreva as primeiras letras de um caminho ou comando e prima `<Tab>`. Se carregar duas vezes, o terminal lista todas as hipóteses.
> * **Histórico com as setas `↑` e `↓`:** Nunca reescreva um comando longo por causa de um pequeno erro de digitação; use a seta para cima para recuperar e editar comandos anteriores.
> * **Cancelar com `Ctrl + C`:** Se um comando ou pedido de rede encravar, prima `Ctrl + C` para interromper imediatamente e regressar à linha de comandos do terminal.
> * **Aspas em Variáveis:** Ao expandir variáveis em comandos (ex: `echo "$MINHA_VAR"`), use sempre aspas duplas para evitar problemas com espaços ou caracteres especiais.

\newpage

# Parte I: Gestão de Ambiente e Cópias de Segurança

## Exercício 1: Variáveis de Ambiente, Subprocessos e Segredos

Neste exercício vai explorar a diferença entre variáveis locais da *shell* e variáveis exportadas para o ambiente global, compreendendo como os subprocessos herdam dados e como proteger credenciais no desenvolvimento de software.

1. **Criar o Diretório da Aula:**
   Crie uma pasta de trabalho para a sessão de hoje dentro do seu diretório pessoal:
   ```bash
   $ mkdir -p ~/IEI/aula02
   $ cd ~/IEI/aula02
   ```

2. **Criar uma Variável Local:**
   Defina uma variável simples na sua sessão interativa:
   ```bash
   $ CURSO="LEI_UA"
   $ echo "O meu curso e: $CURSO"
   ```
   *(Experimente correr `printenv CURSO`: confirme que não devolve nada, pois `printenv` só consulta variáveis de ambiente).*

3. **Testar a Fronteira de Processos com um Script:**
   Crie um script simples para verificar se outros programas conseguem aceder à sua variável:
   ```bash
   $ echo 'echo "Dentro do script o curso e: $CURSO"' > testar_curso.sh
   $ chmod +x testar_curso.sh
   $ ./testar_curso.sh
   ```
   *O que aconteceu?* O script imprimiu `Dentro do script o curso e: ` (vazio). O script corre como um programa independente (processo filho) e **não tem acesso** às variáveis locais da sua janela.

4. **Promover a Variável com `export`:**
   Promova a variável para o ambiente global do sistema e volte a executar o script:
   ```bash
   $ export CURSO="LEI_UA"
   $ ./testar_curso.sh
   ```
   *Resultado:* O script agora consegue ler `LEI_UA`, porque os programas e scripts que executamos herdam uma cópia de todas as variáveis exportadas.

5. **Inspecionar e Limpar o Ambiente:**
   Utilitários como `printenv` e `env` consultam exclusivamente variáveis promovidas com `export`:
   ```bash
   $ printenv CURSO
   $ env | grep CURSO
   ```
   *(Ambos devolvem `CURSO=LEI_UA`).*

   De seguida, elimine a variável da memória da sessão com `unset` e confirme que já não existe:
   ```bash
   $ unset CURSO
   $ printenv CURSO
   ```

6. **Persistência de Ambiente (`~/.bashrc` / `~/.zshrc`) e Segurança com `chmod 600`:**
   Se fechar o terminal ou reiniciar o computador, todas as variáveis exportadas na sessão desaparecem. Para tornar configurações e chaves permanentes entre sessões de forma modular e segura:

   * **Identificar a sua Shell ativa:**
     Verifique qual o interpretador predefinido no seu terminal:
     ```bash
     $ echo "$SHELL"
     ```
     * Em **Linux (Ubuntu/Debian)**: o padrão é o Bash (`/bin/bash`), que utiliza o ficheiro de inicialização **`~/.bashrc`**.
     * No **macOS**: o padrão é o Zsh (`/bin/zsh`), que utiliza o ficheiro de inicialização **`~/.zshrc`**.

   * **Criar um ficheiro pessoal de credenciais (`~/.api_keys`):**
     Na sua pasta pessoal, crie um ficheiro dedicado para chaves e variáveis persistentes:
     ```bash
     $ echo 'export IEI_PERSISTENTE="Ola_IEI"' > ~/.api_keys
     ```

   * **Proteger contra outros utilizadores com `chmod 600`:**
     Em sistemas multi-utilizador (como servidores partilhados e postos de laboratório), outros utilizadores poderiam inspecionar o seu ficheiro se as permissões fossem permissivas (`644`). Aplique o princípio de privilégio mínimo restringindo a leitura e escrita exclusivamente ao seu utilizador:
     ```bash
     $ chmod 600 ~/.api_keys
     $ ls -l ~/.api_keys
     ```
     *(Confirme que a permissão é `-rw-------`: apenas o proprietário pode aceder).*

   * **Configurar o carregamento automático no ficheiro da sua Shell:**
     Adicione a instrução de importação ao ficheiro correspondente ao seu sistema operativo:

     * *No Linux (Bash):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.bashrc
       $ source ~/.bashrc
       ```

     * *No macOS (Zsh):*
       ```bash
       $ echo '[ -f ~/.api_keys ] && source ~/.api_keys' >> ~/.zshrc
       $ source ~/.zshrc
       ```

   * **Confirmar a persistência na sessão atual:**
     ```bash
     $ echo "$IEI_PERSISTENTE"
     ```
     *(O terminal imprime `Ola_IEI`, confirmando que a variável foi carregada nesta janela).*

   * **O Teste Definitivo (Abrir um Novo Terminal):**
     Para comprovar que a configuração é verdadeiramente permanente e independente desta janela:
     1. Abra uma **nova janela ou separador de terminal**.
     2. No novo terminal, sem executar nenhum comando prévio de carregamento, teste:
        ```bash
        $ echo "$IEI_PERSISTENTE"
        ```
     3. Confirme que o valor `Ola_IEI` é impresso imediatamente, demonstrando que a *shell* carregou automaticamente as suas credenciais durante o ciclo de arranque.
     4. Feche esta nova janela de teste (executando `exit` ou fechando a aba) e **regresse ao terminal original** para continuar os exercícios.

-----

## Exercício 2: Cópias de Segurança e Pacotes com `tar`

O utilitário `tar` (*Tape Archive*) é o mecanismo fundamental no mundo Linux para empacotar diretórios inteiros e criar cópias de segurança comprimidas.

1. **Preparar Ficheiros de Teste:**
   Dentro da pasta `~/IEI/aula02`, crie um diretório de simulação de projeto com alguns ficheiros:
   ```bash
   $ mkdir -p ~/IEI/aula02/projeto_exemplo
   $ echo "# Projeto Exemplo IEI" > ~/IEI/aula02/projeto_exemplo/README.md
   $ echo "echo 'Ola Mundo'" > ~/IEI/aula02/projeto_exemplo/app.sh
   $ chmod +x ~/IEI/aula02/projeto_exemplo/app.sh
   $ date > ~/IEI/aula02/projeto_exemplo/timestamp.txt
   ```

2. **Criar um Arquivo Comprimido (`.tar.gz`):**
   Estando na pasta `~/IEI/aula02`, empacote a pasta `projeto_exemplo` num único arquivo comprimido com as opções clássicas `-czvf`:
   ```bash
   $ tar -czvf backup_projeto.tar.gz projeto_exemplo
   ```
   *Compreender as 4 opções fundamentais:*
   * `-c` : **Create** — Cria um novo ficheiro de arquivo.
   * `-z` : **Zip (gzip)** — Comprime os dados para ocupar muito menos espaço.
   * `-v` : **Verbose** — Mostra no ecrã a lista de ficheiros à medida que são empacotados.
   * `-f` : **File** — Define o nome do ficheiro de saída (`backup_projeto.tar.gz`). Deve ser sempre o último argumento das opções, seguido do nome do ficheiro.

3. **Inspecionar o Arquivo:**
   Verifique o tamanho e liste os conteúdos empacotados sem descompactar:
   ```bash
   $ ls -lh backup_projeto.tar.gz
   $ tar -tf backup_projeto.tar.gz
   ```
   *(A opção `-t` lista o índice de ficheiros contidos no arquivo).*

4. **Simular o Restauro noutra Pasta com `-C`:**
   Por omissão, o `tar` extrai os ficheiros exatamente para a pasta onde nos encontramos. Para extrair para um destino diferente sem termos de mudar de pasta com `cd`, usamos a opção **`-C`** (*Change directory*):
   ```bash
   $ mkdir -p /tmp/restauro_iei
   $ tar -xzvf backup_projeto.tar.gz -C /tmp/restauro_iei/
   $ ls -la /tmp/restauro_iei/projeto_exemplo/
   ```
   * *O papel do `-C`:* Indica ao `tar` para mudar temporariamente para a pasta `/tmp/restauro_iei` e descompactar lá dentro, mantendo a sua pasta de trabalho limpa.
   * Confirme que o ficheiro `app.sh` preservou a sua permissão de execução (`x`).

5. **Limpeza:**
   Remova a pasta de teste temporária:
   ```bash
   $ rm -rf /tmp/restauro_iei
   ```

\newpage

# Parte II: Engenharia de IA, Contexto e Agentes na CLI

## Exercício 3: A Primeira Chamada à LLM via `curl`

Neste exercício vai comunicar diretamente com um modelo de linguagem de última geração através do terminal, consumindo uma API REST com o utilitário `curl`.

> **Pré-requisito do Sistema (`python3`):**
> A manipulação de dados JSON na linha de comandos é realizada com o
> utilitário `python3` e o seu módulo nativo `json` (sem necessidade de
> instalar bibliotecas adicionais).

> * **Verificar se está instalado:** `$ python3 --version`
> * **Linux (Ubuntu/Debian — se não estiver instalado):**
>   `$ sudo apt update && sudo apt install -y python3`
> * **macOS (se não estiver instalado):**
>   `$ xcode-select --install`

1. **Obter a Chave de API Gratuita no Google AI Studio:**
   * Abra o navegador e aceda ao **Google AI Studio**: [https://aistudio.google.com/](https://aistudio.google.com/).
   * Inicie sessão com a sua conta Google pessoal (**Gmail**). Caso seja o primeiro acesso, aceite os termos de serviço.
   * Na **barra lateral esquerda**, clique em **"Dashboard"** e de seguida selecione **"API Keys"**.
   * No canto superior direito da página, clique no botão azul **"Create key"** (ou *"Create API key"*).
   * Na janela que se abre:
     * Em **"Name your key"**, introduza um nome descritivo (ex.: `iei-aula02`).
     * Em **"Choose an imported project"**, selecione **"Default Gemini Project"** (ou a opção padrão disponibilizada).
     * Confirme clicando em **"Create"**.
   * No ecrã de detalhes (**"API key details"**):
     * Clique no botão **"Copy key"** (no canto inferior direito) para copiar a chave gerada para a área de transferência.
     * *(Repare também no botão **"Copy cURL quickstart"**: a própria Google disponibiliza um comando `curl` de teste rápido pré-construído, demonstrando como o `curl` é a ferramenta de referência na indústria para interagir diretamente com APIs de IA a partir do terminal).*

   > **!!! Custos de APIs vs. Subscrições de Conta**
   > Ao contrário das subscrições pessoais de utilizador (como ChatGPT Plus, Claude Pro, GitHub Copilot ou Google Antigravity, que cobram uma mensalidade fixa previsível com quotas temporais de pedidos), as APIs de desenvolvedor operam em modelo métrico de pagamento por consumo (*pay-as-you-go*) por cada milhão de tokens. Em agentes e ferramentas que operam em ciclos (*loops*), a totalidade do histórico e dos ficheiros do repositório é reenviada a cada iteração, resultando em encargos financeiros imprevistos e elevados se um script executar em ciclo contínuo (*infinite retry loop*).
   > Em contexto profissional, é indispensável configurar **Hard Spend Limits** (tetos orçamentais estritos) na consola da Cloud. Notar que os **Alertas de Faturação (*Budget Alerts*)** sofrem frequentemente de latência de cálculo de várias horas, pelo que o orçamento estipulado pode ser largamente ultrapassado antes da emissão do aviso. No nosso laboratório utilizamos o Free Tier do Google AI Studio, que opera com limitação de taxa (15 RPM) e sem associação de meios de pagamento, garantindo ausência total de risco financeiro.

2. **Configurar a Chave na Variável de Ambiente:**
   No seu terminal, exporte a chave para a variável de ambiente `GEMINI_API_KEY`:
   ```bash
   $ export GEMINI_API_KEY="COLE_AQUI_A_SUA_CHAVE"
   ```
   *Verifique que a variável foi gravada sem revelar a chave completa:*
   ```bash
   $ echo "Chave configurada: ${GEMINI_API_KEY:0:8}..."
   ```
   *(Dica: para não ter de exportar a chave em cada nova janela de terminal, guarde-a no seu ficheiro protegido: `echo 'export GEMINI_API_KEY="COLE_AQUI_A_SUA_CHAVE"' >> ~/.api_keys`).*

3. **Fazer o Pedido HTTP POST com `curl`:**
   A Google disponibiliza a moderna **Interactions API** (`/v1beta/interactions`) para comunicação unificada com modelos Gemini:
   ```bash
   $ BASE="https://generativelanguage.googleapis.com"
   $ API_URL="${BASE}/v1beta/interactions"
   $ MODEL="gemini-3.5-flash-lite"

   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explica em 1 frase o comando tar -czvf.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }"
   ```
   *(Nota de latência: o parâmetro `"thinking_level": "low"` reduz o raciocínio interno para o essencial, garantindo respostas rápidas em ~2 segundos).*

4. **Analisar a Resposta:**
   Observe a resposta devolvida no terminal. Note a estrutura JSON devolvida pelo serviço, contendo o estado (`status: "completed"`), métricas de utilização (`usage`) e a sequência `steps` com os blocos de texto gerados (`"type": "model_output"`).

   > [!WARNING]
   > **Alerta de Sobrecarga Temporária (`service_unavailable` / 503):**
   > Se a resposta contiver um aviso do servidor como:
   > ```json
   > {
   >   "error": {
   >     "message": "... is currently experiencing high demand ...",
   >     "code": "service_unavailable"
   >   }
   > }
   > ```
   > **Não se trata de um erro de sintaxe nem da sua chave!** No escalão gratuito da Google (*Free Tier*), picos globais de pedidos provocam temporariamente este aviso.
   > - **Resolução rápida:** Aguarde 5 a 10 segundos e repita o comando.
   > - **Alternativa via `$MODEL`:** Se a sobrecarga persistir, mude de modelo na *shell* sem alterar nenhum comando nem script:
   >   ```bash
   >   $ export MODEL="gemini-3.8-flash-lite"
   >   ```
   >   *(E volte a executar a chamada `curl` com o novo `$MODEL`).*

5. **O Utilitário de Extração (`get_text.py`):**
   Como a API devolve um documento JSON completo com metadados técnicos, e nos exercícios seguintes pretendemos analisar diretamente o texto e comandos gerados (com quebras de linha reais), utilizamos o script auxiliar **`get_text.py`** disponibilizado no repositório.
   Pode também criá-lo diretamente na sua pasta de trabalho (`~/IEI/aula02/`):
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/get_text.py
   #!/usr/bin/env python3
   import json, sys

   try:
       d = json.load(sys.stdin)
       t = "".join(c.get("text", "") for s in d.get("steps", [])
                   if s.get("type") == "model_output"
                   for c in s.get("content", []) if c.get("type") == "text")
       if not t and "outputs" in d:
           t = "".join(o.get("text", "") for o in d["outputs"]
                       if o.get("type") == "text")
       if t:
           print(f"\n{t.strip()}\n")
       else:
           print(f"\n{d}\n")
   except Exception as e:
       print("Erro ao processar JSON:", e)
   EOF
   $ chmod +x ~/IEI/aula02/get_text.py
   ```
   *Teste a extração canalizando a resposta do `curl`:*
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Explica em 1 frase o comando tar -czvf.\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```

-----

## Exercício 4: Engenharia de Contexto na CLI (Do Vago ao Estrito)

Os modelos de linguagem modernos não necessitam de personagens teatrais ("*Atua como um engenheiro...*"). Precisam de **tarefas explícitas, delimitação de contexto e restrições estritas**.

1. **O Problema do Prompt Vago:**
   Execute uma consulta com uma formulação comum e vaga:
   ```bash
   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"Como ver ficheiros modificados em 24h no Linux?\",
       \"generation_config\": {
         \"thinking_level\": \"low\"
       }
     }" | ./get_text.py
   ```
   *Reflexão:* A resposta devolvida vem acompanhada de cumprimentos, parágrafos explicativos e blocos de formatação markdown (```bash ... ```). Se tentasse canalizar esta resposta diretamente para um script de automação, ocorreria um erro de sintaxe imediato!

2. **Aplicar os 4 Pilares da Engenharia de Contexto:**
   Vamos reestruturar o pedido aplicando **Tarefa**, **Contexto**, **Restrições** e **Formato de Saída**, reforçado com **Few-Shot**.
   *(Nota: utilizamos o nome `USER_PROMPT` porque no Zsh/macOS a variável `PROMPT` é reservada pelo sistema para configurar a própria linha de comandos do terminal!)*
   ```bash
   $ USER_PROMPT="Converte a intencao num comando Bash de 1 linha.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Exemplo 1:\n"
   $ USER_PROMPT="${USER_PROMPT}Intencao: Ver espaco em disco\n"
   $ USER_PROMPT="${USER_PROMPT}Comando: df -h\n\n"
   $ USER_PROMPT="${USER_PROMPT}Exemplo 2:\n"
   $ USER_PROMPT="${USER_PROMPT}Intencao: Listar ocultos\n"
   $ USER_PROMPT="${USER_PROMPT}Comando: ls -la\n\n"
   $ USER_PROMPT="${USER_PROMPT}Instrucoes Estritas:\n"
   $ USER_PROMPT="${USER_PROMPT}- Devolve EXCLUSIVAMENTE o comando de 1 linha.\n"
   $ USER_PROMPT="${USER_PROMPT}- Nao uses markdown nem explicacoes.\n\n"
   $ USER_PROMPT="${USER_PROMPT}Intencao: Ficheiros .log de ha 24h em /var/log\n"
   $ USER_PROMPT="${USER_PROMPT}Comando:"

   $ curl -s -X POST "$API_URL" \
     -H "x-goog-api-key: $GEMINI_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{
       \"model\": \"${MODEL}\",
       \"input\": \"${USER_PROMPT}\",
       \"generation_config\": {
         \"temperature\": 0.0
       }
     }" | ./get_text.py
   ```
   *(Repare no parâmetro `"generation_config": {"temperature": 0.0}`: tal como estudado na teoria, a temperatura zero força o modelo a selecionar deterministicamente os tokens de maior probabilidade, eliminando variações criativas e assegurando saídas de comandos consistentes e reprodutíveis).*

3. **Avaliar a Saída:**
   Verifique como o modelo gerou imediatamente a resposta limpa e determinista (sem ruído), com a sintaxe exata: `find /var/log -name "*.log" -mtime -1` (ou `-mmin -1440`).

-----

## Exercício 5: Concluir o Assistente de Terminal (`ask_ai.sh`)

Até agora executámos pedidos manuais com `curl` e canalizámos a resposta através de `./get_text.py`. No entanto, em tarefas de engenharia do dia a dia — onde pretendemos injetar ficheiros de contexto (`AGENTS.md`) ou procedimentos especializados (`SKILL.md`) — construir comandos `curl` manuais na consola torna-se repetitivo.

Neste exercício vai concluir o seu próprio assistente de linha de comandos em Bash (**`ask_ai.sh`**). A estrutura geral (validação de variáveis de ambiente, argumentos de entrada, deteção automática de contexto e geração segura do payload JSON) já está preparada num ficheiro esqueleto (*starter template*). O seu desafio prático é **completar a secção do comando `curl`** para realizar o pedido HTTP e canalizar a resposta para o `get_text.py`.

1. **Obter ou Criar o Esqueleto do Script (`ask_ai.sh`):**
   Pode copiar o ficheiro disponibilizado no eLearning ou criá-lo diretamente na sua pasta `~/IEI/aula02/`:
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/ask_ai.sh
   #!/bin/bash
   # ask_ai.sh — Assistente de Consola com Contexto Local
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   BASE="https://generativelanguage.googleapis.com"
   API_URL="${BASE}/v1beta/interactions"
   MODEL="${MODEL:-gemini-3.5-flash-lite}"

   # 1. Validar se a chave de API esta configurada no ambiente
   if [ -z "${GEMINI_API_KEY:-}" ]; then
       echo "Erro: GEMINI_API_KEY nao definida!" >&2
       echo "Execute: export GEMINI_API_KEY=\"a_sua_chave\"" >&2
       exit 1
   fi

   # 2. Validar argumento de pergunta
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"pergunta ou instrucao\" [ficheiro_contexto]" >&2
       exit 1
   fi

   USER_QUERY="$1"
   CONTEXT_FILE="${2:-}"

   # 3. Carregar contexto (do ficheiro indicado ou de AGENTS.md)
   CONTEXT_TEXT=""
   if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
       CONTEXT_TEXT="<contexto>\n$(cat "$CONTEXT_FILE")\n</contexto>\n\n"
       echo "[INFO] Contexto carregado de: $CONTEXT_FILE" >&2
   elif [ -f "AGENTS.md" ]; then
       CONTEXT_TEXT="<project_guidelines>\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}$(cat AGENTS.md)\n"
       CONTEXT_TEXT="${CONTEXT_TEXT}</project_guidelines>\n\n"
       echo "[INFO] Contexto carregado de: AGENTS.md" >&2
   fi

   FULL_INPUT="${CONTEXT_TEXT}Tarefa: ${USER_QUERY}"

   # 4. Montar o payload JSON de forma segura com Python
   PAYLOAD=$(python3 -c '
   import json, sys
   print(json.dumps({
       "model": sys.argv[1],
       "input": sys.argv[2],
       "generation_config": {"thinking_level": "low"}
   }))
   ' "$MODEL" "$FULL_INPUT")

   # 5. Executar o pedido via curl e apresentar a resposta limpa
   echo ""
   echo "=== Resposta da IA ==="
   # TODO [Desafio]: Complete com a chamada curl (Exercicios 3 e 4).
   # Requisitos:
   #  - Metodo POST para "$API_URL"
   #  - Header "x-goog-api-key: ${GEMINI_API_KEY}"
   #  - Header "Content-Type: application/json"
   #  - Enviar dados de "$PAYLOAD"
   #  - Canalizar (|) a saida para: python3 "$SCRIPT_DIR/get_text.py"

   # (Escreva aqui o seu comando curl)

   echo "======================="
   EOF
   ```

2. **Completar o Comando `curl` no Editor:**
   Abra o script com o editor de texto à sua escolha (por exemplo, `nano ~/IEI/aula02/ask_ai.sh` ou no VS Code).
   Localize a secção `# 5` e insira código em falta para que o script fique funcional.


3. **Atribuir Permissões de Execução:**
   Torne o script executável:
   ```bash
   $ chmod +x ~/IEI/aula02/ask_ai.sh
   ```

4. **Testar o Assistente com Perguntas Básicas:**
   Experimente colocar perguntas técnicas diretamente ao seu novo comando:
   ```bash
   $ cd ~/IEI/aula02
   $ ./ask_ai.sh "Diferenca entre variavel local e exportada?"
   $ ./ask_ai.sh "Como ver portas abertas no Linux ou macOS?"
   ```

-----

## Exercício 6: Grounding Arquitetural com `AGENTS.md`

O ficheiro **`AGENTS.md`** é a norma moderna adotada em projetos de engenharia para fornecer a agentes e assistentes de IA (Antigravity, Cursor, Claude Code, Copilot) o contexto arquitetural, as convenções e os limites do repositório.

1. **Criar o `AGENTS.md`:**
   Na pasta `~/IEI/aula02`, crie o ficheiro `AGENTS.md` com a especificação do seu projeto:
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/AGENTS.md
   # Diretrizes de Engenharia: Projeto IEI

   ## 1. Ambiente & Stack
   - Sistema Operativo: Linux Ubuntu / Debian POSIX.
   - Interpretador de Scripts: Bash (#!/bin/bash).
   - Todos os scripts devem usar as opcoes de seguranca
     set -euo pipefail.

   ## 2. Convencoes de Codigo
   - Foco em utilitarios nativos do sistema operativo.
   - E expressamente PROIBIDO sugerir dependencias externas
     para tarefas basicas de sistema.
   - Variaveis devem ser escritas em maiusculas
     e delimitadas entre aspas duplas.

   ## 3. Seguranca & Restricoes
   - NUNCA sugerir comandos que removam dados sem confirmacao
     (ex: proibir rm -rf).
   - NUNCA expor palavras-passe ou tokens hardcoded.
   EOF
   ```

2. **Experimentar o Efeito do Contexto com o Assistente:**
   Execute uma consulta usando o seu assistente. Como o ficheiro `AGENTS.md` existe na pasta atual, o assistente deteta-o e injeta-o automaticamente como contexto da instrução:
   ```bash
   $ ./ask_ai.sh "Gera um script para verificar se o cron esta ativo."
   ```
   *(Observe a mensagem informativa `[INFO] Contexto carregado de: AGENTS.md` emitida pelo script).*

3. **Verificação Crítica:**
   Observe como a IA seguiu rigorosamente as regras definidas no `AGENTS.md`: incluiu `#!/bin/bash`, adicionou a salvaguarda `set -euo pipefail` e usou ferramentas nativas como `systemctl is-active cron` ou `pgrep cron`, sem recorrer a dependências externas.

4. **Desafio Prático: Modificar o `AGENTS.md` e Avaliar a Reação da IA:**
   Abra o seu ficheiro `AGENTS.md` no editor de texto (`nano ~/IEI/aula02/AGENTS.md` ou no VS Code) e adicione uma nova diretriz ao seu contrato.
   Por exemplo, escolha uma das seguintes ideias (ou crie a sua própria regra):
   * **Restrição de Ferramentas:** Adicione uma regra que proíba expressamente o utilitário `systemctl`, exigindo que a verificação de processos use exclusivamente `pgrep` ou `/etc/init.d/`.
   * **Formatação e Registo:** Adicione uma regra que obrigue a que todas as mensagens impressas na consola pelo script contenham um prefixo de data/hora no formato `[YYYY-MM-DD hh:mm:ss]`.
   * **Gestão de Sinais:** Adicione uma regra que obrigue qualquer script a implementar uma função `cleanup()` e a registar um comando `trap` para interceção de `SIGINT` (`Ctrl+C`).

   Grave as alterações e volte a executar o assistente com **a mesma pergunta**:
   ```bash
   $ ./ask_ai.sh "Gera um script para verificar se o cron esta ativo."
   ```
   **O que mudou?** Compare a nova resposta com a anterior. Repare como, sem ter alterado uma única letra na pergunta que enviou, o modelo adaptou a arquitetura do código para cumprir a nova especificação do projeto!


-----

## Exercício 7: Desenhar e Testar uma Skill Modular (`safe-cli`)

Uma **Skill** é um procedimento especializado de conhecimento modular, desenhado para ser ativado sob demanda para uma tarefa específica.

Neste exercício vai criar a skill **`safe-cli`**, concebida para auditar a segurança de comandos de terminal em ambientes UNIX (**Linux e macOS**, abrangendo interpretadores **Bash e Zsh**) antes de os executar.

> **Nota para utilizadores de macOS / Zsh:**
> No macOS, a *shell* predefinida é o Zsh (`/bin/zsh`). A sintaxe de variáveis, redirecionamento e execução deste guião é totalmente compatível. A skill que vamos desenhar deve ser agnóstica ou consciente das especificidades de cada sistema operativo (ex.: `apt` vs. `brew`, `systemctl` vs. `launchctl`, `/var/www/html` vs. `/Library/WebServer/Documents`, e utilitários específicos como `diskutil`).

1. **Criar a Estrutura da Skill:**
   Crie a pasta de competências:
   ```bash
   $ mkdir -p ~/IEI/aula02/skills/safe-cli
   ```

2. **Definir o Procedimento Operacional (`SKILL.md`):**
   Crie o ficheiro com as diretrizes de auditoria para ambientes Linux e macOS:
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/skills/safe-cli/SKILL.md
   ---
   name: safe-cli
   description: Analisador de seguranca para comandos UNIX (Linux e macOS).
   ---

   # Procedimento Operacional da Skill safe-cli:
   Ao receber um comando para inspecionar, segue estes 4 passos:
   1. [Nivel de Risco]: Classifica como [SEGURO], [ATENCAO] ou [PERIGOSO].
   2. [Objetivo]: Resume em uma frase clara o que o comando faz.
   3. [Decomposicao]: Explica cada comando, subcomando e flag utilizada.
   4. [Alerta & Alternativa]: Se o comando tiver impacto destrutivo
      (ex: rm -rf, dd, chmod -R 777, diskutil), adverte sobre o perigo
      e apresenta uma alternativa segura com privilegios minimos.
   EOF
   ```

3. **Testar a Skill Passando-a ao Assistente:**
   Invoque o seu assistente passando o comando a auditar e indicando o ficheiro da skill como segundo argumento:
   ```bash
   $ ./ask_ai.sh "chmod -R 777 ~/" skills/safe-cli/SKILL.md
   ```
   *(Pode também testar comandos específicos do seu ambiente, como `chmod -R 777 /var/www/html` em Linux ou `sudo chmod -R 777 /Library/WebServer/Documents` em macOS).*

4. **Inspecionar o Relatório de Auditoria:**
   Confirme que a IA classificou o comando como **PERIGOSO**, explicou o impacto das permissões `777` recursivas (leitura, escrita e execução universal a qualquer utilizador ou processo) e sugeriu uma alternativa com privilégios mínimos (`chmod 755` ou `chmod 700`).

5. **Discussão Crítica de Encerramento:**
   Repare que o assistente **apresenta** sugestões e auditorias, mas **não as executa automaticamente**.
   *Reflita:* Por que razão, no desenho de ferramentas de engenharia de software, a execução automática de comandos gerados por IA sem validação humana prévia (*Human-in-the-Loop*) constitui uma falha grave de segurança?

-----

## Exercício 8 [Desafio de Consolidação]: O Médico do Terminal (`ai_fix.sh`)

Durante a aprendizagem de sistemas UNIX, é frequente depararmo-nos com mensagens de erro na consola (`No such file or directory`, `Permission denied`, `invalid mode`, etc.).
Como desafio final — para realizar no final da aula ou autonomamente em casa — vai criar uma ferramenta de produtividade real: o **`ai_fix.sh`**, um script que executa um comando com erro, captura a sua mensagem de falha e pede à IA um diagnóstico padronizado e a respetiva correção.

1. **Especificar os Requisitos da Skill de Diagnóstico (`skills/error-fix/SKILL.md`):**
   Com base na estrutura de *Skills* aprendida no Exercício 7 (cabeçalho YAML e procedimento em Markdown), crie a diretoria para a nova skill:
   ```bash
   $ mkdir -p ~/IEI/aula02/skills/error-fix
   ```
   Crie o ficheiro `~/IEI/aula02/skills/error-fix/SKILL.md`. Em vez de receber as instruções prontas, desenhe a sua própria *Skill* para que o assistente analise um comando com erro e devolva **estritamente** este formato de saída:
   ```text
   [Causa]: Explicacao concisa do motivo tecnico da falha.
   [Comando Corrigido]: comando exato pronto a executar
   [Dica]: Recomendacao sobre a flag, sintaxe ou permissao corrigida.
   ```
   **Requisitos a garantir:**
   * Incluir os metadados YAML iniciais (`name` e `description`) na skill.
   * Definir regras operacionais que impeçam o modelo de adicionar saudações, introduções ou texto conversacional supérfluo, limitando-o exclusivamente aos três blocos de diagnóstico indicados.

2. **Dicas Técnicas Essenciais em Bash:**
   Para construir e compreender o script `ai_fix.sh`, analisamos dois conceitos práticos da *shell*:
   * **Como um Script Recebe Argumentos (`$#` e `$*`):**
     Quando executamos um script passando instruções à frente (ex.: `./ai_fix.sh "chmod 999 app.sh"` ou `./ai_fix.sh chmod 999 app.sh`), o Bash disponibiliza variáveis especiais automáticas:
     * **`$#`**: Contém o **número de argumentos** passados. No esqueleto usamos `[ "$#" -eq 0 ]` para verificar se o utilizador se esqueceu de indicar o comando e exibir a mensagem de ajuda (*usage*).
     * **`$*`**: Agrupa **todas as palavras e opções** fornecidas numa única cadeia de texto armazenada na variável `CMD`, permitindo que o utilizador passe o comando comodamente entre aspas ou sem aspas.
   * **Como Utilizar o Script:**
     A forma recomendada de utilização é passar o comando a diagnosticar delimitado entre aspas duplas, preservando pipes e opções especiais:
     ```bash
     $ ./ai_fix.sh "comando_com_erro --flags"
     ```
   * **Captura Dinâmica de Saída e Erros com `eval` e `2>&1`:**
     ```bash
     ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)
     ```
     * `eval "$CMD"`: Avalia e executa a cadeia de texto do comando dinamicamente.
     * `2>&1`: Redireciona o canal de erros (*stderr*, descritor `2`) para o canal normal (*stdout*, descritor `1`), permitindo que a substituição de comandos `$()` capture as mensagens de falha.
     * `|| true`: Garante que, mesmo que o comando termine com código de erro (diferente de 0), o script não seja abortado abruptamente pela opção de segurança `set -e`.

3. **Obter o Esqueleto do Script (`ai_fix.sh`):**
   Crie o ficheiro base na sua pasta `~/IEI/aula02/` (ou copie-o do eLearning):
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/ai_fix.sh
   #!/bin/bash
   # ai_fix.sh — Diagnostica e sugere correcoes para comandos com erro
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validar se o utilizador forneceu um comando
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"comando que falhou\"" >&2
       exit 1
   fi

   # Dica: "$*" agrupa todas as palavras passadas como argumento
   CMD="$*"

   # 2. Executar o comando e capturar stdout e stderr juntos
   echo "A executar: $CMD ..."
   ERROR_OUTPUT=$(eval "$CMD" 2>&1 || true)

   # 3. Formatar o pedido e invocar o assistente com a skill
   # TODO [Desafio]: Monte o prompt com o comando ($CMD) e o erro
   # ($ERROR_OUTPUT), e invoque o ask_ai.sh passando a skill:
   # "$SCRIPT_DIR/skills/error-fix/SKILL.md"

   # (Escreva aqui a chamada ao ask_ai.sh)

   EOF
   ```

4. **Completar o Script no Editor:**
   Abra o script `~/IEI/aula02/ai_fix.sh`. Na secção `# 3`, complete o código para construir o prompt usando as variáveis `$CMD` e `$ERROR_OUTPUT`, e invoque o assistente `ask_ai.sh` passando o ficheiro da *Skill* como segundo argumento:
   ```bash
   INVOCAR_ASK_AI.SH "PROMPT_AQUI" "CAMINHO/PARA/SKILL.md"
   ```

5. **Atribuir Permissões e Testar:**
   Torne o script executável:
   ```bash
   $ chmod +x ~/IEI/aula02/ai_fix.sh
   ```
   Experimente testar comandos propositadamente errados:
   ```bash
   $ cd ~/IEI/aula02
   $ ./ai_fix.sh "cat /ficheiro_que_nao_existe.txt"
   $ ./ai_fix.sh "chmod 999 app.sh"
   $ ./ai_fix.sh "tar -czf backup.tar.gz pasta_fantasma"
   ```
   *Observe como a IA diagnostica com precisão a razão da falha segundo as 3 etapas da Skill (Causa, Comando Corrigido e Dica)!*

\newpage

# Exercícios Opcionais de Prática e Extensão

Estes exercícios destinam-se a ser realizados no tempo restante da aula de laboratório ou autonomamente em casa, consolidando técnicas avançadas de automação em Bash e explorando novas aplicações de engenharia de contexto e skills modulares.

-----

## Exercício 9 [Opcional]: Automação de Cópias com Timestamp (`backup_auto.sh`)

No Exercício 2 aprendeu a criar arquivos comprimidos com `tar -czvf`. No entanto, em tarefas reais de administração de sistemas e engenharia de software, uma rotina de *backup* nunca deve sobrepor um ficheiro existente: deve gerar nomes dinâmicos com **carimbo de data e hora** (*timestamps*) e excluir ficheiros temporários descartáveis.

1. **Testar a Geração Dinâmica de Datas:**
   O utilitário `date` permite formatar datas de forma padronizada para nomes de ficheiros. Experimente no terminal:
   ```bash
   $ date +"%Y%m%d_%H%M%S"
   ```
   *(Devolve algo como `20261006_143022`, ideal para ordenar cronologicamente cópias de segurança).*

2. **Criar Ficheiros Temporários no Projeto:**
   Para testar a capacidade de exclusão do `tar`, crie alguns ficheiros temporários na sua pasta de exemplo:
   ```bash
   $ touch ~/IEI/aula02/projeto_exemplo/cache.tmp
   $ touch ~/IEI/aula02/projeto_exemplo/debug.log
   ```

3. **Obter ou Criar o Esqueleto do Script (`backup_auto.sh`):**
   Pode copiar o ficheiro `backup_auto.sh` disponibilizado no eLearning/repositório ou criá-lo na pasta `~/IEI/aula02/`.
   Repare que a validação de parâmetros, a verificação de existência da pasta com `[ ! -d "$ORIGEM" ]` e o relatório final já vêm pré-construídos:
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/backup_auto.sh
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
   EOF
   ```

4. **Completar o Script no Editor:**
   Abra o script (`nano ~/IEI/aula02/backup_auto.sh` ou no seu editor de código).
   - No **Desafio 1**, defina `TIMESTAMP=$(date +"%Y%m%d_%H%M%S")` e monte a variável `NOME_ARQUIVO`.
   - No **Desafio 2**, escreva o comando `tar` com as opções de exclusão para arquivar `$ORIGEM` em `$NOME_ARQUIVO`.

5. **Atribuir Permissões e Testar:**
   Torne o script executável:
   ```bash
   $ chmod +x ~/IEI/aula02/backup_auto.sh
   ```
   Execute o script e confirme que os ficheiros `.tmp` e `.log` foram ignorados com sucesso:
   ```bash
   $ cd ~/IEI/aula02
   $ ./backup_auto.sh projeto_exemplo
   $ tar -tf backup_projeto_exemplo_*.tar.gz
   ```
   *(Confirme que `cache.tmp` e `debug.log` não aparecem na listagem do arquivo).*

-----

## Exercício 10 [Opcional]: Ponte para Git — Mensagens de Commit com IA (`skills/git-commit`)

Na próxima sessão de laboratório vai começar a trabalhar com o sistema de controlo de versões **Git**. Uma das convenções mais adotadas na indústria de software é a especificação [*Conventional Commits*](https://www.conventionalcommits.org/), que padroniza o histórico do projeto através de prefixos semânticos claros (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).

Neste exercício vai desenhar uma nova *Skill* especializada e um comando auxiliar (`ai_commit.sh`) para transformar anotações informais de alterações em mensagens de *commit* perfeitamente formatadas.

1. **Criar a Estrutura da Skill:**
   Crie o diretório dedicado:
   ```bash
   $ mkdir -p ~/IEI/aula02/skills/git-commit
   ```

2. **Definir a Skill (`skills/git-commit/SKILL.md`):**
   Crie o ficheiro de procedimento com exemplos calibrados (*Few-Shot*):
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/skills/git-commit/SKILL.md
   ---
   name: git-commit
   description: Gerador especializado de mensagens de commit segundo a especificacao Conventional Commits.
   ---

   # Procedimento Operacional:
   Com base na descricao das alteracoes fornecida pelo utilizador, gera estritamente a mensagem de commit no seguinte formato:

   1. Linha de Cabecalho (obrigatoria):
      <tipo>: <resumo no imperativo, em letras minusculas, sem ponto final, max. 50 caracteres>

      Tipos validos:
      - feat: Nova funcionalidade para o utilizador
      - fix: Correcao de um erro ou falha
      - docs: Alteracoes exclusivas de documentacao
      - refactor: Reorganizacao de codigo sem alterar comportamento
      - test: Adicao ou correcao de testes

   2. Corpo (opcional, separado por uma linha em branco):
      Se houver detalhes relevantes, descreve-os em topicos com hifen (-).

   # Regras Estritas:
   - Devolve EXCLUSIVAMENTE a mensagem de commit pronta a usar.
   - Nao uses blocos de formatacao markdown, nem introducoes, nem explicacoes.

   # Exemplos:
   Entrada: fiz um script backup_auto.sh para guardar copias com data e hora
   Saida:
   feat: adicionar script de backup com timestamp

   - suporta exclusao automatica de ficheiros .tmp e .log
   - calcula o tamanho e total de ficheiros preservados
   EOF
   ```

3. **Obter ou Criar o Esqueleto do Script (`ai_commit.sh`):**
   O script já inclui a resolução da pasta e as validações defensivas de argumentos e de existência da skill:
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/ai_commit.sh
   #!/bin/bash
   # ai_commit.sh — Gera mensagens Conventional Commits via assistente
   set -euo pipefail

   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

   # 1. Validar se o utilizador indicou uma descricao das alteracoes
   if [ "$#" -eq 0 ]; then
       echo "Uso: $0 \"descreva brevemente o que alterou no codigo\"" >&2
       exit 1
   fi

   # Validar se o ficheiro da skill existe
   SKILL_FILE="${SCRIPT_DIR}/skills/git-commit/SKILL.md"
   if [ ! -f "$SKILL_FILE" ]; then
       echo "Erro: Ficheiro da skill nao encontrado em: $SKILL_FILE" >&2
       exit 1
   fi

   # 2. Capturar as notas de alteracoes e invocar o assistente com a skill
   # TODO [Desafio]:
   #  - Guarde todas as palavras passadas pelo utilizador na variavel NOTAS (dica: use "$*")
   #  - Invoque o script "$SCRIPT_DIR/ask_ai.sh" passando como primeiro argumento o pedido:
   #    "Gera a mensagem de commit para: $NOTAS"
   #    e como segundo argumento o ficheiro da skill: "$SKILL_FILE"

   # (Escreva aqui a captura de NOTAS e a chamada ao ask_ai.sh)

   EOF
   ```

4. **Completar o Script no Editor:**
   Abra o script `~/IEI/aula02/ai_commit.sh`. Na secção `# 2`, complete o desafio capturando a lista de argumentos com `NOTAS="$*"` e invocando o `ask_ai.sh` passando a instrução e o caminho da skill.

5. **Atribuir Permissões e Testar:**
   Torne o script executável:
   ```bash
   $ chmod +x ~/IEI/aula02/ai_commit.sh
   ```
   Teste a ferramenta com diferentes tipos de tarefas:
   ```bash
   $ cd ~/IEI/aula02
   $ ./ai_commit.sh "corrigi o erro de permissao no ficheiro de chaves mudando para 600"
   $ ./ai_commit.sh "adicionei instrucoes sobre instalacao do python3 no guiao"
   ```
   *Observe como a IA classifica automaticamente o tipo (`fix:` ou `docs:`) e gera a mensagem pronta a copiar para um futuro `git commit -m "..."`!*

-----

## Exercício 11 [Opcional]: Painel de Boas-Vindas no Terminal e Atalhos Globais (`welcome.sh`)

No Exercício 1 explorou como os ficheiros de arranque da *shell* (`~/.bashrc` no Linux ou `~/.zshrc` no macOS) são executados sempre que abre uma nova janela de terminal.
Neste exercício vai construir um painel de boas-vindas (*Message of the Day* / MOTD) dinâmico e criar **atalhos globais (*aliases*)** para invocar as ferramentas desenvolvidas na aula a partir de qualquer pasta do sistema.

> **Regra de Ouro da Portabilidade UNIX (`printf` vs. `echo -e`):**
> No Linux (GNU), o comando `echo -e` interpreta códigos de escape de cores. No entanto, no macOS (BSD), o comando `/bin/echo` não reconhece a opção `-e`, imprimindo literalmente `-e \033...`.
> O padrão **POSIX universalmente compatível** entre Linux e macOS (e entre interpretadores Bash e Zsh) é utilizar o comando **`printf`**:
> ```bash
> VERDE=$(printf '\033[32m')
> RESET=$(printf '\033[0m')
> printf "%s\n" "${VERDE}[OK] Funciona em Linux e macOS!${RESET}"
> ```

1. **Obter ou Criar o Esqueleto do Script (`welcome.sh`):**
   Crie o ficheiro de boas-vindas na pasta `~/IEI/aula02/` (ou copie-o do eLearning/repositório):
   ```bash
   $ cat << 'EOF' > ~/IEI/aula02/welcome.sh
   #!/bin/bash
   # welcome.sh — Painel de Boas-Vindas da Workstation IEI (Linux & macOS)
   set -euo pipefail

   # Definicao portatil de cores ANSI compativel com Linux e macOS (POSIX)
   VERDE=$(printf '\033[32m')
   AMARELO=$(printf '\033[33m')
   AZUL=$(printf '\033[34m')
   RESET=$(printf '\033[0m')

   printf "${AZUL}====================================================${RESET}\n"
   printf "${AZUL}    IEI Workstation — Universidade de Aveiro        ${RESET}\n"
   printf "${AZUL}====================================================${RESET}\n"
   printf " Utilizador : ${VERDE}%s${RESET}\n" "$USER"
   printf " Sistema    : %s (%s)\n" "$(uname -s)" "$(uname -m)"
   printf " Data/Hora  : %s\n" "$(date +"%Y-%m-%d %H:%M:%S")"

   # 1. Verificacao de segredos e estado da API Gemini
   # TODO [Desafio]: Verifique se a variavel GEMINI_API_KEY esta definida e nao vazia.
   # Dica: use [ -n "${GEMINI_API_KEY:-}" ]
   # Se estiver definida:
   #    printf " API Gemini : ${VERDE}[OK] Chave ativa${RESET}\n"
   # Caso contrario:
   #    printf " API Gemini : ${AMARELO}[AVISO] Chave em falta (~/.api_keys)${RESET}\n"

   # (Escreva aqui a condicao if/else)


   # 2. Resumo da pasta de trabalho do laboratorio
   AULA_DIR="$HOME/IEI/aula02"
   if [ -d "$AULA_DIR" ]; then
       TOTAL_FICH=$(find "$AULA_DIR" -maxdepth 1 -type f | wc -l | tr -d ' ')
       printf " Ficheiros  : %s ficheiros na pasta ~/IEI/aula02\n" "$TOTAL_FICH"
   fi

   printf "${AZUL}----------------------------------------------------${RESET}\n"
   printf " Atalhos: ${VERDE}ask${RESET} \"pergunta\" | ${VERDE}fix${RESET} \"cmd_com_erro\"\n"
   printf "${AZUL}====================================================${RESET}\n\n"
   EOF
   ```

2. **Completar o Script no Editor:**
   Abra o script `~/IEI/aula02/welcome.sh` no seu editor de texto. Na secção `# 1`, complete o teste condicional `if [ -n "${GEMINI_API_KEY:-}" ]; then ... else ... fi` para reportar se a chave está configurada no ambiente com as cores apropriadas.

3. **Atribuir Permissões de Execução:**
   Torne o script executável:
   ```bash
   $ chmod +x ~/IEI/aula02/welcome.sh
   ```
   *(Pode testá-lo diretamente na consola executando `./welcome.sh`)*.

4. **Desafio: Registar o Script e os Atalhos no Arranque da Shell:**
   Com base no que aprendeu no **Exercício 1 (passo 6)**, configure o ficheiro de arranque da sua *shell* (`~/.bashrc` no Linux ou `~/.zshrc` no macOS) para tornar estas funcionalidades permanentes.

   > **Como funcionam os Atalhos (*Aliases*):**
   > O comando `alias` permite associar uma palavra curta a um comando longo ou ao caminho de um script, tornando-o invocável em qualquer diretório:
   > ```bash
   > alias nome_do_atalho="comando_ou_caminho_completo"
   > ```
   > *(Atenção à regra de sintaxe em Shell: nunca coloque espaços antes ou depois do sinal `=`, caso contrário o interpretador tentará executar o comando em vez de definir o atalho).*

   **Requisitos a cumprir:**
   * **Executar o painel no arranque:** Adicione a instrução para executar o script `~/IEI/aula02/welcome.sh` em cada nova sessão, recorrendo a uma validação defensiva com `[ -f ... ]` (para prevenir mensagens de erro caso o ficheiro seja movido ou eliminado).
   * **Criar atalhos globais (*aliases*):** Defina os atalhos `ask` (a apontar para o caminho de `~/IEI/aula02/ask_ai.sh`) e `fix` (a apontar para `~/IEI/aula02/ai_fix.sh`).
   * **Recarregar o ambiente:** Recarregue o ficheiro de arranque na sessão atual utilizando o comando `source`.

5. **O Teste Final (Novo Terminal Independente):**
   Abra uma **nova janela de terminal** (ou um novo separador).
   * Verifique o painel com as cores verde e azul exibido instantaneamente ao abrir a consola!
   * Estando em qualquer diretório (ex.: na sua pasta pessoal `cd ~`), experimente usar os novos atalhos diretamente:
     ```bash
     $ ask "Explica a diferenca entre echo e printf em POSIX."
     ```
   *(Observe como o utilitário funciona de imediato a partir de qualquer pasta, sem necessidade de `./` nem de caminhos relativos!).*
