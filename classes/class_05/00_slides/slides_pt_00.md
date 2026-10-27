---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Contentores de Aplicação & Desktop Sandboxing em Linux"
institute: Universidade de Aveiro
date: October 26, 2026
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

  * **Parte I — Dependências e Requisitos de Confinamento:**
      * Docker na infraestrutura vs. limitações no desktop, *dependency hell*, modelos alternativos (Windows, macOS, venv) e requisitos de confinamento.
  * **Parte II — Paradigmas de Contentorização Desktop:**
      * Análise conceptual e comparativa de **AppImage**, **Snap** e **Flatpak** (arquitetura, segurança e distribuição).
  * **Parte III — Empacotamento com AppImage e Flatpak:**
      * Construção prática de artefactos: hierarquia `AppDir`, manifestos YAML, integração gráfica (Pygame) e `flatpak-builder`.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Dependências e Requisitos de Confinamento}}
\end{center}

-----

## Docker e OCI na Infraestrutura vs. Limitações no Desktop

O ecossistema Docker e as normas OCI foram concebidos para serviços de infraestrutura:

  * **Contentores de Infraestrutura (Docker & OCI):**
      * **Serviços *Headless*:** Otimizados para processos de servidor (APIs, bases de dados) sem interface gráfica.
      * **Rede e Orquestração:** Redes virtuais privadas (*bridge*), mapeamento de portas e orquestração em cluster.
      * **Privilégios:** Gestão via daemon centralizado com privilégios de administração (`dockerd` em `root`).

  * **Limitações para Aplicações Desktop:**
      * **Gráficos e Áudio:** Sem suporte nativo para Wayland/X11, aceleração 3D (`/dev/dri`) ou PipeWire.
      * **Integração no Sistema:** Sem atalhos em menus/doca, notificações nativas ou associação a ficheiros.
      * **Segurança e Ficheiros:** Sem delegação dinâmica de acessos; *bind mounts* expõem pastas sem mediação.

-----

## Gestão de Dependências Dinâmicas (*Dependency Hell*)

A distribuição de aplicações desktop enfrenta o desafio das dependências partilhadas:

  * **Arquitetura Tradicional em Linux:**
      * Partilha global de bibliotecas dinâmicas (`.so` em `/usr/lib`).
  * **Conflito de Versões:**
      * Aplicação A requer `libXYZ v1.0` vs. Aplicação B requer `libXYZ v2.0`.
  * **Limitação dos Gestores de Pacotes (`apt`, `dnf`):**
      * Admitem apenas uma versão global de cada biblioteca no sistema.
      * Instalar ou atualizar a Aplicação B quebra a Aplicação A (*breaking changes*).
  * **Fragmentação do Ecossistema:**
      * Exige compilação e empacotamento específico por distribuição (Debian, Fedora, Arch).

-----

## O Problema das Dependências Partilhadas

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{dependency_hell.png}
\end{center}

-----

## Outros Sistemas Operativos: O Modelo de Bundling (Windows e macOS)

Estratégias de empacotamento autónomo para contornar conflitos globais de bibliotecas:

  * **Microsoft Windows (Carregamento Local de DLLs):**
      * Cada aplicação inclui as suas bibliotecas (`.dll`) na sua própria pasta (`Program Files`).
      * **Vantagem:** Evita colisões no sistema global de ficheiros.
      * **Compromisso:** Elevada duplicação em disco; ausência de sandbox por omissão.
  * **Apple macOS (Pacotes Autocontidos .app):**
      * Estrutura de diretório unificada que agrupa binário executável, recursos e bibliotecas (`.dylib`).
      * **Vantagem:** Modelo desacoplado e fácil de transportar pelo utilizador.
      * **Compromisso:** Duplicação de ficheiros; assenta numa plataforma de SO uniforme e proprietária.

-----

## Isolamento ao Nível da Linguagem: O Caso do Python (venv)

Porque não resolver a distribuição desktop apenas com ambientes virtuais de linguagem?

  * **O que o `venv` resolve:**
      * Cria uma árvore local (`.venv`) isolando pacotes e módulos Python (`site-packages`).
      * Garante reprodutibilidade de dependências Python via `requirements.txt`.
  * **Porque não é suficiente para Aplicações Desktop:**
      * **Sem Confinamento:** O código corre com todas as permissões do utilizador (sem sandbox).
      * **Dependência do Sistema Anfitrião:** Exige Python pré-instalado e **não inclui bibliotecas C do sistema** (ex: SDL2, libGL e áudio para jogos em Pygame).
      * **Sem Integração Desktop:** Não cria entradas no menu, não gere permissões de janelas nem associa tipos MIME.

-----

## Requisitos de Isolamento e Confinamento (*Sandboxing*)

Perante as limitações dos modelos tradicionais, o Linux Desktop exige três garantias:

  * **Portabilidade Determinística (*Run Anywhere*):**
      * Execução idêntica e reprodutível em qualquer distribuição Linux.
  * **Estabilidade e Não-Interferência:**
      * Instalar, atualizar ou remover uma aplicação não afeta o resto do sistema.
  * **Confinamento de Segurança (*Sandboxing*):**
      * Sem acesso não autorizado a ficheiros pessoais (`$HOME`, `~/.ssh`), credenciais ou periféricos (câmara, microfone).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Paradigmas de Contentorização Desktop}}
\end{center}

-----

## Contentores de Aplicação em Linux: Três Paradigmas

Três abordagens modernas para distribuição de software no desktop Linux:

  * **1. AppImage:**
      * **Ficheiro único e autónomo (*self-contained*):** "Uma aplicação = um ficheiro".
      * Execução direta pelo utilizador sem instalação nem privilégios de `root`.
  * **2. Snap:**
      * **Pacote universal com sandbox:** Gerido por um daemon de sistema (`snapd`).
      * Criado pela Canonical, com forte integração no Ubuntu e suporte a IoT/servidores.
  * **3. Flatpak:**
      * **Padrão aberto focado no desktop:** Baseado em *Runtimes* partilhados e sandbox rigorosa.
      * Apoiado pela Red Hat, GNOME e KDE; distribuído via **Flathub**.

-----

## Arquiteturas Comparadas: Serviços vs. Desktop

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{desktop_containers_architecture.png}
\end{center}

-----

## Análise Comparativa: AppImage vs. Snap vs. Flatpak

| Vetor de Comparação | AppImage | Snap | Flatpak |
| :--- | :--- | :--- | :--- |
| **Instalação no Sistema** | **Não requer (execução direta)** | Sim (requer privilégios `sudo` e daemon) | Opcional (instalação por utilizador sem `sudo`) |
| **Empacotamento de Dependências** | **100% autónomo (tudo num ficheiro)** | Dependências locais + *core snap* base | *Runtimes* partilhados entre aplicações |
| **Ocupação em Disco** | Elevada (duplicação total) | Média/Elevada (dependências por snap) | **Otimizada (amortizada via *runtimes*)** |
| **Latência de Arranque** | **Rápida** | Mais lenta | **Rápida / quase nativa** |
| **Isolamento de Segurança** | Nenhum por omissão | **AppArmor** | **Bubblewrap** |
| **Acesso a Recursos (Rede/Ficheiros)** | Direto e total (herda do utilizador) | Interfaces declarativas (*plugs* / *slots*) | **Declarativo no manifesto (permissões)** |
| **Integração no Desktop** | Manual (sem atalhos automáticos) | **Automática (menus e ícones do sistema)** | **Automática (menus e ícones do sistema)** |
| **Modelo de Distribuição** | **Descentralizado (download direto)** | Centralizado na Canonical (Snap Store) | **Descentralizado e comunitário (Flathub)** |
| **Comunidade & Apoio** | Comunidade independente aberta | **Canonical (Ubuntu)** | **Red Hat, GNOME, KDE e comunidade** |
| **Principal Caso de Uso** | **Portabilidade rápida ("pen USB")** | **Desktop Ubuntu, servidores e IoT** | **Aplicações desktop gráficas e multimédia** |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Empacotamento com AppImage e Flatpak}}
\end{center}

-----

## AppImage: A Estrutura AppDir

O formato AppImage baseia-se num diretório estruturado denominado **`AppDir`**, comprimido num executável SquashFS:

```text
MeuJogo.AppDir/
├── AppRun               # Ponto de entrada executável (Script obrigatório)
├── meujogo.desktop      # Metadados de integração no menu desktop
├── meujogo.png          # Ícone da aplicação
└── usr/                 # Hierarquia padrão Unix
    ├── bin/             # Binários compilados
    └── lib/             # Bibliotecas dinâmicas (.so) e pacotes Python
```

  * **`AppRun` (Obrigatório):** Script executado na abertura; configura variáveis de ambiente (`PATH`, `PYTHONPATH`) e lança o programa principal.

-----

## AppImage: Integração com o Desktop (.desktop)

O ficheiro `.desktop` integra a aplicação no menu do sistema:

  * **Conteúdo típico de `meujogo.desktop`:**
    ```ini
    [Desktop Entry]
    Name=Meu Jogo
    Exec=AppRun
    Icon=meujogo
    Type=Application
    Categories=Game;
    ```
  * **Associação de Recursos:**
      * `Exec=AppRun`: Invoca o ponto de entrada da raiz da imagem.
      * `Icon=meujogo`: Liga ao ficheiro `meujogo.png` na raiz do `AppDir`.

-----

## AppImage: Exemplo "Hello World"

Criação da estrutura `AppDir` mínima para um script:

```bash
# 1. Criar o diretório de trabalho
mkdir -p HelloWorld.AppDir && cd HelloWorld.AppDir

# 2. Criar o script de arranque executável AppRun
echo '#!/bin/bash' > AppRun
echo 'echo "Hello from an AppImage!"' >> AppRun
chmod +x AppRun

# 3. Criar os metadados de desktop e ícone
echo '[Desktop Entry]' > hello.desktop
echo 'Name=Hello' >> hello.desktop
echo 'Exec=AppRun' >> hello.desktop
echo 'Icon=hello' >> hello.desktop
echo 'Type=Application' >> hello.desktop
touch hello.png
```

-----

## AppImage: Empacotar com o appimagetool

Transformar a pasta `AppDir` num único ficheiro executável e portátil:

```bash
# Regressar ao diretório pai
cd ..

# Descarregar a ferramenta appimagetool (caso não esteja no sistema)
wget https://github.com/AppImage/AppImageKit/releases/\
download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage

# Gerar o ficheiro .AppImage final
ARCH=x86_64 ./appimagetool-x86_64.AppImage HelloWorld.AppDir

# Testar a execução do binário autónomo gerado
./Hello-x86_64.AppImage
```

-----

## Flatpak: O Manifesto Declarativo (.yml)

O Flatpak é construído a partir de um ficheiro de manifesto declarativo (em YAML ou JSON):

  * **`app-id`:** Identificador único global no formato DNS reverso (ex: `pt.ua.deti.iei.HelloWorld`).
  * **`runtime` / `sdk`:** Plataforma base e ferramentas de compilação fornecidas pelo repositório (ex: `org.freedesktop.Platform`).
  * **`command`:** Binário ou script invocado no arranque da sandbox.
  * **`modules`:** Lista declarativa de componentes a descarregar e compilar (fontes git, pacotes PyPI, scripts locais).

-----

## Flatpak: Exemplo de Manifesto (com.example.HelloWorld.yml)

Exemplo de manifesto para um script simples:

```yaml
app-id: com.example.HelloWorld
runtime: org.freedesktop.Platform
runtime-version: '25.08'
sdk: org.freedesktop.Sdk
command: hello.sh
modules:
  - name: hello-module
    buildsystem: simple
    build-commands:
      # Instala o script no diretório de binários da sandbox
      - install -Dm755 hello.sh /app/bin/hello.sh
    sources:
      - type: file
        path: hello.sh
```

-----

## Flatpak no Laboratório: Jogo do Galo (Pygame)

No guião prático, este padrão é aplicado a uma aplicação interativa com interface gráfica e áudio:

  * **Requisitos Gráficos e Aceleração por Hardware:**
      * Declaração de acessos a periféricos em `finish-args`:
        ```yaml
        finish-args:
          - --share=ipc
          - --socket=x11
          - --socket=wayland
          - --device=dri        # Aceleração gráfica GPU
          - --env=PYTHONPATH=/app/lib/game
        ```
  * **Gestão de Dependências Python via Módulos:**
      * O manifesto integra o módulo `pygame` descarregado do PyPI e instala o código do jogo em `/app/lib/game`.
  * **Integração no Desktop:**
      * Ficheiro `.desktop` e ícone instalados nos diretórios padrão XDG da sandbox (`/app/share/applications/` e `/app/share/icons/`).

-----

## Flatpak: A Ferramenta flatpak-builder

O comando `flatpak-builder` processa o manifesto e compila a aplicação num ambiente isolado:

```bash
# 1. Compilar e instalar localmente para o utilizador atual
flatpak-builder --user --install --force-clean \
  build-dir com.example.HelloWorld.yml
```

  * **`--user`:** Instala no perfil do utilizador (`~/.local/share/flatpak`), sem necessidade de `sudo`.
  * **`--install`:** Regista a aplicação no sistema após compilação bem-sucedida.
  * **`--force-clean`:** Limpa a pasta temporária de compilação `build-dir`.

```bash
# 2. Executar a aplicação dentro da sandbox do Flatpak
flatpak run com.example.HelloWorld
```


-----

## Síntese e Pontos-Chave da Sessão

  * **Infraestrutura vs. Desktop:** Docker gere serviços de backend (*headless*); AppImage, Snap e Flatpak distribuem aplicações interativas e gráficas no cliente.
  * **Resolução do *Dependency Hell*:** Empacotamento autónomo elimina conflitos de bibliotecas partilhadas (`.so`), garantindo execução determinística.
  * **AppImage:** Ficheiro único e portátil focado em simplicidade, sem sandbox por omissão.
  * **Snap:** Confinamento mandatório (AppArmor) e distribuição centralizada com forte ligação ao ecossistema Ubuntu.
  * **Flatpak:** Padrão aberto para aplicações desktop, combinando *Runtimes* partilhados com sandbox robusta (*Bubblewrap*).

-----

## Referências Técnicas Autorizadas

Documentação oficial e especificações para aprofundamento em sistemas desktop e sandboxing:

  * **Flatpak Documentation:**
      * [Manual de Desenvolvedor e Arquitetura Flatpak](https://docs.flatpak.org/)
      * [Referência do Utilitário flatpak-builder](https://docs.flatpak.org/en/latest/flatpak-builder.html)
  * **AppImage Documentation:**
      * [Guia Oficial de Empacotamento AppImage](https://docs.appimage.org/)
      * [Especificação do Formato de Ficheiro AppImage](https://github.com/AppImage/AppImageSpec)
  * **Canonical Snapcraft:**
      * [Documentação de Arquitetura e Interfaces Snap](https://snapcraft.io/docs)
  * **Especificações FreeDesktop.org:**
      * [Especificação Desktop Entry (`.desktop`)](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
      * [Especificação XDG Desktop Portals](https://flatpak.github.io/xdg-desktop-portal/)
