# Plano de Aula: Class 07 — Redes Informáticas: Fundamentos, Configuração & Diagnóstico

Este documento estabelece o plano pedagógico, curricular e técnico para a **Class 07 (Módulo C4 — Configuração de Redes Locais IP)**, desenhado especificamente para estudantes do **1.º ano (1.º semestre)** sem conhecimentos prévios de redes de computadores.

---

## 1. Justificação Curricular & Pedagógica

* **Público-Alvo (1.º Ano sem Base Prévia de Redes):** A abordagem evita o formalismo pesado de uma unidade curricular avançada de redes (sem cálculos binários exaustivos de sub-redes, sem protocolos de encaminhamento dinâmico de operadoras como OSPF/BGP e sem listas extensas de protocolos obsoletos). O foco está na construção de um **modelo mental intuitivo e sólido** que permita perceber como os dados viajam, configurar uma rede básica e diagnosticar problemas (*troubleshooting*).
* **Consolidação Retroativa ("Ligar os Pontos" com as Aulas 01 a 06):** Ao longo das primeiras semanas, os estudantes já utilizaram conceitos de rede de forma instrumental:
  * **Aula 02 (Linux II):** Chamadas HTTP com `curl` à API do Gemini.
  * **Aula 03 (Virtualização):** Modos de rede *NAT* vs. *Bridged* nas máquinas virtuais.
  * **Aula 04 (Docker):** Mapeamento de portas (`-p 8080:80`) e redes privadas com resolução automática de nomes no Docker Compose.
  * **Aula 05 (Flatpak):** Concessão da permissão `--share=network` na *sandbox*.
  * **Aula 06 (Git & GitHub):** Geração de chaves criptográficas SSH (`ed25519`) e autenticação remota em `git@github.com`.
  Esta aula desmistifica finalmente o que acontece "por baixo do capô" em cada uma dessas operações.
* **Ponte Direta para a Class 08 (Programação em Redes) e Class 09 (Web):**
  * Na **Class 08**, os estudantes vão programar **Sockets TCP e UDP** em Python, associar servidores a endereços e portas (`bind('127.0.0.1', 65432)` vs. `0.0.0.0`), construir **APIs REST com FastAPI** (`localhost:8000`) e interligar aplicações entre colegas na sala de aula através da rede Wi-Fi `TheOffice` (contornando o isolamento de clientes da rede `eduroam`).
  * Para evitar duplicações, tópicos que já possuem secções inteiras dedicadas nas aulas seguintes — como **MQTT** (lecionado a fundo na Class 08) e **Reverse Proxy com NGINX** (lecionado a fundo na Class 09) — são deixados para o seu momento próprio, mantendo a Class 07 enxuta e focada.

---

## 2. Objetivos de Aprendizagem

Ao concluir esta sessão, o estudante deverá ser capaz de:
1. **Distinguir Escalas de Rede (PAN, LAN, MAN, WAN):** Compreender a hierarquia concêntrica desde o espaço pessoal (PAN) e redes locais (LAN) até às áreas metropolitanas (MAN) e à Internet global (WAN), identificando a função prática de um **Switch**, **Access Point (AP)**, **Router** e **ONT (Modem de Fibra)**.
2. **Compreender o Modelo OSI (7 Camadas) e o Encapsulamento:** Relacionar as 7 camadas padronizadas (Física a Aplicação) e compreender como os dados são encapsulados/desencapsulados com cabeçalhos em cada camada.
3. **Diferenciar Endereço MAC de Endereço IP e Compreender o Roteamento:** Explicar a diferença entre entrega física local salto a salto (MAC / Camada 2 / Switch) e endereçamento lógico fim a fim (IP / Camada 3 / Routers), bem como o papel do **Default Gateway** e do protocolo **ARP**.
4. **Interpretar Endereços IPv4 e Máscaras de Sub-rede:** Compreender intuitivamente a notação `/24` (`255.255.255.0`) para distinguir se um destinatário está na mesma rede local ("mesma rua") ou numa rede externa.
5. **Dominar os Endereços IP Especiais e o IPv6:** Distinguir `127.0.0.1` (`localhost`), endereços de rede (`.0`) e broadcast (`.255`), **IPs Privados** (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) e **IPs Públicos**, bem como reconhecer a estrutura do **IPv6** (`::1`, `fe80::` e `fd00::`).
6. **Compreender Portas Lógicas (Camada 4):** Explicar como as portas (`0–65535`) direcionam o tráfego para a aplicação correta dentro do computador (`IP:Porta`), relacionando-as com o mapeamento `-p` do Docker e o desafio de múltiplos serviços na mesma porta (*Proxy* / *Reverse Proxy*).
7. **Explicar a Configuração de IP e Resolução de Nomes (DHCP e DNS):** Descrever os 4 parâmetros essenciais de rede, como um dispositivo obtém configuração automática via **DHCP** vs. **IP Estático**, como o **DNS** traduz nomes em endereços IP e como se organiza a árvore hierárquica de servidores DNS.
8. **Aplicar uma Metodologia Sistemática de Debug de Rede:** Utilizar ferramentas de linha de comandos (`ip`, `ping`, `traceroute`, `dig`, `ss`, `nmap`, `curl`) para isolar falhas de conectividade, DNS ou portas bloqueadas por **Firewalls / Isolamento de Clientes**.
9. **Executar Operações Remotas Seguras com SSH:** Aceder a servidores Linux remotos via **SSH** com chaves criptográficas, sincronizar projetos com **`rsync`** e criar **Túneis SSH (`ssh -L`)** para aceder a serviços internos isolados.

---

## 3. Gestão Temporal (Aula de 3 Horas = 180 min)

* **0h00 – 0h45 (45 min): Bloco Teórico I — A Arquitetura da Rede, Endereços (MAC, IP, Sub-rede) & Portas**
  * Escalas de rede (PAN, LAN, MAN, WAN) e equipamentos do quotidiano (Switch, Access Point, Router, ONT).
  * O Modelo OSI (7 camadas) e o mecanismo de encapsulamento/desencapsulamento.
  * MAC vs. IP, roteamento prático (Switch vs. Routers), *Default Gateway* e protocolo ARP.
  * IPv4 e Máscara de Sub-rede (`/24`): a regra da "rua" e do "número da porta".
  * IPs especiais (`127.0.0.1`, rede/broadcast, Privados vs. Públicos) e estrutura do IPv6 (`::1`, `fe80::`, `fd00::`).
  * Portas de transporte (`22`, `53`, `80`, `443`, `8000`), mapeamento no Docker (`-p 8080:80`) e desafio de *Reverse Proxy*.
* **0h45 – 0h55 (10 min): Intervalo**
* **0h55 – 1h35 (40 min): Bloco Teórico II — Configuração de Rede (DHCP, Estático), DNS, Diagnóstico & SSH**
  * Como o computador ganha rede: os 4 parâmetros, DHCP vs. IP Estático.
  * A lista telefónica da Internet: **DNS**, `/etc/hosts`, `.local` (mDNS), DNS interno do Docker e a árvore hierárquica de servidores DNS.
  * Ferramentas de configuração e diagnóstico na CLI (`ip`, `ping`, `traceroute`, `dig`, `ss`, `nmap`, `curl`).
  * Firewalls e isolamento em redes Wi-Fi (`eduroam`) + fluxograma de Debug em 5 passos e nota sobre Wireshark/`tcpdump`.
  * Administração remota com **SSH**, sincronização com **`rsync`** e **Túneis SSH (`ssh -L`)**.
* **1h35 – 2h50 (75 min): Trabalho Prático Orientado**
  * Execução acompanhada do guião laboratorial (Partes 0 a 5).
* **2h50 – 3h00 (10 min): Síntese e Preparação para a Class 08**
  * Revisão rápida dos erros mais comuns de rede que vão encontrar na programação de sockets e APIs na aula seguinte.

---

## 4. Estrutura dos Slides (`00_slides/slides_pt_00.md`)

1. **Visão Geral da Sessão:** Resumo estruturado das 4 partes da aula.
2. **Separador — Parte I: Como se Constrói uma Rede? (Do Portátil à Internet)**
3. **O Que é uma Rede? PAN, LAN, MAN e WAN:** A hierarquia geográfica e arquitetural desde os dispositivos pessoais em torno do utilizador (PAN) e da rede do edifício/casa (LAN) até à área metropolitana da cidade (MAN) e à rede global da Internet (WAN), acompanhada por ilustração infográfica isométrica.
4. **Equipamentos da Rede Local: Switch e Access Point:** Como os dispositivos se ligam por cabo (Switch vs. antigo Hub) e sem fios (AP Wi-Fi).
5. **A Fronteira com a Internet: Router e ONT:** Como a nossa LAN se liga à operadora (fibra ótica $\rightarrow$ ONT $\rightarrow$ Router) e o aparelho 4-em-1 doméstico.
6. **Como a Rede se Organiza: O Modelo OSI (7 Camadas):** O modelo concetual padronizado pela ISO com 7 camadas (Física a Aplicação) e o fluxo de encapsulamento e desencapsulamento entre dispositivos.
7. **Separador — Parte II: Endereços e Portas (Encontrar a Máquina e o Programa)**
8. **Dois Endereços em Cada Dispositivo: MAC vs. IP:** Identidade física no enlace local (*hop-by-hop*) vs. endereço lógico fim a fim (*end-to-end*).
9. **Roteamento na Prática: Envio Local (Switch) vs. Salto a Salto (Routers):** Esquema visual em ecrã inteiro `network_routing_mac_vs_ip.png` contrastando o fluxo direto na mesma LAN com o encaminhamento salto a salto pelos Routers.
10. **Como Funciona o Roteamento: O Papel do Gateway e do ARP:** Comunicação remota via *Default Gateway*, comunicação local direta via Switch e descoberta de endereços MAC com o protocolo ARP.
11. **Endereço IPv4 e a Máscara de Sub-rede (Simplificado):** O que significa `192.168.1.10/24` (`255.255.255.0`) explicado sem matemática binária pesada (a Rua vs. o Número da Porta).
12. **IPs Especiais e Gamas de Rede:** `127.0.0.1` (`localhost` / loopback), endereços de rede e broadcast (`.0` e `.255`), IPs Privados (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) e IPs Públicos.
13. **E o IPv6?:** Por que surgiu, estrutura hexadecimal (128 bits), `::1` (`localhost`), `fe80::` (link-local) e `fd00::` (unique local / privado).
14. **O IP Chega ao Computador, a Porta Chega ao Programa:** Introdução concisa ao problema de múltiplos programas num só PC e a infografia `network_ip_port_analogy.png` (os computadores como prédios e os programas como portas/caixas de correio).
15. **Portas Frequentes e Mapeamento de Portas (Docker):** A notação `IP:Porta` (`0–65535`), portas padrão (`22`, `53`, `80`, `443`, `8000`) e a aplicação prática no Docker (`-p 8080:80`).
16. **Para Pensar: Vários Serviços Web na Mesma Porta 80?:** O dilema de múltiplos sites/serviços no mesmo IP/porta e desafio de pesquisa autónoma sobre *Proxy* e *Reverse Proxy*.
17. **Separador — Parte III: Configuração de IP (DHCP vs. Estático) e DNS**
18. **Configuração de IP: Automática (DHCP) vs. Manual (Estático):** Os 4 parâmetros essenciais (IP, Máscara, Gateway, DNS), atribuição automática (DHCP) vs. manual (servidores).
19. **A "Lista Telefónica" da Internet: DNS (*Domain Name System*):** Tradução de nomes (`ua.pt`) em IPs, registos principais (`A`, `AAAA`, `CNAME`), `/etc/hosts`, `.local` (mDNS) e o DNS interno do Docker.
20. **A Hierarquia do DNS: A "Árvore" de Servidores:** Estrutura distribuída em árvore (`.` Raiz $\rightarrow$ TLD `.pt` $\rightarrow$ Autoritativo `ua.pt` $\rightarrow$ Subdomínio `elearning.ua.pt`) com a figura `network_dns_hierarchy_tree.png`.
21. **Separador — Parte IV: Configuração, Diagnóstico (Debug) e Acesso Remoto**
22. **Onde Ver e Configurar a Rede no Linux:** NetworkManager (GUI/`nmcli`) e inspeção rápida no terminal (`ip a`, `ip r`, `/etc/resolv.conf`).
23. **Ferramentas de Diagnóstico (I): `ping` e `traceroute`:** Testar se um destino responde, medir a latência (ms) e descobrir em que salto a rede falha.
24. **Ferramentas de Diagnóstico (II): `dig`, `ss`, `nmap` e `curl`:** Testar nomes DNS, verificar se o nosso servidor está mesmo a escutar (`ss -tuln`), testar portas (`nmap`) e pedidos Web (`curl -I`).
25. **Firewalls e Isolamento de Clientes (O Caso da `eduroam`):** Filtragem de tráfego por porta/direção e por que razão dois portáteis na `eduroam` não comunicam diretamente entre si (*Client Isolation*).
26. **Guia de Sobrevivência: Como Fazer Debug de Rede em 5 Passos:** Fluxograma prático de diagnóstico *bottom-up* passo a passo e nota sobre inspeção profunda de tráfego com **Wireshark** / **`tcpdump`**.
27. **Trabalho Remoto Seguro (I): SSH e Sincronização com `rsync`:** Ligar a servidores remotos por chave SSH e sincronizar pastas enviando apenas diferenças (`rsync -avzP`).
28. **Trabalho Remoto Seguro (II): Túneis SSH e VS Code Remote:** Encaminhar portas de forma segura (`ssh -L`) para aceder a serviços internos fechados e desenvolver remotamente no VS Code.

---

## 5. Estrutura do Guião Prático (`01_exercises/exercises_pt_00.md`)

* **Preparação do Diretório de Trabalho:** Criação de `~/IEI/aula07`.
* **Parte 0 — Preparação do Ambiente & Servidor de Teste (Docker SSH):**
  * Passo 1: Instalação dos utilitários de diagnóstico de rede em Linux (`apt`) e macOS (`brew install nmap iproute2mac`).
  * Passo 2: Verificação ou geração de par de chaves criptográficas SSH (`ed25519`).
  * Passo 3: Instanciação de um servidor OpenSSH isolado em Docker Compose na porta `2222`.
* **Parte 1 — Inspeção da Máquina Local e da Rede Local (LAN):**
  * **Exercício 1:** Identificar endereço MAC, endereço IPv4/IPv6 e máscara de sub-rede `/24` (`ip a` no Linux / `ifconfig` no macOS).
  * **Exercício 2:** Verificar a pilha TCP/IP local (`ping -c 4 127.0.0.1` e `ping -c 4 ::1` / `ping6 -c 4 ::1`).
  * **Exercício 3:** Identificar o *Default Gateway* (`ip route show default` / `netstat -rn -f inet | grep default` / `route -n get default`) e testar a conectividade na LAN (`ping`).
  * **Exercício 4:** Inspecionar a resolução de endereços na tabela ARP (`ip neigh` / `arp -an`).
* **Parte 2 — Da Rede Local para a Internet (WAN, NAT e DNS):**
  * **Exercício 5:** Testar a conectividade externa por endereço IP (`ping 8.8.8.8`) vs. nome de domínio (`ping ua.pt`) e analisar a latência.
  * **Exercício 6:** Rastreio da rota de encaminhamento (`traceroute 8.8.8.8` e `traceroute ua.pt`).
  * **Exercício 7:** Resolução de nomes de domínio com `dig` (`dig ua.pt A +short`, `dig -x 8.8.8.8 +short`) e inspeção de `/etc/hosts`.
  * **Exercício 8:** Determinação do Endereço IP Público e análise do mecanismo de **NAT** (`curl -s https://ipinfo.io/json`).
* **Parte 3 — Portas, Serviços e Diagnóstico de Ligações (`ss` / `lsof`, `nmap`, `127.0.0.1` vs. `0.0.0.0`):**
  * **Exercício 9:** Inspecionar portas em estado de escuta (*LISTEN*) no sistema local (`ss -tuln` no Linux / `lsof -nP -iTCP -sTCP:LISTEN` no macOS, e `nmap localhost`).
  * **Exercício 10 (Associação de Serviços a Interfaces — Preparação para a Class 08):** Explicação técnica de `0.0.0.0` (`INADDR_ANY`) e teste experimental de um servidor HTTP Python associado a `127.0.0.1` vs. `0.0.0.0`, inspecionando o *socket* com `ss`/`lsof` e `curl -I`.
  * **Exercício 11:** Sondagem de portas num servidor público de teste autorizado (`nmap scanme.nmap.org`).
* **Parte 4 — Administração Remota Segura (SSH, `rsync` e Encaminhamento de Portas SSH):**
  * **Exercício 12:** Estabelecer sessão remota via `ssh` (`ssh student@localhost -p 2222`).
  * **Exercício 13:** Sincronização incremental de diretórios com `rsync` (`rsync -avzP -e "ssh -p 2222"`).
  * **Exercício 14 (Encaminhamento Local de Portas via Túnel SSH — *Local Port Forwarding*):** Execução de um servidor HTTP interno no contentor na porta `8000` (não exposta no Docker) e criação de um túnel SSH (`ssh -N -L 8080:localhost:8000 student@localhost -p 2222`) para acesso local em `http://localhost:8080`.
* **Parte 5 — Exercícios Complementares de Consolidação:**
  * **Desafio A:** Captura e inspeção de pacotes ICMP em tempo real com `sudo tcpdump -i any icmp -n`.
  * **Desafio B:** Representação geográfica de rotas IP (Geo-Traceroute).
* **Síntese dos Comandos Abordados:** Tabela de referência técnica (Linux e macOS).

