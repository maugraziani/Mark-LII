# Jarvis Mark 52 — Inventário Funcional

Data inicial: 04/09/2026
Branch: `jarvis-dev`
Status: Etapa 04 em andamento

## Critério de classificação

- **Manter** — entrega valor claro e já está alinhado ao Jarvis desejado.
- **Adaptar** — vale manter, mas precisa simplificação, limites, PT-BR, configuração ou integração.
- **Remover** — baixo valor para nosso uso ou redundância comprovada. Só remover após validação.
- **Estudar** — utilidade, risco, custo ou dependência ainda não suficientemente conhecidos.

## Inventário inicial

| Área / módulo | Função | Classificação inicial | Motivo / decisão preliminar |
|---|---|---|---|
| `main.py` | Orquestra Gemini Live, áudio, tools, memória, plugins e monitoramento | Adaptar | Funciona e é essencial, mas concentra responsabilidades demais |
| `ui.py` | HUD desktop, setup, logs, comando, upload e controles | Adaptar | Interface funciona bem; personalizar e simplificar depois, sem reescrita precoce |
| `core/prompt.txt` | Identidade, idioma e regras do Jarvis | Adaptar | Deve refletir Mauricio, PT-BR, limites e filosofia do projeto |
| `core/plugin_loader.py` | Framework de plugins | Manter | Boa separação e caminho preferencial para novas integrações |
| `core/confirm.py` | Confirmação de ações críticas | Manter | Fundamental para limite entre autonomia e confirmação humana |
| `core/undo.py` | Reversão de alterações suportadas | Manter | Importante para segurança operacional |
| `core/audio_devices.py` | Entrada/saída de áudio | Manter | Essencial para uso por voz |
| `core/installer.py` | Auto-instala dependências faltantes | Estudar | Conveniente, porém não deve instalar silenciosamente sem política clara |
| `core/stt.py` | Speech-to-text alternativo/local | Estudar | Gemini Live já cobre áudio; avaliar se é redundante ou fallback útil |
| `core/tts.py` | Text-to-speech alternativo/local | Estudar | Mesmo ponto: avaliar fallback, custo e latência |
| `actions/open_app.py` | Abrir aplicativos | Manter | Uso diário simples e de alto valor |
| `actions/computer_settings.py` | Volume, brilho, janelas, shortcuts, power etc. | Adaptar | Alto valor, mas precisa política de confirmação por ação |
| `actions/computer_control.py` | Mouse, teclado, clicks, hotkeys e automação de tela | Adaptar | Poderoso; exige limites e pode sobrepor outras actions |
| `actions/desktop.py` | Wallpaper, organizar/limpar desktop e tarefas | Estudar | Parte útil, parte cosmética ou sobreposta |
| `actions/file_controller.py` | Arquivos e pastas | Adaptar | Muito útil, porém criar/mover/apagar/escrever deve respeitar confirmação e undo |
| `actions/file_processor.py` | Processamento de arquivos enviados | Manter | Bom valor para uso cotidiano e integração futura |
| `actions/browser_control.py` | Navegação e automação do navegador | Adaptar | Alto valor; rever sobreposição com computer_control e riscos de ações autenticadas |
| `actions/web_search.py` | Busca, notícias, pesquisa, preços e comparação | Manter | Funcional e útil; custos/fontes serão avaliados na Etapa 05 |
| `actions/weather_report.py` | Clima | Manter | Simples, útil e já validado |
| `actions/system_monitor.py` | CPU, RAM, GPU, temperatura e alertas | Manter | Útil para PC e especialmente futura integração MSFS |
| `actions/proactive.py` | Iniciativa/proatividade | Estudar | Só automatizar depois de contexto e limites sólidos |
| `actions/background_monitor.py` | Monitoramento periódico de tópicos | Estudar | Útil, mas pertence ao estágio posterior de automação |
| `actions/reminder.py` | Lembretes via sistema | Adaptar | Útil; rever implementação e coexistência com futuras integrações Calendar |
| `actions/send_message.py` | Envio de mensagens | Estudar | Valor potencial alto, mas exige integração/consentimento e prevenção de envio indevido |
| `actions/youtube_video.py` | YouTube: play, resumo e trending | Estudar | Pode ser útil, mas não é core do Jarvis diário |
| `actions/flight_finder.py` | Busca de voos | Estudar | Funcionalidade pontual; avaliar custo/manutenção |
| `actions/game_updater.py` | Steam/Epic | Remover candidato | Baixa aderência ao objetivo atual; confirmar antes de remover |
| `actions/code_helper.py` | Criar/editar/rodar código | Estudar | Útil em desenvolvimento, mas não necessariamente core do assistente operacional |
| `actions/dev_agent.py` | Construção autônoma de projetos | Remover candidato | Escopo muito amplo e risco alto para um Jarvis leve; Codex/Claude já cobrem esse uso |
| `actions/screen_processor.py` | Captura de tela/câmera para visão | Manter | Alto valor para assistência contextual e diagnóstico |
| `plugins/` | Extensões independentes | Manter | Destino preferencial para MSFS, God's Eye View e capacidades específicas |
| `memory/memory_manager.py` | Memória persistente e recall | Manter | Arquitetura de contexto enxuta e útil; requer estudo de integração com base de conhecimento |
| `memory/config_manager.py` | Preferências/configuração | Adaptar | Deve convergir para configuração padronizada |
| `dashboard/server.py` | Controle remoto via navegador/celular | Estudar | Potencial alto, mas firewall, rede e exposição aumentam risco/complexidade |
| `dashboard/static/*` | Interface web remota | Estudar | Depende da decisão sobre dashboard |
| Morning briefing | Saudação/notícias no startup | Adaptar | Interessante, mas deve ser configurável e não consumir API desnecessariamente |
| Clipboard intelligence | Reage ao conteúdo copiado | Estudar | Pode ser útil, mas pode gerar ruído e contexto não solicitado |
| Auto-start no Windows | Inicia Jarvis no boot | Adaptar | Será útil depois de o sistema estar confiável |
| Remote control / QR | Acesso pelo telefone | Estudar | Valor real precisa ser comparado com custo de segurança e manutenção |

## Candidatos prioritários para o Jarvis v0.1 utilizável

1. Gemini Live + voz PT-BR.
2. Prompt/identidade Jarvis Mauricio.
3. Abrir aplicativos e ações Windows seguras.
4. Arquivos com undo e confirmação.
5. Busca web, clima e status do PC.
6. Memória local básica.
7. Visão de tela.
8. Plugin framework.
9. Logs e diagnóstico.
10. Start/stop simples.

## Itens que NÃO devem bloquear a v0.1

- MSFS / cockpit.
- God's Eye View.
- Gmail / Calendar / Drive.
- Dashboard remoto avançado.
- Proatividade e monitoramento automático.
- Envio de mensagens.
- Automação autônoma de desenvolvimento.
- Integrações de jogos.

## Próximas validações da Etapa 04

- Identificar sobreposição real entre `computer_settings`, `computer_control`, `desktop_control` e `browser_control`.
- Verificar quais actions fazem chamadas externas adicionais ao Gemini/API.
- Levantar ações que escrevem/apagam arquivos, mudam sistema/rede ou enviam conteúdo externo.
- Confirmar recursos que nunca serão usados pelo Mauricio antes de remover qualquer código.
- Fechar lista final: manter / adaptar / remover / estudar.

## Regra de remoção

Nenhum item marcado como **Remover candidato** será apagado durante o inventário. Remoção só ocorrerá na Etapa 07, após validação de dependências e confirmação de que não quebra fluxo útil existente.
