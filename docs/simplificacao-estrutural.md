# Jarvis Mark 52 — Simplificação Estrutural

Data: 04/09/2026
Branch: `jarvis-dev`
Status: Etapa 07 em andamento

## Objetivo

Reduzir sobreposição, chamadas desnecessárias de IA e funcionalidades fora do escopo da v0.1 sem quebrar o baseline funcional.

## Regra

Não refatorar `main.py` ou `ui.py` apenas por serem grandes. Primeiro retirar exposição desnecessária, eliminar caminhos redundantes e preservar interfaces estáveis.

## Simplificações aprovadas para execução

### 1. `actions/desktop.py`

Manter:

- wallpaper;
- wallpaper por URL;
- wallpaper atual;
- listar Desktop;
- estatísticas;
- organizar;
- limpar/arquivar.

Remover da rota operacional:

- ação genérica `task` baseada em código Python gerado pelo Gemini;
- fallback que envia qualquer `action` desconhecida ao Gemini.

Motivo: `computer_control.py`, `computer_settings.py` e `file_controller.py` já cobrem ações determinísticas. Gerar código para tarefas genéricas aumenta custo, risco e sobreposição.

### 2. `actions/dev_agent.py`

Retirar da superfície de tools da v0.1.

Motivo: desenvolvimento autônomo completo não é função do Jarvis operacional e já é coberto por ferramentas de desenvolvimento dedicadas. O arquivo pode permanecer temporariamente no repositório até validar que nenhuma dependência indireta existe.

### 3. `actions/game_updater.py`

Retirar da superfície de tools da v0.1.

Motivo: baixa aderência ao objetivo atual. Não deve ocupar prompt/tool schema nem manutenção operacional.

### 4. `actions/computer_control.py`

Manter como camada de interação direta:

- mouse;
- teclado;
- clipboard;
- hotkeys;
- screenshot;
- foco de janela.

Manter `screen_find` apenas como fallback visual sob demanda. Não usar Gemini para operações que possuem coordenada, hotkey ou ação determinística.

### 5. `actions/computer_settings.py`

Manter como camada de configurações e atalhos do sistema. Não misturar com automação visual.

### 6. `actions/browser_control.py`

Manter separado. Playwright tem semântica própria e é preferível a coordenadas de tela para navegação estruturada.

### 7. `actions/file_controller.py`

Manter separado de desktop/computer control. É a camada oficial para manipulação de arquivos e undo.

## Limites de responsabilidade após simplificação

| Módulo | Responsabilidade |
|---|---|
| `computer_settings.py` | configurações e atalhos do sistema operacional |
| `computer_control.py` | mouse, teclado, clipboard e visão pontual |
| `browser_control.py` | automação estruturada de navegador |
| `file_controller.py` | arquivos/pastas + undo |
| `desktop.py` | funções específicas do Desktop, sem agente genérico |
| `plugin_loader.py` | novas capacidades isoladas |

## Ordem de alteração

1. retirar rotas genéricas/IA de `desktop.py`;
2. retirar `dev_agent` e `game_updater` da superfície de tools em `main.py` sem apagar arquivos inicialmente;
3. smoke test do baseline;
4. validar imports/referências;
5. somente então apagar código órfão, se realmente não houver dependência;
6. atualizar inventário e documentação.

## Critério de saída da Etapa 07

A etapa só será marcada como concluída depois de:

- nenhuma tool removida continuar declarada ou importada no `main.py`;
- nenhuma referência quebrada existir;
- Jarvis iniciar normalmente;
- Gemini Live, voz, busca, clima, status do PC, arquivos e ações Windows essenciais continuarem operacionais;
- redução de chamadas Gemini auxiliares ser confirmada no fluxo;
- smoke test mínimo passar.

Nenhum merge em `main` será feito nesta etapa.
