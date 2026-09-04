# Jarvis Mark 52 — Inventário Funcional

Data inicial: 04/09/2026
Data de conclusão: 04/09/2026
Branch: `jarvis-dev`
Status: **Etapa 04 concluída**

## Objetivo

Classificar as capacidades atuais do Mark LII em **Manter**, **Adaptar**, **Remover candidato** ou **Estudar**, sem apagar ou refatorar código nesta etapa. O objetivo é definir o que realmente agrega valor ao Jarvis Mark 52 antes das etapas de custo, segurança e simplificação.

## Critério de classificação

- **Manter** — entrega valor claro e está alinhado ao Jarvis desejado.
- **Adaptar** — deve permanecer, mas precisa simplificação, limites, PT-BR, configuração ou integração.
- **Remover candidato** — baixa aderência ao nosso uso ou função melhor coberta por outra ferramenta; remoção somente após validação de dependências na Etapa 07.
- **Estudar** — utilidade, risco, custo ou dependência ainda não justificam decisão definitiva.

## Inventário final

| Área / módulo | Função | Classificação final | Decisão |
|---|---|---|---|
| `main.py` | Orquestra Gemini Live, áudio, tools, memória, plugins e monitoramento | Adaptar | É o núcleo funcional, mas concentra responsabilidades demais; não refatorar antes de mapear dependências e testes |
| `ui.py` | HUD desktop, setup, logs, comandos, upload e controles | Adaptar | Interface funcional; personalizar e simplificar sem reescrita precoce |
| `core/prompt.txt` | Identidade, idioma e regras do Jarvis | Adaptar | Deve refletir Mauricio, PT-BR, limites operacionais e filosofia do projeto |
| `core/plugin_loader.py` | Descoberta e execução de plugins | Manter | Boa separação; caminho preferencial para novas integrações |
| `core/confirm.py` | Confirmação de ações críticas | Manter | Base do limite entre autonomia e confirmação humana |
| `core/undo.py` | Reversão das alterações suportadas | Manter | Elemento central de segurança operacional |
| `core/audio_devices.py` | Entrada e saída de áudio | Manter | Essencial para operação por voz |
| `core/installer.py` | Instala dependências faltantes | Adaptar | Útil no setup, mas instalação automática deve ser explícita e controlada |
| `core/stt.py` | Speech-to-text alternativo/local | Estudar | Pode servir como fallback, porém Gemini Live já cobre o fluxo principal |
| `core/tts.py` | Text-to-speech alternativo/local | Estudar | Mesmo critério do STT; manter até avaliar fallback, latência e custo |
| `core/llm_client.py` | Cliente LLM auxiliar | Estudar | Pode representar caminho alternativo/redundante ao Gemini Live; medir uso real antes de decidir |
| `actions/open_app.py` | Abrir aplicativos | Manter | Uso diário simples, previsível e de alto valor |
| `actions/computer_settings.py` | Volume, brilho, janelas, atalhos, energia e Wi-Fi | Adaptar | Alto valor; ações irreversíveis ou de conectividade exigem confirmação explícita |
| `actions/computer_control.py` | Mouse, teclado, cliques, hotkeys e automação de tela | Adaptar | Poderoso e útil, mas com maior risco e sobreposição parcial com módulos específicos |
| `actions/desktop.py` | Wallpaper, organização e ações de desktop | Estudar | Parte útil, parte cosmética; não é prioridade para v0.1 |
| `actions/file_controller.py` | Criar, mover, copiar, renomear e apagar arquivos/pastas | Adaptar | Muito útil, porém alterações devem respeitar undo e confirmação conforme risco |
| `actions/file_processor.py` | Processamento de arquivos enviados | Manter | Alto valor e bom isolamento funcional |
| `actions/browser_control.py` | Navegação e automação do navegador | Adaptar | Manter como camada de navegador; evitar duplicar automação genérica de tela e exigir confirmação em ações autenticadas/externas |
| `actions/web_search.py` | Busca, notícias, preços e pesquisa | Manter | Já mostrou valor; custos/fontes entram na Etapa 05 |
| `actions/weather_report.py` | Clima | Manter | Simples, útil e de baixa complexidade |
| `actions/system_monitor.py` | CPU, RAM, GPU, temperatura e status | Manter | Útil para operação do PC e futura integração MSFS |
| `actions/proactive.py` | Iniciativa/proatividade | Estudar | Só deve avançar após contexto, limites e logs estarem sólidos |
| `actions/background_monitor.py` | Monitoramento periódico | Estudar | É automação posterior; não deve bloquear o Jarvis básico |
| `actions/reminder.py` | Lembretes locais | Adaptar | Útil, mas deve coexistir com futuras integrações Calendar sem duplicação |
| `actions/send_message.py` | Envio de mensagens | Estudar | Alto impacto externo; depende de consentimento, integração e confirmação adequada |
| `actions/youtube_video.py` | YouTube: reprodução, resumo e tendências | Estudar | Conveniente, mas não é core da primeira versão |
| `actions/flight_finder.py` | Busca de voos | Estudar | Uso pontual; avaliar manutenção, fonte e custo antes de promover |
| `actions/game_updater.py` | Steam/Epic e atualizações de jogos | Remover candidato | Baixa aderência ao objetivo atual; não deve fazer parte do core do Jarvis |
| `actions/code_helper.py` | Criar, editar e executar código | Estudar | Útil em desenvolvimento, mas Codex/Claude já cobrem este domínio melhor |
| `actions/dev_agent.py` | Construção autônoma de projetos | Remover candidato | Escopo amplo, maior risco e redundância com ferramentas especializadas |
| `actions/screen_processor.py` | Captura de tela/câmera para visão | Manter | Alto valor para diagnóstico e assistência contextual |
| `plugins/` | Extensões independentes | Manter | Ponto oficial de expansão para MSFS, God's Eye View e integrações específicas |
| `memory/memory_manager.py` | Memória persistente e recall | Manter | Arquitetura enxuta e consciente de contexto; preservar até estudo da Etapa 11 |
| `memory/config_manager.py` | Preferências e configuração | Adaptar | Deve convergir para configuração única e padronizada |
| `dashboard/server.py` | Dashboard remoto via FastAPI | Estudar | Potencial útil, mas aumenta superfície de rede, firewall e segurança |
| `dashboard/static/*` | Interface web remota | Estudar | Decisão depende do futuro do dashboard |
| Morning briefing | Saudação/notícias no startup | Adaptar | Deve ser opcional e evitar chamadas externas quando desnecessárias |
| Clipboard intelligence | Reação ao conteúdo copiado | Estudar | Pode gerar ruído, captura não solicitada e consumo desnecessário |
| Auto-start no Windows | Inicia Jarvis no boot | Adaptar | Desejável somente depois de start/stop, health check e recuperação estarem confiáveis |
| Remote control / QR | Acesso pelo telefone | Estudar | Só avançar após análise de segurança e necessidade real |

## Validações concluídas

### 1. Sobreposição entre módulos de controle

Há sobreposição funcional, mas não redundância suficiente para exclusão imediata:

- `computer_settings.py` deve continuar responsável por **estado/configuração do sistema**: volume, brilho, janelas, energia, Wi-Fi e atalhos do Windows.
- `computer_control.py` deve ficar como **automação genérica de entrada**: mouse, teclado, cliques e hotkeys.
- `browser_control.py` deve ser a camada **específica do navegador**, preferível à automação genérica quando houver ação estruturada.
- `desktop.py` mistura utilidades e funções cosméticas; permanece em estudo.

**Decisão:** não fundir módulos agora. Primeiro definir contratos claros e depois remover duplicações comprovadas na Etapa 07.

### 2. Chamadas externas e consumo

As capacidades que merecem medição específica na Etapa 05 são:

- Gemini Live / chamadas LLM;
- busca web e notícias;
- clima;
- busca de voos;
- recursos de YouTube;
- monitoramento/proatividade quando ativos;
- dashboard remoto quando exposto à rede.

Nem toda chamada tem custo direto, mas todas podem gerar latência, dependência externa ou tráfego. A Etapa 05 deve separar **API paga, API gratuita, scraping/busca pública e chamada local**.

### 3. Ações com efeito externo ou destrutivo

Foram identificadas quatro classes de risco para a Etapa 06:

- **Sistema/rede:** desligar, reiniciar, alterar Wi-Fi, firewall ou perfil de rede.
- **Arquivos:** apagar, sobrescrever, mover ou renomear conteúdo.
- **Comunicação externa:** enviar mensagens ou executar ações autenticadas em sites.
- **Automação de interface:** mouse/teclado podem operar a janela errada se o contexto estiver incorreto.

**Decisão:** a existência de `confirm.py` e `undo.py` é uma vantagem do projeto original e ambos devem ser preservados.

### 4. Recursos fora do núcleo inicial

Não precisam bloquear a primeira versão utilizável:

- MSFS / cockpit;
- God's Eye View;
- Gmail / Calendar / Drive;
- dashboard remoto avançado;
- proatividade e monitoramento automático;
- envio de mensagens;
- automação autônoma de desenvolvimento;
- integração de jogos;
- flight finder e YouTube avançado.

Isso não significa remover esses recursos agora; significa impedir que ampliem escopo antes da base estar sólida.

## Escopo funcional recomendado para Jarvis v0.1

1. Gemini Live + voz funcional.
2. Identidade Jarvis e PT-BR consistente.
3. Abrir aplicativos.
4. Ações Windows seguras.
5. Operações de arquivos com confirmação/undo conforme risco.
6. Busca web, clima e status do PC.
7. Memória local básica.
8. Visão de tela.
9. Framework de plugins preservado.
10. Logs, diagnóstico e start/stop simples.

## Decisões de arquitetura resultantes da Etapa 04

- **Não adicionar integrações novas diretamente em `main.py`** quando puderem ser plugins ou módulos isolados.
- **Não refatorar `main.py`/`ui.py` ainda**; tamanho e acoplamento são problemas conhecidos, mas mudança prematura criaria risco sem testes.
- **Não apagar módulos nesta etapa.** Os dois candidatos mais fortes para retirada futura são `game_updater.py` e `dev_agent.py`.
- **Preservar plugin loader, memória local, confirmação e undo** como ativos do projeto original.
- **Tratar proatividade como etapa posterior**, não como comportamento padrão da primeira versão.
- **Separar ação local de ação externa** para facilitar política de autorização na Etapa 06.

## Backlog derivado

| Destino | Item |
|---|---|
| Etapa 05 | Medir custos, fontes e dependências externas |
| Etapa 06 | Criar matriz de autonomia / confirmação / proibido |
| Etapa 07 | Validar dependências antes de remover candidatos e sobreposições |
| Etapa 08 | Centralizar configuração, caminhos, chaves e persistência local |
| Etapa 09 | Fixar identidade Jarvis e PT-BR |
| Etapa 11 | Avaliar integração da memória com base de conhecimento |
| Etapa 14 | Formalizar plugins como caminho padrão de expansão |
| Etapa 19–21 | Start/stop, logs e testes antes de qualquer autonomia ampliada |

## Regra de remoção

Nenhum item marcado como **Remover candidato** será apagado durante o inventário. Remoção só poderá ocorrer na Etapa 07, após validação de dependências, teste de regressão e confirmação de que o fluxo útil não será quebrado.

## Encerramento

**Etapa 04 — Inventário funcional: CONCLUÍDA.**

O projeto agora possui uma separação explícita entre o núcleo que queremos preservar, os componentes que serão adaptados, os candidatos a remoção e as capacidades que permanecerão em estudo. O próximo passo do Gate 1 é a **Etapa 05 — Custos e APIs**.