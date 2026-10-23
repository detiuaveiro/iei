---
title: Contentores
subtitle: Introdução à Engenharia Informática
institute: Universidade de Aveiro
date: October 19, 2026
colorlinks: true
highlight-style: tango
geometry: a4paper,margin=2cm
mainfont: NotoSans
mainfontfallback:
  - "NotoColorEmoji:mode=harf"
  - "DejaVu Sans:"
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

**Enquadramento & Objetivos:**  
Na engenharia de software contemporânea, os contentores Docker são a tecnologia padrão para empacotar e gerir **aplicações de backend, APIs web, bases de dados e arquiteturas orientadas a microsserviços**, servindo de alicerce direto para a orquestração em escala na nuvem (como em clusters Kubernetes). Neste laboratório prático de **3 horas**, irá explorar o ciclo de vida de contentores, transformar código em serviços autónomos e orquestrar topologias multi-camada com Docker e Docker Compose:

* **Parte 1 — Instalação e Configuração do Docker:** Configuração do repositório oficial Docker e permissões de utilizador sem necessidade de `sudo`.
* **Parte 2 — Exercício 1: Fundamentos da CLI Docker & Construção Manual de Imagens:** Exploração do ciclo de vida de contentores (`run`, `ps`, `logs`, `exec`, `stop`, `rm`), registo local vs. remoto e compilação do primeiro `Dockerfile` com `docker build`.
* **Parte 3 — Exercício 2: "Hello, World" com Docker Compose:** Estrutura fundamental de um ficheiro `compose.yml` e automação do ciclo de vida de contentores.
* **Parte 4 — Exercício 3: Construção de Imagens Personalizadas com Compose:** Criação de um `Dockerfile` integrado com Compose para empacotar uma aplicação web estática em NGINX.
* **Parte 5 — Exercício 4: Desenvolvimento Dinâmico com Volumes:** Utilização de volumes (*bind mounts*) para desenvolvimento ágil com atualização imediata de código no anfitrião.
* **Parte 6 — Exercício 5: Arquitetura Multi-Serviço com Cache Varnish & NGINX:** Composição de serviços interdependentes, rede privada interna com resolução por DNS e proxy reverso de alto desempenho.
* **Parte 7 — Exercício 6: Implementação de uma Aplicação de Produção:** Implementação de uma aplicação complexa (ex.: Jellyfin) com variáveis de ambiente (`PUID`, `PGID`, `TZ`), volumes de persistência e mapeamento de portas.

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Antes de iniciar os exercícios, crie e aceda à pasta de trabalho dedicada para esta sessão:

```bash
$ mkdir -p ~/IEI/aula04
$ cd ~/IEI/aula04
```

Todos os ficheiros criados durante a aula (ficheiros `compose.yml`, `Dockerfile`, páginas web e configurações) deverão ser organizados em subpastas dentro deste diretório de trabalho.

> **Nota sobre caminhos de ficheiros:**
> Os comandos deste guião assumem que o terminal está posicionado no diretório de trabalho `~/IEI/aula04`. Cada exercício deve ser desenvolvido na respetiva subpasta (p. ex., `ex1-cli`, `ex2-helloworld`, `ex3-build`, etc.).

-----

## Parte 1: Instalação e Configuração do Docker

Se estiver a usar um anfitrião Linux (Debian ou Ubuntu), siga estes passos no seu terminal para instalar a versão mais recente do Docker Engine e do plugin Docker Compose, de acordo com as [instruções oficiais](https://docs.docker.com/engine/install/debian/). *(Em Windows ou macOS, instale o [Docker Desktop](https://docs.docker.com/desktop/)).*

1.  **Configurar o repositório `apt` do Docker:**
    ```bash
    # Remover pacotes não oficiais do docker
    sudo apt remove docker.io docker-doc \
    docker-compose podman-docker containerd runc

    # Atualizar o índice de pacotes e instalar pré-requisitos
    sudo apt update
    sudo apt install ca-certificates curl

    # Adicionar a chave GPG oficial do Docker
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg \
    -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Adicionar o repositório às fontes do Apt:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
      https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    ```
2.  **Instalar os pacotes Docker:**
    ```bash
    sudo apt install docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
    ```
3.  **Gerir o Docker como um utilizador não-root (Recomendado):**
    Para executar comandos `docker` sem `sudo`, adicione o seu utilizador ao grupo `docker`.
    ```bash
    sudo usermod -aG docker $USER
    ```
    **Importante:** Tem de fazer logout e login novamente para que esta alteração tenha efeito.

-----

## Exercício 1: Fundamentos da CLI Docker e Construção Manual de Imagens

**Objetivo:** Praticar os comandos essenciais da CLI Docker (`run`, `ps`, `logs`, `exec`, `stop`, `rm`, `build`), compreender a distinção entre registo local e remoto (Docker Hub), e criar manualmente a primeira imagem a partir de um `Dockerfile`.

1.  **Explorar o Registo Local e Descarregar Imagens (`docker images` e `docker pull`):**
    * Crie uma pasta para este exercício e entre nela:
      ```bash
      $ mkdir -p ex1-cli && cd ex1-cli
      ```
    * Inspecione as imagens presentes no armazenamento local da sua máquina:
      ```bash
      $ docker images
      ```
      *(Se a instalação for recente, a lista estará vazia).*
    * Descarregue a imagem oficial da distribuição minimalista **Alpine Linux** diretamente do Docker Hub (registo remoto oficial):
      ```bash
      $ docker pull alpine:3.20
      ```
    * Volte a listar as imagens locais (`docker images`) e confirme que a imagem `alpine:3.20` está agora em disco (repare no tamanho ultraleve de apenas ~8 MB!).

2.  **Executar um Contentor Interativo e Compreender o Ciclo de Vida (`run -it`, `ps`, `ps -a` e `rm`):**
    * Crie e inicie um contentor interativo com uma sessão de terminal (`sh`):
      ```bash
      $ docker run -it --name meu-terminal alpine:3.20 sh
      ```
    * Repare que o indicador de linha de comandos mudou para `/ #`. Está agora a executar comandos no espaço de processos e sistema de ficheiros isolado do contentor! Experimente:
      ```sh
      / # cat /etc/os-release   # Inspecionar a distribuição do contentor
      / # hostname              # Ver o identificador único atribuído ao contentor
      / # exit                  # Terminar a sessão e sair do contentor
      ```
    * De volta ao terminal da máquina anfitriã, verifique quais os contentores em execução:
      ```bash
      $ docker ps
      ```
      *(O contentor não surge listado porque o seu processo principal `sh` foi concluído).*
    * Liste **todos** os contentores (incluindo os terminados/parados):
      ```bash
      $ docker ps -a
      ```
      Constatará que o contentor `meu-terminal` ainda existe em disco no estado `Exited (0)`.
    * Remova definitivamente o contentor e a sua camada temporária de escrita:
      ```bash
      $ docker rm meu-terminal
      ```

3.  **Serviço em Segundo Plano, Redirecionamento de Portos e Logs (`run -d -p`, `logs` e `exec`):**
    * Inicie um servidor web NGINX em segundo plano (*detached*, flag `-d`) mapeando o porto 8080 do anfitrião para o porto 80 do contentor (flag `-p`):
      ```bash
      $ docker run -d --name meu-servidor -p 8080:80 nginx:alpine
      ```
      *(Como a imagem `nginx:alpine` ainda não existia localmente, o Docker fez o `pull` automático antes de iniciar).*
    * Confirme que o contentor está em execução com o porto mapeado:
      ```bash
      $ docker ps
      ```
    * Abra o seu navegador web em `http://localhost:8080`. Deverá visualizar a página de boas-vindas *"Welcome to nginx!"*.
    * Regresse ao terminal e visualize os registos de acesso HTTP gerados pelo navegador:
      ```bash
      $ docker logs meu-servidor
      ```
    * Abra uma sessão de terminal dentro do contentor que está vivo para alterar a página servida em tempo real:
      ```bash
      $ docker exec -it meu-servidor sh
      / # echo "<h1>Ola do container</h1>" > /usr/share/nginx/html/index.html
      / # exit
      ```
    * Atualize o navegador em `http://localhost:8080` e comprove a alteração em tempo real.
    * Pare o contentor e remova-o:
      ```bash
      $ docker stop meu-servidor
      $ docker rm meu-servidor
      ```

4.  **Criar o Primeiro `Dockerfile` "à Mão" e Compilar (`docker build`):**
    * Dentro da pasta `ex1-cli`, crie um ficheiro `index.html` com uma mensagem personalizada:
      ```html
      <!DOCTYPE html>
      <html>
      <body>
          <h1>Minha primeira imagem construida com Dockerfile!</h1>
      </body>
      </html>
      ```
    * Crie agora o ficheiro de receita declarativa chamado `Dockerfile` (sem extensão):
      ```dockerfile
      FROM nginx:alpine
      COPY index.html /usr/share/nginx/html/index.html
      ```
    * Compile a imagem no contexto do diretório atual (`.`):
      ```bash
      $ docker build -t meu-site-manual:1.0 .
      ```
    * Inspecione o registo local com `docker images`. A sua imagem `meu-site-manual:1.0` surge agora como uma imagem local pronta a distribuir!
    * Inicie um contentor a partir da sua nova imagem personalizada:
      ```bash
      $ docker run -d --name site-manual -p 8080:80 meu-site-manual:1.0
      ```
    * Aceda a `http://localhost:8080` no navegador e verifique o resultado.
    * Conclua limpando o contentor:
      ```bash
      $ docker stop site-manual && docker rm site-manual
      ```
    * Volte ao diretório raiz da aula para prosseguir para o Docker Compose:
      ```bash
      $ cd ~/IEI/aula04
      ```

-----

## Exercício 2: "Hello, World" com Docker Compose

**Objetivo:** Compreender a estrutura básica de um ficheiro `compose.yml` e executar uma imagem pré-construída.

1.  Crie uma nova pasta para este exercício (p. ex., `ex2-helloworld`).
2.  Dentro da pasta, crie um novo ficheiro chamado `compose.yml` com o seguinte conteúdo:
    ```yaml
    services:
      hello:
        image: hello-world
    ```
3.  Abra o seu terminal nesta pasta e execute a aplicação.
    ```bash
    $ docker compose up
    ```
4.  Observe o resultado. O contentor `hello-world` irá arrancar, imprimir a sua mensagem e depois terminar.
5.  Limpe o contentor criado pela execução.
    ```bash
    $ docker compose down
    ```

-----

## Exercício 3: Construir uma Imagem de Servidor Web Personalizada

**Objetivo:** Usar um `Dockerfile` com o Docker Compose para criar uma imagem de aplicação autónoma.

1.  Crie uma nova pasta (`ex3-build`) e uma subpasta dentro dela chamada `my-website`.
2.  Dentro de `my-website`, crie um ficheiro chamado `index.html`:
    ```html
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Esta página foi construída dentro da imagem Docker!</h1>
    </body>
    </html>
    ```
3.  Na raiz da pasta `ex3-build`, crie um `Dockerfile`:
    ```dockerfile
    FROM nginx:alpine
    COPY ./my-website /usr/share/nginx/html
    ```
4.  Finalmente, crie o seu ficheiro `compose.yml`:
    ```yaml
    services:
      webserver:
        build: .
        ports:
          - "8080:80"
    ```
5.  Construa e inicie o serviço. A flag `-d` executa-o em segundo plano.
    ```bash
    $ docker compose up --build -d
    ```
6.  Abra o seu navegador e navegue para `http://localhost:8080`. Deverá ver a sua página web personalizada.

-----

## Exercício 4: Desenvolvimento em Tempo Real com Volumes

**Objetivo:** Compreender como os volumes lhe permitem alterar o conteúdo do seu site sem reconstruir a imagem.

1.  Crie uma nova pasta (`ex4-volumes`) com a mesma estrutura `my-website/index.html` do exercício anterior.
2.  Crie um ficheiro `compose.yml`. Desta vez, vamos usar a imagem padrão `nginx:alpine` e montar a nossa pasta local como um volume. **Não é necessário `Dockerfile`.**
    ```yaml
    services:
      webserver:
        image: nginx:alpine
        ports:
          - "8080:80"
        volumes:
          - ./my-website:/usr/share/nginx/html
    ```
3.  Inicie o serviço: `docker compose up -d`.
4.  Abra o seu navegador em `http://localhost:8080` para confirmar que está a funcionar.
5.  **Atualização em Tempo Real:** Enquanto o contentor está a correr, **edite o ficheiro `index.html`** na sua máquina anfitriã. Altere o cabeçalho para `<h1>Atualização em tempo real com um Volume!</h1>`.
6.  Guarde o ficheiro e **atualize o seu navegador**. A alteração aparece instantaneamente\!

-----

## Exercício 5: Conteúdo em Cache com Varnish & NGINX

**Objetivo:** Construir uma aplicação web de duas camadas com uma cache Varnish a servir uma página web rica a partir de um backend NGINX.

1.  **Criar a Estrutura de Ficheiros:**
      * Crie uma nova pasta (p. ex., `ex5-varnish-cache`).
      * Dentro dela, crie duas subpastas: `varnish` e `my-dynamic-website`.
2.  **Criar o Conteúdo Web:**
      * Encontre um GIF animado divertido online e guarde-o dentro de `my-dynamic-website` como `animation.gif`.
      * Dentro de `my-dynamic-website`, crie um ficheiro `index.html` para exibir o GIF:
        ```html
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <title>Teste de Cache Varnish</title>
            <style> body { font-family: sans-serif; text-align: center; } </style>
        </head>
        <body>
            <h1>Esta página está a ser servida pela cache do Varnish!</h1>
            <img src="animation.gif" alt="Animação em cache">
        </body>
        </html>
        ```
3.  **Criar a Configuração do Varnish:**
      * Dentro da pasta `varnish`, crie um ficheiro chamado `default.vcl`. Isto diz ao Varnish onde encontrar o servidor NGINX.
        ```vcl
        vcl 4.1;
        backend default {
            .host = "nginx";
            .port = "80";
        }
        ```
4.  **Criar o Ficheiro Compose:**
      * Na raiz da sua pasta `ex5-varnish-cache`, crie o `compose.yml`:
        ```yaml
        services:
          cache:
            image: varnish:stable
            volumes:
              - ./varnish:/etc/varnish
            ports:
              - "8080:80"
            depends_on:
              - nginx

          nginx:
            image: nginx:alpine
            volumes:
              - ./my-dynamic-website:/usr/share/nginx/html
        ```
5.  **Executar e Verificar:**
      * Inicie os serviços: `docker compose up -d`.
      * Abra o seu navegador em `http://localhost:8080`. Deverá ver a sua página web com o GIF. O ponto-chave aqui é que foi o **Varnish** que lhe serviu a página, não o NGINX diretamente.
      * **Veja a cache em ação:** Verifique os logs do NGINX para o primeiro pedido.
        ```bash
        $ docker compose logs nginx
        ```
      * Agora, atualize a página do seu navegador várias vezes. Verifique os logs do `nginx` novamente. Deverá ver **nenhum novo registo de log**, porque o Varnish está a servir o conteúdo da sua cache sem contactar o backend NGINX.

-----

## Exercício 6: Implementar uma Aplicação do Mundo Real

**Objetivo:** Aprender a ler documentação oficial e a implementar um serviço complexo auto-hospedado à sua escolha.

1.  **Escolha um Serviço:** Crie uma nova pasta de trabalho (p. ex., `ex6-jellyfin` ou `ex6-realworld`). Vá a [LinuxServer.io](https://www.linuxserver.io/) e navegue pela lista de imagens populares. Escolha uma que lhe interesse, por exemplo:

      * **Jellyfin:** Um servidor de multimédia para os seus filmes e música.
      * **Nextcloud:** Uma nuvem pessoal para ficheiros, contactos e calendários.
      * **Home Assistant:** Uma plataforma de automação residencial de código aberto.

2.  **Leia a Documentação:** Na página da imagem escolhida, encontre a secção "Docker Compose". Leia-a com atenção, prestando especial atenção aos **volumes** e **variáveis de ambiente** necessários.

      * **Volumes (`- ./config:/config`):** É aqui que a configuração da aplicação será armazenada na sua máquina anfitriã.
      * **Variáveis de Ambiente (`PUID`, `PGID`, `TZ`):** Estas são críticas. `TZ` define o seu fuso horário (p. ex., `Europe/Lisbon`). `PUID` e `PGID` garantem que os ficheiros criados pelo contentor têm a propriedade correta. Em Linux/macOS, encontre o seu ID executando o comando `id` no seu terminal. Um valor comum é `1000`.

3.  **Crie o seu `compose.yml`:** Com base na documentação, crie o ficheiro. Aqui está um exemplo para o **Jellyfin**:

    ```yaml
    services:
      jellyfin:
        image: lscr.io/linuxserver/jellyfin:latest
        container_name: jellyfin
        environment:
          - PUID=1000
          - PGID=1000
          - TZ=Europe/Lisbon
        volumes:
          - ./config:/config
          - ./series:/data/tvshows
          - ./filmes:/data/movies
        ports:
          - "8096:8096"
        restart: unless-stopped
    ```

4.  **Prepare e Implemente:**

      * Crie as pastas locais que definiu nos seus volumes (p. ex., `mkdir config series filmes`).
      * Execute a aplicação: `docker compose up -d`.

5.  **Explore:** Verifique a documentação para o número da porta padrão. Para o Jellyfin, é `8096`. Abra o seu navegador em `http://localhost:8096` e siga o assistente de configuração para o seu novo serviço\!

