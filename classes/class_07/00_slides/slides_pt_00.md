---
title: 47138 - Introdução à Engenharia Informática
subtitle: "Redes Informáticas: Fundamentos, Configuração & Diagnóstico"
institute: Universidade de Aveiro
date: November 09, 2026
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

  * **Parte I — Como se Constrói uma Rede? (Do Portátil à Internet):**
      * As escalas de rede (**PAN**, **LAN**, **MAN**, **WAN**), os equipamentos do dia a dia (**Switch**, **Access Point**, **Router**, **ONT**) e o **Modelo OSI (7 camadas)** com encapsulamento.
  * **Parte II — Endereços e Portas (Encontrar a Máquina e o Programa):**
      * Endereço físico (**MAC**) vs. endereço lógico (**IP**), roteamento (*Switch* vs. *Routers*), **Default Gateway** e **ARP**, **IPv4** e máscara (`/24`), IPs especiais, **IPv6** e **Portas** (incluindo mapeamento Docker e desafio de *Reverse Proxy*).
  * **Parte III — Configuração de IP (DHCP vs. Estático) e DNS:**
      * Os 4 parâmetros essenciais de rede, configuração automática (**DHCP**) vs. manual (**IP Estático**), resolução de nomes (**DNS**) e a hierarquia em árvore de servidores DNS.
  * **Parte IV — Configuração, Diagnóstico (Debug) e Acesso Remoto:**
      * Ferramentas essenciais no Linux (`ip`, `ping`, `traceroute`, `dig`, `ss`, `nmap`, `curl`), **Firewalls** e isolamento na `eduroam`, metodologia de **Debug em 5 passos** e trabalho remoto seguro com **SSH**, **`rsync`** e **Túneis SSH**.

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte I: Como se Constrói uma Rede? (Do Portátil à Internet)}}
\end{center}

-----

## O Que é uma Rede? PAN, LAN, MAN e WAN

Uma rede de computadores é um sistema de dispositivos interligados que comunicam e partilham recursos entre si. Consoante a escala geográfica:

\vspace{0.2em}

\begin{center}
\includegraphics[width=0.96\linewidth,height=0.40\textheight,keepaspectratio]{figures/network_scales_lan_man_wan.jpg}
\end{center}

\vspace{-0.4em}

::::: columns
::: {.column width="50%"}

  * **PAN (*Personal Area*):** Dispositivos em torno do utilizador (~poucos metros; Bluetooth / Wi-Fi Direct).
  * **LAN (*Local Area*):** Casa, sala, edifício ou Docker (alta velocidade via cabo Ethernet e Wi-Fi).

:::
::: {.column width="50%"}

  * **MAN (*Metropolitan Area*):** Múltiplos edifícios ou polos numa cidade ou campus alargado (anéis de fibra).
  * **WAN (*Wide Area*):** Cidades, países e continentes interligados (a **Internet** global via cabos e satélite).

:::
:::::

-----

## Equipamentos da Rede Local: Switch e Access Point

Interligação de dispositivos dentro da mesma LAN:

::::: columns
::: {.column width="54%"}

  * **Switch (Comutador):**
      * Liga dispositivos por cabo (Ethernet).
      * Entrega pacotes **apenas** à porta do destinatário.
      * *(Substituiu o antigo **Hub**, que gerava colisões).*
  * **Access Point (AP — Ponto de Acesso):**
      * Liga dispositivos sem fios (Wi-Fi) à rede cablada.
      * Integra portáteis e telemóveis na mesma LAN.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{Switches e AP ligam dispositivos na mesma LAN.}}
\end{center}

:::
:::::

-----

## A Fronteira com a Internet: Router e ONT

Comunicação para além da rede local:

::::: columns
::: {.column width="54%"}

  * **Router (Encaminhador):**
      * Interliga **redes diferentes** (LAN 1, LAN 2 e Internet).
      * Encaminha pacotes entre redes através do melhor caminho.
  * **ONT (*Optical Network Terminal*):**
      * Converte sinal ótico (fibra da rua) em elétrico (Ethernet).
  * **O "Router de Casa":**
      * Aparelho **4-em-1**: integra ONT, Router, Switch e AP numa única caixa.

:::
::: {.column width="46%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/network_devices_router_switch_ap.jpg}

\vspace{0.2em}
{\tiny \textit{O Router interliga redes distintas (LAN 1, LAN 2 e Internet).}}
\end{center}

:::
:::::

-----

## Como a Rede se Organiza: O Modelo OSI (7 Camadas)

O modelo **OSI** (*Open Systems Interconnection*) padroniza a comunicação entre sistemas através de **7 camadas**:

\vspace{0.3em}

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_7_layers_osi_encapsulation.jpg}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte II: Endereços e Portas (Encontrar a Máquina e o Programa)}}
\end{center}

-----

## Dois Endereços em Cada Dispositivo: MAC vs. IP

Cada interface de rede (cabo Ethernet ou Wi-Fi) opera com **dois níveis de endereçamento**:

::::: columns
::: {.column width="50%"}

  * **Endereço MAC (Físico / Camada 2 - Ligação de Dados):**
      * Exemplo: `00:1A:2B:3C:4D:5E` (48 bits em hexadecimal).
      * Gravado de fábrica na placa de rede (imutável no hardware).
      * **Para que serve:** Identifica a interface no **enlace local imediato (*hop-by-hop*)**. O MAC de destino muda a cada salto de router.
      * **Analogia:** O seu **Cartão de Cidadão** (identifica o dispositivo no local onde se encontra).

:::
::: {.column width="50%"}

  * **Endereço IP (Lógico / Camada 3 - Rede):**
      * Exemplo: `192.168.1.10` (IPv4).
      * Atribuído logicamente pela rede onde está ligado.
      * **Para que serve:** Identifica a máquina de **origem e destino final (*end-to-end*)** através de várias redes interligadas.
      * **Analogia:** A sua **Morada Postal** (muda quando viaja ou muda de rede).

:::
:::::

\vspace{0.6em}

\begin{center}
\textbf{O IP define o destino global final da viagem; o MAC define quem recebe a trama no próximo salto local (seja o router ou o destino final na LAN).}
\end{center}

-----

## Roteamento na Prática: Envio Local (Switch) vs. Salto a Salto (Routers)

\begin{center}
\includegraphics[width=\linewidth,keepaspectratio]{figures/network_routing_mac_vs_ip.png}
\end{center}

-----

## Como Funciona o Roteamento: O Papel do Gateway e do ARP

  * **1. Comunicação Remota (Noutra rede):**
      * O **Portátil 4** (`192.168.3.90`) quer enviar dados para o **Portátil 1** (`192.168.1.100` noutra rede).
      * O **Endereço de Rede Destino (IP: `192.168.1.100`) é constante (*end-to-end*)** em toda a viagem.
      * Como o destino está fora da sub-rede local, o Portátil 4 entrega a trama física na sua "porta de saída": o **Default Gateway (Router 1)**, colocando `MAC Destino = FF:FF:FF:FF:FF:FF`.
      * O **Router 1** desencapsula a trama, consulta a sua tabela de rotas e encaminha para a rede `192.168.1.0`, atualizando o MAC a cada salto (*hop-by-hop*).
  * **2. Comunicação Local (Mesma rede):**
      * Se o Portátil 2 (`192.168.1.101`) enviar para o Portátil 1 (`192.168.1.100`), a trama vai **diretamente pelo Switch** com `MAC Destino = AA:AA:AA:AA:AA:AA` (não passa pelo Router!).
  * **3. O Papel do ARP (*Address Resolution Protocol*):**
      * Para preencher o MAC físico na trama Ethernet, a máquina emissora pergunta:
      * **Destino na mesma rede $\rightarrow$** ARP descobre o MAC da própria máquina de destino.
      * **Destino fora da rede $\rightarrow$** ARP descobre o MAC do seu **Default Gateway**!

-----

## Endereço IPv4 e a Máscara de Sub-rede (Simplificado)

Um endereço IPv4 tem 4 números de `0` a `255` separados por pontos, e vem **sempre** acompanhado de uma **Máscara de Sub-rede**:

  * **Endereço IP:** `192.168.1.10`
  * **Máscara de Sub-rede:** `255.255.255.0` (que também se escreve de forma curta como **`/24`**).
  * **Como ler isto de forma simples?**
      * Onde a máscara tem `255`, o número identifica **a Rua (a Rede)**: `192.168.1.x`
      * Onde a máscara tem `0`, o número identifica **o Número da Porta (o Dispositivo)**: `.10` (pode ir de `.1` a `.254`).

\vspace{0.4em}

```text
Endereço IP:      192  .  168  .   1   .   10
Máscara (/24):    255  .  255  .  255  .   0
                [---- A MESMA RUA ----] [PORTA]
```

\vspace{0.3em}

  * **Para que serve na prática?**
      * Quero falar com `192.168.1.25` $\rightarrow$ Começa por `192.168.1.` $\rightarrow$ **Está na minha rua (LAN)!** Envio diretamente pelo Switch.
      * Quero falar com `8.8.8.8` $\rightarrow$ Não começa por `192.168.1.` $\rightarrow$ **Está noutra rua (Internet)!** Envio para o meu **Router**.

-----

## IPs Especiais e Gamas de Rede

  * **`127.0.0.1` (`localhost` / Interface de Loopback):**
      * Significa **"este próprio computador"**. O tráfego é processado internamente pelo sistema operativo e nunca sai para a placa de rede/cabo/Wi-Fi.
      * Ideal para testar servidores e aplicações localmente sem necessitar de ligação à rede.
  * **Endereços Reservados na Sub-rede (ex.: numa rede `/24`):**
      * **Primeiro endereço (`... .0`):** Identifica a **própria rede** (não pode ser atribuído a máquinas).
      * **Último endereço (`... .255`):** Endereço de **Broadcast** (uma mensagem enviada para aqui é recebida por todas as máquinas da LAN).
  * **Endereços IP Privados (RFC 1918 — Apenas para LANs):**
      * Gamas reservadas: `10.0.0.0/8` (empresas/universidades), `172.16.0.0/12` (redes internas Docker) e `192.168.0.0/16` (redes domésticas).
      * **Não são roteáveis na Internet pública:** São exclusivos para utilização dentro de redes locais (LANs).
  * **Endereços IP Públicos:**
      * Globalmente únicos no mundo e diretamente acessíveis na Internet (ex.: `8.8.8.8` da Google ou `193.136.172.10` da UA).

-----

## E o IPv6?

O IPv4 só permite cerca de **4 mil milhões** de endereços — e já esgotaram! O **IPv6** foi criado para "nunca mais acabar":

::::: columns
::: {.column width="56%"}

  * **Formato e Estrutura do Endereço:**
      * Usa **8 blocos hexadecimais** separados por dois-pontos (`:`), com 128 bits:
        `2001:0db8:85a3::8a2e:0370:7334`
      * *(A notação `::` é um atalho para omitir blocos consecutivos de zeros).*
  * **Endereços IPv6 que deve reconhecer:**
      * **`::1`** $\rightarrow$ O **`localhost`** do IPv6 (equivalente ao `127.0.0.1`).
      * **`fe80::...`** (*Link-Local*) $\rightarrow$ Gerado automaticamente pela placa para comunicar na LAN.
      * **`fd00::...`** (*Unique Local*) $\rightarrow$ O equivalente aos **endereços privados** de IPv4 (redes internas).

:::
::: {.column width="44%"}

\begin{center}
\includegraphics[width=\linewidth,height=0.68\textheight,keepaspectratio]{figures/ipv4vsipv6.png}

\vspace{0.2em}
{\tiny \textit{IPv4 (32 bits) vs. IPv6 (128 bits).}}
\end{center}

:::
:::::

-----

## O IP Chega ao Computador, a Porta Chega ao Programa

Vários programas comunicam em simultâneo no mesmo PC: o **IP** identifica a máquina e a **Porta (Camada 4)** identifica a aplicação de destino.

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.78\textheight,keepaspectratio]{figures/network_ip_port_analogy.png}
\end{center}

-----

## Portas Frequentes e Mapeamento de Portas (Docker)

Cada ligação é identificada pelo par **`IP:Porta`** (portas de `0` a `65535`, ex.: `192.168.1.10:80`):

::::: columns
::: {.column width="52%"}

  * **Portas Frequentes:**
      * **`22`:** SSH (Terminal remoto e Git)
      * **`53`:** DNS (Tradução de nomes)
      * **`80` / `443`:** HTTP / HTTPS (Web e APIs)
      * **`3000`, `5000`, `8000`, `8080`:** Desenvolvimento local (Node.js, Flask, FastAPI)

:::
::: {.column width="48%"}

  * **Mapeamento no Docker (`-p`):**
      * Exemplo:
        ```bash
        docker run -p 8080:80 nginx
        ```
      * Encaminha o tráfego da porta `8080` do anfitrião (*host*) para a porta `80` do contentor.

:::
:::::

-----

## Para Pensar: Vários Serviços Web na Mesma Porta 80?

Se a regra da rede é *"uma única aplicação por porta"*, surge uma questão prática incontornável:

  * **O Dilema:**
      * Num servidor queremos alojar múltiplos serviços Web (ex.: `ua.pt`, `moodle.ua.pt` e `mail.ua.pt`).
      * Todos são serviços Web públicos e os browsers acedem por defeito à **porta `80` (HTTP)** ou **`443` (HTTPS)**, sem que o utilizador escreva números estranhos no URL (como `:8080`).
      * **Se só temos uma porta `80` no servidor, como podemos distinguir e entregar os pedidos aos serviços certos?**

\vspace{0.8em}

  * **Trabalho de Pesquisa:**
      * Como resolvem as empresas e equipas de engenharia este problema no mundo real?
      * Fica para pesquisa autónoma o estudo dos conceitos de **Proxy** e **Reverse Proxy** (ex.: *Nginx*, *Traefik*, *HAProxy* ou *Caddy*).

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte III: Configuração de IP (DHCP vs. Estático) e DNS}}
\end{center}

-----

## Configuração de IP: Automática (DHCP) vs. Manual (Estático)

Para comunicar na rede e na Internet, qualquer dispositivo precisa de **4 parâmetros**:
**1. Endereço IP** | **2. Máscara de Sub-rede** | **3. Default Gateway** | **4. Servidor DNS**.

::::: columns
::: {.column width="50%"}

  * **Configuração Automática — DHCP (Clientes):**
      * Ao ligar ao Wi-Fi ou cabo, o dispositivo não tem IP.
      * O protocolo **DHCP** pede automaticamente os 4 parâmetros ao Router:
          1. *Cliente:* "Alguém me atribui um IP?" (*Discover*)
          2. *Servidor DHCP (Router):* "Usa o `192.168.1.50` durante 24 horas!" (*Offer / ACK*)

:::
::: {.column width="50%"}

  * **Configuração Manual — IP Estático (Servidores):**
      * Se o IP de um **servidor**, router ou impressora mudasse todos os dias, ninguém o conseguia contactar.
      * O administrador reserva uma faixa para clientes via DHCP (ex.: `.100` a `.200`) e configura um **IP Estático** fixo nos servidores (ex.: `.10`) e no próprio Router (`.1`).

:::
:::::

-----

## A "Lista Telefónica" da Internet: DNS (*Domain Name System*)

Nós memorizamos nomes (`ua.pt`, `google.com`), mas os pacotes de rede só encaminham por números (`193.136.172.10`):

  * **O que é o DNS:**
      * Serviço que traduz **Nomes de Domínio $\rightarrow$ Endereços IP** antes de qualquer ligação ser iniciada.
      * **Registos principais:**
          * **`A`:** Nome $\rightarrow$ Endereço IPv4.
          * **`AAAA`:** Nome $\rightarrow$ Endereço IPv6.
          * **`CNAME`:** Atalho (*alias*) de um nome para outro domínio.
  * **Resolução de nomes no dia a dia:**
      1. **Ficheiro `/etc/hosts`:** Tabela local no computador consultada **antes** de perguntar ao servidor DNS externo.
      2. **Nomes `.local` (mDNS):** Descoberta automática de máquinas na mesma LAN sem servidor central (ex.: `raspberrypi.local`).
      3. **DNS interno do Docker:** Na Aula 04, ligar à base de dados pelo nome `db` funcionou graças ao servidor DNS embutido no Docker!

-----

## A Hierarquia do DNS: A "Árvore" de Servidores

Não existe um único servidor com todos os nomes do mundo: o DNS organiza-se numa **árvore hierárquica distribuída**, resolvida da direita para a esquerda (ex.: `elearning.ua.pt.`):

\vspace{0.2em}

\begin{center}
\includegraphics[width=\linewidth,height=0.76\textheight,keepaspectratio]{figures/network_dns_hierarchy_tree.png}
\end{center}

-----

\vspace{5em}

\begin{center}
{\LARGE \textbf{Parte IV: Configuração, Diagnóstico (Debug) e Acesso Remoto}}
\end{center}

-----

## Onde Ver e Configurar a Rede no Linux

No Ubuntu / Linux, existem três formas principais de ver ou alterar as configurações de rede:

  * **1. Ambiente Gráfico Desktop (NetworkManager):**
      * O ícone de Wi-Fi / Rede no canto superior direito do Ubuntu (ou o comando `nmcli` / `nmtui` no terminal) permite escolher entre DHCP automático ou definir um IP Estático e DNS.
  * **2. Inspecionar Interfaces e Rotas no Terminal (`ip`):**
      * `ip addr show` (ou simplesmente **`ip a`**): Mostra todas as placas de rede, o endereço MAC (`link/ether`) e o endereço IP com máscara (`inet`).
      * `ip route show` (ou simplesmente **`ip r`**): Mostra por que porta saem os pacotes e qual é o seu **Default Gateway** (`default via ...`).
  * **3. Ver que Servidor DNS está a ser usado:**
      * Pode consultar o ficheiro `/etc/resolv.conf` ou executar `resolvectl status`.

-----

## Ferramentas de Diagnóstico (I): `ping` e `traceroute`

Quando algo não comunica, estas são as duas primeiras ferramentas a usar no terminal:

::::: columns
::: {.column width="50%"}

  * **`ping` — "Estás aí e quanto demoras?"**
      * Envia pequenos pacotes de teste (ICMP) e mede o tempo de ida e volta (**latência** em milissegundos, `ms`).
      * Dica: Use sempre `-c 4` no Linux para enviar apenas 4 pacotes e parar!
      ```bash
      $ ping -c 4 8.8.8.8
      64 bytes from 8.8.8.8: time=8.2 ms
      ```

:::
::: {.column width="50%"}

  * **`traceroute` — "Por onde vais e onde bloqueias?"**
      * Mostra todos os routers (**saltos** / *hops*) pelos quais o pacote passa desde o seu portátil até ao destino.
      * Excelente para ver se o bloqueio está logo no seu router de casa (salto 1) ou lá fora na operadora.
      ```bash
      $ traceroute 8.8.8.8
       1  192.168.1.1 (Router)  1.2 ms
       2  10.254.0.1 (Operador) 6.4 ms
      ```

:::
:::::

-----

## Ferramentas de Diagnóstico (II): `dig`, `ss`, `nmap` e `curl`

Para diagnosticar problemas de nomes (DNS), portas ou servidores que não respondem:

  * **`dig` (Testar a tradução DNS):**
      * Pergunta diretamente ao DNS qual é o IP de um site: `dig ua.pt +short` (ou `dig -x 8.8.8.8 +short` para descobrir o nome a partir de um IP).
  * **`ss -tuln` (Ver que Portas estão abertas na MINHA máquina):**
      * Mostra todos os servidores que estão a escutar por ligações TCP (`-t`) ou UDP (`-u`) neste momento no seu computador.
  * **`nmap` (Descobrir que Portas estão abertas numa máquina alvo):**
      * Faz um *scan* para ver que portas aceitam ligação (ex.: `nmap localhost`). *(Nota: Só deve ser usado nas suas próprias máquinas ou em alvos autorizados de teste como `scanme.nmap.org`).*
  * **`curl -I` (Testar um Servidor Web / API sem browser):**
      * Faz um pedido HTTP rápido e mostra se o servidor devolve `200 OK` ou erro: `curl -I http://localhost:8000`.

-----

## Firewalls e Isolamento de Clientes (O Caso da `eduroam`)

Mesmo com o IP correto e o servidor a correr na porta certa, a ligação pode ser recusada por **regras de segurança**:

  * **Firewall (no Sistema Operativo ou na Rede):**
      * Filtra o tráfego por **porta** e **direção** (ex.: `ufw` no Linux ou Firewall do Windows).
      * Por defeito, permite ligações de saída (ex.: aceder a sites na porta `443`), mas **bloqueia ligações de entrada** em portas não autorizadas (ex.: porta `8000`).

  * **Isolamento de Clientes (*Client Isolation*) na `eduroam`:**
      * Redes Wi-Fi públicas ou universitárias (como a **`eduroam`**) impedem, por segurança, a comunicação direta entre dispositivos na mesma WLAN.
      * **Consequência prática:** Dois portáteis na `eduroam` conseguem aceder à Internet, mas **não conseguem ligar diretamente um ao outro**!

-----

## Guia de Sobrevivência: Como Fazer Debug de Rede em 5 Passos

Perante uma falha de comunicação na rede, siga esta ordem lógica de diagnóstico (*bottom-up*):

\vspace{0.15em}

\begin{center}
\begin{tikzpicture}[
    stepbox/.style={rectangle, draw=black!75, rounded corners=3pt, thick, text width=11.2cm, minimum height=0.76cm, inner sep=3.5pt, align=left, font=\scriptsize},
    arr/.style={-{Latex[length=1.6mm]}, thick, color=uagreen!80!black}
]
\node[stepbox, fill=black!5]    (s1) at (0, 4.08) {\textbf{Passo 1 — A placa de rede está ativa e tem IP?}\\Execute \texttt{ip a}. Sem IP atribuído, verifique o cabo/Wi-Fi ou o servidor DHCP.};
\node[stepbox, fill=uagreen!12] (s2) at (0, 3.06) {\textbf{Passo 2 — Chego ao meu Default Gateway (Router)?}\\Consulte o gateway com \texttt{ip r} e teste a rede local com \texttt{ping -c 4 <IP\_Gateway>}.};
\node[stepbox, fill=blue!10]    (s3) at (0, 2.04) {\textbf{Passo 3 — Tenho saída para a Internet (por endereço IP)?}\\Execute \texttt{ping -c 4 8.8.8.8} (ou \texttt{traceroute}). Se falhar, o problema está no encaminhamento externo.};
\node[stepbox, fill=orange!12]  (s4) at (0, 1.02) {\textbf{Passo 4 — O servidor DNS está a traduzir nomes?}\\Se \texttt{ping 8.8.8.8} funciona mas \texttt{ping ua.pt} falha $\rightarrow$ falha de DNS (teste com \texttt{dig ua.pt}).};
\node[stepbox, fill=red!10]     (s5) at (0, 0.00) {\textbf{Passo 5 — O serviço está a escutar na porta certa e sem Firewall?}\\Confirme com \texttt{ss -tuln} (local), \texttt{nmap}/\texttt{curl -I} (remoto) e verifique se a Firewall bloqueia a porta.};

\draw[arr] (s1.south) -- (s2.north);
\draw[arr] (s2.south) -- (s3.north);
\draw[arr] (s3.south) -- (s4.north);
\draw[arr] (s4.south) -- (s5.north);
\end{tikzpicture}
\end{center}

\vspace{0.15em}

  * **Inspeção profunda de tráfego:** Quando é necessário analisar os pacotes reais ao detalhe, utilizam-se analisadores de pacotes como o **Wireshark** (interface gráfica) ou o **`tcpdump`** (terminal).

-----

## Trabalho Remoto Seguro (I): SSH e Sincronização com `rsync`

Na engenharia informática, quase todos os servidores Linux correm na nuvem sem ecrã nem rato. Como trabalhamos neles a partir do nosso portátil?

  * **1. Ligar ao terminal remoto com `ssh` (*Secure Shell* — Porta 22):**
      * Abre um terminal totalmente encriptado dentro do servidor remoto (usando o par de chaves pública/privada `ed25519` que criaram na aula de Git!):
      ```bash
      # Ligar ao utilizador 'student' na máquina remota (na porta 2222)
      $ ssh student@localhost -p 2222
      ```
  * **2. Enviar e sincronizar pastas com `rsync` (sobre SSH):**
      * Esqueça protocolos antigos e inseguros como o FTP. O **`rsync`** é inteligente: compara a sua pasta local com a do servidor e **envia apenas os ficheiros (ou pedaços) que mudaram**!
      ```bash
      # -a: preserva permissões; -v: mostra ficheiros; -z: comprime; -P: barra de progresso
      $ rsync -avzP -e "ssh -p 2222" ./meu-projeto/ student@servidor:~/projetos/
      ```

-----

## Trabalho Remoto Seguro (II): Túneis SSH e VS Code Remote

E se um servidor remoto tiver uma aplicação web interna a correr em `localhost:8000`, mas a porta `8000` estiver bloqueada pela Firewall para ninguém da Internet entrar?

  * **O "Superpoder" do Túnel SSH (*Local Port Forwarding* — `-L`):**
      * Podemos criar um "tubo secreto" dentro da ligação SSH que liga a porta `8080` do nosso portátil diretamente à porta `8000` lá dentro do servidor:
      ```bash
      $ ssh -N -L 8080:localhost:8000 student@servidor -p 2222
      ```
      * Agora basta abrir o browser do nosso portátil em **`http://localhost:8080`** e vemos a página interna do servidor em total segurança!
  * **VS Code Remote - SSH:**
      * A extensão oficial *Remote - SSH* do VS Code usa exatamente este mecanismo: abre o editor gráfico no seu portátil, mas edita os ficheiros e corre os programas diretamente dentro do servidor remoto!
