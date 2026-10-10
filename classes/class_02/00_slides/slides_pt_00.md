---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Linux II: Gestão de Ambiente, Automação & IA na Engenharia de Software"
institute: Universidade de Aveiro
date: September 28, 2026
colorlinks: true
highlight-style: tango
mainfont: NotoSans
fontsize: 9pt
titlegraphic: "../../../resources/ua_logo2.png"
titlegraphicoptions: "width=6.5cm"
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
header-includes:
 - \usetheme[sectionpage=none,numbering=fraction,progressbar=none]{metropolis}
 - \definecolor{uagreen}{HTML}{92D400}
 - \setbeamercolor{title separator}{fg=uagreen}
 - \setbeamersize{text margin left=1.5em, text margin right=1.5em}
 - |
    \setbeamertemplate{title graphic}{
      \begin{tikzpicture}[remember picture,overlay]
        \node[anchor=north west, xshift=0cm, yshift=-0cm] at (current page.north west) {
          \inserttitlegraphic
        };
        \node[anchor=south east, xshift=-0.2cm, yshift=0.6cm, opacity=0.08] at (current page.south east) {
          \includegraphics[width=4.8cm]{../../../resources/_deti_black.png}
        };
      \end{tikzpicture}
    }
 - \usepackage{tikz}
 - \usetikzlibrary{positioning,arrows.meta,calc}
 - \usepackage{etoolbox}
 - \BeforeBeginEnvironment{Shaded}{\vspace{1.0em}}
 - \AfterEndEnvironment{Shaded}{\vspace{0.6em}}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Parte I: Gestão de Ambiente Linux e Automação

Tópicos abordados nesta primeira parte:

  * **Variáveis de Ambiente:**
      * Variáveis locais vs. globais (`export`) e herança em subprocessos e scripts.
  * **Inspeção e Gestão do Ambiente:**
      * Comandos `printenv`, `env` e remoção com `unset`.
  * **Persistência e Segurança:**
      * Configuração no `~/.bashrc`, recarregar com `source` e proteção com `chmod 600`.
  * **Arquivos e Cópias de Segurança:**
      * Empacotamento e compressão de projetos com o utilitário `tar`.

-----

## Da Sessão Anterior: As Variáveis de Ambiente do Sistema

Na sessão anterior utilizámos variáveis de contexto disponibilizadas pela *shell*:

  * **`$USER`:** O utilizador com sessão ativa (`echo $USER`).
  * **`$HOME`:** O caminho absoluto para a pasta pessoal (`echo $HOME`).
  * **`$PATH`:** O catálogo de pastas onde a *shell* procura programas executáveis (`echo $PATH`).

**De onde surgem estas variáveis?**

  * Não são propriedades mágicas do terminal: são **variáveis de ambiente globais** já configuradas pelo sistema no arranque da sessão.
  * Por estarem no ambiente, qualquer comando ou script (`ls`, `python`, `./meu_script.sh`) consegue ler o seu valor.

-----

## Variáveis na Shell: Locais vs. Globais

  * **Variáveis Locais:**
      * Criadas com uma atribuição simples (`NOME="valor"`).
      * Existem **estritamente na janela/linha de comandos atual** (privadas).
      * Não são passadas a programas, comandos ou scripts instanciados a partir dessa sessão.

      ```bash
      $ CURSO="LEI"
      ```

  * **Variáveis de Ambiente (Globais):**
      * Criadas ou promovidas explicitamente com o comando **`export`**.
      * Ficam registadas no ambiente do sistema da sessão ativa.
      * São disponibilizadas e partilhadas com **todos os comandos e scripts** que executamos.

      ```bash
      $ export CURSO="LEI"
      ```

-----

## Herança de Variáveis na Shell

A *shell* inicia um  **processo filho** independente ao executar um script:

  * O processo filho **não herda** as variáveis locais da janela progenitora.
  * O processo filho **recebe uma cópia** de todas as variáveis promovidas com `export` (globais).

```bash
# Conteúdo do script 'saudacao.sh' (criado com permissão chmod +x):
# echo "Bem-vindo ao curso: $CURSO"

# 1. Com variável local: o script não tem acesso ao valor
$ CURSO="LEI"
$ ./saudacao.sh
Bem-vindo ao curso:

# 2. Promovendo a variável com export: o script herda o valor
$ export CURSO="LEI"
$ ./saudacao.sh
Bem-vindo ao curso: LEI
```

-----

## Inspeção e Gestão de Variáveis de Ambiente (Globais)

  * **`printenv [CHAVE]` (Consulta Rápida):** Inspeciona uma variável de ambiente específica (ou lista todas):

    ```bash
    $ printenv USER          # Devolve o utilizador atual
    $ printenv CURSO         # Devolve "LEI" (apenas se exportada; vazio se local)
    ```

  * **`env` (Ambiente e Execução Controlada):** Exibe as variáveis de ambiente ou executa comandos com variáveis temporárias:

    ```bash
    $ env                    # Lista todas as variáveis exportadas
    $ env PORT=8080 comando  # Aplica PORT apenas durante a execução do comando
    ```

  * **`unset` (Eliminar da Sessão):** Elimina a variável (local ou exportada) da sessão ativa:

    ```bash
    $ unset CURSO
    $ printenv CURSO         # Não devolve conteúdo (já não existe)
    ```

-----

## Persistência de Ambiente: Ficheiros de Inicialização da Shell

O conteúdo alocado na memória volátil é descartado ao encerrar uma sessão de terminal. A persistência de variáveis e configurações é assegurada por ficheiros de arranque:

  * **Ciclo de Inicialização da Shell Interativa:**
      * No arranque de uma nova sessão, a shell processa o ficheiro de configuração no `$HOME`:
        * No **Linux (Bash)**: processa o ficheiro **`~/.bashrc`**.
        * No **macOS (Zsh)**: processa o ficheiro **`~/.zshrc`**.
      * Quaisquer definições exportadas tornam-se disponíveis em todas as sessões subsequentes.

  * **Registo de Variáveis Persistentes:**

    ```bash
    # Registo no ficheiro pessoal (~/.bashrc no Linux ou ~/.zshrc no Mac)
    $ echo 'export GEMINI_API_KEY="AIzaSy..."' >> ~/.bashrc  # ou ~/.zshrc
    ```

  * **Arquitetura Modular de Configuração:**
      * Por razões de organização e isolamento, credenciais devem residir em ficheiros dedicados (e.g., `~/.api_keys`), importados no ficheiro da shell.

        ```bash
        [ -f ~/.api_keys ] && source ~/.api_keys
        ```

-----

## Recarregar o Ambiente com source e Segurança com chmod 600

  * **O Comando `source`:**
      * Executa as instruções do ficheiro especificado **no contexto da shell ativa**, sem instanciar um novo processo.
      * Permite atualizar o estado de variáveis sem necessidade de reiniciar a sessão de terminal.

        ```bash
        $ source ~/.bashrc   # ou: source ~/.zshrc
        ```

  * **Segurança em Ambientes Multi-utilizador:**
      * Permissões por omissão (e.g., `644`) autorizam a leitura de ficheiros por qualquer utilizador.
      * Ficheiros com credenciais ou chaves criptográficas exigem restrição de leitura e escrita apenas ao proprietário.

        ```bash
        $ chmod 600 ~/.api_keys
        $ ls -l ~/.api_keys
        -rw------- 1 aluno aluno 52 Sep 28 10:00 /home/aluno/.api_keys
        ```

-----

## Arquivo e Compressão de Dados com tar

O utilitário **`tar`** (*Tape Archive*) representa a norma POSIX padrão para agregar hierarquias de ficheiros e pastas num único arquivo comprimido:

  * **Criação de arquivo comprimido (`.tar.gz`):**

    ```bash
    $ tar -czvf backup_projeto.tar.gz ~/IEI/meu_projeto/
    ```

    * `-c` : Criação de um novo arquivo (*create*).
    * `-z` : Compressão através do algoritmo **gzip**.
    * `-v` : Listagem detalhada dos ficheiros processados (*verbose*).
    * `-f` : Especificação do nome do ficheiro de saída (*file*).

  * **Inspeção de integridade e conteúdo sem descompressão:**

    ```bash
    $ tar -tf backup_projeto.tar.gz
    ```

  * **Extração para diretório de destino específico (`-C`):**

    ```bash
    $ tar -xzvf backup_projeto.tar.gz -C /tmp/restauro/
    ```

-----

## Parte II: Inteligência Artificial na Engenharia de Software

Tópicos abordados nesta segunda parte:

  * **Fundamentos e Mecânica de LLMs:**
      * Inferência estatística, tokens, janelas de contexto e mitigação de alucinações.
  * **Consumo e Gestão de Custos:**
      * Paradigmas de interação, consumo de APIs via `curl` e controlo de custos (*FinOps*).
  * **Engenharia de Contexto:**
      * Formulação técnica direta, delimitação de contexto e calibração por exemplos (Few-Shot).
  * **Agentes Autónomos e Segurança:**
      * Arquitetura com `AGENTS.md`, Skills, protocolo MCP e salvaguardas rígidas (*hard guardrails*).

-----

## A Postura da Engenharia Informática perante a IA

> *"Em engenharia, não tratamos a inteligência artificial como um oráculo mágico, mas como um componente computacional com entradas, saídas, custos mensuráveis e modos de falha."*

\vspace{0.8em}

::::: columns
::: {.column width="70%"}

  * **A Mudança de Paradigma na Indústria:**
      * Os Modelos de Linguagem de Grande Escala (LLMs) evoluíram de assistentes de conversação para **peças estruturais na automação e construção de software**.
  * **A Postura do Engenheiro Informático:**
      * O consumidor comum maravilha-se passivamente com o texto gerado.
      * O engenheiro precisa de **compreender** o motor, **controlar** o determinismo das respostas e **validar** criticamente os resultados.

:::
::: {.column width="30%"}

\begin{center}
\includegraphics[width=0.95\linewidth,height=0.48\textheight,keepaspectratio]{ai_engineering_concept.jpg}
\end{center}

:::
:::::

-----

## Como Funcionam as LLMs: Da Estatística às Representações Internas

Um **LLM** assenta na arquitetura **Transformer** e no cálculo de probabilidade condicional:

  * **Mecanismo Autoregressivo Fundamental:**
      * Treinado para estimar a distribuição de probabilidades do próximo elemento de texto: $P(w_t \mid w_1, \dots, w_{t-1})$.
  * **Modelos Internos e Semântica:**
      * Prever com rigor texto humano complexo exige mais do que memorização superficial: nas camadas intermédias da rede emergem **representações geométricas de conceitos**, relações de causalidade e estruturas lógicas abstratas.
  * **Inferência de Intenção e Deliberação (Pós-Treino & RL):**
      * O alinhamento por aprendizagem por reforço especializa o modelo para **deduzir a meta e intenção do utilizador**, permitindo aos modelos contemporâneos deliberar internamente (*reasoning tokens*) antes de responder.

-----

## Falibilidade das LLMs: O Fenómeno das Alucinações

> Apesar da sofisticação atual, **LLMs permanecem sistemas probabilísticos** e desprovidos de **verificação factual formal**, mantendo a suscetibilidade a respostas sintaticamente perfeitas mas falsas (**alucinações**).

\vspace{1em}

\begin{center}
\includegraphics[width=0.68\linewidth,height=0.42\textheight,keepaspectratio]{ai_hallucination_pizza_glue.jpg}\\
\vspace{0.2em}
\textit{\tiny Caso real (Google AI Overviews, 2024): ingestão de sátira do Reddit recomendando cola não-tóxica para fixar queijo à pizza.}
\end{center}

-----

## Unidade de Processamento: Tokens vs. Palavras

LLMs não operam sobre palavras completas nem caracteres isolados:

  * A unidade de processamento fundamental é o **Token**.
  * Um token $\Leftrightarrow$ fragmento de texto (subpalavra, pontuação, caractere, etc.).
  * Em média **100 palavras $\approx 140$ tokens** (Inglês)
    * Em português a razão é ligeiramente superior.
  * Decomposição em tokens:
    * `"Terminal"` $\rightarrow$ `["Term", "inal"]` (2 tokens)
    * `"echo 'ola'"` $\rightarrow$ `["echo", " '", "ola", "'"]` (4 tokens)

### Implicações:
  1. **Horizonte de Atenção:** Volume total de tokens (instruções, histórico e resposta) que LLM consegue correlacionar e manter em memória ativa num dado instante.
  2. **Métricas de Consumo:** Utilização de APIs quantificada e tarifada em função do volume total de tokens processados.

-----

## Janela de Contexto e Hiperparâmetros

Conceitos e parâmetros operacionais essenciais associados a LLMs:

  * **Janela de Contexto ($L_{\max}$) vs. Teto de Saída (*Max Output Tokens*):**
      * Janela total (memória de trabalho ativa) atinge **1.000.000+ tokens** para leitura/ingestão
        * Resposta gerada por chamada tem um teto inferior (e.g., **4.096** a **8.192 tokens**).
  * **Higiene de Contexto (*Context Reset*):**
      * **Boa prática:** Limpar a janela de contexto (iniciar nova sessão ou `/clear`) na transição de tarefas.
      * Sessões prolongadas acumulam contexto obsoleto (*context drift*), encarecem cada pedido e aumentam substancialmente o risco de alucinações.
  * **Temperatura ($\tau$):**
      * **Baixa ($\tau = 0.0$ a $0.2$):** Saídas deterministas e consistentes (**adequado para código e comandos**).
      * **Alta ($\tau = 0.8$ a $1.2$):** Maior dispersão estocástica e criatividade (**adequado para exploração conceptual**).

-----

## Alucinações e Validação Crítica em Engenharia

Riscos operacionais na geração de instruções para a linha de comandos com LLMs:

  * O modelo pode sugerir **parâmetros e opções sintáticas inexistentes** (e.g., `tar -z --exclude-all-errors`).
  * O modelo pode induzir **comandos com efeitos destrutivos irreversíveis** perante ambiguidades no pedido (`rm -rf /tmp/..`).
  * O modelo pode alucinar dependências e bibliotecas inexistentes no sistema operativo alvo.
  * **Poluição de Contexto (*Context Drift*):** Misturar tarefas distintas na mesma sessão faz o modelo ancorar-se em premissas antigas e contraditórias.

**A responsabilidade de execução e validação técnica recai exclusivamente no engenheiro.**

-----

## Paradigmas de Interação com Modelos de IA

\begin{center}
\includegraphics[height=0.68\textheight,keepaspectratio]{ai_interaction_paradigms.jpg}
\end{center}

-----

## Modelos de Consumo: Subscrições vs. Interfaces de Programação (APIs)

Dois modelos de consumo de LLMs:

  * **Subscrições de Utilizador (Tarifário Fixo / Flat-Rate):**
      * Exemplos: Claude Pro, Copilot, Antigravity, ChatGPT Plus.
      * Custo periódico fixo por credencial do utilizador, com suporte para interfaces web, IDEs e ferramentas de terminal.
      * Consumo baseado em **quotas temporais**: o esgotamento temporário suspende pedidos adicionais sem gerar encargos financeiros inesperados.

  * **APIs de Desenvolvedor (Pagamento por Consumo / Pay-as-you-go):**
      * Faturação calculada estritamente por milhão de tokens (entrada e saída), autenticada através de **Chaves de API (*API Keys*)**.
      * Padrão mandatório para **pipelines de CI/CD**, serviços autónomos e **automação de sistemas**.
      * **Risco Operacional:** Não possui limites de consumo pré-estabelecidos por omissão; **iterações descontroladas incorrem em débito direto e contínuo de custos operacionais.**

-----

## Gestão de Custos em APIs e o Efeito Multiplicador de Agentes

O desenvolvimento de agentes e scripts de automação exige governança financeira estrita (**FinOps**):

  * **O Efeito Multiplicador em Agentes Autónomos:**
      * Num fluxo de deliberação iterativo com 30 passos, a cada ciclo o agente retransmite **o histórico conversacional acumulado e a totalidade dos ficheiros ingeridos**.
      * Um repositório com 50.000 tokens executado em 30 iterações totaliza **1.500.000 tokens de entrada** numa única validação.
  * **Risco de Ciclos Infinitos (*Infinite Retry Loops*):**
      * Falhas na definição de condições de paragem em scripts de automação originam invocações contínuas da API com consumo financeiro acelerado.

-----

## Gestão de Custos em APIs: Salvaguardas e Cuidados

  1. **Limites Rígidos de Despesa (*Hard Spend Limits*):** Configurar um teto financeiro inultrapassável na consola de gestão da API (suspensão imediata do serviço ao atingir o montante).
  2. **Alertas de Faturação (*Budget Alerts*):** Ativar sempre como boa prática de monitorização; contudo, ter consciência da sua latência (várias horas), não travando consumos descontrolados em tempo real.
  3. **Controlo no Código (*Loop Cap* e `max_output_tokens`):** Impor limites máximos de iterações em scripts (`MAX_RETRIES=5`) e limitar tokens de resposta no pedido JSON.
  4. **Proteção de Chaves de API:** Nunca utilizar codificação estática (*hardcoding*) em ficheiros de código ou scripts guardados em repositórios; utilizar sempre variáveis de ambiente, secret vaults, e controlos de acesso rigorosos.
  5. **Utilização de *Free Tiers*:** Usar, por exemplo, o Google AI Studio (Free Tier) que impõe quotas rígidas por minuto (15 RPM) sem exigir cartão de crédito, eliminando passivos financeiros.

-----

## A Interface de Linha de Comandos no Ecossistema de IA

Propriedades técnicas que fundamentam a preferência pelo terminal na integração de LLMs:

  * **Composabilidade Operacional:** A resposta gerada por um LLM pode ser redirecionada diretamente para ficheiros, compiladores ou scripts via *pipes* (`|`).
  * **Execução Headless e Automação:** Processos agendados (*cron*) ou pipelines de integração contínua (CI/CD) comunicam com LLMs sem dependência de interfaces gráficas.
  * **Interoperabilidade REST:** Através do utilitário `curl`, qualquer sistema POSIX pode estabelecer comunicação com LLMs.

-----

## Integração com APIs via curl no Terminal

Consumo direto de modelos generativos a partir da linha de comandos através de pedidos HTTP POST com payload JSON para a moderna **Gemini Interactions API**:

```bash
$ curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/interactions" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-3.5-flash-lite",
    "input": "Explica em 1 frase o comando: tar -czvf arq.tar.gz dir/"
  }'
```

  * **`-s` :** Modo silencioso (omissão de indicadores de transferência).
  * **`-X POST` :** Método HTTP para transmissão de dados de inferência.
  * **`-H "x-goog-api-key: $GEMINI_API_KEY"` :** Autenticação segura por cabeçalho HTTP (evita expor o segredo no URL).
  * **`-H "Content-Type: application/json"` :** Tipificação do corpo do pedido.
  * **`model` e `input` :** Especificação do modelo (`gemini-3.5-flash-lite`) e instrução a processar.

-----

## Formulação de Instruções: O Mito das Personas

Ao interagir com LLMs, via janelas de chat, ferramentas de consola ou APIs, surge a questão central: *como formular instruções técnicas eficazes?*

### Na Fase Inicial de Disseminação da Tecnologia

  * Popularizou-se o recurso a papéis figurativos: **Atua como um engenheiro Linux sénior com 30 anos de experiência e responde...**

### Comportamento em Modelos Contemporâneos

  * Em tarefas formais de lógica, computação e engenharia, a especificação de personas não apresenta melhoria estatística no desempenho.
    * Induz frequentemente respostas prolixas e preâmbulos conversacionais não informativos.
  * Modelos de fronteira já possuem conhecimento técnico consolidado; a precisão depende do **contexto fornecido sobre o sistema** e da **clareza das restrições estipuladas**.

-----

## Transição: Da Engenharia de Prompts para Engenharia de Contexto

A abordagem operacional evoluiu da redação empírica para a **Engenharia de Contexto**:

\vspace{0.8em}
\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    boxemp/.style={draw=black!40, fill=black!5, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\footnotesize},
    arr/.style={-{Latex[length=2.5mm]}, dashed, thick, color=uagreen!80!black}
]
\node[boxemp] (P) {\textbf{Abordagem Empírica}\\\scriptsize(Personas e Truques Textuais)};
\node[box, right=2.0cm of P] (C) {\textbf{Engenharia de Contexto}\\\scriptsize(Fronteiras, Restrições e Dados)};
\draw[arr] (P) -- node[above, font=\scriptsize, text=black!70] {Evolução da Prática} (C);
\end{tikzpicture}
\end{center}
\vspace{0.6em}

A parametrização do modelo baseia-se em princípios deterministas:

  1. Especificação formal e direta do objetivo a cumprir.
  2. Fornecimento delimitado dos dados de entrada (ficheiros, esquemas e registos).
  3. Estipulação de restrições negativas inequívocas (operações proibidas).
  4. Definição do formato estrutural obrigatório da resposta.

-----

## Os Quatro Pilares da Engenharia de Contexto

Exemplo: Estruturação de pedidos para integração determinista em ambientes de terminal (*shell*):

| Componente | Objetivo | Exemplo Técnico |
| :--- | :--- | :--- |
| **1. Tarefa (Task)** | Enunciado direto do objetivo técnico | *"Gera o comando Bash para listar ficheiros modificados nas últimas 24 horas."* |
| **2. Contexto (Context)** | Ambiente de execução e dados | *"Ambiente Linux POSIX (Ubuntu 24.04), interpretador Bash, caminho /var/log."* |
| **3. Restrições (Constraints)**| Limites formais de execução | *"Não utilizar interpretadores externos (awk, python). Utilizar estritamente o utilitário find."* |
| **4. Formato (Format)** | Estrutura sintática da resposta | *"Devolver exclusivamente o comando em linha única, sem blocos markdown ou preâmbulos."* |

-----

## Delimitação Estruturada de Contexto

Na transmissão de ficheiros ou registos (*logs*) para um modelo, é imperativo separar formalmente **instruções** de **dados** recorrendo a delimitadores inequívocos (e.g., tags XML ou blocos de formatação):

```markdown
Analisa o log de erros abaixo e identifica o serviço afetado.

<error_log>
Sep 28 10:14:02 srv1 nginx[1420]: bind() to 0.0.0.0:80 failed (98: Address already in use)
Sep 28 10:14:02 srv1 systemd[1]: nginx.service: Failed with result 'exit-code'.
</error_log>

Responde no formato:
Serviço: <nome>
Causa: <motivo>
```

**A delimitação estruturada clarifica o papel de cada bloco e reduz o risco de o modelo interpretar dados ou mensagens de erro como novas instruções (*prompt injection*).**

-----

## Calibração por Exemplos: Zero-Shot vs. Few-Shot

Ao contrário da instrução direta (**Zero-Shot**), a abordagem **Few-Shot** recorre a exemplos resolvidos no *prompt* para o modelo deduzir a estrutura e campos por analogia (*in-context learning*), dispensando regras exaustivas:

```text
Analisa o incidente e devolve o diagnóstico estruturado.

[Exemplo 1]
Entrada: O disco /dev/sda1 atingiu 98% de ocupação na pasta /var.
Saída:
  Severidade: ALTA
  Componente: Armazenamento (/var)
  Ação:       Purgar logs e ficheiros temporários

[Exemplo 2]
Entrada: Três tentativas falhadas de autenticação SSH para root.
Saída:
  Severidade: MÉDIA
  Componente: Segurança (SSH)
  Ação:       Inspecionar logs e bloquear IP de origem

[Novo Pedido a Processar]
Entrada: O processo de backup consumiu 95% da CPU durante 40 min.
Saída:
  Severidade: ALTA                                   <-- [CAMPOS
  Componente: Processador (Backup)                   <--  GERADOS
  Ação:       Ajustar prioridade do processo.        <--  PELA IA]
```

-----

## Além da Invocação Pontual: Agentes Autónomos

Transição de paradigma: da **invocação pontual** (pergunta-resposta estática) para **sistemas autónomos** que operam em ciclo fechado sobre o sistema:

* **Definição Formal de Agente (Ciência da Computação & IA):**
    * Uma entidade computacional autónoma que **perceciona o seu ambiente** através de sensores, **delibera** em função de objetivos, e **atua sobre o ambiente** através de atuadores num ciclo contínuo (*Perceive $\rightarrow$ Reason $\rightarrow$ Act*).

* **Concretização em Agentes de Engenharia de Software (Coding Agents):**
    * **Ambiente:** O repositório de código, o sistema de ficheiros e o terminal / *shell* Linux.
    * **Perceção (Sensores):** Leitura de ficheiros, inspeção de erros de compilação e captura da saída de comandos (`stdout`/`stderr`).
    * **Raciocínio (Deliberação):** Decomposição de tarefas, seleção de ferramentas e consulta de regras do projeto (`AGENTS.md`).
    * **Ação (Atuadores):** Edição de ficheiros e execução de comandos de teste/compilação no terminal.
    * **Ciclo de Feedback:** Avaliação dos resultados e correção iterativa até à conclusão do objetivo.

-----

## Arquitetura de Controlo: AGENTS.md, Skills e MCP

O controlo e extensão de agentes em ambientes de engenharia assenta em três pilares complementares:

\vspace{0.6em}
\begin{center}
\begin{tikzpicture}[
    agentbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\small},
    pillar/.style={draw=uagreen!80!black, fill=uagreen!8, rounded corners=3pt, thick, align=center, inner sep=4pt, text width=3.4cm, font=\scriptsize},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!70}
]
\node[agentbox] (AGENT) {\textbf{Agente de IA}};
\node[pillar, below=0.7cm of AGENT] (R2) {\textbf{2. Skills}\\\textbf{Playbooks Modulares}\\\textit{\tiny(Conhecimento especializado sob demanda)}};
\node[pillar, left=0.35cm of R2] (R1) {\textbf{1. AGENTS.md}\\\textbf{Constituição \& Regras}\\\textit{\tiny(Contexto permanente do repositório)}};
\node[pillar, right=0.35cm of R2] (R3) {\textbf{3. Protocolo MCP}\\\textbf{Conetores de Ferramentas}\\\textit{\tiny(Padronização de ferramentas e acessos)}};

\draw[arr] (AGENT.south) -- (R1.north);
\draw[arr] (AGENT.south) -- (R2.north);
\draw[arr] (AGENT.south) -- (R3.north);
\end{tikzpicture}
\end{center}
\vspace{0.4em}

-----

## Especificação do Repositório: O Ficheiro AGENTS.md

### Conceito e Finalidade:

  * Ficheiro em formato Markdown posicionado na raiz do repositório de código ou em pastas específicas a que o agente tenha acesso.
  * Constitui o documento de referência e alinhamento normativo para assistentes e agentes autónomos que operam sobre a base de código.
  * Ambientes de desenvolvimento e agentes autónomos (Antigravity, Cursor, Claude Code, Copilot) ingerem este contexto antes da geração de código ou execução de tarefas.
  * **Âmbito Hierárquico:** Pode ser definido globalmente na raiz do projeto ou especializado por subpasta (e.g., `frontend/AGENTS.md`, `backend/AGENTS.md`).

-----

## Especificação do Repositório: O Ficheiro AGENTS.md

### Objetivos Operacionais:
  * Elimina a introdução indevida de tecnologias e dependências não previstas no projeto.
  * Impõe a conformidade com as normas arquiteturais, estilo de código e tratamento de erros estabelecidos pela equipa.
  * Define diretrizes operacionais explícitas (proibição de comandos destrutivos e obrigatoriedade de validação por testes).

-----

## Estrutura Típica de um Ficheiro AGENTS.md

Exemplo de especificação normativa para um projeto curricular:

```markdown
# Diretrizes do Projeto IEI - Laboratório

## 1. Stack Tecnológica & Ambiente
- Sistema Operativo: Linux POSIX (Ubuntu 24.04 / WSL 2).
- Shell: Bash 5.x. Scripts devem iniciar com `#!/bin/bash`.

## 2. Comandos Padrão de Execução
- Testes: executar `make test` antes de submeter alterações.
- Compilação: executar `make all`.

## 3. Regras de Código & Segurança
- Nunca usar palavras-passe ou chaves de API hardcoded.
- Não utilizar bibliotecas externas sem autorização prévia.
- Variáveis locais em scripts devem usar nomes descritivos em minúsculas.
```

-----

## Padronização de AGENTS.md em Projetos de Software

::::: columns
::: {.column width="60%"}

  * **Comandos de Projeto (Mandatório):**
    * Comandos para *build*, *lint*, execução e testes unitários.
  * **Estrutura de Código (Mandatório):**
    * Mapa do diretório (`src/api`, `src/core`, `tests/`) para evitar navegação cega do agente.
  * **Convenções e Estilo (Recomendado):**
    * Tipificação estrita, *docstrings* e padrões de commits (*Conventional Commits*).
  * **Fronteiras e Restrições (*Boundaries*):**
    * Ficheiros e pastas que o agente está **estritamente proibido** de alterar (e.g., migrações, segredos).

\vspace{0.3em}
\textit{\tiny Referência: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.74\textheight,keepaspectratio]{agents_md_template_generator.png}
\end{center}

:::
:::::

-----

## Estudo de Caso: AGENTS.md num Projeto Real de Produção

Especificação completa para um serviço backend (FastAPI, PostgreSQL e Poetry):

\vspace{0.2em}

::::: columns
::: {.column width="52%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{example_agents_md_part1.png}
\end{center}

:::
::: {.column width="48%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.45\textheight,keepaspectratio]{examples_agents_md_part2.png}
\end{center}

\vspace{0.2em}
\textit{\tiny Fonte: Addy Osmani, \href{https://addyosmani.com/agents/15-agents-md/}{addyosmani.com/agents/15-agents-md/}}

:::
:::::

-----

## Impacto do Contexto no Comportamento do Agente

Comparação perante a mesma solicitação técnica: *"Gera o script de backup do projeto."*

### Sem `AGENTS.md` (Inferência não ancorada no repositório):

```python
# O modelo introduz Python e dependências externas de cloud
import boto3
s3 = boto3.client('s3')
s3.upload_file('backup.zip', 'meu-bucket', 'backup.zip')
```
*(Incompatível com as restrições de um projeto estritamente centrado em utilitários Bash nativos)*

### Com `AGENTS.md` (Conformidade com o contrato operacional do projeto):

```bash
#!/bin/bash
set -euo pipefail
tar -czvf "backup_$(date +%Y%m%d).tar.gz" .
echo "Backup gerado com sucesso."
```
*(Total conformidade com o ambiente e as convenções definidas no repositório)*

-----

## Segurança Rigorosa: Soft vs. Hard Guardrails

Princípio fundamental de segurança em inteligência artificial:

> **"Prompts em linguagem natural não constituem barreiras de segurança."**

A enunciação de proibições no `AGENTS.md` (e.g., *"Nunca executes `rm -rf`"*) representa uma **Soft Boundary**:

  * O modelo opera por cooperação estatística, podendo ser contornado através de **Prompt Injection** (instruções maliciosas embutidas em ficheiros ingeridos) ou alucinação.

-----

## Segurança Rigorosa: Soft vs. Hard Guardrails

### Barreiras Rígidas de Segurança (Hard Boundaries Deterministas)
A integridade do sistema requer mecanismos de controlo deterministas externos ao modelo:

  * **Intercetores de Ferramentas (*Tool Interceptors / Allowlist*):**
      * Módulos de software que analisam os comandos antes do seu envio ao sistema operativo, bloqueando execuções com padrões não autorizados.
  * **Humano no Ciclo (*Human-in-the-Loop* - HITL):**
      * Obrigatoriedade de confirmação manual explícita para quaisquer ações suscetíveis de causar efeitos irreversíveis.
  * **Isolamento em Sandbox (Contentores Docker):**
      * Execução em ambientes efémeros sem privilégios administrativos e com sistemas de ficheiros do anfitrião montados em modo de apenas leitura (*read-only*).

-----

## Skills: Procedimentos Modulares sob Demanda

Enquanto o `AGENTS.md` estabelece a especificação global do repositório, uma **Skill** define o procedimento técnico detalhado para uma tarefa específica.

  * **Critério de Eficiência de Contexto:**
      * A inclusão exaustiva de todos os procedimentos técnicos no `AGENTS.md` provocaria a saturação desnecessária da janela de contexto.
  * **Princípio Operacional:**
      * Uma skill é estruturada num diretório dedicado com um ficheiro descritor `SKILL.md`, ingerido pelo agente estritamente mediante necessidade funcional.
      * Exemplos: *Skill de Auditoria de Segurança de Comandos*, *Skill de Migração de Esquemas SQL*, *Skill de Validação de Acessibilidade*.

-----

## Implementação de uma Skill: safe-cli


```markdown
---
name: safe-cli
description: Avalia a segurança e o nível de risco de comandos UNIX (Linux e macOS).
---

# Procedimento de Análise:
Ao receber um comando para validação:
1. Classifica o risco: [SEGURO], [ATENÇÃO] ou [PERIGOSO].
2. Sintetiza o objetivo do comando numa frase técnica.
3. Decompõe as opções e argumentos utilizados.
4. Perante operações potencialmente destrutivas (rm, dd, chmod 777, redirecionamento >),
   adverte sobre o impacto potencial e propõe uma alternativa segura.
```

-----

## Model Context Protocol (MCP): Arquitetura de Conetividade

  * **Limitação Histórica:** Ferramentas desenvolviam conetores proprietários *ad-hoc* para interagir com bases de dados, repositórios Git ou ficheiros.
  * **Arquitetura Cliente-Servidor:**
      * **Servidor MCP:** expõe ferramentas, recursos e contexto operacional de forma controlada.
      * **Cliente MCP (IDE/Agente):** faz a mediação entre o modelo e os recursos externos.

\vspace{0.3em}
\begin{center}
\begin{tikzpicture}[
    clientbox/.style={draw=black!70, fill=black!5, rounded corners=4pt, thick, align=center, inner sep=5pt, font=\footnotesize},
    serverbox/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=3pt, text width=3.2cm, font=\scriptsize},
    arr/.style={{Latex[length=2mm]}-{Latex[length=2mm]}, thick, color=uagreen!80!black}
]
\node[clientbox] (IDE) {\textbf{Agente / IDE}\\\scriptsize(Cliente MCP)};
\node[serverbox, right=2.6cm of IDE.center, yshift=1.05cm] (S1) {\textbf{Servidor Git}\\\tiny(commits, branches, diffs)};
\node[serverbox, right=2.6cm of IDE.center] (S2) {\textbf{Servidor Base de Dados}\\\tiny(consultas SQL, esquemas)};
\node[serverbox, right=2.6cm of IDE.center, yshift=-1.05cm] (S3) {\textbf{Servidor Sistema Ficheiros}\\\tiny(leitura e escrita de ficheiros)};

\draw[arr] (IDE.east) -- node[above, sloped, font=\tiny, text=black!70] {Protocolo MCP} (S1.west);
\draw[arr] (IDE.east) -- node[above, font=\tiny, text=black!70] {Protocolo MCP} (S2.west);
\draw[arr] (IDE.east) -- node[below, sloped, font=\tiny, text=black!70] {Protocolo MCP} (S3.west);
\end{tikzpicture}
\end{center}
\vspace{0.2em}

Com o MCP, o acesso a recursos externos realiza-se sob permissões explícitas e canais padronizados.

-----

## MCP na Prática: Implementação e Registo de Ferramentas

Exemplo de conetividade local entre processos via canais padrão (\texttt{stdio}):

::::: columns
::: {.column width="50%"}

### 1. Servidor MCP (`servidor_git.py`) - expõe função:
```python
# SDK para implementar MCP
from mcp.server.fastmcp import FastMCP
import subprocess

# Nome servidor MCP
mcp = FastMCP("git-tools")

# Regista ferramenta para o LLM
@mcp.tool()
def git_status() -> str:
    # Descrição para o LLM saber o que este método faz
    """Devolve ficheiros modificados."""
    return subprocess.check_output(
        # Comando a executar no sistema operativo para este método
        ["git", "status", "-s"], text=True
    )

if __name__ == "__main__":
    # Inicia servidor com comunicação via stdio (JSON-RPC)
    mcp.run()
```

:::
::: {.column width="50%"}

### 2. Registo no (IDE / Agente) Cliente (`mcp_config.json`):
```json
{
  "mcpServers": {
    "git-tools": {
      "command": "python",
      "args": ["servidor_git.py"]
    }
  }
}
```

:::
:::::

-----

## Referências e Recursos Técnicos

Documentação de apoio e normas técnicas para consulta:

  * **Google AI Studio (Acesso e Gestão de Chaves de API):**
      * [https://aistudio.google.com/](https://aistudio.google.com/)
  * **Documentação Oficial da API Google Gemini:**
      * [https://ai.google.dev/docs](https://ai.google.dev/docs)
  * **Especificação do Model Context Protocol (MCP):**
      * [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
  * **Diretrizes de Context Engineering & Prompts (Anthropic):**
      * [https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
  * **Addy Osmani — Building Effective Agents with AGENTS.md:**
      * [https://addyosmani.com/agents/15-agents-md/](https://addyosmani.com/agents/15-agents-md/)
