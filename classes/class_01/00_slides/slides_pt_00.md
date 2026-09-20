---
title: 47138 - Introdução à Engenharia Informática
subtitle: Terminal Linux
institute: Universidade de Aveiro
date: September 21, 2026
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
 - \usepackage{longtable,booktabs}
 - \usepackage{etoolbox}
 - \AtBeginEnvironment{longtable}{\tiny}
 - \usepackage{caption}
 - \captionsetup[longtable]{labelformat=empty,skip=0pt}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\tiny}
 - \AtBeginEnvironment{verbatim}{\tiny}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

## Bem-vindo à Linha de Comandos\! 🐧

### Mais do que uma Caixa Preta

O **Terminal** é a sua ligação direta, baseada em texto, ao sistema operativo.

  * **Porquê usá-lo?**
      * **Poder e Velocidade:** Execute tarefas complexas instantaneamente.
      * **Automação:** Crie *scripts* para tarefas repetitivas.
      * **Eficiência:** Utiliza o mínimo de recursos do sistema.
      * **Padrão da Indústria:** Essencial para programadores e administradores de sistemas.

**Analogia:** A GUI é o menu do restaurante: só pode escolher o que já está previsto. A CLI é entrar na cozinha e criar a receita à sua medida.

-----

## A Shell & o Bash

A ***shell*** é o programa que interpreta os seus comandos. O terminal é a janela; a *shell* é o cérebro lá dentro.

  * Existem várias *shells* no mundo Unix/Linux:
      * `sh` (Bourne Shell): A *shell* histórica clássica.
      * `zsh` (Z Shell): Padrão moderno no macOS, altamente personalizável.
      * `fish`: Focada na experiência interactiva pronta a usar.
      * **`bash` (Bourne Again SHell):** O padrão *de facto* na maioria das distribuições Linux e o foco da nossa aula.

-----

## Sobrevivência & Produtividade na Shell ⚡

Quatro atalhos essenciais que poupam tempo e evitam frustrações:

  * **Tecla `<Tab>` (Autocompletar):**
      * Comece a escrever e prima `<Tab>`: completa nomes de comandos ou caminhos.
      * Duplo `<Tab>`: lista todas as opções que correspondem ao que escreveu.
  * **Setas `↑` e `↓` (Histórico):**
      * Permite recuperar e editar comandos anteriores sem os reescrever.
      * O comando `history` lista os comandos executados recentemente.
  * **`Ctrl + C` (Cancelar / Interromper):**
      * Interrompe imediatamente um comando encravado ou ciclo infinito.
  * **`clear` ou `Ctrl + L`:**
      * Limpa o ecrã do terminal sem fechar a sessão.

-----

## Como Pedir Ajuda no Terminal 💡

Nunca tente decorar todos os comandos e argumentos — aprenda a consultar a ajuda:

  * **Opção `--help`:**
      * Ajuda rápida integrada com resumo de sintaxe e *flags*.
      ```bash
      $ ls --help
      $ grep --help
      ```
  * **Manual do Sistema (`man`):**
      * Documentação oficial detalhada de comandos e programas.
      ```bash
      $ man ls
      ```
      * Use as setas `↑` e `↓` para rolar; prima `/` para pesquisar texto; prima `q` para sair.

-----

## O Sistema de Ficheiros do Linux (Parte 1)

O sistema de ficheiros é uma árvore hierárquica unificada com raiz em **`/`**.

  * `/`: O **diretório raiz**. O ponto de partida de tudo.
  * `/home`: Pastas pessoais dos utilizadores (ex: `/home/student` ou `/home/aluno`).
  * `/bin`: **Binários** essenciais do sistema (programas como `ls`, `cp`, `bash`).
  * `/etc`: Ficheiros de **configuração** de todo o sistema.
  * `/var`: Ficheiros com dados **variáveis**, como *logs* (`/var/log`).
  * `/tmp`: Diretório para ficheiros **temporários** (limpos ao reiniciar).

-----

## O Sistema de Ficheiros do Linux (Parte 2)

Outros diretórios importantes no dia a dia:

  * `/opt`: *Software* opcional de terceiros instalado de forma autónoma.
  * `/usr`: Utilitários e aplicações dos utilizadores (`/usr/bin`, `/usr/lib`).
  * `/usr/local`: Programas e bibliotecas instalados localmente pelo administrador.
  * `/root`: O diretório pessoal do **superutilizador** (*root*). Não confundir com `/`!

-----

## Caminhos: Absolutos vs. Relativos 🧭

Saber onde estamos e como referenciar ficheiros é indispensável:

  * **Caminho Absoluto:**
      * Começa sempre a partir da raiz `/`. É inequívoco, independentemente de onde estamos.
      ```bash
      $ cd /var/log
      $ ls /etc/os-release
      ```
  * **Caminho Relativo:**
      * Começa a partir do diretório atual onde nos encontramos (*working directory*).
      ```bash
      $ cd Documentos/Trabalho
      $ ls ./relatorio.txt
      ```
  * **Atalho `~` (Home):**
      * Representa o diretório pessoal do utilizador atual (ex: `~/IEI` equivale a `/home/aluno/IEI`).

-----

## Ficheiros & Diretórios Ocultos

Ficheiros cujo nome começa por um ponto (`.`) são tratados como ocultos.

  * Utilizados habitualmente para guardar configurações e histórico:
      * `~/.bashrc`: Ficheiro de arranque e personalização da *shell* Bash.
      * `~/.bash_history`: Histórico dos comandos executados.
      * `~/.gitconfig`: Configuração global da ferramenta Git.
      * `~/.config`: Diretório padrão de definições de aplicações.
  * Por omissão, o comando para listar conteúdos, `ls`, não mostra ficheiros ocultos.

-----

## Navegação Básica: `pwd` e `cd`

Comandos fundamentais para navegação na árvore de diretórios:

  * `pwd`: **P**rint **W**orking **D**irectory. Devolve o caminho absoluto da localização atual.
    ```bash
    $ pwd
    /home/student
    ```
  * `cd`: **C**hange **D**irectory. Muda o diretório atual de trabalho.
    ```bash
    $ cd /var/log          # Caminho absoluto
    $ cd Documents         # Caminho relativo para subdiretório
    ```

-----

## Atalhos de Navegação com `cd`

Atalhos indispensáveis para navegação rápida:

  * **Subir um nível na árvore (`..`):**
    ```bash
    $ cd ..
    ```
  * **O diretório atual (`.`):**
    ```bash
    $ cd .
    ```
  * **Ir diretamente para a sua pasta pessoal (`~`):**
    ```bash
    $ cd ~                 # ou apenas: cd
    ```
  * **Voltar ao diretório anterior (último onde esteve):**
    ```bash
    $ cd -
    ```

-----

## Listar Conteúdo: `ls`

O comando `ls` lista ficheiros e subdiretórios:

  * **Listagem simples:**
    ```bash
    $ ls
    Documentos  Downloads  Musica  Scripts
    ```
  * **Listagem longa (`-l`):** Mostra permissões, proprietário, tamanho e data.
    ```bash
    $ ls -l
    -rw-r--r-- 1 student student 4096 Sep 21 09:30 doc.txt
    drwxr-xr-x 2 student student 4096 Sep 21 09:30 Scripts
    ```
  * **Mostrar ficheiros ocultos (`-a`):**
    ```bash
    $ ls -a
    .  ..  .bashrc  .profile  Documentos
    ```
  * **Combinar opções (`-la` ou `-lah`):**
    `-h` apresenta os tamanhos em formato legível (*human-readable*: K, M, G).

-----

## Criar Diretórios: `mkdir`

Utilize `mkdir` (**m**a**k**e a **dir**ectory) para criar pastas:

  * **Criar um único diretório:**
    ```bash
    $ mkdir o_meu_projeto
    ```
  * **Criar uma árvore aninhada (`-p` / parents):**
    Cria todos os diretórios pais necessários no caminho que ainda não existam.
    ```bash
    $ mkdir -p Documentos/Trabalho/2026/Relatorios
    ```

-----

## Criar & Editar Ficheiros: `touch` & `nano`

  * **`touch`:** Cria um ficheiro novo vazio ou atualiza a data de modificação:
    ```bash
    $ touch notas.txt
    ```
  * **`nano`:** Editor de texto simples para consola:
    ```bash
    $ nano notas.txt
    ```
      * Escreva e edite o texto diretamente no ecrã.
      * `Ctrl + O` e prima `Enter`: Guardar alterações.
      * `Ctrl + X`: Sair do editor (pergunta se quer guardar caso existam alterações).

-----

## Copiar & Mover: `cp` e `mv` 📂

  * **`cp` (Copy):** Copia ficheiros ou diretórios para um novo destino.
    ```bash
    $ cp notas.txt notas_backup.txt       # Copiar ficheiro
    $ cp notas.txt ~/Documentos/           # Copiar para diretório
    $ cp -r pasta/ pasta_copia/            # Copiar diretório recursivamente (-r)
    ```
  * **`mv` (Move):** Move ou renomeia ficheiros e diretórios.
    ```bash
    $ mv notas.txt notas_importantes.txt   # Renomear ficheiro
    $ mv notas_importantes.txt ~/IEI/      # Mover para outro diretório
    ```

-----

## Apagar & Visualizar: `rm` e `cat` 🗑️

  * **`rm` (Remove):** Apaga ficheiros ou pastas.
    ```bash
    $ rm notas_backup.txt                  # Apagar ficheiro
    $ rm -r pasta_antiga/                  # Apagar diretório recursivamente (-r)
    ```
    ⚠️ **Atenção:** No terminal **não há caixote do lixo**. Ficheiros apagados com `rm` são eliminados em definitivo!
  * **`cat` (Concatenate):** Imprime todo o conteúdo de um ficheiro no terminal:
    ```bash
    $ cat /etc/os-release
    ```

-----

## Ver Ficheiros Grandes: `head`, `tail` e `less` 📄

Se o ficheiro for muito longo, o `cat` inunda o ecrã. Use utilitários dedicados:

  * **`head` e `tail`:** Visualizam o início ou o fim de um ficheiro.
    ```bash
    $ head -n 5 /var/log/syslog           # Primeiras 5 linhas
    $ tail -n 5 /var/log/syslog           # Últimas 5 linhas
    ```
  * **`less` (Paginação interactiva):**
    ```bash
    $ less /var/log/syslog
    ```
      * `↑` / `↓` ou `Espaço`: Rolar o texto.
      * `/termo`: Pesquisar por uma palavra.
      * `q`: Sair do visualizador.

-----

## Redirecionamento de Saída: `>` e `>>`

Em Linux, pode redirecionar a saída de texto de um comando para um ficheiro:

  * **Operador `>` (Sobrescrever):**
    Guarda o *output* num ficheiro, **substituindo** o conteúdo anterior:
    ```bash
    $ echo "Primeira linha" > notas.txt
    $ ls -l /var/log > lista_logs.txt
    ```
  * **Operador `>>` (Anexar / Append):**
    Adiciona o novo *output* ao **final** do ficheiro, preservando o existente:
    ```bash
    $ echo "Segunda linha" >> notas.txt
    $ echo "Registo em $(date)" >> atividade.log
    ```

-----

## Pesquisa de Conteúdo & Ficheiros: `grep` e `find` 🔎

  * **`grep` (Pesquisa de Texto):** Procura palavras ou padrões dentro de ficheiros.
    ```bash
    $ grep "root" /etc/passwd              # Linhas que contêm 'root'
    $ grep -i "confidencial" relatorio.txt # Pesquisa insensível a maiúsculas (-i)
    $ grep -rn "TODO" ~/IEI/               # Recursivo (-r) com linha (-n)
    ```
  * **`find` (Pesquisa de Ficheiros):** Localiza ficheiros na árvore de diretórios.
    ```bash
    $ find ~/IEI -name "*.txt"             # Ficheiros com extensão .txt
    $ find /var/log -type f -name "*.log"  # Apenas ficheiros normais (-type f)
    ```

-----

## O Poder do Pipe `|`

O **Pipe (`|`)** é o coração da filosofia Unix: *conectar a saída de um programa à entrada do seguinte*.

$$\text{Comando A} \xrightarrow{\quad\text{output}\quad} \mathbf{\huge\mid} \xrightarrow{\quad\text{input}\quad} \text{Comando B}$$

  * **Exemplo 1: Filtrar uma listagem:**
    ```bash
    $ ls /var/log | grep ".log"
    ```
  * **Exemplo 2: Procurar um processo em execução:**
    ```bash
    $ ps aux | grep "bash"
    ```
  * **Exemplo 3: Contar linhas de saída:**
    ```bash
    $ ls -l /etc | wc -l
    ```

-----

## Utilizadores: Padrão vs. Superutilizador

O Linux é um sistema multiutilizador com isolamento de segurança:

  * **Utilizador Padrão** (ex: `student` ou o seu nome):
      * Utilização regular com permissões limitadas aos seus ficheiros pessoais.
  * **Superutilizador (`root`):**
      * Administrador supremo com controlo total sobre o sistema operativo e hardware.
  * **O Comando `sudo` (SuperUser DO):**
      * Permite a um utilizador autorizado executar comandos administrativos pontuais com privilégios de *root*:
      ```bash
      $ sudo apt update
      ```

-----

## Compreender Permissões de Ficheiros 🔐

O comando `ls -l` exibe permissões em 10 caracteres (ex: `-rwxr-xr--`):

  * **1.º Carácter:** Tipo (`-` ficheiro normal, `d` diretório, `l` link).
  * **9 Caracteres seguintes:** 3 grupos de 3 permissões:
    * **Proprietário (*User* - u)**: `rwx`
    * **Grupo (*Group* - g)**: `r-x`
    * **Outros (*Others* - o)**: `r--`
  * **Significado:**
    * `r` (*read*): Ler conteúdo (ficheiro) ou listar ficheiros (diretório).
    * `w` (*write*): Modificar/apagar ficheiro ou criar/remover itens (diretório).
    * `x` (*execute*): Executar ficheiro como programa ou aceder/entrar na pasta.

-----

## Gerir Permissões com `chmod`

O comando `chmod` (**ch**ange **mod**e) altera as permissões de acesso:

  * **Método 1: Notação Simbólica (`u`, `g`, `o`, `a` com `+` e `-`):**
    ```bash
    $ chmod u+x script.sh          # Adicionar permissão de execução ao dono
    $ chmod go-w secret.txt        # Retirar permissão de escrita a grupo e outros
    $ chmod a+r documento.txt      # Dar leitura a todos (all)
    ```
  * **Método 2: Notação Octal / Numérica ($r=4, w=2, x=1$):**
    * Cada classe soma os valores: $4 (\text{leitura}) + 2 (\text{escrita}) + 1 (\text{execução}) = 7$.
    ```bash
    $ chmod 755 script.sh          # u=rwx (7), g=rx (5), o=rx (5)
    $ chmod 644 texto.txt          # u=rw (6), g=r (4), o=r (4)
    $ chmod 000 secret.txt         # Nenhuma permissão para ninguém (0, 0, 0)
    ```

-----

## Informação do Sistema & Processos ⚙️

Comandos rápidos para inspeção do estado da máquina:

  * `whoami`: Nome do utilizador ativo na sessão.
  * `date`: Data e hora atuais do sistema.
  * `uname -a`: Detalhes sobre o *kernel* Linux e arquitetura do processador.
  * **O que é um Processo?**
      * É um programa em execução. Cada processo tem um número único de identificação: o **PID** (*Process ID*).
  * `ps aux`: Lista detalhada de todos os processos ativos na máquina.

-----

## Controlar Processos: Segundo Plano e `kill`

  * **Processos em Segundo Plano (*Background*):**
      * Adicionar `&` no fim do comando liberta a consola imediatamente:
      ```bash
      $ sleep 120 &
      [1] 4521                       # [Job] e PID atribuído
      ```
  * **Procurar o PID de um processo:**
      * Utilize `pgrep`:
      ```bash
      $ pgrep sleep
      4521
      ```
  * **Terminar um Processo (`kill`):**
      * Envia um sinal para terminar o processo com o PID indicado:
      ```bash
      $ kill 4521                    # Terminação limpa (SIGTERM)
      $ kill -9 4521                 # Terminação forçada imediata (SIGKILL)
      ```

-----

## Gestão de Pacotes com o APT 📦

O **APT** (*Advanced Package Tool*) gere a instalação e atualização de software em distribuições Debian/Ubuntu (equivalente à *App Store* da consola):

  1. **Atualizar índice de pacotes disponíveis (`update`):**
     ```bash
     $ sudo apt update
     ```
  2. **Procurar uma ferramenta (`search`):**
     ```bash
     $ apt search htop
     ```
  3. **Instalar uma ferramenta (`install`):**
     ```bash
     $ sudo apt install htop
     ```
  4. **Remover a ferramenta (`remove` / `purge`):**
     ```bash
     $ sudo apt remove htop         # Remove o programa
     $ sudo apt purge htop          # Remove o programa e configurações
     ```

-----

## Variáveis Essenciais da Sessão: `$USER`, `$HOME` e `$PATH`

A *shell* disponibiliza variáveis com informação de contexto da sessão (em MAIÚSCULAS):

  * **`$USER`:** O nome do utilizador autenticado na sessão (`echo $USER`).
  * **`$HOME`:** O caminho absoluto para a sua pasta pessoal (fundamental em *scripts* e no *cron*):
    ```bash
    $ echo $HOME
    /home/student
    ```
  * **`$PATH`:** Lista de pastas (separadas por `:`) onde a *shell* procura programas executáveis:
    ```bash
    $ echo $PATH
    /usr/local/bin:/usr/bin:/bin
    ```
  * **Porque precisamos de `./` para correr scripts?**
    * A pasta atual (`.`) **não** está no `$PATH` por segurança. Por isso, indicamos o caminho relativo: `./meu_script.sh`.

-----

## Personalizar a Shell: `.bashrc` & Aliases

O ficheiro `~/.bashrc` é executado automaticamente sempre que abre um novo terminal.

  * **Criar Atalhos (*Aliases*):**
    Abra `~/.bashrc` com o `nano` e adicione no final:
    ```bash
    alias ll='ls -al'
    alias c='clear'
    ```
  * **Recarregar as alterações:**
    As novas definições entram em vigor num novo terminal ou correndo:
    ```bash
    $ source ~/.bashrc
    ```
  * Teste executando o novo atalho: `ll`.

-----

## Introdução ao Bash Scripting

Um *script* Bash é um ficheiro de texto executável com uma sequência de comandos:

  1. **Shebang (1.ª linha obrigatória):** Indica qual o interpretador a usar:
     ```bash
     #!/bin/bash
     ```
  2. **Comentários:** Linhas iniciadas por `#` explicam o código.
  3. **Permissões de Execução:** É necessário conceder permissão `+x`:
     ```bash
     $ chmod +x meu_script.sh
     ```
  4. **Execução:**
     ```bash
     $ ./meu_script.sh
     ```
     *(O `./` indica explicitamente que o executável está na pasta atual).*

-----

## Exemplo de Script 1: Olá Mundo

Utilização de variáveis e do comando `echo`:

**Ficheiro: `ola.sh`**
```bash
#!/bin/bash
# Script simples de boas-vindas

NOME="Estudante"
echo "Olá, $NOME!"
echo "A tua pasta pessoal é: $HOME"
```

**Para executar:**
```bash
$ chmod +x ola.sh
$ ./ola.sh
```

-----

## Exemplo de Script 2: Condições com `if`

Testar se um ficheiro ou pasta existe antes de executar ações:

**Ficheiro: `verifica.sh`**
```bash
#!/bin/bash
DIRETORIO="$HOME/IEI"

# -d testa se o diretório existe (-f testa se é ficheiro normal)
if [ -d "$DIRETORIO" ]; then
  echo "O diretório $DIRETORIO já existe."
else
  echo "O diretório não existe. A criar..."
  mkdir -p "$DIRETORIO"
fi
```

-----

## Exemplo de Script 3: Ciclos com `for`

Repetir tarefas sobre listas de ficheiros ou valores:

**Ficheiro: `criar_pastas.sh`**
```bash
#!/bin/bash
# Cria uma estrutura modular de pastas de projeto

PROJETO="$HOME/IEI/projeto"

for modulo in dados codigo relatorios docs
do
  mkdir -p "$PROJETO/$modulo"
  echo "-> Subpasta criada: $modulo"
done

echo "Estrutura criada com sucesso em $PROJETO!"
```

-----

## Agendamento de Tarefas com o `cron` 🕒

O ***cron*** é o serviço do sistema que executa tarefas agendadas em segundo plano (*cron jobs*):

  * **Comandos principais do `crontab`:**
      * `crontab -e`: **Editar** as suas tarefas agendadas (abre o editor).
      * `crontab -l`: **Listar** as suas tarefas ativas.
      * `crontab -r`: **Remover** todas as suas tarefas (*use com muito cuidado!*).

### Sintaxe dos 5 Campos Temporais:
```
┌───────────── minuto (0 - 59)
│ ┌───────────── hora (0 - 23)
│ │ ┌───────────── dia do mês (1 - 31)
│ │ │ ┌───────────── mês (1 - 12)
│ │ │ │ ┌───────────── dia da semana (0 - 6, onde 0 = Domingo)
│ │ │ │ │
* * * * * /caminho/absoluto/para/o/comando
```

-----

## Exemplos de `crontab`

Dicas essenciais para agendamento no `crontab`:

  * Use sempre **caminhos absolutos** para scripts e utilitários.
  * O asterisco `*` significa "a cada" unidade de tempo.

**Exemplo 1: Executar um script todos os dias às 03:30 da madrugada:**
```cron
30 3 * * * /home/aluno/scripts/backup.sh
```

**Exemplo 2: Executar a cada minuto e registar a saída num ficheiro de log:**
```cron
* * * * * /home/aluno/IEI/log_time.sh >> /home/aluno/IEI/cron_log.txt 2>&1
```

*(O `2>&1` redireciona também eventuais mensagens de erro para o log).*

-----

## Da Teoria à Prática

Resumo do que abordámos e que vamos agora praticar:

  * **Navegação & Gestão:** `pwd`, `cd`, `ls`, `mkdir`, `touch`, `cp`, `mv`, `rm`, `cat`.
  * **Pesquisa & Fluxos:** `grep`, `find`, redirecionamentos (`>`, `>>`) e *pipes* (`|`).
  * **Segurança & Processos:** Permissões (`chmod` simbólico/octal), `sudo`, `ps`, `kill`.
  * **Ambiente & Automação:** `$PATH`, `.bashrc`, scripts Bash e `cron`.

**Agora é a vossa vez:** mãos no terminal e bom trabalho no guião prático! 🚀

-----

## Apoio & Mais Recursos 📚

Consulte estas referências para aprofundar e esclarecer dúvidas:

  * **Linux Command Line Cheat Sheet:**
      * [https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/](https://www.geeksforgeeks.org/linux-unix/linux-commands-cheat-sheet/)
  * **Gerador Visual de Expressões Cron:**
      * [https://crontab.guru/](https://crontab.guru/)
  * **Guia Bash Scripting:**
      * [https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet](https://developers.redhat.com/cheat-sheets/bash-shell-cheat-sheet)
