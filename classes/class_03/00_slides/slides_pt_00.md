---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Virtualização: Arquitetura, Hipervisores & Virtualização de Sistemas"
institute: Universidade de Aveiro
date: October 12, 2026
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

Esta sessão aborda os fundamentos arquiteturais e os mecanismos práticos da virtualização de sistemas:

  * **Fundamentos de Virtualização & Hipervisores:** Abstração de hardware, anéis de privilégio da CPU, hipervisores Tipo-1 vs. Tipo-2.
  * **Emulação vs. Virtualização:** Princípios de tradução por software, desempenho relativo e casos de uso em engenharia.
  * **E/S, Armazenamento & Redes Virtuais:** Framework VirtIO, formatos de disco (QCOW2, VDI) e topologias de rede (NAT, Bridge, Host-Only).
  * **Ferramentas Práticas de Virtualização:** Oracle VirtualBox, CLI do QEMU/KVM, Proxmox VE e matriz comparativa.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Fundamentos \& Hipervisores}}
\end{center}

-----

## Virtualização: Definição

A **Virtualização** abstrai o hardware físico para instanciar múltiplos ambientes virtuais isolados (*VMs*) num único computador:

  * **Anfitrião (Host):** Plataforma física de hardware (CPU, memória, armazenamento, rede).
  * **Hipervisor (VMM):** Software que gere o hardware, isola instâncias e escalona recursos.
  * **Máquina Virtual (VM):** Limite de abstração isolado que expõe hardware virtual (vCPU, vRAM, vDisk, vNIC).
  * **Convidado (Guest):** Sistema operativo e VM que o executa.

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.50\textheight,keepaspectratio]{virtual_vs_traditional_architecture.png}
\end{center}

-----

## O Desafio da Virtualização: Anéis de Privilégio

As arquiteturas modernas de processadores impõem níveis de privilégio de hardware (anéis) para isolar código de aplicação de código de execução do kernel:

  * **Ring 3 (Espaço de Utilizador):** As aplicações executam instruções não privilegiadas. Operações privilegiadas exigem a invocação de chamadas de sistema (`syscall`) ao kernel.
  * **Ring 0 (Espaço de Kernel / Modo Supervisor):** O kernel do sistema operativo executa instruções privilegiadas (ex.: controlo direto da MMU, tratamento de interrupções, portos de entrada/saída E/S).

  **Como podem os diversos Guests acederem então executar instruções privilegiadas e controlar o hardware ?**

  * A resposta está no hipervisor como mediador e árbitro. Os hipervisores interferem nas instruções críticas e interceptam o acesso ao hardware, delegando a execução ao hardware real quando possível.

-----

## Tipos de Hipervisores: Tipo-1 e Tipo-2

\begin{center}
\includegraphics[width=0.92\linewidth,height=0.75\textheight,keepaspectratio]{hypervisor_types.png}
\end{center}

-----

## Hipervisores Tipo-1 (Bare-Metal)

Os **Hipervisores Tipo-1** executam diretamente sobre o hardware físico, sem a intermediação de um sistema operativo de uso geral:

  * **Camada de Execução:** Opera diretamente na camada de privilégio de hardware. O hipervisor atua como kernel primário e árbitro de recursos.
  * **Arquitetura:** Os controladores de dispositivos e domínios de gestão executam dentro de um microkernel mínimo do hipervisor ou numa partição de gestão dedicada (ex.: Xen Dom0, Linux KVM).
  * **Características Principais:**
      * Sobrecarga de abstração negligenciável e latência de hipervisor sub-milissegundo.
      * Elevado débito de E/S e máxima eficiência de utilização de hardware.
      * Independência do ciclo de vida ou falhas de um sistema operativo desktop.
  * **Exemplos em Produção:** VMware ESXi, Proxmox VE / KVM, Microsoft Hyper-V, Xen.

-----

## Hipervisores Tipo-2 (Hospedado)

Os **Hipervisores Tipo-2** executam como processos padrão no espaço de utilizador sobre um sistema operativo anfitrião já existente:

  * **Camada de Execução:** Depende do kernel do sistema operativo anfitrião para escalonamento de recursos físicos, gestão de memória e controladores de dispositivos.
  * **Arquitetura:** Utiliza drivers de modo kernel para aceder às extensões de virtualização de hardware, encaminhando os pedidos de E/S através dos subsistemas do SO anfitrião.
  * **Características Principais:**
      * Sobrecarga de duplo escalonamento: o kernel convidado escalona processos virtuais e o SO anfitrião escalona os processos do hipervisor.
      * Grande facilidade de instalação e utilização em postos de trabalho e portáteis pessoais.
      * Integração desktop conveniente entre anfitrião e convidado (área de transferência partilhada, redimensionamento dinâmico de janela, pastas partilhadas).
  * **Exemplos em Produção:** Oracle VirtualBox, VMware Workstation, Parallels Desktop.

-----

## Comparação Hipervisores: Tipo-1 vs. Tipo-2

| Dimensão Arquitetural | Tipo-1 (Bare-Metal) | Tipo-2 (Hospedado) |
| :--- | :--- | :--- |
| **Camada de Execução** | Diretamente sobre o hardware físico | Sobre o SO Anfitrião |
| **Requisito de SO Anfitrião** | Nenhum (o hipervisor é o kernel) | SO desktop/servidor padrão obrigatório |
| **Sobrecarga de Desempenho** | Mínima (< 2% de CPU) | Moderada (latência do duplo escalonador e pilha de E/S) |
| **Latência de E/S** | Direta / Quase nativa | Mediada pelos drivers do SO anfitrião |
| **Isolamento de Falhas** | Elevado (VMs independentes) | Acoplado à estabilidade do SO anfitrião |
| **Casos de Uso Principais** | Centros de Dados, Nuvem (AWS, GCP) | Desenvolvimento de Software, Testes, Ensino |
| **Ferramentas Representativas**| Proxmox VE, VMware ESXi, KVM | Oracle VirtualBox, VMware Workstation |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Emulação vs. Virtualização}}
\end{center}

-----

## Emulação: Definição e Casos de Uso

A **Emulação** recria o comportamento do hardware e do conjunto de instruções (ISA) de um sistema diferente inteiramente por software:

  * **Mecanismo:** Intérprete de software ou Tradutor Binário Dinâmico (JIT). O emulador converte em tempo real cada instrução do sistema convidado em instruções nativas da CPU do anfitrião.
  * **Independência Arquitetural:** O ISA do convidado pode diferir completamente do ISA do anfitrião (ex.: executar código ARM64, PowerPC ou x86-16 num anfitrião x86-64).
  * **Sobrecarga de Desempenho:** Penalização computacional muito elevada (tipicamente de 5x a 20x mais lento do que a execução nativa).
  * **Casos de Uso em Engenharia:**
      * Execução de sistemas operativos e software legados (ex.: FreeDOS com emulação de placa de som SoundBlaster na Parte 2 dos exercícios).
      * Desenvolvimento cruzado para sistemas embebidos (ex.: QEMU para ARM ou RISC-V).
      * Simulação de plataformas móveis (ex.: Android Virtual Device / AVD).

-----

## Emulação vs. Virtualização

| Dimensão | Emulação por Software | Virtualização Assistida por Hardware |
| :--- | :--- | :--- |
| **Conjunto de Instruções (ISA)** | Pode ser diferente (ex.: ARM em x86) | Idêntico (ex.: x86 em x86) |
| **Execução de Instruções** | Traduzido instrução a instrução por software | Executado diretamente no silício da CPU |
| **Desempenho de CPU** | Muito lento (5x a 20x de penalização) | Quase nativo (< 3% de sobrecarga) |
| **Desempenho de E/S** | Muito lento (circuitos simulados em código) | Acelerado por drivers paravirtualizados (VirtIO) |
| **Flexibilidade** | Máxima (qualquer hardware pode ser simulado) | Restrita à arquitetura física do processador |
| **Exemplo Prático** | FreeDOS / DOOM (Parte 2 dos exercícios) | Alpine Linux / VirtualBox (Parte 3 dos exercícios) |

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: E/S, Armazenamento \& Redes Virtuais}}
\end{center}

-----

## Virtualização de E/S: Hardware Emulado vs. Framework VirtIO

Os dispositivos de entrada/saída (disco e rede) representam o principal desafio de desempenho na virtualização:

  * **Hardware Emulado (Compatível, mas Lento):**
      * O hipervisor simula o comportamento de circuitos clássicos por software (ex.: placa de rede Intel E1000, controlador de disco IDE).
      * Permite que qualquer sistema operativo funcione sem controladores adicionais, mas cada leitura/escrita tem de ser intercetada e processada em software pelo hipervisor.
      * Resulta em latência e sobrecarga elevadas sob tráfego de rede intenso ou transferências pesadas de disco.
  * **E/S Paravirtualizada com VirtIO (Cooperativa e Eficiente):**
      * O sistema operativo convidado utiliza controladores dedicados (**VirtIO**), tendo consciência de que está a executar numa máquina virtual.
      * Elimina a simulação de hardware: o convidado e o hipervisor transferem dados diretamente através de canais de memória partilhada.
      * Permite agrupar pedidos em lote com sobrecarga mínima, atingindo desempenho próximo do nativo (o padrão usado na nuvem e no QEMU com `-device virtio-net-pci`).

-----

## Acesso Direto a Hardware: Passthrough & IOMMU

O **Passthrough** concede a uma máquina virtual o controlo exclusivo e direto sobre um periférico físico (PCIe ou USB) do anfitrião:

  * **Desempenho Nativo:** O sistema operativo convidado comunica diretamente com o dispositivo real, eliminando qualquer intermediação ou atraso do hipervisor.
  * **O Papel da IOMMU (Isolamento de Segurança):**
      * Componente de hardware no processador e motherboard (Intel **VT-d**, AMD **AMD-Vi**).
      * **Isolamento de Memória:** Garante que o dispositivo físico acede estritamente à memória RAM alocada àquela máquina virtual, impedindo que um dispositivo aceda à memória do anfitrião ou de outras VMs.
  * **Casos de Uso em Engenharia:**
      * **GPU Dedicada:** Aceleração gráfica e treino de modelos de Inteligência Artificial / Machine Learning dentro da VM.
      * **Periféricos USB:** Ligação direta de placas de desenvolvimento e microcontroladores (Arduino, ESP32) à máquina virtual.

-----

## Armazenamento Virtual: Arquiteturas de Discos Virtuais

As máquinas virtuais armazenam dados persistentes em ficheiros de imagem de disco virtual que encapsulam os blocos do sistema de ficheiros convidado:

  * **Formato RAW:**
      * Uma réplica linear setor a setor do disco físico.
      * Desempenho máximo de leitura e escrita sequencial.
      * Não suporta nativamente snapshots, expansão esparsa ou compressão interna.
  * **Formato QCOW2 (QEMU Copy-On-Write 2):**
      * Formato avançado com suporte a alocação dinâmica, compressão (zstd/zlib) e múltiplos níveis de snapshots.
      * Implementa imagens base (backing files): uma imagem modelo de base pode ser partilhada por várias VMs através de camadas diferenciais de escrita.
  * **Formatos VDI (VirtualBox) & VMDK (VMware):**
      * Formatos orientados a estações de trabalho que suportam expansão dinâmica e snapshots pontuais.

-----

## Aprovisionamento de Armazenamento: Alocação Fixa vs. Dinâmica

As imagens de disco virtual suportam duas estratégias fundamentais de alocação de armazenamento:

  * **Alocação Pré-alocada (Fixa / Preallocated):**
      * O hipervisor reserva imediatamente a capacidade total especificada no disco do anfitrião aquando da criação (ex.: cria logo um ficheiro de 20 GB).
      * Vantagens: Elimina a fragmentação no sistema de ficheiros anfitrião e assegura latências de escrita previsíveis durante cargas intensivas.
      * Desvantagem: Desperdiça espaço de disco no anfitrião enquanto o sistema de ficheiros convidado estiver vazio.
  * **Alocação Dinâmica (Esparsa / Thin Provisioned):**
      * O ficheiro do disco virtual inicia apenas com metadados e cresce à medida que novos blocos são escritos pelo sistema operativo convidado.
      * Vantagens: Maximiza a densidade de armazenamento e permite sobre-alocação (overcommit) de armazenamento físico.
      * Desvantagem: Ligeira penalização de escrita aquando da alocação de novos blocos e risco de esgotamento de espaço se o disco do anfitrião encher.

-----

## Rede Virtual: Modo NAT & Redirecionamento de Portas

O hipervisor gere a ligação das máquinas virtuais ao mundo exterior:

  * **Modo NAT (Predefinição):**
      * A máquina virtual partilha a ligação de rede do computador anfitrião.
      * **Acesso à Internet:** O convidado acede à internet sem necessidade de configurações adicionais (ex.: descarregar pacotes ou navegar na web).
      * **Protegida do Exterior:** Dispositivos externos na rede local não conseguem iniciar ligações diretamente para a VM.
  * **Redirecionamento de Portas (Port Forwarding):**
      * Permite criar uma passagem de uma porta específica do anfitrião para um serviço dentro da VM.
      * **Exemplo Prático:** Mapear `localhost:8006` no computador anfitrião para a porta `8006` da VM permite aceder ao painel web do Proxmox no browser sem expor a VM à rede física.

-----

## Rede Virtual: Modo Bridge & Modo Host-Only

Outras topologias para cenários de servidores ou ambientes de teste isolados:

  * **Modo Bridge (Ligação em Ponte):**
      * A máquina virtual passa a comportar-se como se fosse um computador físico independente ligado ao router.
      * Obtém um endereço IP próprio na rede local (ex.: `192.168.1.x`), tal como o anfitrião ou um telemóvel na mesma rede.
      * **Ideal para Servidores:** Qualquer computador na rede local consegue aceder aos serviços da VM (como testado no exercício do servidor web em Alpine).
  * **Modo Host-Only (Exclusivo do Anfitrião):**
      * Cria uma rede privada e fechada exclusivamente entre o anfitrião e as suas máquinas virtuais.
      * Sem ligação à internet nem à rede local; ideal para cenários de teste controlados e segurança reforçada.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Ferramentas Práticas de Virtualização}}
\end{center}

-----

## Oracle VirtualBox: Arquitetura & Fluxo Desktop

O Oracle VirtualBox fornece uma plataforma de virtualização Tipo-2 de nível de produção otimizada para ambientes desktop:

  * **Componentes Centrais:**
      * **Gestor Gráfico VirtualBox:** Interface intuitiva para criação de VMs, gestão de snapshots e meios virtuais.
      * **Interface CLI VBoxManage:** Controlo total e programável de todas as funcionalidades do hipervisor por linha de comandos.
      * **VirtualBox Guest Additions:** Módulos de kernel instalados dentro do convidado para fornecer aceleração gráfica, redimensionamento dinâmico do ecrã, sincronização temporal, área de transferência bidirecional e pastas partilhadas.
  * **Extension Pack:** Pacote adicional para suporte a controladores USB 2.0/3.0, passthrough de webcam e encriptação RDP.

-----

## QEMU + KVM: Arquitetura & Integração com o Kernel

A combinação QEMU + KVM constitui a base de virtualização de alto desempenho dos servidores Linux modernos e da infraestrutura de nuvem:

  * **KVM (Kernel-based Virtual Machine):**
      * Módulo integrado no kernel Linux (`kvm.ko`, `kvm-intel.ko` / `kvm-amd.ko`) que expõe a interface `/dev/kvm`.
      * Transforma o kernel Linux num hipervisor Tipo-1, gerindo o escalonamento de CPU, paginação de memória (EPT/NPT) e execução assistida por hardware.
  * **QEMU (Quick EMUlator):**
      * Processo em espaço de utilizador responsável pela emulação de dispositivos de E/S, barramentos, armazenamento e interface de ecrã.
      * Quando executado com a flag `-enable-kvm`, as instruções da CPU convidada correm diretamente no processador físico via KVM, alcançando desempenho quase nativo.

-----

## Configuração e Permissões do QEMU/KVM

A configuração do ambiente KVM em distribuições baseadas em Debian/Ubuntu:

  * **1. Instalação dos Pacotes do Hipervisor:**
    ```bash
    $ sudo apt update
    $ sudo apt install qemu-system-x86 kvm bridge-utils
    ```
  * **2. Permissões de Execução:** Adicionar o utilizador ao grupo `kvm` para permitir acesso direto ao nó `/dev/kvm` sem privilégios de `root`:
    ```bash
    $ sudo usermod -aG kvm $USER
    ```

-----

## Gestão de Discos com `qemu-img`

Criação e inspeção de imagens de disco virtual a partir da linha de comandos:

  * **Criar Imagem QCOW2 com Alocação Dinâmica:**
    ```bash
    $ qemu-img create -f qcow2 disco_alpine.qcow2 8G
    ```
  * **Inspecionar Formato e Ocupação Real:**
    ```bash
    $ qemu-img info disco_alpine.qcow2
    ```

-----

## Lançamento de uma Máquina Virtual no QEMU

Comando completo para iniciar uma VM combinando aceleração KVM, disco VirtIO e rede:

```bash
$ qemu-system-x86_64 \
    -enable-kvm \
    -m 4096 \
    -smp 4 \
    -cpu host \
    -drive file=disco_alpine.qcow2,if=virtio,format=qcow2 \
    -netdev user,id=net0,hostfwd=tcp::8080-:80 \
    -device virtio-net-pci,netdev=net0 \
    -display gtk
```

  * `-enable-kvm` & `-cpu host`: Ativa a aceleração nativa por hardware através do módulo KVM.
  * `-m 4096` & `-smp 4`: Alocação de 4 GB de memória RAM e 4 núcleos virtuais de processador.
  * `-drive if=virtio`: Disco virtual de alto desempenho com controladores VirtIO.
  * `-netdev ... -device virtio-net-pci`: Placa de rede VirtIO em modo NAT com redirecionamento da porta `8080` (anfitrião) para `80` (VM).
  * `-display gtk`: Abre a janela gráfica para visualização e interação com o sistema operativo convidado.

-----

## Proxmox Virtual Environment (VE)

O **Proxmox VE** é uma plataforma empresarial aberta para gestão de virtualização em servidores:

  * **Arquitetura Subjacente:** Construído sobre Debian Linux, integrando KVM para virtualização por hardware e LXC para contentores de sistema.
  * **Interface de Gestão:** Painel web completo acessível por omissão no porto `8006` (`https://<ip-servidor>:8006`) com suporte integral a API REST.
  * **Armazenamento e Redes:** Suporte nativo para soluções empresariais (ZFS, Ceph, LVM-thin, NFS) e pontes de rede Linux (`vmbr0`).
  * **Ambiente de Laboratório (Virtualização Aninhada):** Em computadores pessoais ou postos de trabalho, pode ser executado dentro de outro hipervisor (VirtualBox ou QEMU) recorrendo a **virtualização aninhada** (*nested virtualization*).

-----

## Ecossistema de Hipervisores: Matriz Comparativa

| Métrica de Avaliação | Oracle VirtualBox | QEMU + KVM | Proxmox VE |
| :--- | :--- | :--- | :--- |
| **Tipo de Hipervisor** | Tipo-2 (Hospedado) | Tipo-1 / Híbrido | Tipo-1 (Bare-Metal) |
| **Sistema Operativo Anfitrião**| Windows, macOS, Linux | Linux | Base Debian Dedicada |
| **Interface Primária** | GUI Desktop | Linha de Comandos (CLI) | Portal Web Centralizado |
| **Sobrecarga de Desempenho** | Moderada | Mínima (Quase nativa) | Mínima (Nível de produção) |
| **Capacidade de Automação** | VBoxManage (Boa) | Flags CLI / Libvirt (Ampla)| API REST / CLI / GUI (Total)|
| **Formatos de Armazenamento** | VDI, VMDK | RAW, QCOW2 | ZFS, Ceph, QCOW2, LVM |
| **Público Alvo** | Utilizadores desktop, alunos | Devs de kernel, sysadmins | Centros de dados, clusters |

-----

## Referências Técnicas Autorizadas

Documentação oficial e especificações arquiteturais para aprofundamento em engenharia de sistemas:

  * **Kernel-based Virtual Machine (KVM):**
      * [Documentação de Virtualização do Kernel Linux](https://docs.kernel.org/virt/kvm/)
  * **Emulação de Sistemas com QEMU:**
      * [Manual do Utilizador de Emulação de Sistemas do QEMU](https://www.qemu.org/docs/master/system/index.html)
  * **Oracle VirtualBox:**
      * [Manual do Utilizador do Oracle VirtualBox](https://www.virtualbox.org/manual/)
  * **Proxmox Virtual Environment:**
      * [Guia de Administração do Proxmox VE](https://pve.proxmox.com/pve-docs/)
  * **Especificação VirtIO:**
      * [Especificação Padronizada VirtIO (OASIS)](https://docs.oasis-open.org/virtio/virtio/v1.2/virtio-v1.2.html)
