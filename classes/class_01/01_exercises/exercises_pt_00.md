---
title: Terminal Linux
subtitle: Introdução Engenharia Informática
#author: Mário Antunes
institute: Universidade de Aveiro
date: September 21, 2026
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
 - \AtBeginEnvironment{Shaded}{\normalsize}
 - \AtBeginEnvironment{verbatim}{\normalsize}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guião Prático de Laboratório

Este guião foi desenhado para uma sessão de **3 horas** e está dividido em duas partes:

* **Parte I — Competências Fundamentais (Exercícios 1 a 8):** O núcleo essencial da sessão. Todos os estudantes devem concluir estes exercícios durante o tempo de aula.
* **Parte II — Personalização, Scripting e Automação (Exercícios 9 a 12):** Exercícios de aprofundamento e desafios. Se não concluir durante a aula, deverá terminá-los em trabalho autónomo.

\vspace{1em}

> **Dicas de Sobrevivência no Terminal:**
>
> * **Autocompletar com `<Tab>`:** Escreva as primeiras letras de uma pasta, ficheiro ou comando e prima `<Tab>`. Se carregar duas vezes, o terminal lista todas as hipóteses possíveis.
> * **Histórico com as setas `↑` e `↓`:** Nunca reescreva um comando longo se apenas falhou uma letra; use a seta para cima para recuperá-lo e editá-lo.
> * **Cancelar com `Ctrl + C`:** Se um comando ficar bloqueado ou encravado, prima `Ctrl + C` para regressar à linha de comandos.

\newpage

# Parte I: Competências Fundamentais

## Exercício 1: A Orientar-se

Este exercício consolida os comandos de navegação e inspeção **`pwd`**, **`ls`**, **`cd`** e informações do utilizador.

1. Abra o seu terminal. Verifique a sua localização inicial (o seu diretório pessoal, ou *home directory*) imprimindo o diretório de trabalho atual:
   ```bash
   $ pwd
   ```
2. Liste o conteúdo do seu diretório pessoal. De seguida, liste-o novamente em formato de lista **longa** (`-l`) e mostrando **todos** os ficheiros (`-a`), incluindo os ocultos:
   ```bash
   $ ls
   $ ls -la
   ```
3. Navegue para o diretório de registos (*logs*) do sistema em `/var/log` e liste o seu conteúdo.
   *(Experimente escrever `cd /var/l` e carregar em `<Tab>` para autocompletar!)*
   ```bash
   $ cd /var/log
   $ ls
   ```
4. Obtenha informação básica sobre a sessão: o seu nome de utilizador e a data atual do sistema:
   ```bash
   $ whoami
   $ date
   ```
5. Regresse ao seu diretório pessoal utilizando o atalho mais rápido:
   ```bash
   $ cd ~
   ```
   *(Nota: executar simplesmente `cd` sem argumentos produz exatamente o mesmo resultado).*

-----

## Exercício 2: A Explorar Diretórios Chave do Sistema

Reforce o seu conhecimento da árvore do sistema de ficheiros explorando diretórios essenciais.

1. Navegue para o diretório `/etc`, onde residem as configurações de todo o sistema:
   ```bash
   $ cd /etc
   ```
2. Liste o seu conteúdo. Verá centenas de ficheiros e pastas de configuração:
   ```bash
   $ ls
   ```
3. Veja o conteúdo do ficheiro `os-release` para consultar detalhes sobre a distribuição Linux instalada:
   ```bash
   $ cat os-release
   ```
   *(O utilitário `cat` imprime o ficheiro completo no terminal. Se quiser ver apenas as primeiras 5 linhas, experimente: `head -n 5 os-release`).*
4. Navegue agora para o diretório `/bin` (onde se encontram os programas e comandos essenciais do sistema):
   ```bash
   $ cd /bin
   $ ls
   ```
   *(Verifique se reconhece alguns comandos que já utilizou, como `ls`, `date` ou `pwd`).*
5. Regresse à sua pasta pessoal:
   ```bash
   $ cd ~
   ```

-----

## Exercício 3: A Criar e Gerir Ficheiros

Neste exercício irá criar, copiar, mover, renomear e apagar ficheiros e pastas.

1. A partir do seu diretório pessoal, crie um novo diretório chamado `IEI`:
   ```bash
   $ cd ~
   $ mkdir IEI
   ```
2. Entre no novo diretório:
   ```bash
   $ cd IEI
   ```
3. Crie um ficheiro vazio chamado `notes.txt`:
   ```bash
   $ touch notes.txt
   ```
4. Escreva texto no ficheiro usando o operador de redirecionamento `>` e verifique o resultado com `cat`:
   ```bash
   $ echo "A minha primeira linha de texto na consola." > notes.txt
   $ cat notes.txt
   ```
5. Faça uma cópia do ficheiro com o nome `notes_backup.txt`:
   ```bash
   $ cp notes.txt notes_backup.txt
   $ ls -l
   ```
6. Renomeie o ficheiro original `notes.txt` para `important_notes.txt`:
   ```bash
   $ mv notes.txt important_notes.txt
   $ ls -l
   ```
7. Elimine o ficheiro de cópia de segurança:
   ```bash
   $ rm notes_backup.txt
   $ ls -l
   ```
   *(⚠️ Lembre-se: o terminal Linux não tem caixote do lixo. Ficheiros eliminados com `rm` não podem ser restaurados facilmente).*

-----

## Exercício 4: A Compreender Permissões de Acesso

Este exercício foca-se na interpretação e alteração de permissões com o comando **`chmod`**.

1. Dentro da sua pasta `~/IEI`, crie um novo ficheiro chamado `secret_data.txt`:
   ```bash
   $ touch secret_data.txt
   ```
2. Inspecione as permissões padrão atribuídas ao ficheiro:
   ```bash
   $ ls -l secret_data.txt
   ```
3. Remova todas as permissões para todas as classes (proprietário, grupo e outros) através da notação octal:
   ```bash
   $ chmod 000 secret_data.txt
   $ ls -l secret_data.txt
   ```
   *(Na notação numérica, $r=4$, $w=2$ e $x=1$. O valor $0$ significa que ninguém tem permissão para ler, escrever ou executar o ficheiro).*
4. Tente visualizar o conteúdo do ficheiro com `cat`:
   ```bash
   $ cat secret_data.txt
   ```
   *(Deverá receber a mensagem de erro **"Permission denied"**).*
5. Restaure a permissão de leitura (`r`) e escrita (`w`) exclusivamente para si próprio (proprietário/user):
   ```bash
   $ chmod u+rw secret_data.txt
   $ cat secret_data.txt
   ```
6. Crie um ficheiro de *script* vazio `my_script.sh` e conceda-lhe permissão de execução:
   ```bash
   $ touch my_script.sh
   $ chmod u+x my_script.sh
   $ ls -l my_script.sh
   ```
   *(Repare no `x` presente nas permissões do proprietário e, dependendo do terminal, na alteração da cor do nome do ficheiro).*

-----

## Exercício 5: A Encontrar Ficheiros e Conteúdo com `find` e `grep`

Aprenda a localizar ficheiros pelo nome e a pesquisar por padrões de texto no interior de ficheiros.

1. Dentro da pasta `~/IEI`, crie uma subpasta e um ficheiro com conteúdo confidencial:
   ```bash
   $ mkdir -p ~/IEI/reports
   $ echo "Este e um relatorio confidencial da UC de IEI." > ~/IEI/reports/report-2026.txt
   ```
2. Utilize o comando `find` para localizar qualquer ficheiro com terminação `.txt` dentro da árvore `~/IEI`:
   ```bash
   $ find ~/IEI -name "*.txt"
   ```
3. Utilize o comando `grep` para pesquisar a palavra "confidencial" no interior do relatório. A opção `-i` torna a pesquisa insensível a maiúsculas e minúsculas:
   ```bash
   $ grep -i "confidencial" ~/IEI/reports/report-2026.txt
   ```

-----

## Exercício 6: A Gerir Processos

Aprenda a lançar processos em segundo plano (*background*), identificar o seu PID e terminá-los a partir da consola.

1. Inicie um processo que ficará em espera durante 120 segundos. O operador `&` no final coloca o processo a correr em segundo plano, libertando a linha de comandos:
   ```bash
   $ sleep 120 &
   ```
   *(O terminal apresenta o número do job, ex: `[1]`, seguido do **PID** — Process ID atribuído).*
2. Confirme que o processo está em execução e obtenha o seu PID através do utilitário `pgrep`:
   ```bash
   $ pgrep sleep
   ```
3. Termine o processo utilizando o comando `kill` seguido do PID obtido no passo anterior (substitua `PID` pelo número real devolvido):
   ```bash
   $ kill PID
   ```
4. Verifique que o processo foi encerrado com sucesso:
   ```bash
   $ pgrep sleep
   ```
   *(O comando agora não deverá devolver qualquer linha, confirmando que o processo já não se encontra ativo).*

-----

## Exercício 7: A Gerir Software com o APT

Instale e remova ferramentas através do gestor de pacotes oficial do Ubuntu/Debian.

1. Sincronize a lista de pacotes local com os repositórios oficiais:
   ```bash
   $ sudo apt update
   ```
   *(Se for solicitada a palavra-passe do utilizador para autorização `sudo`, introduza-a; note que no terminal não aparecem caracteres ao digitar a password).*
2. Pesquise pelo visualizador de processos interativo `htop`:
   ```bash
   $ apt search htop
   ```
3. Instale o pacote `htop`:
   ```bash
   $ sudo apt install htop
   ```
4. Execute o programa recém-instalado para inspecionar os recursos da máquina:
   ```bash
   $ htop
   ```
   *(Prima a tecla `q` para sair e regressar ao terminal).*
5. Remova o pacote do sistema:
   ```bash
   $ sudo apt remove htop
   ```

-----

## Exercício 8: A Combinar Comandos com Pipes e Redirecionamento

Explore a ligação de fluxos com o **pipe (`|`)** e a gravação com o operador de acréscimo (**`>>`**).

1. O comando `ps aux` lista todos os processos em execução no computador. Utilize o *pipe* para enviar essa saída para o `grep`, filtrando apenas os processos relacionados com a *shell* "bash":
   ```bash
   $ ps aux | grep "bash"
   ```
2. Crie um ficheiro de registo de atividade `activity.log` com um primeiro carimbo de data e hora:
   ```bash
   $ echo "$(date): Inicio da sessao de trabalho." > ~/IEI/activity.log
   ```
3. Adicione uma segunda linha ao ficheiro sem sobrescrever o conteúdo anterior, utilizando o operador de anexação (`>>`):
   ```bash
   $ echo "$(date): Conclusao da Parte I do guiao." >> ~/IEI/activity.log
   ```
4. Verifique que o ficheiro de registo contém ambas as entradas:
   ```bash
   $ cat ~/IEI/activity.log
   ```

\newpage

# Parte II: Personalização, Scripting e Automação

## Exercício 9: A Personalizar o Seu Ambiente com `.bashrc`

Crie atalhos personalizados (*aliases*) permanentes para a sua *shell* Bash.

1. Abra o ficheiro de configuração `~/.bashrc` com o editor de texto `nano`:
   ```bash
   $ nano ~/.bashrc
   ```
2. Desloque o cursor até ao final do ficheiro (use as setas do teclado ou `Alt + /` / `Page Down`) e adicione a seguinte linha:
   ```bash
   alias ll='ls -alF'
   ```
3. Guarde as alterações com `Ctrl + O`, confirme com a tecla `Enter`, e saia do editor com `Ctrl + X`.
4. Carregue as novas definições na sessão atual do terminal:
   ```bash
   $ source ~/.bashrc
   ```
5. Teste o novo atalho criado:
   ```bash
   $ ll
   ```

-----

## Exercício 10: A Compreender a Variável `$PATH`

Descubra como o sistema operativo localiza os executáveis que invoca pelo nome.

1. Inspecione o valor atual da variável de ambiente `$PATH`:
   ```bash
   $ echo $PATH
   ```
   *(Note que é uma sequência de pastas separadas pelo carácter `:`).*
2. Crie um pequeno *script* executável chamado `hello` (sem extensão) dentro da pasta `~/IEI`:
   ```bash
   $ echo '#!/bin/bash' > ~/IEI/hello
   $ echo 'echo "Ola! Este comando customizado esta a correr com sucesso!"' >> ~/IEI/hello
   $ chmod +x ~/IEI/hello
   ```
   *(Em Linux, os ficheiros não necessitam obrigatoriamente da extensão `.sh` para serem executados; o sistema identifica o executável pelo shebang `#!/bin/bash` e pela permissão `+x`).*
3. Tente executar o comando apenas escrevendo o seu nome:
   ```bash
   $ hello
   ```
   *(O comando falhará com "command not found", uma vez que a pasta `~/IEI` não se encontra na lista de diretórios do `$PATH`).*
4. Execute o ficheiro indicando o seu caminho relativo:
   ```bash
   $ cd ~/IEI
   $ ./hello
   ```
5. Adicione temporariamente a pasta `~/IEI` ao seu `$PATH` e volte a invocar o comando pelo nome a partir de qualquer diretório:
   ```bash
   $ export PATH="$HOME/IEI:$PATH"
   $ cd ~
   $ hello
   ```
   *(Esta alteração à variável `$PATH` é válida apenas durante a sessão atual do terminal. O estudo aprofundado de variáveis de ambiente, exportação e persistência será realizado na próxima aula).*

-----

## Exercício 11: Desafio de Scripting em Bash

Automatize a criação de uma estrutura padronizada de projeto com validações em *shell script*.

1. Abra um novo ficheiro de *script* com o `nano`:
   ```bash
   $ nano ~/IEI/setup_project.sh
   ```
2. Insira o seguinte código Bash no ficheiro:
   ```bash
   #!/bin/bash
   PROJECT_DIR="$HOME/IEI/my_project"

   # Validação: interrompe caso o diretório já exista
   if [ -d "$PROJECT_DIR" ]; then
     echo "Erro: O diretorio '$PROJECT_DIR' ja existe."
     exit 1
   fi

   mkdir -p "$PROJECT_DIR"
   echo "Diretorio principal criado em: $PROJECT_DIR"

   # Criação modular com ciclo for
   for folder in assets source docs tests
   do
     mkdir "$PROJECT_DIR/$folder"
     echo "-> Subpasta criada: $folder"
   done

   echo "Estrutura do projeto inicializada com sucesso!"
   ```
3. Guarde o ficheiro (`Ctrl + O`, depois `Enter`) e saia do editor (`Ctrl + X`).
4. Conceda permissão de execução e corra o *script*:
   ```bash
   $ chmod +x ~/IEI/setup_project.sh
   $ ~/IEI/setup_project.sh
   ```
5. Inspecione a árvore de pastas criada:
   ```bash
   $ ls -R ~/IEI/my_project
   ```
6. Tente executar o script uma segunda vez para comprovar que a validação de existência com `if` funciona:
   ```bash
   $ ~/IEI/setup_project.sh
   ```

-----

## Exercício 12: A Agendar Tarefas com o `cron`

Crie uma rotina automática agendada para correr periodicamente a cada minuto.

1. **Criar o Script de Registo:** Na pasta `~/IEI`, crie o ficheiro `log_time.sh`:
   ```bash
   $ echo '#!/bin/bash' > ~/IEI/log_time.sh
   $ echo 'date >> $HOME/IEI/cron_log.txt' >> ~/IEI/log_time.sh
   $ chmod +x ~/IEI/log_time.sh
   ```
2. **Identificar o Caminho Absoluto:**
   O serviço `cron` requer caminhos absolutos e não possui o ambiente interativo da sua consola. Obtenha o caminho completo para o script:
   ```bash
   $ echo "$HOME/IEI/log_time.sh"
   ```
   *(Exemplo de saída: `/home/student/IEI/log_time.sh` ou `/home/aluno/IEI/log_time.sh`).*
3. **Configurar o Crontab:**
   Abra o gestor de agendamentos:
   ```bash
   $ crontab -e
   ```
   *(Se for a primeira vez, selecione o editor `nano` — habitualmente opção 1).*
4. **Adicionar a Tarefa:**
   Desloque o cursor para o fim do ficheiro e insira a linha seguinte (substituindo `/caminho/absoluto/completo` pelo resultado obtido no passo 2):
   ```cron
   * * * * * /caminho/absoluto/completo/IEI/log_time.sh
   ```
   Guarde e feche o editor (`Ctrl + O`, `Enter`, `Ctrl + X`).
5. **Verificar a Execução:**
   > **Nota para utilizadores de WSL (Windows Subsystem for Linux):** No WSL o serviço do cron pode não arrancar automaticamente. Se estiver no WSL, execute antes: `sudo service cron start`.

   Aguarde cerca de 2 minutos enquanto a tarefa corre em segundo plano. Verifique depois se o ficheiro foi criado e preenchido com as datas:
   ```bash
   $ cat ~/IEI/cron_log.txt
   ```
6. **Limpeza:**
   Para evitar que o script continue a correr indefinidamente a cada minuto na sua máquina, remova as tarefas do crontab:
   ```bash
   $ crontab -r
   ```
   *(⚠️ Atenção: `crontab -r` elimina todas as tarefas agendadas do seu utilizador sem pedir confirmação).*
