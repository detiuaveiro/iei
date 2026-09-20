---
title: 47138 - Introdução à Engenharia Informática
subtitle: Configuração do Ambiente de Trabalho
institute: Universidade de Aveiro
date: September 14, 2026
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

# Configurar o Ambiente de Trabalho Digital

**Objetivo da sessão:** Garantir que todos dispõem de um ambiente de desenvolvimento pronto para as aulas práticas.

### Agenda da sessão:
1. **Conceitos fundamentais:** Sistemas operativos e sistemas de ficheiros
2. **A escolha Linux:** Porquê padronizar num ambiente baseado em Unix/Linux?
3. **Três caminhos de configuração:**
   - Opção 1: Instalação nativa (*dual-boot*)
   - Opção 2: Máquina Virtual pré-configurada (VirtualBox / UTM)
   - Opção 3: Windows Subsystem for Linux (WSL 2)
4. **Comparativo e próximos passos**

# O que é um Sistema Operativo (SO)?

O Sistema Operativo é o **gestor central** de todos os recursos de hardware e software do computador:

- **Gestão de recursos:** CPU (processamento), RAM (memória ativa) e disco (armazenamento persistente).
- **Interface:** Disponibiliza interfaces gráficas (GUI) e de linha de comandos (CLI).

### Principais famílias de Sistemas Operativos:
- **Windows:** O SO de *desktop* mais comum em computadores pessoais.
- **Linux:** Sistema de código aberto (*open-source*), baseado em Unix. Domina servidores web, computação na nuvem (*cloud*), supercomputadores e desenvolvimento de software.
- **macOS:** Baseado em Unix (Darwin/BSD). Partilha a arquitetura de linha de comandos (POSIX) com o Linux.

# Sistemas de Ficheiros (*Filesystem*)

Um sistema de ficheiros é o **catálogo da biblioteca** do seu computador. É a forma como o SO organiza, armazena e encontra os seus ficheiros. 🗂️

\vspace{2em}

**Compreender a estrutura de caminhos é crucial para encontrar os seus ficheiros e executar programas a partir da linha de comandos\!**

## Sistema de Ficheiros - Windows (NTFS)

  - Utiliza **letras de unidade** independentes (`C:`, `D:`).
  - Separador de caminho: **barra invertida (`\`)**
    — P. ex.: `C:\Users\Nome\documento.txt`.
  - Nomes de ficheiros **insensíveis a maiúsculas/minúsculas** (*case-insensitive*): `ficheiro.txt` e `Ficheiro.txt` são o mesmo ficheiro.

## Sistema de Ficheiros - Linux (ext4, Btrfs, etc.)

  - **Árvore única e unificada** com raiz em `/` (não há letras de unidade).
  - Tudo, incluindo dispositivos, é tratado como um ficheiro.
  - Separador de caminho: **barra normal (`/`)**
    — P. ex.: `/home/nome/documento.txt`.
  - Nomes de ficheiros **sensíveis a maiúsculas/minúsculas** (*case-sensitive*): `ficheiro.txt` $\neq$ `Ficheiro.txt`.

# Porquê um Ambiente Padronizado? (A Escolha Linux)


Nesta unidade curricular padronizamos o trabalho num ambiente de linha de comandos **baseado em Linux** porque:

- **Padrão da Indústria:** É a espinha dorsal da Web, computação em nuvem (AWS, GCP, Azure) e computação científica.
- **Ferramentas Incomparáveis:** Ecossistema poderoso de utilitários de terminal, *scripting* (Bash), programação e automação.
- **Transparência e Controlo:** Permite compreender a fundo o funcionamento dos processos, redes e sistema operativo sem camadas ocultas.

# Três Caminhos para o Ambiente Linux 🗺️

1. **Instalação Nativa (Dual-Boot ou Dedicada)** 🐧
   - O Linux é instalado diretamente no hardware do computador.
   - *Ideal para:* Desempenho máximo e imersão total no ecossistema Linux.

2. **Máquina Virtual (VM Pré-configurada)** 🖥️
   - Um sistema Linux completo corre dentro de uma janela no SO anfitrião.
   - *Ideal para:* Segurança, isolamento e simplicidade de instalação.

3. **Subsistema Windows para Linux (WSL 2)** 🪟+🐧
   - Integração de um kernel Linux nativo diretamente no Windows.
   - *Ideal para:* Utilizadores Windows que pretendem terminal Linux integrado e rápido.

# Opção 1: Instalação Nativa de Linux 🐧

Instalação direta de uma distribuição Linux no hardware (ao lado do Windows em *dual-boot* ou em disco dedicado).

- **Vantagens:**
  - **✅ Desempenho máximo:** Acesso direto ao CPU, GPU e memória sem camadas de virtualização.
  - **✅ Imersão total:** Excelente para aprender e adaptar-se ao ambiente Linux.
- **Desvantagens:**
  - **❌ Configuração complexa:** Requer redimensionar discos e configurar BIOS/UEFI (risco de perda de dados).
  - **❌ Compatibilidade hardware:** Algum hardware poderá não ter totalmente suportado ou exigir configuração extra.

**Para quem é:** Estudantes mais aventureiros, experientes ou com um computador secundário disponível para experiências.

# Opção 1: Cuidados e Passos de Instalação

### Cuidados essenciais antes de começar:
- **Backup:** Faça cópia de segurança de todos os seus ficheiros importantes.
- **BitLocker (Windows 11):** Salve previamente a chave de recuperação de 48 dígitos (disponível na sua conta Microsoft).

### Passos recomendados:
1. **Distribuição:** Recomendamos **Ubuntu 26.04 LTS** (estável, com suporte de longo prazo).
2. **Pen USB de arranque:** Criar através de ferramentas como [Rufus](https://rufus.ie/) ou [BalenaEtcher](https://www.balena.io/etcher/).
3. **Arranque (Boot):** Reiniciar, aceder ao menu de boot (F12 / F2 / Del) e seguir instruções do instalador.

# Opção 2: Máquina Virtual (VM) 🖥️

Um *hypervisor* (VirtualBox ou similar) emula um computador completo em software, executando uma imagem Linux já pronta.

- **Vantagens:**
  - **✅ Segurança total (*sandbox*):** Qualquer erro fica confinado à VM, sem perigo para o sistema anfitrião.
  - **✅ Recuperação instantânea:** Suporta *snapshots* (pontos de restauro).
- **Desvantagens:**
  - **❌ Consumo de recursos:** Requer máquina com 8 GB+ de RAM e múltiplos núcleos de CPU, pois executa dois sistemas operativos ao mesmo tempo.
  - **❌Desempenho gráfico:** Menos fluidez face a uma instalação nativa.

**Para quem é:** Opção padrão recomendada para a maioria dos estudantes pelo equilíbrio entre segurança e simplicidade.

# Opção 2: Instalação e Recomendações

### Passos de configuração:
1. **Instalar VirtualBox:** Descarregue a versão mais recente do [VirtualBox](https://www.virtualbox.org/) e o respetivo *Extension Pack*.
2. **Obter a Imagem Linux:** Descarregue uma imagem .iso Linux. P. ex. [Ubuntu 26.04 LTS](https://ubuntu.com/download/desktop).
3. **Criar nova VM:** No VirtualBox, selecione `Machine > New`, e siga as instruções.
4. **Iniciar:** Após criada, selecione a VM e clique em **Start**.

**⚠️ Nota para utilizadores Mac (Apple Silicon - M1/M2/M3/M4):** Em Mac Apple Silicon, recomenda-se o uso do **UTM** (com imagem Ubuntu ARM64) ou a utilização das ferramentas Unix nativas via **Homebrew**.

# Opção 3: Subsistema Windows para Linux (WSL 2) 🪟+🐧

O WSL permite-lhe executar um *kernel* e ambiente Linux genuínos diretamente no Windows, sem a sobrecarga de uma VM completa. Proporciona uma poderosa integração entre os dois sistemas.

# Opção 3: Subsistema Windows para Linux (WSL 2) 🪟+🐧

### Características interessantes:
- **Rede:** O WSL partilha automaticamente a ligação de rede do seu anfitrião Windows.
- **Integração de Sistema de Ficheiros:** As suas unidades do Windows (como `C:`) são montadas automaticamente dentro do Linux em `/mnt/`. Por exemplo, a sua pasta `C:\Users\OSeuNome` está acessível em `/mnt/c/Users/OSeuNome`.

**⚠️ Importante:** Para o melhor desempenho, trabalhe sempre com os seus ficheiros dentro do sistema de ficheiros do Linux (`/home/oseunome/`), e não nas unidades do Windows montadas (`/mnt/c/`).

# Opção 3: Subsistema Windows para Linux (WSL 2) 🪟+🐧

- **Vantagens:**
  - **✅ Excelente Desempenho:** Velocidade quase nativa para compilação e ferramentas de terminal.
  - **✅ Excelente integração:** Permite invocar ferramentas Linux a partir do Windows e vice-versa. Por exemplo, pode usar o VS Code no Windows para editar ficheiros diretamente no WSL.
- **Desvantagens:**
  - **❌ Foco em CLI:** Vocacionado essencialmente para linha de comandos (aplicações gráficas exigem WSLg).
  - **❌ Potencial Complexidade:** Acesso avançado a redes ou *hardware* pode ser mais complexo vs VM ou instalação nativa.

**Para quem é:** Utilizadores de Windows que querem um ambiente baseado em linha de comandos rápido e integrado.

# Opção 3: Instalação do WSL 2

1. **Ative o WSL:** Abra o **PowerShell** ou **Terminal do Windows** como **Administrador**.
2. **Executar instalação:**
   ```powershell
   wsl --install
   ```
   *Este comando ativa os componentes necessários, obtém o kernel Linux mais recente e instala o Ubuntu por omissão.*
3. **Reiniciar:** Reinicie o computador quando solicitado.
4. **Definir credenciais:** Na janela do terminal Ubuntu que se abre, defina o seu utilizador e palavra-passe (*guarde esta password!*).
4.  **Aceder ao terminal Linux** Pode iniciar o seu terminal Linux a partir do Menu Iniciar (procure por "Ubuntu").

# Resumo Comparativo das Opções

A escolha ideal depende do seu sistema operativo, capacidade do computador e experiência:

| Característica | Instalação Nativa | Máquina Virtual (VM) | WSL 2 (Windows) |
| :--- | :---: | :---: | :---: |
| **Desempenho** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Isolamento e Segurança** | ⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Facilidade de Instalação** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Integração no SO** | N/A | ⭐ | ⭐⭐⭐ |
| **Recomendado para** | Entusiastas / Experientes | **Todos (Padrão seguro)** | Utilizadores Windows |

*Utilizadores de macOS: Podem utilizar o terminal Unix nativo (com Homebrew) ou VM com UTM.*

# Próximos Passos

1. **Escolher e configurar** uma das três opções (Nativa, VM ou WSL 2) no seu computador portátil.
2. **Testar o terminal Linux:** Abrir a linha de comandos e verificar que tem acesso a uma shell funcional (`bash`).
3. **Confirmar ferramentas básicas:** Testar que comandos como `whoami`, `uname -a`, e `pwd` respondem.

### Dúvidas ou dificuldades?
- Peça apoio aos docentes nos períodos de atendimento e nas aulas práticas.
- Não hesite em recorrer aos colegas e monitores de apoio.

**Ter o ambiente de trabalho pronto é o primeiro grande passo para o sucesso na disciplina. Bom trabalho! 🎉**
