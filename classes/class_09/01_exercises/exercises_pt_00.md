---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Páginas Web & Publicação"
institute: Universidade de Aveiro
date: 23 de Novembro de 2026
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
 - \AtBeginEnvironment{longtable}{\footnotesize}
 - \AtBeginEnvironment{cslreferences}{\tiny}
 - \AtBeginEnvironment{Shaded}{\small}
 - \AtBeginEnvironment{verbatim}{\small}
 - \setmonofont[Contextuals={Alternate}]{FiraCodeNerdFontMono-Retina}
---

# Guião Prático de Laboratório

**Enquadramento Pedagógico & Objetivos:**
Nesta sessão laboratorial constrói-se e publica-se uma página web estática de raiz, aplicando os fundamentos de **HTML5 semântico**, **CSS3 (Box Model)** e **publicação em contentores Docker com Nginx**. O guião está estruturado em três blocos progressivos e um desafio opcional:

* **Bloco 1 — Estruturação Semântica em HTML5:** Criação da estrutura base de um documento HTML5, inspeção da árvore **DOM**, utilização de contentores semânticos (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<footer>`), listas, hiperligações (`mailto:`) e elementos multimédia nativos (`<figure>`/`<img>` e `<video>`).
* **Bloco 2 — Estilização e Layout com CSS3:** Separação de responsabilidades através de uma folha de estilos externa (`css/style.css`), aplicação de seletores, regras de tipografia/cor e formatação de cartões com o **CSS Box Model** (`box-sizing: border-box`, `padding`, `border` e `margin`).
* **Bloco 3 — Publicação com Nginx, Docker Compose e Inspeção HTTP:** Separação entre código-fonte (`src/`) e configuração de infraestrutura, execução do servidor web `nginx:alpine` com volume *read-only* (`:ro`) e análise do ciclo de pedidos HTTP via `curl` e *DevTools*.
* **Desafio Opcional — Arquitetura de *Reverse Proxy* com Nginx:** Encaminhamento de pedidos numa única porta pública (`8080`) entre o site estático (`/`) e um serviço interno de API (`/api/`) isolados numa rede privada Docker.

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Crie o diretório dedicado ao projeto desta aula e verifique se o Docker Compose se encontra operacional:

```bash
mkdir -p ~/IEI/aula09/o-meu-portfolio
cd ~/IEI/aula09/o-meu-portfolio
docker compose version
```

-----

## Bloco 1: Estruturação Semântica em HTML5

### Passo 1.1: Documento HTML5 Base e Árvore DOM

Crie um ficheiro chamado `index.html` na raiz do diretório `o-meu-portfolio` com a estrutura base de um documento HTML5 válido:

```html
<!DOCTYPE html>
<html lang="pt">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1.0">
  <title>O Meu Portfólio</title>
</head>
<body>
  <h1>Olá, Mundo!</h1>
  <p>Documento HTML5 inicial servido localmente.</p>
</body>
</html>
```

* **`<!DOCTYPE html>`:** Instrui o navegador a interpretar o documento no modo standard HTML5.
* **`<head>`:** Contém metadados não renderizados na área principal da página (`UTF-8` para suporte correto de acentuação, `viewport` para adaptação a ecrãs móveis e `<title>` para o separador do navegador).
* **`<body>`:** Contém todos os elementos visíveis renderizados na janela.

**Verificação:**

1. Abra o ficheiro `index.html` no navegador (através do explorador de ficheiros ou arrastando-o para uma janela do navegador).
2. Observe o endereço apresentado na barra de URL — trata-se de um caminho local do sistema de ficheiros (`file:///.../o-meu-portfolio/index.html`) — e confirme que o separador apresenta o título *"O Meu Portfólio"*.
3. Abra as **Ferramentas de Programador (*DevTools*)** (`F12` ou *Botão direito $\rightarrow$ Inspecionar*) e observe no separador **Elements / Inspector** a árvore **DOM** gerada pelo navegador.

### Passo 1.2: Contentores Semânticos, Navegação e Hiperligações

Substitua o bloco `<body>` do ficheiro `index.html` por uma estrutura semântica composta por cabeçalho (`<header>`), navegação (`<nav>`), conteúdo principal (`<main>`), artigo autónomo (`<article>`) e rodapé (`<footer>`) com uma hiperligação `mailto:`:

```html
<body>
  <header>
    <h1>O Meu Portfólio</h1>
    <nav>
      <ul>
        <li><a href="index.html">Início</a></li>
        <li><a href="#sobre">Sobre Mim</a></li>
        <li><a href="#media">Multimédia</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <h2>Bem-vindo</h2>
    <p>
      Página desenvolvida de raiz em <strong>HTML5</strong>
      e <em>CSS3</em> no âmbito de IEI.
    </p>

    <article id="sobre">
      <h3>Sobre Mim</h3>
      <p>
        Sou estudante do 1.º ano de Engenharia Informática
        na Universidade de Aveiro.
      </p>
      <p>
        As minhas áreas de interesse incluem [Interesse 1]
        e [Interesse 2].
      </p>
    </article>
  </main>

  <footer>
    <p>
      Contacto: <a href="mailto:seu.email@ua.pt">seu.email@ua.pt</a>
    </p>
    <p>&copy; 2026 O Seu Nome</p>
  </footer>
</body>
```

**Tarefas:**

1. Substitua os marcadores `[Interesse 1]`, `[Interesse 2]`, `seu.email@ua.pt` e `O Seu Nome` pelos seus dados.
2. Guarde o ficheiro, atualize o navegador e observe que, embora a estrutura semântica esteja definida, **todos os blocos aparecem empilhados verticalmente sem formatação** (comportamento padrão sem CSS).
3. Teste a hiperligação `mailto:` no rodapé e verifique a navegação interna através das âncoras `#sobre` e `#media`.

### Passo 1.3: Elementos Multimédia Nativos (`<figure>`/`<img>` e `<video>`)

1. Crie os diretórios para armazenar os recursos multimédia:
   ```bash
   mkdir -p images videos
   ```
2. Descarregue uma imagem de exemplo em formato JPEG (ou copie uma fotografia própria para `images/profile.jpg`) e um vídeo curto de teste em formato MP4:
   ```bash
   curl -L "https://placehold.co/400x400/004a8c/ffffff/jpg?text=IEI" \
     -o images/profile.jpg
   curl -L "https://www.w3schools.com/html/mov_bbb.mp4" \
     -o videos/my-clip.mp4
   ```
3. No ficheiro `index.html`, incorpore a imagem com legenda semântica (`<figure>` e `<figcaption>`) no interior do `<article id="sobre">` e adicione uma nova `<section id="media">` no interior do `<main>` (mantendo o `<article>` existente):

   ```html
   <main>
     <h2>Bem-vindo</h2>
     <p>
       Página desenvolvida de raiz em <strong>HTML5</strong>
       e <em>CSS3</em> no âmbito de IEI.
     </p>

     <article id="sobre">
       <h3>Sobre Mim</h3>
       <figure>
         <img src="images/profile.jpg"
              alt="Fotografia de perfil do autor" width="150">
         <figcaption>Engenharia Informática — UA</figcaption>
       </figure>
       <p>
         Sou estudante do 1.º ano de Engenharia Informática
         na Universidade de Aveiro.
       </p>
       <p>
         As minhas áreas de interesse incluem [Interesse 1]
         e [Interesse 2].
       </p>
     </article>

     <section id="media">
       <h3>Demonstração de Vídeo HTML5</h3>
       <video controls width="100%">
         <source src="videos/my-clip.mp4" type="video/mp4">
         O seu navegador não suporta vídeo HTML5.
       </video>
     </section>
   </main>
   ```

4. **Teste de acessibilidade (`alt`):** Altere temporariamente o atributo `src` da imagem para um caminho inexistente (ex.: `images/inexistente.jpg`), atualize o navegador e confirme a exibição do texto alternativo definido em `alt`. Reponha de seguida o caminho correto (`images/profile.jpg`).

-----

## Bloco 2: Estilização e Layout com CSS3

### Passo 2.1: Folha de Estilos Externa, Tipografia e Cores

Para garantir a **separação de responsabilidades** entre conteúdo (HTML) e apresentação (CSS), crie um diretório `css` e o ficheiro `css/style.css`:

```bash
mkdir -p css
```

1. Adicione a ligação à folha de estilos externa na secção `<head>` do ficheiro `index.html`:
   ```html
   <head>
     <meta charset="UTF-8">
     <meta name="viewport"
           content="width=device-width, initial-scale=1.0">
     <title>O Meu Portfólio</title>
     <link rel="stylesheet" href="css/style.css">
   </head>
   ```
2. Defina as regras base de tipografia, cores e seletores no ficheiro `css/style.css`:
   ```css
   /* Inclui padding e border no cálculo de width/max-width */
   * {
       box-sizing: border-box;
   }

   body {
       background-color: #f0f0f0;
       font-family: Arial, Helvetica, sans-serif;
       line-height: 1.6;
       color: #333;
       margin: 0;
       padding: 16px;
   }

   header h1 {
       color: #004a8c;
       margin-top: 0;
   }

   a {
       color: #005a9c;
       text-decoration: none;
   }

   a:hover {
       text-decoration: underline;
   }
   ```
3. Guarde ambos os ficheiros e atualize o navegador para confirmar a aplicação da folha de estilos externa.

### Passo 2.2: Modelo de Caixa (*CSS Box Model*) e Layout em Cartões

Adicione ao final de `css/style.css` as regras de espaçamento, molduras e disposição em cartões centrados:

```css
/* Layout em cartões centrados (CSS Box Model) */
header, main, footer {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.08);
}

/* Menu de navegação horizontal */
nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: 16px;
}

nav a {
    font-weight: bold;
}

/* Evita que o elemento flutuante extravase o contentor <article> */
article {
    display: flow-root;
}

article figure {
    float: left;
    margin: 0 20px 10px 0;
    text-align: center;
}

article img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border-radius: 50%;
    border: 2px solid #004a8c;
}

figcaption {
    font-size: 0.78em;
    color: #555;
    margin-top: 4px;
}

footer {
    text-align: center;
    font-size: 0.9em;
    color: #666;
}
```

**Verificação:** Atualize o navegador e observe o resultado do **Box Model** (`max-width: 800px` + `margin: 20px auto`), o menu horizontal e o enquadramento circular da imagem de perfil sem sobreposição com a secção de vídeo.

-----

## Bloco 3: Publicação com Nginx, Docker Compose e Inspeção HTTP

### Passo 3.1: Reorganização para Publicação (`src/`)

Num fluxo de trabalho estruturado, separa-se o **código-fonte público** da página da **configuração de publicação (*deployment*)**. Mova os ficheiros do site para um subdiretório `src/`:

```bash
mkdir -p src
mv index.html css images videos src/
```

Verifique que a estrutura de diretórios corresponde ao seguinte esquema:

```text
o-meu-portfolio/
└── src/
    ├── index.html
    ├── css/
    │   └── style.css
    ├── images/
    │   └── profile.jpg
    └── videos/
        └── my-clip.mp4
```

> **Observação:** Caso atualize o separador anterior do navegador (`file:///.../o-meu-portfolio/index.html`), o carregamento falhará porque o ficheiro foi movido. No passo seguinte passaremos a servir o site através do protocolo HTTP.

### Passo 3.2: Configuração do Servidor Web Nginx em Docker Compose

Na raiz de `o-meu-portfolio` (ao lado de `src/`), crie o ficheiro `docker-compose.yml`:

```yaml
services:
  webserver:
    image: nginx:alpine
    container_name: o_meu_portfolio_site
    ports:
      - "8080:80"
    volumes:
      - ./src:/usr/share/nginx/html:ro
```

* **`image: nginx:alpine`:** Imagem oficial e reduzida do servidor web Nginx baseada em Alpine Linux.
* **`ports: - "8080:80"`:** Encaminha o tráfego da porta `8080` da máquina anfitriã (*host*) para a porta `80` do contentor.
* **`volumes: - ./src:/usr/share/nginx/html:ro`:** Monta o diretório local `./src` no diretório raiz servido pelo Nginx em modo apenas de leitura (*read-only*), prevenindo alterações não autorizadas a partir do contentor.

Inicie o serviço em segundo plano (*detached mode*) e aceda ao endereço no navegador:

```bash
docker compose up -d
```

Aceda a **`http://localhost:8080`** no navegador e confirme que o site completo (HTML, CSS, imagem e vídeo) é servido corretamente.

### Passo 3.3: Inspeção do Ciclo de Pedidos HTTP (`curl` e *DevTools*)

1. **Inspeção de cabeçalhos via terminal:** Execute `curl -I` para inspecionar a resposta HTTP devolvida pelo servidor Nginx:
   ```bash
   curl -I http://localhost:8080
   curl -I http://localhost:8080/css/style.css
   ```
   Observe o código de estado (`HTTP/1.1 200 OK`), o cabeçalho `Server: nginx/...` e a diferença no cabeçalho `Content-Type` (`text/html` vs. `text/css`).

2. **Inspeção no navegador (*DevTools*):**
   * Em `http://localhost:8080`, abra as **DevTools** (`F12`) $\rightarrow$ separador **Network** (*Rede*).
   * Ative a opção **Disable cache** (*Desativar cache*) e recarregue a página (`Ctrl+R` / `Cmd+R`).
   * Confirme que o carregamento de uma única página origina **múltiplos pedidos HTTP** individuais (`/` ou `index.html`, `style.css`, `profile.jpg` e `my-clip.mp4`).

3. Quando terminar este bloco, pare e remova o contentor:
   ```bash
   docker compose down
   ```

-----

## Desafio Opcional: Arquitetura de *Reverse Proxy* com Nginx

**Objetivo:** Reproduzir a arquitetura de **Reverse Proxy** abordada na aula teórica, expondo **dois serviços internos isolados** através de uma única porta pública (`8080`):
* Pedidos para **`/`** $\rightarrow$ encaminhados para o contentor **`site`** (o seu portfólio HTML/CSS);
* Pedidos para **`/api/`** $\rightarrow$ encaminhados para o contentor **`api`** (um serviço interno que devolve dados JSON, simulando a API REST da Aula 08).

1. Na raiz de `o-meu-portfolio`, crie um ficheiro de configuração mínimo `api.conf` para o serviço interno `api`:
   ```nginx
   events {}
   http {
     server {
       listen 8000;
       location / {
         default_type application/json;
         return 200 '{"servico":"api-iei","estado":"operacional"}';
       }
     }
   }
   ```

2. Crie o ficheiro `nginx.conf` com as regras de encaminhamento do **Reverse Proxy**:
   ```nginx
   events {}
   http {
     server {
       listen 80;

       location /api/ {
         proxy_pass http://api:8000/;
       }

       location / {
         proxy_pass http://site:80;
       }
     }
   }
   ```

3. Crie um ficheiro `docker-compose.proxy.yml` onde **apenas o serviço `proxy` expõe portas ao exterior**:
   ```yaml
   services:
     proxy:
       image: nginx:alpine
       ports:
         - "8080:80"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf:ro
       depends_on:
         - site
         - api

     site:
       image: nginx:alpine
       volumes:
         - ./src:/usr/share/nginx/html:ro
       # Sem 'ports': acessível apenas na rede privada Docker

     api:
       image: nginx:alpine
       volumes:
         - ./api.conf:/etc/nginx/nginx.conf:ro
       # Substituível pela sua imagem FastAPI da Aula 08
   ```

4. Inicie a arquitetura completa e valide o encaminhamento em ambos os caminhos:
   ```bash
   docker compose -f docker-compose.proxy.yml up -d
   curl -i http://localhost:8080/api/
   ```
   * Aceda a **`http://localhost:8080/`** no navegador (servido pelo contentor `site`).
   * Aceda a **`http://localhost:8080/api/`** (servido pelo contentor `api`, devolvendo JSON).
   * Verifique com `docker ps` que apenas o contentor `proxy` possui mapeamento de porta para o *host* (`0.0.0.0:8080->80/tcp`), mantendo `site` e `api` isolados na rede interna.

5. Para encerrar os serviços do desafio:
   ```bash
   docker compose -f docker-compose.proxy.yml down
   ```

-----

## Síntese dos Resultados Obtidos

Ao concluir este guião prático, executou o fluxo completo de desenvolvimento e publicação de páginas web estáticas:

* Construção de um documento **HTML5 semântico** válido com navegação, hiperligações (`mailto:`) e multimédia nativa (`<figure>`/`<img>` e `<video>`).
* Aplicação de **CSS3** externo com separação de responsabilidades, seletores e controlo de layout através do **CSS Box Model** (`box-sizing: border-box`).
* Empacotamento e publicação do site com **Nginx + Docker Compose** em modo *read-only* (`:ro`), validação dos pedidos HTTP com `curl` e *DevTools*, e (opcionalmente) configuração de encaminhamento via **Reverse Proxy**.
