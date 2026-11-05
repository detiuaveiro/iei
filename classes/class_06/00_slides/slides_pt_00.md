---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Controlo de Versões com Git & Plataforma Colaborativa GitHub"
institute: Universidade de Aveiro
date: November 02, 2026
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
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \BeforeBeginEnvironment{Shaded}{\vspace{1.0em}}
 - \AfterEndEnvironment{Shaded}{\vspace{0.6em}}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Visão Geral da Sessão

  * **Parte I — Fundamentos do Controlo de Versões & Arquitetura:**
      * O desafio da evolução do código e colaboração, falhas das abordagens ingénuas (cópias manuais e nuvem), taxonomia de VCS, matriz comparativa (CVCS vs. DVCS) e o Git como padrão de facto da indústria.
  * **Parte II — Aspetos Funcionais do Git & Ciclo de Vida Local:**
      * Conceitos fundamentais (`Repositório`, `Commit`, `Branch`, `HEAD`), as três zonas operacionais e estados dos ficheiros, comandos essenciais (`init`, `clone`, `status`, `add`, `commit`), regras e Conventional Commits, `log`, etiquetagem (`tag`) e `.gitignore`.
  * **Parte III — Ramificação, Integração & Resolução de Conflitos:**
      * O paradigma de ramos (*branches*) e ponteiro `HEAD`, estratégias de integração (`merge` *fast-forward* vs. *3-way*), linearização com `rebase`, comparação arquitetural e gestão de conflitos.
  * **Parte IV — Colaboração Distribuída & Workflows em Equipa:**
      * Repositórios remotos (`origin`), sincronização (`fetch`, `pull`, `push`), modelos colaborativos (*GitFlow* vs. *Trunk-Based Development*), *Feature Branches* com *Pull Requests* e publicação de versões (*releases*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos do Controlo de Versões \& Arquitetura}}
\end{center}

-----

## O Desafio da Evolução do Código e Colaboração em Software

O desenvolvimento de software é inerentemente dinâmico e colaborativo:

  * **Natureza Dinâmica do Código:**
      * Evolução contínua: correção de *bugs*, expansão de funcionalidades e refatoração.
      * Múltiplos ficheiros interdependentes a mudar em simultâneo.
  * **Três Questões Centrais da Engenharia:**
      * **Rastreabilidade:** *O que* mudou, *quando*, *por que razão* e por *quem*?
      * **Reversibilidade:** Como testar novas ideias sem comprometer a versão estável?
      * **Colaboração Concorrente:** Como trabalhar em equipa sem sobrescrever o trabalho alheio?

\vspace{0.8em}

\begin{center}
\textbf{Perante estes desafios, quais foram as soluções intuitivas (e incorretas) mais comuns?}
\end{center}

-----

## Abordagens Ingénuas (I): O Caos das Cópias Manuais

::::: columns
::: {.column width="60%"}

A primeira reação para guardar versões antigas e testar ideias é duplicar ficheiros:

  * **Anti-Padrão dos Sufixos:**
      * `projeto_v1.c`, `projeto_v2_corrigido.c`
      * `projeto_final.c`, `projeto_final_AGORA_VAI.c`
  * **Porque Falha?**
      * **Opacidade:** O nome não revela que linhas ou funções foram alteradas.
      * **Sem Contexto:** Perde-se a explicação técnica (*porquê*) de cada alteração.
      * **Reversibilidade Frágil:** Reverter um ficheiro quebra o projeto global.
      * **Datas Infiáveis:** Metadados do SO são facilmente alterados ao copiar ficheiros.

\vspace{0.4em}
\textbf{A duplicação manual é opaca, propensa a erros e inviável à escala de um projeto real.}

:::
::: {.column width="40%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.72\textheight,keepaspectratio]{figures/phd_not_final.png}

\vspace{0.2em}
\textit{\tiny "notFinal.doc" --- Jorge Cham (PhD Comics)}
\end{center}

:::
:::::

-----

## Abordagens Ingénuas (II): Sincronização em Nuvem e E-mail

Para resolver a **colaboração em equipa**, o recurso habitual são canais comuns de partilha:

  * **1. Pastas Partilhadas na Nuvem (Dropbox, Google Drive):**
      * **Foco Errado:** Concebidas para sincronizar documentos, não código-fonte.
      * **Gravação Cega (*Last-Write-Wins*):** O último a gravar apaga silenciosamente o trabalho dos outros.
      * **Conflitos Destrutivos:** Edições concorrentes geram ficheiros duplicados (`Cópia em Conflito`), sem fusão de código.
  * **2. Partilha de Ficheiros Compactados (.zip) por E-mail:**
      * Troca de versões paralelas (`projeto_v3_mario.zip` vs. `projeto_v3_ana.zip`).
      * **Pesadelo do Merge Manual:** Fundir alterações linha a linha via *copiar-colar* é inviável e gera erros graves.

\vspace{0.8em}

\begin{center}
\textbf{Sincronização de ficheiros $\neq$ Controlo de versões. Colaborar exige fusão estruturada de código.}
\end{center}

-----

## A Solução: Sistemas de Controlo de Versões (VCS)

Um **VCS** é a ferramenta que regista metadados e a evolução temporal de um projeto:

  * **Rastreabilidade Total:** Registo inequívoco de *quem*, *quando* e *porquê*.
  * **Reversibilidade (*Time Machine*):** Recuperação instantânea de qualquer estado anterior estável.
  * **Análise Diferencial:** Inspeção precisa linha a linha entre versões.
  * **Colaboração Segura:** Trabalho concorrente de múltiplos programadores com fusão controlada.

\vspace{0.8em}

\begin{center}
\textbf{O VCS converte o desenvolvimento num processo seguro, auditável e reprodutível.}
\end{center}

-----

## Taxonomia de VCS: Centralizado vs. Distribuído

\begin{center}
\includegraphics[width=\linewidth,height=0.80\textheight,keepaspectratio]{figures/vcs_centralized_vs_distributed.png}
\end{center}

-----

## Análise Comparativa: CVCS vs. DVCS

| Vetor de Comparação | CVCS (ex.: Subversion / Perforce) | DVCS (ex.: Git / Mercurial) |
| :--- | :--- | :--- |
| **Repositório e Histórico Local** | Apenas a cópia de trabalho atual (*working copy*) | **Clone completo com todo o histórico do projeto** |
| **Operação sem Rede (Offline)** | Limitada (apenas edição e `diff` da versão atual) | **Total (`commit`, `branch`, `log`, `merge` 100% locais)** |
| **Tolerância a Falhas (SPOF)** | Baixa (se o servidor central falhar, ninguém submete) | **Elevada (cada clone completo funciona como backup)** |
| **Velocidade de Operações** | Penalizada pela latência de rede ao servidor | **Quase instantânea (leitura/escrita em disco local)** |
| **Identificação de Versões** | Números sequenciais globais (`r1`, `r2`, `r3`...) | **Hashes criptográficos distribuídos (SHA)** |
| **Ramificação (*Branching*) e *Merge*** | Pesada (pastas no servidor; *merges* historicamente lentos) | **Leve e instantânea (ponteiros locais; fusão rápida)** |
| **Ficheiros Binários e *Locking*** | **Excelente (suporta *file locking* central e *checkouts* parciais)** | Fraco nativamente (histórico incha; sem *lock* offline; requer *Git LFS*) |
| **Controlo de Acesso (Segurança)** | **Granular (permissões de leitura/escrita por pasta/ficheiro)** | Global ao repositório (quem clona acede a toda a árvore) |

-----

## Git: O Padrão de Facto da Indústria

::::: columns
::: {.column width="66%"}

  * **Adoção Universal ($>90\%$ da Indústria):**
      * Ferramenta **open-source** que se tornou o padrão absoluto e a «língua franca» da engenharia de software contemporânea.
  * **Origem Pragmática (2005):**
      * Criado por **Linus Torvalds** para o **Kernel Linux**, exigindo um sistema distribuído livre, rápido e capaz de escalar para milhares de programadores.
  * **Por que Motivo Conquistou a Indústria?**
      * **Desempenho Local:** Operações executadas diretamente em disco local (em C nativo), sem penalização de latência de rede.
      * **Ramificação Leve ($O(1)$):** Criar ramos (*branches*) resume-se a criar ponteiros leves, viabilizando trabalho paralelo sem atrito.
      * **Integridade Criptográfica:** Histórico estruturado por hashes SHA (impossível adulterar ou corromper dados **sem deteção**).

:::
::: {.column width="34%"}

\begin{center}
\includegraphics[width=0.65\linewidth,keepaspectratio]{figures/git_logo.png}

\vspace{0.4em}
\includegraphics[width=0.95\linewidth,keepaspectratio]{figures/git_branching_illustration.png}

\vspace{0.3em}
{\scriptsize \href{https://git-scm.com/}{\texttt{git-scm.com}}}
\end{center}

:::
:::::

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Aspetos Funcionais do Git \& Ciclo de Vida Local}}
\end{center}

-----

## Conceitos Fundamentais do Git: O Modelo Mental

::::: columns
::: {.column width="55%"}

  * **1. Repositório (*Repository* / `.git/`):**
      * Base de dados local que guarda todo o histórico e metadados.
  * **2. *Commit* (*Snapshot*):**
      * Ponto de restauro imutável que regista a evolução do código.
      * Identificado por uma **Hash SHA** (ex.: \texttt{98ca9c2})
  * **3. Ramo (*Branch*):**
      * Representa linha independente de evolução do código.
      * Ponteiro móvel e leve para um commit (`main`, `feature`).
  * **4. Ponteiro `HEAD`:**
      * Indicador que aponta para o ramo e commit ativos no momento.

:::
::: {.column width="45%"}

\vspace{0.3em}

\begin{center}
\begin{tikzpicture}[
    commit/.style={circle, draw=uagreen!80!black, fill=uagreen!15, thick, font=\tiny\bfseries, inner sep=1pt, minimum size=5.5mm},
    branch/.style={rectangle, draw=blue!70!black, fill=blue!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    head/.style={rectangle, draw=red!70!black, fill=red!10, rounded corners=2pt, thick, font=\tiny\ttfamily\bfseries, inner sep=2pt},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=black!70},
    repo/.style={draw=black!30, dashed, rounded corners=4pt, fill=black!2}
]
% Enclosure
\draw[repo] (-0.5,-1.65) rectangle (4.6,1.4);
\node[anchor=north west, font=\tiny\bfseries, color=black!60] at (-0.45,1.35) {Repositório (.git/)};

% Commits with short SHA hashes
\node[commit] (C1) at (0.2,0) {C1};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (0.2,-0.32) {98ca9c2};

\node[commit] (C2) at (1.3,0) {C2};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (1.3,-0.32) {34ac2e1};

\node[commit] (C3) at (2.4,0.6) {C3};
\node[anchor=south, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,0.92) {f30ab12};

\node[commit] (C4) at (2.4,-0.6) {C4};
\node[anchor=north, font=\fontsize{4.5pt}{5.5pt}\ttfamily, color=black!60] at (2.4,-0.92) {7a12dc8};

% Commit arrows (chronological evolution of code)
\draw[arr] (C1) -- (C2);
\draw[arr] (C2) -- (C3);
\draw[arr] (C2) -- (C4);

% Branches
\node[branch] (main) at (3.7,0.6) {main};
\draw[arr, color=blue!70!black] (main) -- (C3);

\node[branch] (feat) at (3.7,-0.6) {feature};
\draw[arr, color=blue!70!black] (feat) -- (C4);

% HEAD pointing to active branch (feature)
\node[head] (head) at (3.7,-1.25) {HEAD};
\draw[arr, color=red!70!black] (head) -- (feat);
\end{tikzpicture}
\end{center}

:::
:::::

-----

## As Três Zonas Operacionais do Git

Localmente, os ficheiros de um repositório Git articulam-se através de três zonas distintas:

  * **1. Diretório de Trabalho (*Working Tree / Directory*):**
      * A pasta visível no disco onde o programador consulta, cria e edita ficheiros nos seus editores habituais.
      * Os ficheiros são extraídos da base de dados do Git para manipulação direta.
  * **2. Área de Preparação (*Staging Area / Index*):**
      * Camada intermédia de seleção (registada em `.git/index`).
      * Permite escolher cirurgicamente quais as modificações que irão entrar no próximo commit, sem obrigar a gravar tudo de uma vez.
  * **3. Repositório Local (*Local Repository / .git*):**
      * Base de dados onde o Git grava de forma permanente e comprimida todos os commits (*snapshots*) do projeto.

-----

## Fluxo Operacional e Estados dos Ficheiros

\vspace{0.4em}

\begin{center}
\begin{tikzpicture}[
    box/.style={draw=uagreen!80!black, fill=uagreen!10, rounded corners=3pt, thick, align=center, inner sep=6pt, font=\scriptsize, minimum width=2.6cm, minimum height=1.1cm},
    arr/.style={-{Latex[length=2.2mm]}, thick, color=black!75},
    arrback/.style={-{Latex[length=2.2mm]}, dashed, thick, color=red!70!black}
]
\node[box] (WT) {\textbf{Working Tree}\\\textit{Ficheiros Locais em Disco}};
\node[box, right=1.2cm of WT] (SA) {\textbf{Staging Area}\\\textit{Index / Preparação}};
\node[box, right=1.2cm of SA] (RP) {\textbf{Repositório (.git)}\\\textit{Snapshots Permanentes}};

\draw[arr] (WT.north east) -- node[above, font=\tiny\ttfamily] {git add} (SA.north west);
\draw[arr] (SA.north east) -- node[above, font=\tiny\ttfamily] {git commit} (RP.north west);

\draw[arrback] (SA.south west) -- node[below, font=\tiny\ttfamily] {git restore --staged} (WT.south east);
\draw[arrback] (RP.south) to[bend left=25] node[below, font=\tiny\ttfamily] {git checkout / switch} (WT.south);
\end{tikzpicture}
\end{center}

\vspace{0.3em}

Ao transitar entre estas zonas, cada ficheiro assume um de **quatro estados**:

  * **Untracked (Não Rastreado):** Ficheiro novo no *Working Tree* que o Git ainda não monitoriza.
  * **Modified (Modificado):** Ficheiro já rastreado cujo conteúdo em disco difere do último commit.
  * **Staged (Preparado):** Alteração indexada na *Staging Area* (`git add`), pronta para o próximo commit.
  * **Unmodified (Inalterado):** Ficheiro gravado no *Repositório* (`git commit`), sem edições locais pendentes.

-----

## Inicialização e Clonagem de Repositórios

Existem duas formas de estabelecer um repositório Git local:

  * **1. Inicializar um Repositório Novo (`git init`):**
      * Transforma uma pasta local existente num repositório Git:
        ```bash
        mkdir meu-projeto && cd meu-projeto
        git init
        # Inicializado repositório Git vazio em /caminho/meu-projeto/.git/
        ```
  * **2. Clonar um Repositório Existente (`git clone`):**
      * Transfere uma cópia integral de um repositório remoto (histórico, ramos e etiquetas):
        ```bash
        git clone https://github.com/utilizador/meu-projeto.git
        ```

\vspace{0.3em}

  * Em ambos os casos é criada a diretoria oculta **`.git/`**, que aloja toda a base de dados local.


-----

## Comandos do Ciclo Local: `status` e `add`

::::: columns
::: {.column width="45%"}

  * **Inspeção com `git status`:**
      * Revela o estado dos ficheiros nas zonas de trabalho locais.
      * **Vermelho:** Alterações não preparadas (*Untracked* / *Modified*).
      * **Verde:** Alterações prontas na *Staging Area* (*Staged*).
  * **Preparação com `git add`:**
      * Promove alterações para a *Staging Area*:
        ```bash
        git add main.c   # Ficheiro
        git add src/     # Pasta
        git add .        # Diretório atual
        git add -p       # Por blocos
        ```

:::
::: {.column width="55%"}

\vspace{0.4em}
\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_status_add_pt.png}
\end{center}

:::
:::::

-----

## Persistência de Alterações: `git commit`

O comando `git commit` consolida o conteúdo da *Staging Area* num novo snapshot imutável no repositório:

```bash
git commit -m "feat: implementa validação de credenciais de utilizador"
```

  * **Dinâmica Operacional:**
      * O Git empacota as alterações preparadas na *Staging Area*, calcula o seu **Hash SHA** e liga o novo commit ao commit anterior (*parent*).
      * O ramo ativo (ex.: `main`) e o ponteiro `HEAD` avançam automaticamente para este novo commit.
  * **Princípio da Atomicidade:**
      * Cada commit deve representar uma **única unidade lógica e coesa** de trabalho (evitar misturar refatorações estéticas com correções de bugs no mesmo commit).
      * Permite reverter ou auditar uma alteração específica sem efeitos colaterais no resto do projeto.

-----

## Boas Práticas em Mensagens de Commit

::::: columns
::: {.column width="50%"}

  * **Princípio Central:**
      * O código (`diff`) mostra **o que** mudou; a mensagem deve explicar **o porquê** da alteração.
  * **Convenção 50/72 da Indústria:**
      * **Modo Imperativo:** Escrever como instrução (ex.: `Adiciona`, `Corrige`, `Fix`, e não *Adicionado*).
      * **Assunto ($\le 50$ car.):** Conciso, inicial maiúscula e sem ponto final.
      * **Corpo ($\le 72$ car./linha):** Separado do assunto por uma **linha em branco**; detalha motivação e impacto.

:::
::: {.column width="50%"}

  * **Anti-Padrão (Informação Nula):**
    ```bash
    git commit -m "corrigir bugs e alterações"
    ```

  * **Modelo Recomendado (Regra 50/72):**
    ```text
    Fix: Corrige validação de sessão expirada

    A verificação anterior ignorava o TTL no
    Redis, permitindo reutilizar sessões.

    Adiciona validação estrita de expiração
    e devolve HTTP 401 Unauthorized.
    ```

:::
:::::

-----

## Padronização com Conventional Commits (I): Estrutura e Tipos

::::: columns
::: {.column width="48%"}

  * **Conceito & Anatomia:**
      * Convenção para mensagens de commit estruturadas, legíveis por humanos e ferramentas.
  * **Estrutura Canónica:**
    ```text
    <tipo>[âmbito opcional]: <descrição>

    [corpo opcional]

    [rodapé opcional]
    ```
  * **Exemplos Práticos:**
    ```bash
    git commit -m \
      "feat(auth): adiciona token JWT"

    git commit -m \
      "fix(api): corrige timeout de login"
    ```

:::
::: {.column width="52%"}

  * **Tipos Canónicos Principais:**
      * `feat:` Nova funcionalidade para o utilizador.
      * `fix:` Resolução de um bug ou defeito de código.
      * `docs:` Modificações exclusivamente na documentação.
      * `refactor:` Reorganização sem alterar comportamento.
      * `test:` Adição ou refatoração de testes.
      * `chore:` Tarefas de manutenção ou dependências.
      * `ci:` / `build:` Automação, CI/CD ou empacotamento.

:::
:::::

-----

## Padronização com Conventional Commits (II): Automação e Ciclo de Vida

::::: columns
::: {.column width="46%"}

  * **Porquê adotar na Engenharia?**
      * **Geração Automática de *Changelogs*:**
          * Ferramentas analisam o histórico e geram notas de lançamento categorizadas.
      * **Versionamento Semântico (SemVer):**
          * `fix:` $\rightarrow$ incrementa versão **PATCH** (`x.y.Z`)
          * `feat:` $\rightarrow$ incrementa versão **MINOR** (`x.Y.z`)
          * `BREAKING CHANGE:` $\rightarrow$ incrementa versão **MAJOR** (`X.y.z`)
      * **Rastreabilidade e Auditoria:**
          * Facilita *code review*, triagem e auditorias em equipa.

:::
::: {.column width="54%"}

\centering
\includegraphics[width=\linewidth,keepaspectratio]{figures/git_conventional_commits.png}

\vspace{0.4em}

\footnotesize
\textbf{Especificação Oficial:} \href{https://www.conventionalcommits.org/}{\texttt{conventionalcommits.org}}

:::
:::::

-----

## Inspeção do Histórico: `git log`

O utilitário `git log` permite explorar e filtrar a linha temporal do projeto:

```bash
# 1. Apresentação detalhada padrão
git log

# 2. Visão compacta de uma linha por commit (Hash curto + Assunto)
git log --oneline

# 3. Representação visual da topologia de branches e fusões em ASCII
git log --graph --oneline --all

# 4. Exibição das diferenças de código introduzidas nos últimos 2 commits
git log -p -2

# 5. Resumo estatístico de ficheiros alterados, inserções e deleções
git log --stat
```

-----

## Marcação de Versões: `git tag`

Uma **Tag** é um ponteiro fixo e imutável que referencia um commit específico na história do projeto:

::::: columns
::: {.column width="50%"}

  * **Conceito & Finalidade:**
      * Funciona como uma "etiqueta" ou marco permanente (uma versão de lançamento).
      * Ao contrário de um ramo (*branch*), **não se move** quando são criados novos commits.
  * **Versionamento Semântico ([SemVer](https://semver.org/)):**
      * Formato padronizado: `vMAJOR.MINOR.PATCH`
        * `v1.0.0` $\rightarrow$ Versão inicial estável
        * `v1.1.0` $\rightarrow$ Nova funcionalidade compatível
        * `v1.1.1` $\rightarrow$ Correção de bug (*patch*)
      * Especificação: \href{https://semver.org/}{\texttt{semver.org}}

:::
::: {.column width="50%"}

  * **Comandos Principais:**
    ```bash
    # 1. Cria uma tag no commit atual (HEAD)
    git tag v1.0.0

    # 2. Cria uma tag num commit anterior
    git tag v0.9.0 9f1a2b3

    # 3. Listar todas as tags existentes
    git tag

    # 4. Visualizar commits com tags
    git log --oneline --decorate
    ```
  * As tags facilitam a recuperação determinista de qualquer versão lançada.

:::
:::::

-----

## Ficheiros Não-Rastreados: O Papel do `.gitignore`

Nem todos os ficheiros gerados num projeto devem ser versionados no repositório:

  * **Ficheiros a Excluir Mandatoriamente:**
      * Binários compilados e bibliotecas (`*.o`, `*.class`, `*.exe`).
      * Dependências descarregadas (`node_modules/`, `.venv/`).
      * Segredos, credenciais e variáveis de ambiente locais (`.env`, `credentials.json`).
      * Metadados transitórios de editores e sistemas operativos (`.DS_Store`, `.vscode/`).
  * **Exemplo de `.gitignore` Estruturado:**
    ```gitignore
    # Binários e diretórios de compilação
    bin/
    build/
    *.o

    # Ambientes virtuais Python
    .venv/
    __pycache__/

    # Ficheiros sensíveis e de configuração local
    .env
    .DS_Store
    ```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Ramificação, Integração \& Resolução de Conflitos}}
\end{center}

-----

## O Paradigma de Ramificação (*Branching*) no Git

Em muitos sistemas tradicionais, criar um ramo implicava copiar diretórios inteiros de código-fonte:

  * **No Git, um *Branch* é Apenas um Ponteiro Móvel e Leve:**
      * Consiste num simples ficheiro de 41 bytes (40 caracteres do hash SHA-1 + `\n`) que aponta para um commit.
      * **Criar ou apagar** branches tem **custo computacional constante ($O(1)$)**; **comutar** de ramo atualiza apenas os ficheiros que divergem na *Working Tree*.
  * **O Ponteiro Especial `HEAD` (Referência Simbólica):**
      * Aponta para o **ramo ativo** no momento (ex.: `HEAD` $\rightarrow$ `main`).
      * Ao criar um novo commit, o ponteiro do ramo ativo avança automaticamente para o novo snapshot (e o `HEAD` acompanha-o por lhe apontar).
  * **Finalidade:** Isolar o desenvolvimento de novas funcionalidades, experiências ou correções de bugs sem desestabilizar a linha principal (`main`).

-----

## Comandos Essenciais de Gestão de Ramos

Comandos para criação, alternância e consulta de branches locais:

```bash
# 1. Criar um novo branch sem mudar para ele
git branch feature-login

# 2. Comutar para um branch existente (sintaxe moderna recomendada)
git switch feature-login

# 3. Criar e mudar para o branch num único passo
git switch -c feature-login        # Sintaxe moderna
git checkout -b feature-login      # Sintaxe clássica equivalente

# 4. Listar branches locais e remotos
git branch -a

# 5. Eliminar um branch local já integrado (merge efetuado)
git branch -d feature-login
```

-----

## Visualização Estrutural de Branches

\begin{center}
\includegraphics[width=0.85\linewidth,keepaspectratio]{figures/git_branch_00.png}
\end{center}

  * **Ramo Principal (`main`):** Linha cronológica de código estável e validado.
  * **Ramos de Funcionalidade (*Feature Branches*):** Bifurcações temporárias onde o código evolui de forma hermética.
  * A conclusão do trabalho culmina na integração (*merge*) de volta à linha principal.

-----

## Estratégias de Integração: `git merge`

\begin{center}
\includegraphics[width=\linewidth,height=0.36\textheight,keepaspectratio]{figures/git_merge_types_pt.png}
\end{center}

\vspace{-0.6em}

::::: columns
::: {.column width="45%"}

  * **Sequência de Comandos no Terminal:**
    ```bash
    # 1. Comutar para o ramo de destino
    git switch main

    # 2. Integrar o ramo de trabalho
    git merge feature-login
    ```

:::
::: {.column width="55%"}

  * **1. Fusão *Fast-Forward* (Linear):**
      * `main` avança diretamente ($O(1)$) até `feature` (**sem novos commits**).
  * **2. Fusão *3-Way Merge* (Divergente):**
      * Combina o ancestral comum e os dois topos num novo **Commit de Fusão**.

:::
:::::

-----

## O Desafio dos Merges Excessivos: Histórico Complexo

\begin{center}
\includegraphics[width=\linewidth,height=0.46\textheight,keepaspectratio]{figures/git_messy_history.png}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **O Problema ("Grafo *Spaghetti*"):**
      * Sincronizações repetidas com `git merge` criam dezenas de *merge commits* redundantes (*"Merge branch 'main' into..."*).
      * O histórico fica dominado por ruído administrativo em vez de código com valor funcional.

:::
::: {.column width="50%"}

  * **Impacto & Alternativa:**
      * **Trazabilidade Difícil:** Dificulta a leitura em `git log` e quebra a eficácia do `git bisect` na caça a bugs.
      * **Solução:** Como manter ramos atualizados com histórico linear e limpo? $\rightarrow$ `git rebase`!

:::
:::::

-----

## Linearização do Histórico com `git rebase`

::::: columns
::: {.column width="48%"}

  * **Conceito & Mecanismo:**
      * "Desprende" os commits de `feature` e reaplica-os um a um sobre o topo atualizado de `main`.
      * Cria novos commits (`E'`, `F'`, `G'`) com novos hashes SHA, mantendo o grafo perfeitamente retilíneo.

  * **Fluxo Recomendado de Trabalho:**
    ```bash
    # 1. Atualizar o main com o servidor
    git switch main
    git pull --rebase

    # 2. Reaplicar feature sobre o main
    git switch feature-login
    git rebase main
    ```

  * **A Regra de Ouro do Rebase:**
      * **NUNCA** executar rebase sobre ramos públicos partilhados. Reescrever histórico partilhado desestabiliza a sincronização da equipa.

:::
::: {.column width="52%"}

\centering
\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{figures/git_merge_vs_rebase_bytebytego.jpg}

:::
:::::

-----

## Análise Comparativa: `git merge` vs. `git rebase`

| Critério | `git merge` | `git rebase` |
| :--- | :--- | :--- |
| **Topologia do Histórico** | Não-linear (preserva ramificações e grafos) | **Estritamente linear (sequência única contínua)** |
| **Imutabilidade de Hashes** | **Preserva os hashes SHA originais** | Reescreve e recalcula todos os hashes |
| **Commit de Fusão** | Gera um commit específico (salvo *fast-forward*) | **Não gera merge commits adicionais** |
| **Fidelidade Cronológica** | Reflete com exatidão temporal a evolução | Reorganiza a história dos commits |
| **Segurança em Equipa** | **Totalmente seguro para branches partilhados** | **Perigoso se aplicado sobre ramos públicos** |
| **Caso de Uso Primário** | Incorporação definitiva de código em `main` | Limpeza local antes de submeter um Pull Request |

-----

## Deteção e Resolução de Conflitos de Merge

Um **conflito de fusão (*merge conflict*)** ocorre quando dois ramos alteram **as mesmas linhas no mesmo ficheiro** de forma contraditória:

  * O Git suspende a operação de merge e insere marcadores visuais no ficheiro afetado:
    ```text
    <<<<<<< HEAD (estado no ramo atual main)
    int timeout_ms = 5000;
    =======
    int timeout_ms = 10000;
    >>>>>>> feature-login (estado no ramo a integrar)
    ```
  * **Protocolo de Resolução:**
      1. Abrir o ficheiro em conflito e decidir a versão correta (ou combinada).
      2. Eliminar os marcadores textuais (`<<<<<<<`, `=======`, `>>>>>>>`).
      3. Adicionar o ficheiro corrigido à Staging Area: `git add ficheiro.c`.
      4. Concluir o merge commit executando `git commit`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Colaboração Distribuída \& Workflows em Equipa}}
\end{center}

-----

## Arquitetura Distribuída: Repositórios Remotos

Num DVCS, a partilha de trabalho realiza-se através de repositórios remotos (*remotes*):

  * **Conceito de Remote:**
      * Um identificador nomeado que aponta para um endereço de rede (URL SSH ou HTTPS) de outro clone do repositório.
  * **O Nome Convencional `origin`:**
      * Nome padrão atribuído automaticamente ao repositório central de onde o código foi clonado.
  * **Comandos de Gestão de Remotes:**
    ```bash
    # Listar remotos associados e respetivos URLs
    git remote -v

    # Associar um novo repositório remoto sob o nome 'origin'
    git remote add origin https://github.com/ua-deti/iei-repo.git

    # Renomear ou alterar o URL de um remoto existente
    git remote set-url origin git@github.com:ua-deti/iei-repo.git
    ```

-----

## Sincronização Remota: `fetch`, `pull` e `push`

A transferência bidirecional de dados entre repositórios locais e remotos envolve três operações fundamentais:

  * **1. `git fetch origin`:**
      * Descarrega os novos commits, branches e referências do servidor para o repositório local.
      * **Não toca nem altera os ficheiros do seu Working Tree**; apenas atualiza os ramos remotos (ex.: `origin/main`).
  * **2. `git pull origin main`:**
      * Executa de forma combinada um `git fetch` seguido imediatamente de um `git merge` no ramo ativo local.
  * **3. `git push origin feature-login`:**
      * Publica os commits efetuados localmente no repositório remoto, atualizando a referência no servidor.

-----

## Git vs. GitHub: Diferenciação Conceptual Rigorosa

É frequente a confusão entre a ferramenta de controlo de versões e a plataforma de alojamento na nuvem:

| Vetor de Comparação | Git | GitHub |
| :--- | :--- | :--- |
| **Natureza Primária** | **Ferramenta de software e protocolo CLI** | **Plataforma web de alojamento e colaboração** |
| **Instalação / Execução** | Localmente no sistema operativo do utilizador | Infraestrutura na nuvem (servidores Microsoft) |
| **Modelo de Licenciamento** | Software Livre de Código Aberto (GPLv2) | Serviço comercial proprietário (SaaS) |
| **Dependência de Rede** | **100% operacional sem ligação à Internet** | Requer conectividade com a Internet |
| **Funcionalidades Chave** | Commits, snapshots, branches, merge, rebase | Pull Requests, Code Review, Issues, CI/CD Actions |
| **Alternativas no Mercado** | Mercurial, SVN | GitLab, Bitbucket, Gitea, Sourcehut |

-----

## Modelos de Workflow Colaborativo: GitFlow

::::: columns
::: {.column width="56%"}

Modelo clássico ([Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/)) assente em múltiplos ramos de longa duração (`main`, `develop`, `feature/*`, `release/*`, `hotfix/*`):

  * **Vantagens:**
      * Desenvolvimento paralelo estruturado.
      * Lançamentos (*releases*) estáveis e controlados.
      * Suporta múltiplas versões em produção em simultâneo.
  * **Desvantagens:**
      * **Fluxo altamente complexo** e burocrático.
      * Ciclos de lançamento lentos (*slow releases*).
      * **Conflitos de *merge* frequentes** e difíceis de resolver entre ramos divergentes.

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[height=0.74\textheight,keepaspectratio]{figures/git_flow_nvie.png}
\end{center}

:::
:::::

-----

## Modelos de Workflow Colaborativo: Trunk-Based Development

No modelo [**Trunk-Based Development**](https://trunkbaseddevelopment.com/#one-line-summary) puro, toda a equipa integra código diretamente num único ramo partilhado (**`trunk` / `main`**) através de pequenos *commits* diários:

\begin{center}
\includegraphics[width=0.72\linewidth,keepaspectratio]{figures/trunk_based_pure.png}
\end{center}

::::: columns
::: {.column width="48%"}

  * **Vantagens:**
      * Redução drástica de conflitos de *merge*.
      * Complexidade e sobrecarga (*overhead*) mínimas.
      * Maior colaboração e integração contínua real.

:::
::: {.column width="52%"}

  * **Desvantagens:**
      * Exige uma **equipa altamente madura** e disciplinada.
      * Isolamento limitado de funcionalidades em curso.
      * **Risco elevado de quebrar a produção** (*main*).

:::
:::::

-----

## Modelo Proposto: Trunk-Based Escalado (Feature Branches)

A variação **Scaled Trunk-Based Development** preserva as vantagens do modelo *trunk-based*, oferecendo **maior controlo e segurança para equipas em crescimento**:

\begin{center}
\includegraphics[width=0.74\linewidth,keepaspectratio]{figures/trunk_based_scaled.png}
\end{center}

  * ***Short-Lived Feature Branches*:** Ramos criados a partir de `main` por **1 pessoa e com duração máxima de poucos dias** (evitando divergência prolongada).
  * **Controlo de Qualidade pré-integração:** O código passa obrigatoriamente por **Pull Request (*Code Review* + testes/build automáticos CI)** antes do *merge* em `main`.

-----

## O Coração da Engenharia Colaborativa: Pull Requests (PR)

No modelo *Trunk-Based com Feature Branches*, o **Pull Request (PR)** atua como o portão de qualidade antes de integrar alterações no ramo `main`:

  * **Um PR Não é um Comando Git:** É um mecanismo colaborativo das plataformas (GitHub / GitLab).
  * **Pilares de um Pull Request Profissional:**
      * **Revisão de Código por Pares (*Code Review*):** Inspeção linha a linha do *diff* por colegas de equipa para detetar *bugs*, falhas de segurança e melhorar a legibilidade.
      * **Automação de Build e Testes (CI/CD):** Compilação e execução automática de testes e *linters* — o *merge* só é permitido se a *build* passar.
      * **Discussão Técnica e Registo:** Histórico transparente das decisões antes da fusão no `main`.

-----

## Exemplo Prático: Workflow Trunk-Based com Feature Branches

```bash
# 1. Garantir que o ramo 'main' local está sincronizado e criar o feature branch de curta duração
git switch main && git pull --rebase
git switch -c feat/autenticacao-oauth

# 2. Desenvolver de forma iterativa com commits pequenos e atómicos (Conventional Commits)
git add src/auth.c
git commit -m "feat: adiciona validação de token OAuth2"

# 3. Antes de submeter, atualizar o 'main' e linearizar o feature branch (prevenir conflitos)
git switch main && git pull --rebase
git switch feat/autenticacao-oauth && git rebase main

# 4. Publicar o ramo no repositório remoto e abrir o Pull Request (Code Review + CI) no GitHub
git push -u origin feat/autenticacao-oauth

# 5. Após aprovação e merge do PR no GitHub, atualizar o 'main' local e remover o ramo temporário
git switch main && git pull --rebase
git branch -d feat/autenticacao-oauth
```

-----

## Publicação de Versões e GitHub Releases

A disponibilização pública de versões assenta no envio de tags e na criação de *Releases*:

::::: columns
::: {.column width="48%"}

  * **Publicação de Tags no Remoto:**
      * Por omissão, o `git push` não envia tags para o servidor remoto (`origin`).
      * Devem ser enviadas explicitamente:
        ```bash
        # Enviar uma tag específica
        git push origin v1.0.0

        # Enviar todas as tags locais
        git push origin --tags
        ```
  * Toda a equipa e sistemas de CI/CD passam a poder aceder ao marco exato da versão.

:::
::: {.column width="52%"}

  * **GitHub Releases:**
      * Funcionalidade da plataforma associada a uma tag do repositório.
      * **Vantagens na Distribuição:**
          * Associa notas de lançamento formatadas (*Release Notes / Changelogs*).
          * Permite descarregar binários pré-compilados (instaladores, pacotes `.deb`, ficheiros `.zip`).
          * Permite sinalizar versões preliminares (*pre-releases*).

:::
:::::

-----

## Síntese e Pontos-Chave da Sessão

  * **Resolução do Caos Manual:** O Git substitui cópias manuais e sincronizações inseguras por um registo histórico criptograficamente seguro e auditável.
  * **Arquitetura Distribuída:** Cada clone contém o histórico completo e autónomo, garantindo resiliência e operações locais instantâneas.
  * **Três Estados Locais:** A disciplina operacional assenta no domínio de **Working Tree**, **Staging Area** e **Repositório Local**.
  * **Branching Leve e Eficiente:** Ramificações instantâneas ($O(1)$) viabilizam fluxos de desenvolvimento paralelos sem sobreposição destrutiva.
  * **Git vs. GitHub:** Git é o motor de controlo de versões distribuído; GitHub é a infraestrutura social de colaboração, revisão por pares e automação.
  * **Colaboração Ágil e Segura:** O modelo *Trunk-Based Development* com *Feature Branches* de curta duração e *Pull Requests* garante integração rápida, revisão por pares e estabilidade contínua no ramo `main`.

-----

## Referências Técnicas Autorizadas

Documentação oficial, especificações e referências recomendadas para aprofundamento:

  * **Documentação Oficial do Git & Livro Pro Git:**
      * [Pro Git Book (Scott Chacon & Ben Straub)](https://git-scm.com/book/en/v2) — Leitura canónica e gratuita
      * [Manual de Referência Oficial do Git](https://git-scm.com/docs)
  * **Workflows Colaborativos & GitHub:**
      * [Trunk Based Development (Paul Hammant)](https://trunkbaseddevelopment.com/)
      * [Boas Práticas de Colaboração com Pull Requests](https://docs.github.com/en/pull-requests)
  * **Normas e Especificações da Indústria:**
      * [Especificação Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
      * [Especificação Semantic Versioning 2.0.0 (SemVer)](https://semver.org/)
  * **Tutoriais e Prática Interativa:**
      * [Learn Git Branching (Simulador Gráfico Interativo)](https://learngitbranching.js.org/)
      * [Atlassian Git Workflows & Tutorials](https://www.atlassian.com/git/tutorials)
