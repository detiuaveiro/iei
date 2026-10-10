---
title: "Exercícios de Consolidação Vevox"
subtitle: "Introdução à Engenharia Informática — Sessões 00, 01 e 02"
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
 - \AtBeginEnvironment{longtable}{\small}
 - \AtBeginEnvironment{cslreferences}{\small}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Banco de Questões Vevox: Consolidação de Matéria

Este documento reúne **25 questões pedagógicas estritamente técnicas**, formuladas de forma **concisa e direta** para garantir excelente legibilidade em telemóveis e ecrãs de projeção durante as votações interativas no **Vevox**.

### Distribuição por Nível de Dificuldade:
* **Baixa (36% — 9 questões):** Focadas em recordação direta de comandos, convenções e conceitos base.
* **Média (44% — 11 questões):** Aplicação de comandos, cálculo de permissões, sintaxe e relações conceptuais.
* **Média-Alta (20% — 5 questões):** Diagnóstico de execução, isolamento de processos, arquitetura e análise crítica.

---

\newpage

# Bloco I: Sistemas Operativos, Ficheiros e Ambientes Linux (Class 00)

## Questão 01 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Principal diferença entre os sistemas de ficheiros Linux e Windows?

- [ ] **A)** Linux usa letras de unidade (`C:`) e Windows usa raiz unificada (`/`).
- [x] **B)** Linux tem raiz única (`/`) e é *case-sensitive*; Windows usa letras (`C:`) e é *case-insensitive*.
- [ ] **C)** Ambos usam letras de unidade e tratam maiúsculas como o mesmo ficheiro.
- [ ] **D)** Linux não suporta criação de pastas com letras maiúsculas.

**Resposta Correta:** B  
**Explicação Pedagógica:** No Linux, todos os dispositivos e partições são montados sob uma raiz única (`/`), sendo o sistema estritamente *case-sensitive* (`dados.txt` $\neq$ `Dados.txt`). O Windows usa letras de unidade (`C:`, `D:`), barra invertida (`\`) e é *case-insensitive*.

---

## Questão 02 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Principal vantagem de uma Máquina Virtual (VM) face à instalação nativa?

- [ ] **A)** Maior desempenho de processamento e gráfico do que no hardware real.
- [x] **B)** Isolamento seguro (*sandbox*) e recuperação fácil com *snapshots*.
- [ ] **C)** Dispensa de instalar qualquer sistema operativo no computador.
- [ ] **D)** Sem consumo de memória RAM nem espaço em disco do computador anfitrião.

**Resposta Correta:** B  
**Explicação Pedagógica:** A VM corre isolada sobre o hipervisor (*sandbox*). Erros ou comandos destrutivos ficam confinados ao disco virtual e podem ser revertidos com *snapshots*, sem risco de corrupção do SO anfitrião.

---

## Questão 03 [Escolha Múltipla | Dificuldade: Média-Alta]
**Enunciado:** WSL 2: acesso ao disco `C:` e localização recomendada para código?

- [ ] **A)** Acesso em `/windows/c/`; código no `C:\` do Windows.
- [x] **B)** Acesso em `/mnt/c/`; código na pasta nativa Linux (`/home/utilizador/`).
- [ ] **C)** Acesso em `/media/c/`; código na pasta temporária `/tmp/`.
- [ ] **D)** Sem capacidade de aceder ao disco do Windows.

**Resposta Correta:** B  
**Explicação Pedagógica:** No WSL 2, as unidades Windows são montadas sob `/mnt/`. Devido à sobrecarga de I/O na partição NTFS via WSL, a boa prática é guardar projetos no sistema de ficheiros ext4 nativo (`/home/utilizador/`).

---

## Questão 04 [Correspondência / Matching | Dificuldade: Média]
**Enunciado:** Associe cada abordagem de ambiente Linux à respetiva característica:

| Coluna A (Abordagem) | Coluna B (Característica Técnica) |
| :--- | :--- |
| **1.** Instalação Nativa | **A.** Acesso direto ao hardware (máximo desempenho) |
| **2.** Máquina Virtual (VM) | **B.** Isolamento total (*sandbox* e *snapshots*) |
| **3.** WSL 2 (Windows) | **C.** Kernel integrado com unidades em `/mnt/` |
| **4.** Comando `uname -a` | **D.** Identifica versão do kernel e arquitetura |

**Pares Corretos (Configurados nativamente em `vevox_pt_00.xlsx` como `Type = Matching`):**
* **1 $\rightarrow$ A** (Instalação Nativa corre no hardware com desempenho total)
* **2 $\rightarrow$ B** (VM corre em *sandbox* isolada com suporte a *snapshots*)
* **3 $\rightarrow$ C** (WSL 2 integra o kernel no Windows com discos em `/mnt/`)
* **4 $\rightarrow$ D** (`uname -a` imprime metadados da versão do kernel e arquitetura)

**Explicação Pedagógica:** Diferentes estratégias equilibram isolamento, desempenho e integração no SO anfitrião.

\newpage

# Bloco II: Terminal Linux e Ferramentas de Shell (Class 01)

## Questão 05 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Diferença entre Terminal e Shell, e efeito do atalho `Ctrl + C`?

- [ ] **A)** Terminal executa comandos; Shell é a janela; `Ctrl + C` copia texto selecionado.
- [x] **B)** Terminal é a janela de interface; Shell é o interpretador; `Ctrl + C` interrompe o comando (`SIGINT`).
- [ ] **C)** Terminal e Shell são idênticos; `Ctrl + C` limpa o ecrã do terminal.
- [ ] **D)** Shell é a janela gráfica; `Ctrl + C` suspende o processo em segundo plano.

**Resposta Correta:** B  
**Explicação Pedagógica:** O terminal é a janela de interface de entrada/saída de texto; a shell (ex: Bash, Zsh) é o interpretador de comandos. `Ctrl + C` envia o sinal `SIGINT` para interromper o processo em execução.

---

## Questão 06 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Na pasta `/home/aluno/IEI/projeto`, onde fica o utilizador após `cd ../..` ?

- [ ] **A)** `/home`
- [x] **B)** `/home/aluno`
- [ ] **C)** `/` (raiz do sistema)
- [ ] **D)** `/home/aluno/IEI`

**Resposta Correta:** B  
**Explicação Pedagógica:** O identificador `..` referencia o diretório pai. A partir de `/home/aluno/IEI/projeto`, o primeiro `..` recua para `/home/aluno/IEI` e o segundo recua para `/home/aluno`.

---

## Questão 07 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Identificação de ficheiros ocultos e comando para listagem longa?

- [ ] **A)** Termina em `.hidden`; comando `dir /all`.
- [x] **B)** Começa com um ponto (`.`); comando `ls -la`.
- [ ] **C)** Tem permissão de leitura desativada; comando `cat -a`.
- [ ] **D)** Fica guardado em `/tmp`; comando `find . -hidden`.

**Resposta Correta:** B  
**Explicação Pedagógica:** Ficheiros cujo nome começa com `.` são ocultos por convenção na listagem simples. A flag `-a` do `ls` lista todos os ficheiros e a flag `-l` exibe o formato longo com permissões e tamanhos.

---

## Questão 08 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Redirecionamento de saída: diferença entre `>` e `>>` ?

- [ ] **A)** `>` adiciona no fim (*append*); `>>` sobrescreve o conteúdo.
- [x] **B)** `>` sobrescreve o ficheiro; `>>` adiciona no fim (*append*).
- [ ] **C)** `>` redireciona erros (`stderr`); `>>` redireciona a saída padrão.
- [ ] **D)** `>` envia para o ecrã; `>>` guarda na memória RAM.

**Resposta Correta:** B  
**Explicação Pedagógica:** O operador `>` trunca e sobrescreve o conteúdo do ficheiro de destino. O operador `>>` adiciona os novos dados no final do ficheiro existente (*append*).

---

## Questão 09 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Resultado do comando: `cat lista.txt | grep "LEI" | wc -l` ?

- [ ] **A)** Executa os três comandos em paralelo e cria o ficheiro `wc -l`.
- [x] **B)** Conta o número de linhas de `lista.txt` que contêm a palavra "LEI".
- [ ] **C)** Substitui a palavra "LEI" pelo número de caracteres do ficheiro.
- [ ] **D)** Apaga todas as linhas com "LEI" do ficheiro `lista.txt`.

**Resposta Correta:** B  
**Explicação Pedagógica:** O pipe (`|`) liga o `stdout` de um comando ao `stdin` do seguinte. O `cat` lê o ficheiro, o `grep` filtra as linhas com "LEI" e o `wc -l` conta essas linhas.

---

## Questão 10 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Permissão octal correspondente a `-rw-------` (leitura e escrita apenas pelo dono)?

- [ ] **A)** `chmod 700`
- [x] **B)** `chmod 600`
- [ ] **C)** `chmod 644`
- [ ] **D)** `chmod 755`

**Resposta Correta:** B  
**Explicação Pedagógica:** Em notação octal, $r=4$, $w=2$, $x=1$. Para o dono `rw-` ($4+2=6$), para o grupo `---` ($0$) e para outros `---` ($0$). O valor total é `600`.

---

## Questão 11 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Comando que força o encerramento imediato do processo PID 5842 via kernel?

- [ ] **A)** `kill -STOP 5842`
- [x] **B)** `kill -9 5842` (ou `kill -SIGKILL 5842`)
- [ ] **C)** `ps -kill 5842`
- [ ] **D)** `bg 5842`

**Resposta Correta:** B  
**Explicação Pedagógica:** O sinal 9 (`SIGKILL`) não pode ser intercetado nem ignorado pelo processo; é executado diretamente pelo kernel do Linux, terminando o processo de imediato.

---

## Questão 12 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Debian/Ubuntu: diferença entre `apt update` e `apt upgrade`?

- [ ] **A)** `update` instala novas versões; `upgrade` limpa a cache do disco.
- [x] **B)** `update` atualiza a lista de repositórios; `upgrade` instala as novas versões dos pacotes.
- [ ] **C)** `update` desinstala programas antigos; `upgrade` instala o kernel.
- [ ] **D)** Ambos executam rigorosamente a mesma operação.

**Resposta Correta:** B  
**Explicação Pedagógica:** `apt update` descarrega os índices atualizados dos repositórios. `apt upgrade` analisa os pacotes instalados e procede à instalação das novas versões disponíveis.

---

## Questão 13 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Agendamento crontab: quando executa `15 3 * * 2 /home/aluno/backup.sh` ?

- [ ] **A)** No dia 15 de março, a cada 2 minutos.
- [ ] **B)** De 15 em 15 minutos, durante as primeiras 3 horas do dia.
- [x] **C)** Todas as terças-feiras às 03h15.
- [ ] **D)** No dia 2 de fevereiro às 03h15.

**Resposta Correta:** C  
**Explicação Pedagógica:** Os campos do cron são: minuto (`15`), hora (`3`), dia do mês (`*`), mês (`*`) e dia da semana (`2` = terça-feira). Executa todas as terças-feiras às 03h15.

---

## Questão 14 [Correspondência / Matching | Dificuldade: Baixa]
**Enunciado:** Associe cada comando Linux à respetiva função:

| Coluna A (Comando) | Coluna B (Função) |
| :--- | :--- |
| **1.** `pwd` | **A.** Imprime o caminho do diretório atual |
| **2.** `head -n 5 log.txt` | **B.** Mostra as 5 primeiras linhas do ficheiro |
| **3.** `touch novo.txt` | **C.** Cria ficheiro vazio ou atualiza timestamp |
| **4.** `grep -i "erro" log.txt` | **D.** Pesquisa texto sem distinguir maiúsculas |

**Pares Corretos (Configurados nativamente em `vevox_pt_00.xlsx` como `Type = Matching`):**
* **1 $\rightarrow$ A** (`pwd` imprime o diretório de trabalho atual)
* **2 $\rightarrow$ B** (`head -n 5` extrai o início do ficheiro)
* **3 $\rightarrow$ C** (`touch` cria ficheiro ou atualiza timestamps)
* **4 $\rightarrow$ D** (`grep -i` efetua pesquisa textual insensível a maiúsculas)

**Explicação Pedagógica:** Comandos fundamentais do kit Unix para navegação, inspeção, criação e filtragem.

\newpage

# Bloco III: Gestão de Ambiente Linux e Engenharia de IA (Class 02)

## Questão 15 [Escolha Múltipla | Dificuldade: Média-Alta]
**Enunciado:** Após `CHAVE="123"` na shell, porque é que `./script.sh` não a lê (`echo $CHAVE` vazio)?

- [ ] **A)** O comando `echo` não expande variáveis em scripts externos.
- [x] **B)** A variável é local à shell; tem de ser exportada com `export CHAVE="123"`.
- [ ] **C)** O script necessita de ser executado com permissões de superutilizador (`sudo`).
- [ ] **D)** Nomes de variáveis têm de conter obrigatoriamente um prefixo numérico.

**Resposta Correta:** B  
**Explicação Pedagógica:** Variáveis sem `export` residem apenas na memória da shell atual. Ao correr `./script.sh`, é criada uma subshell (processo filho) que apenas herda variáveis globais de ambiente (`export`).

---

## Questão 16 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Como aplicar alterações do `~/.bashrc` na sessão sem fechar o terminal?

- [ ] **A)** `./~/.bashrc`
- [x] **B)** `source ~/.bashrc` (ou `. ~/.bashrc`)
- [ ] **C)** `chmod +x ~/.bashrc`
- [ ] **D)** Reiniciar o computador.

**Resposta Correta:** B  
**Explicação Pedagógica:** O comando interno `source` (ou `.`) lê e executa o ficheiro no contexto da shell ativa corrente, sem criar um subprocesso efémero.

---

## Questão 17 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Motivo para aplicar `chmod 600` a ficheiros de segredos (`.env`) em PCs partilhados?

- [x] **A)** Impedir que outros utilizadores do sistema leiam o ficheiro (permissão padrão é 644).
- [ ] **B)** Cifrar o conteúdo do ficheiro no disco rígido.
- [ ] **C)** Exigência de leitura do interpretador de Python.
- [ ] **D)** Evitar que o dono apague o ficheiro acidentalmente.

**Resposta Correta:** A  
**Explicação Pedagógica:** A permissão padrão de criação é normalmente `644` (leitura aberta ao grupo e outros). Com `chmod 600` (`rw-------`), apenas o dono tem acesso de leitura e escrita.

---

## Questão 18 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Comando `tar` para criar o arquivo comprimido `backup.tar.gz` da pasta `projeto/` ?

- [ ] **A)** `tar -xzvf backup.tar.gz projeto/`
- [x] **B)** `tar -czvf backup.tar.gz projeto/`
- [ ] **C)** `tar -zip backup.tar.gz projeto/`
- [ ] **D)** `tar -extract backup.tar.gz projeto/`

**Resposta Correta:** B  
**Explicação Pedagógica:** No `tar`: `-c` cria o arquivo (*create*), `-z` comprime com gzip, `-v` ativa o modo detalhado (*verbose*) e `-f` indica o nome do ficheiro. Para extrair usa-se `-x`.

---

## Questão 19 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Processamento em LLMs: relação prática entre tokens e palavras?

- [ ] **A)** Processam ficheiros byte a byte, correspondendo 1 byte a 1 palavra.
- [x] **B)** Processam *tokens* (pedaços de palavras); 1 token $\approx$ 0,75 palavras em inglês.
- [ ] **C)** Cada token representa obrigatoriamente uma frase gramatical completa.
- [ ] **D)** Os modelos descartam pontuação e leem apenas palavras inteiras do dicionário.

**Resposta Correta:** B  
**Explicação Pedagógica:** As LLMs utilizam tokenização estatística (como BPE). Os tokens são fragmentos de palavras e símbolos. Em inglês, 1 token corresponde a cerca de 0,75 palavras; em português consome frequentemente mais tokens por palavra.

---

## Questão 20 [Escolha Múltipla | Dificuldade: Baixa]
**Enunciado:** Temperatura ($\tau$) na API para gerar código Bash determinista com menor alucinação?

- [ ] **A)** Temperatura alta ($\tau \approx 1.8$ a $2.0$).
- [x] **B)** Temperatura baixa ($\tau \approx 0.0$ a $0.2$).
- [ ] **C)** A temperatura não se aplica a modelos de texto.
- [ ] **D)** Temperatura 100 para acelerar a resposta da API.

**Resposta Correta:** B  
**Explicação Pedagógica:** Temperaturas baixas tornam a amostragem de probabilidades determinista e focada nos tokens mais prováveis, ideal para código e testes técnicos.

---

## Questão 21 [Escolha Múltipla | Dificuldade: Média-Alta]
**Enunciado:** Diferença económica entre chat web e APIs, e risco em agentes de terminal?

- [ ] **A)** Chat cobra por minuto; API é sempre gratuita.
- [x] **B)** Chat tem subscrição fixa; API é *pay-as-you-go*, com risco de custos em *retry loops* sem limites.
- [ ] **C)** APIs exigem pagamento prévio em criptomoedas.
- [ ] **D)** O tráfego de rede para APIs é gratuito por lei na nuvem.

**Resposta Correta:** B  
**Explicação Pedagógica:** O chat tem preço fixo mensal. As APIs cobram ao milhão de tokens (*pay-as-you-go*). Agentes em loops automáticos de tentativa e erro podem disparar custos se não tiverem *Hard Spend Limits*.

---

## Questão 22 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Engenharia de Contexto: que prática substitui personas ("Age como um perito...")?

- [ ] **A)** Escrever prompts longos e informais na esperança de bom resultado.
- [x] **B)** Estruturar com: Tarefa direta, tags XML de dados, restrições e exemplos (*Few-Shot*).
- [ ] **C)** Repetir a mesma frase várias vezes com letras maiúsculas.
- [ ] **D)** Incluir saudações cordiais para melhorar a empatia do modelo.

**Resposta Correta:** B  
**Explicação Pedagógica:** Modelos de raciocínio não precisam de personas. Devem usar-se os 4 pilares: tarefa direta, contexto estruturado em XML, restrições explícitas de formato e calibração por Few-Shot.

---

## Questão 23 [Escolha Múltipla | Dificuldade: Média]
**Enunciado:** Função principal do ficheiro `AGENTS.md` na raiz de um repositório?

- [ ] **A)** Compilar binários executáveis de forma automática.
- [x] **B)** Definir o contrato do projeto para o agente (stack, comandos de build/teste e restrições).
- [ ] **C)** Armazenar chaves privadas de API em texto aberto.
- [ ] **D)** Limpar a cache temporária do sistema operativo.

**Resposta Correta:** B  
**Explicação Pedagógica:** O `AGENTS.md` funciona como a constituição operacional do repositório para agentes de código, estabelecendo a stack, convenções de compilação/teste e restrições arquiteturais.

---

## Questão 24 [Escolha Múltipla | Dificuldade: Média-Alta]
**Enunciado:** Porque é que "Não apagues ficheiros" num prompt é um Soft Guardrail sem segurança real?

- [ ] **A)** Os modelos de linguagem não compreendem texto em português.
- [x] **B)** Prompts são heurísticas probabilísticas; segurança real exige Hard Guardrails no SO (permissões/sandbox).
- [ ] **C)** O terminal executa sempre todos os comandos com permissões de root.
- [ ] **D)** Os modelos dão prioridade máxima a instruções destrutivas.

**Resposta Correta:** B  
**Explicação Pedagógica:** Instruções textuais são barreiras suaves (*soft boundaries*) e podem falhar ou ser contornadas. A segurança real em engenharia depende de barreiras rígidas (*hard boundaries*): permissões mínimas, contentores/sandboxes e *Human-in-the-Loop*.

---

## Questão 25 [Correspondência / Matching | Dificuldade: Média-Alta]
**Enunciado:** Associe cada conceito de IA à respetiva definição técnica:

| Coluna A (Conceito) | Coluna B (Definição Técnica) |
| :--- | :--- |
| **1.** Model Context Protocol (MCP) | **A.** Protocolo aberto para ligar LLMs a ferramentas |
| **2.** Alucinação (Hallucination) | **B.** Resposta incorreta gerada com tom confiante |
| **3.** Calibração Few-Shot | **C.** Exemplos no prompt para guiar o formato |
| **4.** Hard Spend Limit | **D.** Teto de custos na cloud para bloquear gastos |

**Pares Corretos (Configurados nativamente em `vevox_pt_00.xlsx` como `Type = Matching`):**
* **1 $\rightarrow$ A** (MCP é o padrão aberto de conectores de ferramentas)
* **2 $\rightarrow$ B** (Alucinação é a geração errada assertiva)
* **3 $\rightarrow$ C** (Few-Shot ancora padrões através de exemplos)
* **4 $\rightarrow$ D** (Hard Spend Limit protege o orçamento na cloud)

**Explicação Pedagógica:** Conceitos basilares para a engenharia de software contemporânea assistida por modelos de linguagem e agentes.
