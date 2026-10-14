---
title: Virtualização
subtitle: Introdução à Engenharia Informática
institute: Universidade de Aveiro
date: October 12, 2026
colorlinks: true
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

Este guião foi concebido para uma sessão de **3 horas** e estrutura-se em cinco partes progressivas de experimentação com sistemas de virtualização:

* **Parte 1 — Configuração do Ambiente de Virtualização:** Preparação das plataformas de virtualização de referência através de duas abordagens: gráfica (Oracle VirtualBox) e linha de comandos (QEMU em Linux e macOS).
* **Parte 2 — Emulação de Plataformas Legadas com FreeDOS:** Emulação por software de CPU x86-16, periféricos de áudio clássicos (SoundBlaster 16) e injeção de meios de armazenamento secundários.
* **Parte 3 — Virtualização de Sistemas com Alpine Linux:** Instalação de uma distribuição Linux minimalista, exploração de topologias de rede (NAT vs. Bridge) e disponibilização de serviços de rede (HTTP).
* **Parte 4 — Virtualização Aninhada com Proxmox VE:** Despliegue de um hipervisor Tipo-1 bare-metal dentro de uma máquina virtual (*nested virtualization*) e administração via consola web.
* **Parte 5 — Extensão Autónoma: Emulação de Arquiteturas Móveis (Android):** Simulação de plataformas móveis e gestão de periféricos com o Android Virtual Device (AVD).

\vspace{0.5em}

### Preparação do Diretório de Trabalho

Antes de iniciar os exercícios, crie e aceda à pasta de trabalho dedicada para esta sessão:

```bash
$ mkdir -p ~/IEI/aula03
$ cd ~/IEI/aula03
```

Todos os ficheiros gerados durante a aula (discos virtuais `*.qcow2`, imagens ISO descarregadas e pastas de partilha) deverão ser mantidos dentro desta diretoria.

> **Nota sobre caminhos de ficheiros:**
> Os comandos deste guião assumem que o terminal está posicionado no diretório de trabalho `~/IEI/aula03`. Caso descarregue imagens ISO para outra localização (como a pasta de transferências do browser), mova-as para `~/IEI/aula03` ou adapte o argumento do comando com o caminho correspondente (ex.: `"$HOME/Downloads/FD14LIVE.iso"`).

-----

## Parte 1: Configuração do Ambiente de Virtualização

O guião disponibiliza duas abordagens fundamentais para a realização dos exercícios práticos: uma **abordagem gráfica** baseada no Oracle VirtualBox e uma **abordagem de linha de comandos (CLI)** baseada no QEMU. Pode optar por uma delas ou explorar ambas em paralelo.

### Abordagem A: Interface Gráfica (Desktop) — Oracle VirtualBox
*(Disponível para Windows, macOS e Linux)*

1. **Obtenção e Instalação:**
   * Aceda à [página oficial de downloads do VirtualBox](https://www.virtualbox.org/wiki/Downloads) e descarregue o instalador binário correspondente ao seu sistema operativo.
   * Descarregue igualmente o **VirtualBox Extension Pack** disponível na mesma página.
   * Execute o instalador seguindo as opções predefinidas. No macOS, é obrigatório autorizar a extensão de sistema da Oracle em `Definições do Sistema > Privacidade e Segurança`.
   * Abra o ficheiro do Extension Pack descarregado para instalar os controladores adicionais (suporte a USB 2.0/3.0 e aceleração RDP).

2. **Fluxo de Operação no VirtualBox:**
   * A gestão de máquinas virtuais realiza-se através da interface gráfica de administração.
   * O botão **"Novo"** ativa o assistente guiado para criação de uma nova máquina virtual (definição de nome, tipo de SO, memória RAM e disco virtual).
   * As propriedades e dispositivos de hardware virtual de qualquer VM são ajustadas selecionando a máquina e acedendo ao menu **"Definições"**.

### Abordagem B: Linha de Comandos (CLI) — QEMU
*(Disponível nativamente em Linux, em WSL2 no Windows, nativamente no macOS via Homebrew, ou no terminal da VM Ubuntu criada na Aula 00 via VirtualBox)*

1. **Instalação do QEMU:**
   * **Em Linux / WSL2 (ou no interior da VM Ubuntu da Aula 00):**
     Execute no terminal:
     ```bash
     $ sudo apt update
     $ sudo apt install qemu-system-x86 qemu-system-i386 bridge-utils
     ```
     Adicione o seu utilizador ao grupo `kvm` para permitir o acesso direto a `/dev/kvm` sem `sudo` (encerre a sessão e volte a entrar para ativar):
     ```bash
     $ sudo usermod -a -G kvm $USER
     ```
   * **No macOS:**
     Utilizando o gestor de pacotes Homebrew, execute no terminal:
     ```bash
     $ brew install qemu
     ```

2. **Sintaxe Geral e Anatomia de Comandos:**
   O QEMU opera através de opções explícitas na linha de comandos, que serão aplicadas nos exercícios seguintes:
   * **Criação de Discos (`qemu-img`):** Utiliza a sintaxe `qemu-img create -f <formato> <ficheiro> <tamanho>` (por exemplo, criando imagens dinâmicas no formato `qcow2`).
   * **Instanciação de Máquinas Virtuais (`qemu-system-*`):** Invoca-se o binário da arquitetura pretendida (`qemu-system-i386` para 16/32-bit ou `qemu-system-x86_64` para 64-bit), especificando os recursos atribuídos:
     * `-m <RAM>`: Alocação de memória (ex.: `128` ou `1G`);
     * `-cpu <modelo>` ou `-accel <tipo>`: Tipo de processador e aceleração (ex.: `tcg`, `kvm` ou `hvf`);
     * `-hda <disco>` / `-drive ...`: Disco rígido principal ou unidades adicionais;
     * `-cdrom <iso>` e `-boot <ordem>`: Suporte de instalação e ordem de arranque (ex.: `-boot d` para arrancar do CD).

-----

## Parte 2: Emulação de Plataformas Legadas com FreeDOS

O FreeDOS é uma implementação livre e compatível com o MS-DOS, constituindo um sistema operativo monotarefa de 16-bit. Esta experiência permite analisar a emulação por software de hardware clássico (controladora de vídeo Cirrus Logic, periféricos de áudio SoundBlaster 16 e temporizador RTC).

1. **Obtenção dos Recursos:**
   * Descarregue a imagem **FreeDOS 1.4 Live CD** a partir do [repositório oficial](https://www.freedos.org/download/), utilizando o arquivo comprimido `FD14-LiveCD.zip` [disponível aqui](https://www.ibiblio.org/pub/micro/pc-stuff/freedos/files/distributions/1.4/FD14-LiveCD.zip). Extraia o ficheiro e coloque a imagem `FD14LIVE.iso` na sua pasta de trabalho `~/IEI/aula03/`.
   * Obtenha o ficheiro comprimido do jogo shareware **DOOM** (`doom19s.zip`), disponível na página de **eLearning** da unidade curricular. Guarde o ficheiro em `~/IEI/aula03/` e extraia-o para a subpasta `./doom`:
     ```bash
     $ cd ~/IEI/aula03
     $ mkdir -p doom
     $ unzip -o doom19s.zip -d doom/
     ```

2. **Criação e Instalação da Máquina Virtual FreeDOS:**

   #### Opção 1: Oracle VirtualBox (GUI)
   1. Selecione **"Novo"**. Defina o nome como `FreeDOS`, o Tipo como `Other` e a Versão como `DOS`.
   2. Memória RAM: atribua `64 MB`.
   3. Disco Virtual: crie uma nova imagem VDI com `128 MB`, de tamanho fixo.
   4. Aceda a **Definições > Armazenamento**, selecione a unidade ótica virtual vazia na controladora IDE e escolha o ficheiro `FD14LIVE.iso` localizado na sua pasta de trabalho.
   5. Inicie a VM e siga as instruções do assistente do FreeDOS. Na primeira fase, o disco é particionado com o FDISK e o sistema reinicia; após o reinício, confirme a formatação do volume `C:` e conclua a instalação dos pacotes.
   6. Concluída a instalação, encerre a VM e remova a imagem ISO da unidade de CD virtual.

   #### Opção 2: QEMU (CLI)
   1. Certifique-se de que está na pasta `~/IEI/aula03` e crie o disco virtual de 128 MB:
      ```bash
      $ cd ~/IEI/aula03
      $ qemu-img create -f qcow2 freedos.qcow2 128M
      ```
   2. Inicie a máquina virtual com o Live CD de instalação:
      * **Em Linux / WSL2 (com aceleração KVM/TCG e interface gráfica GTK):**
        ```bash
        $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
            -k pt-pt -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display gtk -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
      * **No macOS (com emulação TCG e interface gráfica nativa Cocoa):**
        ```bash
        $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
            -rtc base=localtime -device adlib -device sb16 \
            -device cirrus-vga -display cocoa -hda freedos.qcow2 \
            -cdrom FD14LIVE.iso -boot d
        ```
   3. **Instalação do FreeDOS:**
      * Selecione "Install to harddisk".
      * O instalador opera em duas etapas: cria a partição com o FDISK e solicita reiniciar a máquina. No arranque seguinte, confirme a formatação da partição `C:` e aguarde a cópia de ficheiros.
      * Quando surgir a mensagem final de confirmação de instalação, encerre a janela do QEMU.

3. **Injeção do Jogo (DOOM) e Execução:**
   Para transferir os binários do jogo para a máquina virtual:

   #### No VirtualBox:
   * Crie uma imagem ISO a partir da pasta `./doom` (ou utilize utilitários de sistema).
   * Em **Definições > Armazenamento**, adicione a unidade ótica com essa imagem ISO.
   * Inicie o FreeDOS. O meio de armazenamento secundário surgirá na unidade `D:`.

   #### No QEMU (Linux e macOS):
   * Inicie o FreeDOS a partir do disco rígido (`-boot c`), mapeando a pasta local `./doom` diretamente como unidade FAT secundária:
     * **Em Linux / WSL2:**
       ```bash
       $ qemu-system-i386 -machine accel=kvm:tcg -m 128 -cpu host \
           -k pt-pt -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display gtk -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```
     * **No macOS:**
       ```bash
       $ qemu-system-i386 -accel tcg -m 128 -cpu pentium \
           -rtc base=localtime -device adlib -device sb16 \
           -device cirrus-vga -display cocoa -hda freedos.qcow2 -boot c \
           -drive file=fat:rw:./doom,format=raw
       ```

4. **Instalação e Execução do Jogo no FreeDOS:**
   * Na linha de comandos do FreeDOS (`C:\>`), mude para a unidade virtual secundária:
     ```bat
     D:
     dir
     ```
   * Execute o instalador:
     ```bat
     INSTALL.BAT
     ```
   * Siga os passos predefinidos (instalação em `C:\DOOM`). Na configuração de áudio, selecione **Sound Blaster** (Porto 220, IRQ 5 ou 7, DMA 1).
   * Inicie o jogo:
     ```bat
     C:
     cd DOOM
     DOOM.EXE
     ```
   * Valide o comportamento da emulação: resolução gráfica em modo VGA (320x200), resposta do temporizador e síntese de áudio através do dispositivo SoundBlaster 16 emulado.

-----

## Parte 3: Virtualização de Sistemas com Alpine Linux

O Alpine Linux é uma distribuição orientada à segurança e eficiência de recursos baseada em musl libc e BusyBox. É amplamente utilizada na indústria como imagem de base para contentores de software e ambientes virtuais ultraleves.

1. **Obtenção da Imagem do Alpine Linux:**
   * Aceda à [página oficial de downloads do Alpine Linux](https://alpinelinux.org/downloads/) e descarregue a imagem **STANDARD**, guardando-a na pasta `~/IEI/aula03/` com o nome `alpine.iso`:
     * Em sistemas com processador x86-64 (Intel/AMD): descarregue a ISO **x86_64**.
     * No macOS com processadores Apple Silicon (M1/M2/M3/M4): descarregue a ISO **aarch64** para beneficiar de aceleração nativa por hardware com o Hypervisor.framework (`-accel hvf`).

2. **Criação e Instalação da Máquina Virtual:**

   #### Opção 1: Oracle VirtualBox (GUI)
   1. Crie uma nova VM: Nome `Alpine`, Tipo `Linux`, Versão `Linux 2.6 / 3.x / 4.x (64-bit)`.
   2. Memória RAM: `1 GB`. Disco Rígido Virtual: `8 GB`.
   3. Associe a imagem `alpine.iso` em **Definições > Armazenamento**.
   4. Inicie a máquina virtual e autentique-se como `root` (sem palavra-passe). Execute `setup-alpine`, selecionando o modo de instalação `"sys"` sobre o disco `sda`. Concluído o processo, encerre a VM e desanexe a imagem ISO.

   #### Opção 2: QEMU (CLI)
   1. Certifique-se de que está na pasta `~/IEI/aula03` e crie a imagem de disco virtual:
      ```bash
      $ cd ~/IEI/aula03
      $ qemu-img create -f qcow2 alpine.qcow2 8G
      ```
   2. Inicie a instalação a partir da imagem ISO:
      * **Em Linux / WSL2 (com KVM e imagem x86_64):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 1G -smp 2 -cpu host \
            -display gtk -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
      * **No macOS Apple Silicon (com HVF nativo e imagem aarch64):**
        ```bash
        $ qemu-system-aarch64 -accel hvf -M virt -cpu host -m 1G -smp 2 \
            -display cocoa -hda alpine.qcow2 -cdrom alpine.iso -boot d
        ```
        *(Nota: se utilizar a imagem x86_64 no macOS Apple Silicon, utilize `qemu-system-x86_64` com `-accel tcg`).*
   3. No terminal da VM, autentique-se como `root` e execute `setup-alpine`. Escolha a instalação `"sys"` em `sda`. Terminado o processo, encerre a VM e arranque subsequentemente sem a opção `-cdrom`.

3. **Análise de Topologias de Rede Virtual:**
   * **Modo NAT (Predefinição):**
     Inicialize a máquina virtual com a interface em modo NAT e verifique o endereço atribuído:
     ```bash
     # No terminal da VM Alpine
     $ ip addr show
     ```
     Verifique que o endereço IP atribuído pertence a uma rede privada interna (ex.: `10.0.2.15`). Teste a conectividade externa com `ping google.com`. Observe que a VM acede ao exterior, mas os nós da rede local física não conseguem estabelecer ligações de entrada diretas para a VM.
   * **Modo Bridge (Placa em Modo Ponte):**
     Encerre a máquina virtual para alterar a topologia de rede:
     * **No VirtualBox:** Em **Definições > Rede**, altere a opção **Ligada a:** de `NAT` para `Placa em modo Bridge (Bridged Adapter)`.
     * **No QEMU (Linux):** Configure uma interface de ponte de rede associada ao dispositivo físico:
       ```bash
       echo -e "Configurar Interface Bridge"
       sudo /sbin/ip link add virtbr0 type bridge
       sudo /sbin/ip link set dev $INTERFACE master virtbr0
       sudo /sbin/ip addr flush dev $INTERFACE
       sudo /sbin/dhclient virtbr0
       sudo /sbin/ip link set dev $INTERFACE up
       sudo /sbin/ip link set dev virtbr0 up

       echo -e "Iniciar Alpine (BRIDGE)"
       sudo qemu-system-x86_64 -machine accel=kvm:tcg -m 4G -smp 4 -cpu host \
           -k pt-pt -rtc base=localtime -display gtk -hda alpine.qcow2 \
           -netdev bridge,id=net0,br=virtbr0 -device virtio-net-pci,netdev=net0

       echo -e "Limpar Interface Bridge"
       sudo /sbin/ip link set virtbr0 down
       sudo /sbin/ip link del virtbr0
       sudo /sbin/dhclient $INTERFACE
       ```
     * Inicie a VM novamente e execute `ip addr show`. Confirme que o endereço IP obtido pertence agora ao mesmo segmento de rede física local do computador anfitrião (ex.: `192.168.1.x`).

4. **Disponibilização de um Serviço Web (HTTP):**
   * O BusyBox inclui um servidor HTTP integrado (`httpd`). Instale o pacote com ferramentas adicionais:
     ```bash
     # No terminal da VM Alpine
     $ apk add busybox-extras
     ```
   * Crie a diretoria para o conteúdo web estático:
     ```bash
     $ mkdir -p /var/www/localhost/htdocs
     ```
   * Crie uma página HTML simples:
     ```bash
     $ echo '<h1>Laboratório de Virtualização - Alpine Linux</h1>' > /var/www/localhost/htdocs/index.html
     ```
   * Inicie o serviço escutando na porta padrão 80:
     ```bash
     $ httpd -f -p 80 -h /var/www/localhost/htdocs
     ```
   * Aceda ao navegador web na máquina anfitriã e navegue até ao endereço IP da VM Alpine. Confirme a receção da resposta HTTP.

-----

## Parte 4: Virtualização Aninhada com Proxmox VE

O Proxmox Virtual Environment (VE) é uma plataforma empresarial aberta para gestão de virtualização em servidores baseada em Debian, integrando hipervisores KVM para máquinas virtuais completas e tecnologia LXC para contentores de sistema.

> **NOTA TÉCNICA: Virtualização Aninhada (Nested Virtualization)**
> A execução de um hipervisor dentro de outro hipervisor requer a passagem de instruções de virtualização da CPU física (Intel VT-x ou AMD-V) para a vCPU da máquina virtual. Esta técnica tem um impacto considerável no desempenho computacional e destina-se a fins estritamente experimentais e laboratoriais.

1. **Obtenção do Proxmox VE:**
   * Aceda à [página oficial de downloads do Proxmox VE](https://www.proxmox.com/en/downloads) e descarregue a imagem ISO do instalador mais recente, guardando-a em `~/IEI/aula03/` com o nome `proxmox.iso`.

2. **Provisionamento da Máquina Virtual Proxmox:**
   Esta máquina requer uma alocação mais substancial de recursos físicos:

   #### Opção 1: Oracle VirtualBox (GUI)
   1. Crie uma VM: Nome `Proxmox`, Tipo `Linux`, Versão `Debian (64-bit)`.
   2. Memória RAM: mínimo de `4096 MB`. Processadores: mínimo de `2` vCPUs.
   3. Disco Virtual: `32 GB` ou superior.
   4. Em **Definições > Sistema > Processador**, selecione obrigatoriamente a opção **Ativar VT-x/AMD-V Aninhado**.
   5. Em **Definições > Rede**, mantenha o modo `NAT`.
   6. Configure uma regra de **Redirecionamento de Portas (Port Forwarding)** mapeando a porta `8006` do anfitrião para a porta `8006` do convidado.
   7. Associe o ficheiro `proxmox.iso` na controladora de armazenamento.

   #### Opção 2: QEMU (CLI)
   1. Certifique-se de que está na pasta `~/IEI/aula03` e crie o disco virtual de 32 GB:
      ```bash
      $ cd ~/IEI/aula03
      $ qemu-img create -f qcow2 proxmox.qcow2 32G
      ```
   2. Inicie a máquina com suporte a virtualização aninhada e redirecionamento da porta web `8006`:
      * **Em Linux / WSL2 (com aceleração KVM):**
        ```bash
        $ qemu-system-x86_64 -enable-kvm -m 4096 -smp 2 -cpu host \
            -hda proxmox.qcow2 -cdrom proxmox.iso -boot d \
            -netdev user,id=net0,hostfwd=tcp::8006-:8006 \
            -device virtio-net-pci,netdev=net0 -display gtk
        ```
      * **No macOS:**
        *(Nota: O Proxmox VE é baseado em arquitetura x86-64. No macOS com processadores Intel x86, pode ser executado com `-accel hvf`. Em computadores Apple Silicon ARM64, a execução de um hipervisor x86 requer emulação total via TCG ou recomenda-se a realização deste exercício em Linux / VirtualBox x86).*

3. **Instalação e Configuração Inicial:**
   * Inicie a máquina virtual e prossiga através do assistente gráfico de instalação do Proxmox.
   * Na configuração de rede estática, atribua um endereço de gestão adequado (ex.: `192.168.1.200/24`).
   * Terminada a instalação, reinicie o sistema convidado e desanexe a imagem ISO.

4. **Acesso à Consola Web de Administração:**
   * Na consola de texto do Proxmox, verifique o URL de acesso HTTPS. Aceda ao navegador do computador anfitrião e introduza `https://localhost:8006`.
   * Confirme o aviso de segurança relativo ao certificado digital autoassinado.
   * Efetue a autenticação com o utilizador `root` e a palavra-passe definida na fase de instalação.

5. **Instanciação de uma Instância Convidada no Proxmox:**
   * Na consola web do Proxmox, explore a criação de recursos virtualizados.
   * Desafio prático: Transfira a imagem ISO do Alpine Linux para o armazenamento local do Proxmox e crie uma máquina virtual aninhada através do painel de administração web.

-----

## Parte 5: Extensão Autónoma — Emulação de Arquiteturas Móveis (Android)

A emulação da plataforma Android permite simular a arquitetura de processamento e os subsistemas de hardware de dispositivos móveis. Sob a interface gráfica do Android Studio, o emulador oficial é suportado por uma versão especializada do motor QEMU.

1. **Obtenção e Instalação do Android Studio:**
   * Aceda à [página oficial do Android Studio](https://developer.android.com/studio) e transfira o instalador correspondente à sua plataforma anfitriã.
   * Conclua a instalação padrão do pacote e dos componentes fundamentais do Android SDK.

2. **Gestão de Dispositivos Virtuais (AVD Manager):**
   * Abra Android Studio (sem necessidade de inicializar um projeto de desenvolvimento).
   * A partir do ecrã principal ou do menu **Tools**, selecione a ferramenta **Virtual Device Manager** (AVD).

3. **Provisionamento do Dispositivo Virtual:**
   * Selecione **"Create Virtual Device..."**.
   * Escolha um perfil de hardware de referência (ex.: Google Pixel 7).
   * Selecione e transfira a imagem de sistema recomendada da plataforma Android.
   * Confirme as configurações de memória e denomine o perfil AVD.

4. **Execução e Inspeção do Sistema Emulado:**
   * No gestor de dispositivos AVD, acione o comando de execução no dispositivo criado.
   * O motor de emulação inicializa o sistema operativo Android completo numa janela gráfica dedicada. Analise o tempo de inicialização, a responsividade do subsistema gráfico e a abstração de sensores e periféricos do dispositivo móvel.
