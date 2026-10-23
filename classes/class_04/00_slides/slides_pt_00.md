---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Contentores: Arquitetura, Docker & Docker Compose"
institute: Universidade de Aveiro
date: October 19, 2026
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

  * **Parte I — Fundamentos & Arquitetura de Isolamento:** O problema da portabilidade, virtualização de SO, namespaces, cgroups e suporte fora do Linux.
  * **Parte II — Do Kernel às Ferramentas: Ecossistema & OCI:** A evolução de LXC a Docker, a normalização OCI (`runc`, especificações abertas) e o Podman.
  * **Parte III — Imagens, Armazenamento & Redes:** Terminologia, tags, ciclo de vida, camadas (Copy-on-Write), volumes e redes com DNS.
  * **Parte IV — O Docker na Prática & Anatomia do `Dockerfile`:** Comandos CLI fundamentais, instruções, formas exec/shell e `CMD` vs. `ENTRYPOINT`.
  * **Parte V — Orquestração Local com Docker Compose:** Sintaxe de `compose.yml`, comandos de gestão e padrões essenciais de arquitetura multi-serviço.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos \& Arquitetura}}
\end{center}

-----

## O Desafio da Portabilidade de Software

A heterogeneidade de configurações entre plataformas de desenvolvimento, teste e produção constitui um desafio central na engenharia de software:

  * **Ambiente de Desenvolvimento:**
      * Configuração com versões específicas de interpretadores (ex.: Python 3.11), bibliotecas dinâmicas e variáveis de ambiente locais.
  * **Ambiente de Produção ou Teste:**
      * Sistemas operativos com versões distintas de bibliotecas partilhadas do sistema ou políticas de segurança restritivas.
      * Risco de falhas de execução por incompatibilidade de dependências (*dependency hell*).

\vspace{1em}

\begin{center}
\textbf{Seria útil encapsular a aplicação e todas as suas dependências num artefacto padronizado, garantindo uma execução determinística e reprodutível.}
\end{center}

-----

## As Máquinas Virtuais como Solução?

O isolamento proporcionado pelas Máquinas Virtuais acarreta custos elevados para a execução de aplicações:

  * **Propriedades da Virtualização de Hardware:**
      * Isolamento integral ao nível do hardware via hipervisor.
      * Kernel e sistema operativo dedicados por máquina virtual.
  * **Limitações no Contexto Aplicacional:**
      * **Sobrecarga:** Alocação estática de gigabytes de RAM e disco por instância.
      * **Redundância:** Duplicação de sistemas operativos completos para executar um único serviço.
      * **Latência:** Arranque lento (minutos), limitando a escalabilidade dinâmica.

\vspace{1em}

\begin{center}
\textbf{A virtualização ao nível do hardware é desproporcionada para isolar e distribuir aplicações individuais.}
\end{center}

-----

## A Solução: Contentores

A resposta passa pela **virtualização ao nível do sistema operativo**:

  * **Conceito de Contentor:** Unidade padronizada com a aplicação e todas as dependências.
  * **Mudança de Paradigma:**
      * Partilha do **kernel do anfitrião**, sem virtualizar hardware.
      * Isolamento dos processos garantido **pelo próprio kernel** (via *namespaces* e *cgroups*).
  * **Portabilidade Determinística:** Execução idêntica em ambientes de desenvolvimento, teste ou infraestruturas na nuvem.

\vspace{1em}

\begin{center}
\textbf{O contentor marítimo desacoplou as mercadorias dos veículos de transporte (navio, comboio, rodovia). O contentor de software desacopla a aplicação do sistema operativo anfitrião.}
\end{center}

-----

## Arquitetura Comparada: VMs vs. Contentores

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{vm_vs_container_architecture.png}
\end{center}

-----

## Comparação Sistemática: VMs vs. Contentores

| Dimensão Técnica | Máquinas Virtuais (VMs) | Contentores |
| :--- | :--- | :--- |
| **Nível de Abstração** | **Virtualização de Hardware** | **Virtualização de SO** (Processos) |
| **Kernel do Sistema** | Kernel convidado dedicado por VM | **Kernel do anfitrião partilhado** |
| **Consumo de Memória (RAM)** | Elevado (memória estática alocada ao SO) | **Mínimo** (apenas o que a aplicação gasta) |
| **Tamanho da Imagem** | Gigabytes (GB) | Megabytes (MB) |
| **Tempo de Inicialização** | Dezenas de segundos a minutos | **Milissegundos a segundos** |
| **Sobrecarga de Desempenho** | Baixa a moderada (latência de hipervisor) | **Quase nativa** (sem intermediação de hardware) |
| **Fronteira de Isolamento** | Muito forte (hardware / anéis CPU) | Forte (mecanismos de isolamento no kernel) |
| **Caso de Uso Típico** | Sistemas multi-OS, isolamento estrito | Backends, Microsserviços, APIs, Kubernetes |

-----

## Mecanismos do Kernel: Namespaces do Linux

Os **Namespaces do Linux** delimitam o perímetro de visibilidade dos recursos do sistema operativo (o que o processo consegue **ver**):

  * **PID (Process ID):** Isola a tabela de processos (aplicação com **PID 1** no contentor).
  * **NET (Network):** Interfaces virtuais próprias (`eth0`), tabelas de encaminhamento e espaço de portos independente.
  * **MNT (Mount):** Pontos de montagem isolados, com um diretório raiz (`/`) dedicado.
  * **UTS (Hostnames):** Atribuição de nome de máquina (*hostname*) e domínio próprios.
  * **USER:** Mapeamento de utilizadores (ex.: `root` no contentor sem privilégios no anfitrião).
  * **IPC (Inter-Process Communication):** Isolamento de memória partilhada e semáforos entre processos.

-----

## Isolamento em Ação: Mapeamento de Namespaces

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{linux_namespaces_isolation.png}
\end{center}

-----

## Mecanismos do Kernel: Control Groups (cgroups)

Os **Control Groups (cgroups)** permitem ao kernel impor limites estritos de hardware a cada contentor:

  * **CPU:** Limita a percentagem de tempo de processador ou número de núcleos dedicados (ex: máximo de 1.5 vCPUs).
  * **Memória RAM:** Impõe um teto máximo de memória (ex: 512 MB). Se a aplicação ultrapassar o limite, o kernel encerra o processo (*Out Of Memory Killer - OOM*).
  * **E/S de Armazenamento (Block I/O):** Evita que um contentor sobrecarregue o disco com operações de leitura/escrita concorrentes.
  * **Controlo de PIDs (pids cgroup):** Limita o número de processos filhos para proteger o anfitrião contra *fork bombs*.

\vspace{1em}

\begin{center}
\textbf{Enquanto os \textit{namespaces} definem o perímetro de visibilidade e isolamento lógico, os \textit{cgroups} impõem quotas quantitativas e garantias de afetação (\textit{fair-share}) sobre os recursos computacionais.}
\end{center}

-----

## Contentores Linux Fora do Linux: macOS e Windows

Como dependem do kernel Linux (*namespaces* e *cgroups*), executar **contentores Linux** em macOS ou Windows requer uma máquina virtual de suporte (gerida por ferramentas como **Docker Desktop** ou **Podman**):

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_desktop_architecture.png}
\end{center}

-----

## Contentores Linux Fora do Linux: macOS e Windows

  * **Em Linux (Execução Nativa):**
      * Execução direta sobre o kernel do anfitrião, com desempenho nativo.
      * Sem hipervisores nem sobrecarga de virtualização.
  * **Em macOS e Windows (Docker Desktop, Podman, etc.):**
      * Kernels anfitriões (Darwin / NT) não executam binários Linux nativamente.
      * As ferramentas criam uma **micro-VM Linux** (*Virtualization.framework* / *WSL2*) partilhada pelos contentores.
      * *(Nota: O Windows suporta contentores NT nativos, mas a quase totalidade do ecossistema assenta em imagens Linux).*
  * **Impacto Operacional:**
      * Alocação fixa de RAM e CPU dedicados à máquina virtual de suporte.
      * Maior latência de E/S na partilha de ficheiros (*bind mounts*) através da VM.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Do Kernel às Ferramentas: Ecossistema \& OCI}}
\end{center}

-----

## A Evolução: Linux Containers (LXC) vs. Docker

A tecnologia de contentores não nasceu com o Docker:

  * **LXC (Linux Containers, 2008):**
      * Primeira solução abrangente que integrou cgroups e namespaces no kernel Linux.
      * Focado em **contentores de sistema**: funcionam como máquinas virtuais leves executando um sistema `init` completo (systemd), múltiplos processos e serviços de fundo.
  * **A Revolução do Docker (2013):**
      * O Docker utilizou inicialmente o LXC como motor subjacente, criando uma camada de abstração muito superior.
      * Introduziu o conceito de **contentores de serviço / microsserviço**: cada contentor executa **um único processo principal**.
      * Popularizou o formato de imagens em camadas (`Dockerfile`) e o registo global partilhado (Docker Hub), transformando a forma como a indústria constrói software.

-----

## Normalização e Padrões Abertos: A OCI

Para evitar a dependência de uma única empresa, a indústria criou a **Open Container Initiative (OCI)**:

  * **Especificação de Imagem (Image Spec):**
      * Define o formato binário exato das camadas e dos manifestos de imagens.
      * Uma imagem construída pelo Docker cumpre a especificação OCI e pode ser executada sem alterações pelo Podman, containerd, CRI-O ou Kubernetes.
  * **Especificação de Execução (Runtime Spec):**
      * Define a interface com o kernel para criar contentores.
      * A implementação de referência aberta é o **`runc`**, utilizado universalmente tanto pelo Docker como pelo Podman.

-----

## O Podman e a Segurança de Contentores

O **Podman** (desenvolvido pela Red Hat) surgiu como uma resposta moderna aos desafios de segurança e arquitetura do Docker tradicional:

  * **Arquitetura sem Daemon (*Daemonless*):**
      * O Docker depende de um daemon central (`dockerd`) sempre ativo como `root`. Se o daemon falhar, a gestão de todos os contentores é afetada.
      * O Podman não tem daemon central: cada contentor é um processo filho direto de quem o invocou.
  * **Execução Não-Privilegiada (*Rootless by Design*):**
      * Permite a utilizadores sem privilégios de administração (sem `sudo`) criar, obter e executar contentores em Linux através de *User Namespaces*.
  * **Compatibilidade Total de Linha de Comandos:**
      * A sintaxe de comandos é 100% idêntica:
        ```bash
        $ alias docker=podman
        $ docker run -d -p 8080:80 nginx:alpine
        ```

\vspace{1em}

\begin{center}
\textbf{As ferramentas partilham os mesmos comandos e normas OCI; dominar a interface Docker confere competências universais para todo o ecossistema.}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Imagens, Armazenamento \& Redes}}
\end{center}

-----

## Terminologia Fundamental: Imagem vs. Contentor

Existem três conceitos fundamentais relacionados com contentores:

  * **1. Imagem de Contentor (Image):**
      * Molde estático e imutável (*read-only*) com o sistema de ficheiros, binários e bibliotecas.
      * **Analogia:** Equivale a uma **Classe** (especificação estática).
  * **2. Contentor (Container):**
      * Instância viva de uma imagem em execução, isolada pelo kernel.
      * **Analogia:** Equivale a um **Objeto** (múltiplas instâncias podem derivar da mesma imagem).
  * **3. Registo (Registry):**
      * Repositório central de distribuição e partilha de imagens versionadas (ex: Docker Hub, GitHub Packages).

-----

## O Ciclo de Vida do Docker

\begin{center}
\includegraphics[width=0.98\linewidth,keepaspectratio]{docker_lifecycle.png}
\end{center}

-----

## Identificação e Nomenclatura de Imagens

As imagens são identificadas seguindo a convenção padronizada:

$$\texttt{[registo/][repositório/]nome\textbf{:}tag}$$

  * **Repositório Oficial:** Imagens oficiais no Docker Hub omitem o registo (ex: `nginx`, `alpine`, `ubuntu`).
  * **Papel da *Tag*:** Identifica a versão ou variante; por omissão assume `:latest`.
  * **Exemplos:**
      * `nginx:alpine` $\rightarrow$ NGINX sobre distribuição minimalista Alpine Linux (~20 MB).
      * `python:3.11-slim` $\rightarrow$ Python 3.11 sem ferramentas pesadas de compilação.
      * `lscr.io/linuxserver/jellyfin:latest` $\rightarrow$ Imagem oriunda de registo externo (`lscr.io`).
  * **Digest (SHA-256):** Hash criptográfico único que garante a integridade e imutabilidade exata da imagem.

-----

## A Anatomia da Imagem: Camadas & Copy-on-Write (CoW)

Uma imagem Docker não é um ficheiro monolítico, mas sim uma **pilha de camadas imutáveis**:

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{container_layers_cow.png}
\end{center}

-----

## Mecanismo Copy-on-Write (CoW): Eficiência e Imutabilidade

  * **Partilha de Camadas no Disco:**
      * Camadas base comuns (ex: `alpine:3.20`) são guardadas em disco **uma única vez**.
      * Poupança substancial de tráfego de rede e espaço de armazenamento.
  * **Imutabilidade das Camadas (*Read-Only*):**
      * A imagem original nunca é alterada ou corrompida por nenhum contentor.
  * **Camada de Escrita do Contentor (*Read-Write Layer*):**
      * Camada temporária criada no topo da pilha ao iniciar o contentor.
      * **Leitura:** Ficheiros são lidos diretamente das camadas partilhadas inferiores.
      * **Modificação (CoW):** Ao alterar um ficheiro existente, este é copiado para a camada R/W antes da edição.
      * **Destruição:** Ao remover o contentor, apenas esta camada volátil de escrita é eliminada.

-----

## Persistência de Dados: Tipos de Armazenamento

Por omissão, o sistema de ficheiros de um contentor é **efémero**. Para gerir dados, existem três mecanismos fundamentais:

  * **1. Camada de Escrita (Writable Layer):**
      * **Ciclo de Vida:** Efémera; eliminada permanentemente quando o contentor é destruído.
      * **Uso Típico:** Ficheiros temporários de trabalho e serviços *stateless* (sem estado).
  * **2. Mapeamentos Locais (*Bind Mounts*):**
      * **Mecanismo:** Mapeia uma pasta do anfitrião diretamente no contentor (`host:contentor`).
      * **Uso Típico:** **Desenvolvimento local** (alterações no código refletem-se ao vivo sem recriar a imagem).
  * **3. Volumes Geridos (*Named Volumes*):**
      * **Mecanismo:** Espaço de armazenamento gerido pelo motor numa área isolada do sistema.
      * **Uso Típico:** **Produção e persistência** (bases de dados, elevada performance de I/O e sobrevivência à remoção de contentores).

-----

## Redes Virtuais: Modo Bridge e Mapeamento de Portas

Por omissão, cada contentor é ligado a uma rede virtual privada em modo ponte (*Bridge Network*):

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.72\textheight,keepaspectratio]{docker_network_ports_dns.png}
\end{center}

-----

## Redes em Contentores: Isolamento e Resolução DNS

  * **Rede Virtual Privada (*Bridge Network*):**
      * Isolamento entre contentores e a rede exterior através de regras de *bridge* e NAT no kernel.
      * Cada contentor recebe um endereço IP privado interno dinâmico (ex: `172.20.0.x`).
  * **Mapeamento de Portas (`-p <porto_anfitrião>:<porto_contentor>`):**
      * Encaminha o tráfego que chega a um porto do anfitrião para a porta do contentor (ex: `-p 8080:80`).
      * Permite aceder à aplicação a partir do exterior via `http://localhost:8080`.
  * **Resolução por DNS Embutido:**
      * Contentores na mesma rede comunicam diretamente através do **nome do serviço** (ex: `postgres://db:5432`).
      * Desacoplamento total face aos endereços IP efémeros atribuídos dinamicamente.
  * **Isolamento de Segurança:**
      * Serviços internos (ex: base de dados `db`) operam sem portas expostas ao anfitrião.
      * Totalmente invisíveis e protegidos de acessos diretos da rede externa ou Internet*.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: O Docker na Prática \& Anatomia do Dockerfile}}
\end{center}

-----

## Comandos Docker Essenciais

A ferramenta de linha de comandos `docker` controla o ciclo de vida dos contentores:

| Comando | Descrição |
| :--- | :--- |
| `docker run [opções] <imagem>` | Cria e inicia um novo contentor a partir de uma imagem. |
| `docker run -d -p 8080:80 <imagem>` | Executa em segundo plano (*detached*) mapeando o porto 8080. |
| `docker ps` | Lista os contentores atualmente em execução. |
| `docker ps -a` | Lista todos os contentores (incluindo os parados/terminados). |
| `docker stop <id/nome>` | Envia sinal `SIGTERM` para parar o contentor de forma controlada. |
| `docker rm <id/nome>` | Remove definitivamente um contentor parado e a sua camada R/W. |
| `docker logs -f <id/nome>` | Inspeciona e acompanha os logs da saída padrão (`stdout`/`stderr`). |
| `docker exec -it <nome> sh` | Abre uma sessão de terminal interativa dentro de um contentor vivo. |
| `docker images` | Lista todas as imagens armazenadas localmente no disco. |
| `docker rmi <imagem>` | Remove uma imagem local do armazenamento. |

-----

## Visão Global: Exemplo de um `Dockerfile`

Um `Dockerfile` define a receita declarativa e automatizada para construir uma imagem:

```dockerfile
# 1. Imagem base de partida
FROM python:3.11-slim

# 2. Diretório de trabalho dentro do contentor
WORKDIR /app

# 3. Cópia de ficheiros e instalação de dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4. Metadados de rede e comando de arranque
EXPOSE 8080
CMD ["python", "app.py"]
```

```bash
$ docker build -t minha-app:1.0 .             # Constrói a imagem localmente (.)
$ docker run -d -p 8080:8080 minha-app:1.0    # Executa o contentor
```

-----

## Anatomia do `Dockerfile`: Instruções de Estrutura

Com o exemplo em mente, analisemos as instruções responsáveis pelo sistema de ficheiros:

  * `FROM <imagem>:<tag>`
      * Especifica a imagem base a partir da qual a nova imagem é derivada (ex: `alpine:3.20`).
  * `WORKDIR <caminho>`
      * Define o diretório de trabalho para as instruções seguintes (cria a pasta se não existir).
  * `COPY <origem> <destino>`
      * Copia ficheiros do computador anfitrião para o sistema de ficheiros da imagem.
  * `RUN <comando>`
      * Executa comandos durante a construção e grava o resultado numa nova camada imutável (ex: `RUN apk add --no-cache curl`).

-----

## Anatomia do `Dockerfile`: Ambiente, Portos & Segurança

  * `ENV <chave>=<valor>`
      * Define variáveis de ambiente persistentes durante toda a execução do contentor (ex: `ENV PORT=8080`).
  * `ARG <nome>=<valor>`
      * Define variáveis temporárias usadas exclusivamente no momento da compilação da imagem.
  * `EXPOSE <porto>`
      * **Metadados de documentação**: indica os portos em que a aplicação escuta (não publica no anfitrião).
  * `USER <utilizador>`
      * Define o utilizador dos processos seguintes, evitando a execução com privilégios de `root`.

-----

## Anatomia do `Dockerfile`: Execução (`CMD` & `ENTRYPOINT`)

Para definir o processo que é iniciado quando o contentor arranca, o Docker disponibiliza duas instruções fundamentais:

  * `CMD ["executável", "arg1", ...]`
      * Define o comando e/ou argumentos **por omissão** a executar no arranque.
      * Se forem passados argumentos adicionais em `docker run`, todo o `CMD` é substituído.
  * `ENTRYPOINT ["executável", "arg1", ...]`
      * Configura o contentor para operar como um **executável dedicado e fixo**.
      * Argumentos fornecidos em `docker run` são acrescentados como parâmetros ao executável.

-----

## `CMD` vs. `ENTRYPOINT` na Prática: Demonstração

Considere dois cenários representativos construídos sobre Alpine Linux:

**Cenário A: Apenas `CMD` (Comando flexível por omissão)**
```dockerfile
FROM alpine:3.20
CMD ["echo", "Mensagem padrao"]
```
```bash
$ docker run demo-cmd              # Imprime: "Mensagem padrao"
$ docker run demo-cmd uname -a     # Executa uname -a; substitui o comando CMD original
```

**Cenário B: `ENTRYPOINT` com `CMD` (Executável fixo + Argumento flexível)**
```dockerfile
FROM alpine:3.20
ENTRYPOINT ["echo", "Ambiente:"]
CMD ["Producao"]
```
```bash
$ docker run demo-ep               # Imprime: "Ambiente: Producao"
$ docker run demo-ep Homologacao   # Imprime: "Ambiente: Homologacao" (substitui o CMD)
```

-----

## O Contexto de Construção (*Build Context*) e o `.dockerignore`

Ao executar o comando de compilação da imagem:

```bash
$ docker build -t meu-servico:1.0 .
```

  * **Significado do Argumento de Caminho (`.`):**
      * Define a raiz do **Contexto de Construção** (*Build Context*).
      * O cliente Docker arquiva o conteúdo integral desse diretório e transmite-o para o Docker Daemon antes de iniciar o processamento das instruções.
  * **O Ficheiro `.dockerignore`:**
      * Apresenta semântica análoga ao `.gitignore`.
      * Impede que diretórios extensos ou artefactos sensíveis sejam transmitidos para o daemon:
        ```text
        .git
        node_modules
        .env
        *.log
        ```
      * Reduz a latência de transferência para o daemon e impede a inclusão acidental de credenciais, chaves criptográficas ou dependências locais nas camadas da imagem.

-----

## Exemplo Integrador: Construção e Inspeção de um Serviço

Considere um `Dockerfile` que compila um serviço de diagnóstico com utilizador sem privilégios administrativos:

```dockerfile
FROM alpine:3.20
WORKDIR /app
RUN adduser -D -u 1000 appuser
USER appuser
CMD ["sh", "-c", "while true; do echo \"[LOG] Servico ativo em $(date)\"; sleep 5; done"]
```

**Sequência de Validação na Interface de Comandos:**

```bash
# 1. Compilar a imagem atribuindo uma etiqueta formal
$ docker build -t logging-service:1.0 .

# 2. Iniciar o contentor em segundo plano
$ docker run -d --name logger logging-service:1.0

# 3. Inspecionar o ambiente de execução
$ docker exec -it logger whoami        # Confirma a execucao sob appuser (nao-root)
$ docker logs --tail 3 logger          # Consulta as mensagens de registo recentes
$ docker stop logger && docker rm logger
```

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte V: Orquestração Local com Docker Compose}}
\end{center}

-----

## Motivação e Âmbito do Docker Compose

Na arquitetura de sistemas reais, as soluções raramente operam com um único contentor isolado:

  * Uma aplicação web típica necessita de um servidor web (NGINX), um servidor de aplicação (Python/Node) e uma base de dados (PostgreSQL).
  * Iniciar esta arquitetura manualmente com comandos `docker run` exige:
      * Criar redes manualmente (`docker network create`).
      * Iniciar cada contentor individualmente com dezenas de parâmetros de portas, volumes e variáveis de ambiente.
      * Garantir a ordem correta de inicialização.
  * **Docker Compose:**
      * É uma ferramenta declarativa que define e gere aplicações multi-contentor através de um único ficheiro: `compose.yml`.
      * Toda a infraestrutura da aplicação é descrita em código (*Infrastructure as Code*) e partilhada no repositório Git do projeto.

-----

## Anatomia do Ficheiro `compose.yml`

Um ficheiro `compose.yml` organiza a topologia dos serviços da aplicação:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"                  # host:contentor
    volumes:
      - ./site:/usr/share/nginx/html
    environment:
      - TZ=Europe/Lisbon           # Fuso horário
    restart: unless-stopped        # Politica de recuperacao de falhas

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=segredo  # Variavel de inicializacao
    volumes:
      - dados_db:/var/lib/postgresql/data

volumes:
  dados_db:                        # Volume nomeado gerido pelo Docker
```

-----

## Comandos do Docker Compose

A orquestração do conjunto de serviços é gerida de forma unificada a partir do diretório onde reside o ficheiro `compose.yml`:

| Comando | Ação Executada |
| :--- | :--- |
| `docker compose up -d` | Descarrega imagens, cria redes, volumes e inicia todos os serviços em segundo plano. |
| `docker compose up --build -d` | Força a reconstrução de imagens locais (`build:`) antes de iniciar. |
| `docker compose ps` | Lista o estado e as portas de todos os serviços da aplicação. |
| `docker compose logs -f` | Acompanha a saída combinada de logs de todos os serviços em tempo real. |
| `docker compose logs -f <serviço>` | Filtra os logs de um único serviço (ex: `docker compose logs -f web`). |
| `docker compose stop` | Suspende a execução dos serviços sem eliminar contentores ou redes. |
| `docker compose down` | Pára e remove os contentores e redes virtuais criadas pelo Compose. |
| `docker compose down -v` | Encerra os serviços, removendo também os volumes nomeados persistentes. |

-----

## Padrão Compose 1: Empacotamento de Imagem Personalizada

```yaml
services:
  webserver:
    build: .             # Localização do Dockerfile no contexto local
    ports:
      - "8080:80"        # Mapeamento do porto 8080 do anfitrião
```

  * **Conceito:** O código-fonte é incorporado nas camadas da imagem durante o processo de compilação.
  * **Comportamento:** O contentor resultante constitui um artefacto autónomo e imutável, adequado para homologação e implantação.
  * **Atualização:** Alterações no código-fonte requerem a recompilação explícita da imagem (`docker compose up --build -d`).

-----

## Padrão Compose 2: Desenvolvimento Dinâmico com Volumes

```yaml
services:
  webserver:
    image: nginx:alpine                  # Imagem oficial de catálogo
    ports:
      - "8080:80"
    volumes:
      - ./my-website:/usr/share/nginx/html # Mapeamento dinâmico de diretório local
```

  * **Conceito:** Dispensa a criação de um `Dockerfile` dedicado, reutilizando diretamente a imagem oficial do NGINX.
  * **Mapeamento Direto:** O diretório `./my-website` do anfitrião é montado sobre a raiz documental do servidor web.
  * **Ciclo Rápido de Teste:** Alterações no código-fonte no anfitrião refletem-se de imediato no serviço web sem recriação do contentor.

-----

## Padrão Compose 3: Aplicação Multi-Serviço (Web + Base de Dados)

```yaml
services:
  web:
    build: .
    ports:
      - "8080:80"                        # Porta exposta ao anfitrião
    depends_on:
      - db                               # Arranca após a base de dados
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=segredo
    volumes:
      - dados_db:/var/lib/postgresql/data # Sem portas expostas ao anfitrião
volumes:
  dados_db:                              # Volume de persistência gerido
```

  * **Comunicação por Nome:** O serviço `web` acede a `postgres://db:5432` resolvido automaticamente pelo DNS interno.
  * **Isolamento de Segurança:** Apenas o `web` tem porta pública (`:8080`); a base de dados fica resguardada na rede interna.
  * **Persistência com Volume:** Os dados gravam-se em `dados_db`, sobrevivendo a paragens e reinícios (`docker compose down`).

-----


## Referências Técnicas Autorizadas

Documentação oficial e especificações para aprofundamento em engenharia de sistemas e computação em nuvem:

  * **Docker Documentation:**
      * [Guia Oficial e Referência de Arquitetura do Docker](https://docs.docker.com/)
      * [Referência do Dockerfile](https://docs.docker.com/reference/dockerfile/)
      * [Especificação do Compose File (Compose Specification)](https://docs.docker.com/compose/compose-file/)
  * **Open Container Initiative (OCI):**
      * [Especificações Oficiais OCI Image e Runtime](https://opencontainers.org/)
  * **Podman Documentation:**
      * [Guia de Utilização e Arquitetura do Podman](https://docs.podman.io/)
  * **Documentação do Kernel Linux:**
      * [Namespaces do Linux (`namespaces(7)`)](https://man7.org/linux/man-pages/man7/namespaces.7.html)
      * [Control Groups do Linux (`cgroups(7)`)](https://man7.org/linux/man-pages/man7/cgroups.7.html)
