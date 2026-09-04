# Jarvis Mark 52 — Arquitetura Atual

Data do levantamento: 04/09/2026
Branch de trabalho: `jarvis-dev`

## Objetivo

Registrar a arquitetura real do Mark LII antes de qualquer simplificação estrutural. Este documento é descritivo: não propõe refatoração prematura.

## Fluxo principal

```text
Usuário
  ↓ voz / texto
ui.py
  ↓
main.py
  ↓
Gemini Live API
  ↓
Tool routing
  ├─ actions/*
  ├─ core/*
  ├─ plugins/*
  ├─ memory/*
  └─ dashboard/*
```

## Componentes

| Componente | Responsabilidade atual | Dependências / integração | Observação inicial |
|---|---|---|---|
| `main.py` | Orquestra sessão Gemini Live, áudio, prompt, tools, plugins, memória e monitoramento | `ui`, `actions`, `core`, `memory`, Google Gemini | Principal ponto de acoplamento; preservar funcionalidade antes de dividir |
| `ui.py` | HUD desktop, setup inicial, logs, entrada de texto, upload, controles, overlays e métricas | PyQt6, config, memory | Funcional e grande; não refatorar antes do inventário |
| `core/prompt.txt` | Regras de identidade, idioma, execução, memória e roteamento | Carregado por `main.py` | Ponto central de comportamento do agente |
| `core/plugin_loader.py` | Descoberta, validação, colisões, ativação e dispatch de plugins | `plugins/`, config | Boa extensão modular; candidato preferencial para novas capacidades |
| `core/confirm.py` | Gate de confirmação para ações irreversíveis | UI + actions | Deve ser preservado e ampliado conforme limites humanos |
| `core/undo.py` | Reversão de ações suportadas | actions / UI | Importante para confiabilidade |
| `core/audio_devices.py` | Seleção/configuração de dispositivos de áudio | sounddevice / UI | Essencial para operação por voz |
| `core/installer.py` | Instala dependências ausentes conforme configuração | pip / Playwright | Útil, mas requer limites claros para instalação automática |
| `actions/*` | Implementação das ferramentas operacionais | Windows, web, filesystem, browser, APIs | Camada prática de execução; precisa inventário por valor/risco |
| `plugins/*` | Extensões desacopladas do core | `plugin_loader` | Atualmente só template; excelente ponto para MSFS, God's Eye View e futuras integrações |
| `memory/memory_manager.py` | Memória persistente local, trimming, prompt reduzido e recall sob demanda | JSON local | Boa separação entre armazenamento e orçamento de contexto |
| `memory/config_manager.py` | Preferências/configuração operacional | arquivos locais | Deve ser considerado na futura centralização de configuração |
| `dashboard/server.py` | Dashboard remoto FastAPI, upload e controle via LAN | FastAPI, uvicorn, firewall/rede | Útil, porém pode alterar firewall/rede; requer regra de confirmação |
| `config/api_keys.json` | Chave Gemini e sistema operacional local | UI + main + dashboard | Segredo local; não deve ir ao GitHub |

## Fluxo de inicialização observado

```text
python main.py
  ↓
carrega UI e módulos
  ↓
verifica config/api_keys.json
  ↓ ausente
SetupOverlay → Gemini API Key + OS
  ↓
grava configuração local
  ↓
conecta Gemini Live
  ↓
carrega memória + prompt + tools + plugins
  ↓
abre streams de áudio
  ↓
JARVIS LISTENING
```

## Fluxo de solicitação

```text
Microfone / texto
  ↓
Gemini Live
  ↓
interpretação + seleção de tool
  ↓
main.py despacha
  ↓
action nativa OU plugin
  ↓
resultado retorna ao Gemini
  ↓
resposta textual/voz
  ↓
UI / Activity Log
```

## Pontos de integração confirmados

- Gemini Live API: núcleo de conversação e áudio em tempo real.
- Ferramentas nativas: declaradas/orquestradas em `main.py`, executadas em `actions/`.
- Plugins: carregados dinamicamente por `core/plugin_loader.py` e podem ser habilitados/desabilitados.
- Memória: persistência local em JSON, com pequena fatia enviada ao prompt e recall sob demanda.
- Dashboard remoto: FastAPI na rede local, porta 8000.
- Windows: diversas actions executam controle de sistema, arquivos, janelas, teclado, navegador e tarefas.

## Gargalos / riscos iniciais

1. `main.py` concentra muitas responsabilidades.
2. `ui.py` também é grande e mistura apresentação com algumas decisões operacionais.
3. Existem ferramentas com escopo sobreposto (`computer_settings`, `computer_control`, `desktop_control`, partes de `browser_control`).
4. Algumas actions podem executar mudanças de alto impacto no Windows e precisam de limites consistentes.
5. O dashboard pode alterar firewall/perfil de rede para acesso LAN.
6. Instalação automática de dependências é conveniente, mas deve ficar sob política explícita.
7. API/configuração ainda está distribuída entre arquivos locais e módulos diferentes.

## Decisão arquitetural provisória

Até concluir o inventário funcional:

- não dividir `main.py`;
- não reescrever `ui.py`;
- não remover actions;
- preservar `plugin_loader`, memória, confirmação e undo;
- preferir plugins para novas integrações específicas do Mauricio;
- qualquer simplificação será feita somente após comprovar sobreposição ou baixo valor.

## Critério para encerrar a Etapa 03

A Etapa 03 é considerada concluída quando estiverem registrados: fluxo de inicialização, fluxo de solicitação, responsabilidades principais, dependências, pontos de integração e gargalos iniciais. Este documento atende esses critérios e deve ser revisado se o inventário revelar dependências ocultas.
