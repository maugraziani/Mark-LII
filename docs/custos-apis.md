# Jarvis Mark 52 — Custos e APIs

Data: 04/09/2026
Branch: `jarvis-dev`
Status: Etapa 05 concluída

## Objetivo

Mapear serviços externos, pontos de consumo, risco de cobrança e regras de operação antes de simplificar ou automatizar o Jarvis Mark 52.

## Política de custo do projeto

- Operar a v0.1 no nível gratuito sempre que tecnicamente viável.
- Não habilitar faturamento, plano pago ou nova API paga sem confirmação humana explícita.
- Não adicionar serviço externo quando uma solução local ou gratuita entregar o mesmo valor com complexidade aceitável.
- Chamadas auxiliares de IA devem ser exceção, não padrão, quando a sessão Live já puder resolver o problema.
- Toda chamada externa futura deverá ter motivo, fallback e logging suficiente para diagnosticar consumo.
- O alvo de custo para a v0.1 é **US$ 0 de cobrança recorrente**; qualquer exceção será uma decisão explícita de projeto.

## Baseline observado

Painel do Google AI Studio apresentado em 04/09/2026 durante os testes iniciais:

- modelo exibido: Gemini 2.5 Flash Native Audio Dialog;
- aproximadamente 31 mil tokens de entrada;
- 3 solicitações;
- painel sem valor de tokens de saída naquele recorte;
- nenhum dado de cobrança apresentado.

Este baseline será usado para comparação após as otimizações. Não é tratado como medição financeira completa porque o painel mostrado não detalhava modalidade de cada token nem saída.

## Inventário de serviços externos

| Serviço / recurso | Onde é usado | Situação | Custo / risco | Decisão |
|---|---|---|---|---|
| Gemini 2.5 Flash Native Audio — Live API | `main.py` | Ativo / core | Principal consumidor potencial; sessão longa recompõe contexto e pode aumentar consumo por turno | **Manter** e controlar contexto/tempo de sessão |
| Gemini Flash + Google Search grounding | `actions/web_search.py` | Ativo sob demanda | Pode consumir quota própria de grounding; código já possui circuit breaker e DDG fallback | **Adaptar** para DDG-first sempre que síntese Gemini não for necessária |
| Gemini Flash | `actions/desktop.py` | Sob demanda | Gera código Python para automação; custo adicional e risco operacional | **Estudar/limitar**; evitar uso para tarefas determinísticas |
| Gemini Flash-Lite | `actions/computer_control.py` | Sob demanda | Visão para localizar elementos em screenshot | **Manter sob demanda**, nunca chamar para cliques simples |
| Gemini Flash / Flash-Lite | `actions/flight_finder.py` | Sob demanda | Pode fazer uma chamada para interpretar data e outra para extrair voos | **Estudar**; função não bloqueia v0.1 |
| DuckDuckGo via `ddgs` | `actions/web_search.py` | Ativo | Sem chave de API no código e sem cobrança por chamada pelo projeto; sujeito a rate limit/bloqueio do serviço | **Manter como fallback e fonte de baixo custo** |
| Google Search via navegador | `actions/weather_report.py` | Ativo | Apenas abre busca no navegador; não usa API paga própria | **Manter provisoriamente** |
| Google Flights via navegador | `actions/flight_finder.py` | Sob demanda | Navegação web + posterior interpretação Gemini | **Estudar** |
| Playwright | `actions/browser_control.py` | Ativo local | Biblioteca local; páginas acessadas podem ter seus próprios termos/limites, mas não há API Playwright paga | **Manter** |
| WhatsApp / Telegram / Signal / Discord / Instagram / Messenger | `actions/send_message.py` | Sob demanda | Automação local de interface; não usa APIs oficiais pagas no código atual | **Estudar por segurança**, não por custo |
| EdgeTTS | `core/tts.py` | Opcional | Serviço online sem chave no código; sem cobrança por API configurada pelo projeto | **Fallback possível** |
| Kokoro TTS | `core/tts.py` | Opcional | Modelo local; download inicial e depois execução local | **Preferível para fallback offline**, se desempenho for adequado |
| Whisper / Vosk STT | `core/stt.py` | Opcional | Execução local; download inicial de modelo quando necessário | **Manter como candidatos de fallback local** |
| ElevenLabs | `core/tts.py` | Opcional / não necessário para v0.1 | API externa potencialmente paga e exige chave própria | **Não ativar na v0.1** |
| Hugging Face | downloads de Whisper/Kokoro | Somente primeiro uso quando modelo não estiver em cache | Tráfego de download, sem custo de inferência depois de armazenado localmente | **Aceitável somente quando necessário** |

## Preços Gemini relevantes em 04/09/2026

Fonte oficial: Google AI for Developers — Gemini Developer API Pricing.

### Gemini 2.5 Flash Native Audio — Live API

Modelo atualmente usado pelo projeto: `gemini-2.5-flash-native-audio-preview-12-2025`.

Nível gratuito atual: sem cobrança por tokens segundo a página oficial consultada em 04/09/2026.

Nível pago, por 1 milhão de tokens:

- entrada texto: US$ 0,50;
- entrada áudio/vídeo: US$ 3,00;
- saída texto: US$ 2,00;
- saída áudio: US$ 12,00.

### Gemini 2.5 Flash

Nível pago padrão, por 1 milhão de tokens:

- entrada texto/imagem/vídeo: US$ 0,30;
- entrada áudio: US$ 1,00;
- saída, incluindo thinking: US$ 2,50.

Grounding com Google Search no Gemini 2.5 Flash:

- nível gratuito: até 500 prompts fundamentados por dia, compartilhado com Flash-Lite;
- nível pago: 1.500 prompts fundamentados por dia sem cobrança; depois US$ 35 por 1.000 prompts fundamentados.

### Gemini 2.5 Flash-Lite

Nível pago padrão:

- entrada texto/imagem/vídeo: US$ 0,10 por 1 milhão de tokens;
- saída: US$ 0,40 por 1 milhão de tokens.

O nível gratuito existe, sujeito aos limites vigentes do projeto/modelo.

## Risco principal encontrado: custo acumulativo da Live API

A documentação atual da Google alerta que a Live API mantém contexto persistente e os tokens anteriores podem ser reprocessados a cada novo turno. Portanto, uma conversa muito longa pode aumentar progressivamente o consumo mesmo que cada nova fala seja curta.

A Google recomenda usar `contextWindowCompression` para limitar o crescimento do contexto. Na inspeção atual do repositório não foi encontrada configuração explícita de `contextWindowCompression`.

**Backlog para Etapa 22 — Otimização:** medir sessões longas e configurar compressão de contexto somente após validar impacto em memória e qualidade da conversa.

## Desperdícios / oportunidades identificadas

1. `web_search.py` já melhorou o consumo ao usar DDG primeiro para notícias e ao bloquear temporariamente grounding após erro de quota. Este padrão deve ser preservado.
2. `gemini-flash-latest` e `gemini-flash-lite-latest` são aliases móveis. Eles facilitam atualização, mas podem mudar comportamento, preço ou qualidade sem alteração no nosso código. Na Etapa 08 devemos decidir entre aliases e modelos explicitamente fixados.
3. `desktop.py` usa Gemini para gerar código mesmo existindo várias tarefas que podem ser determinísticas. Este é candidato forte a simplificação na Etapa 07.
4. `computer_control.py` deve usar visão Gemini apenas para localização visual que realmente necessite interpretação; mouse, teclado, hotkeys e clipboard são operações locais e gratuitas.
5. `flight_finder.py` pode consumir duas chamadas Gemini na mesma tarefa. Como não é core da v0.1, não vale otimizar agora.
6. Weather atual não requer API meteorológica: abre uma pesquisa Google no navegador. Não há razão de custo para adicionar API de clima neste momento.
7. Mensageria atual não usa APIs oficiais externas; a principal questão será confirmação humana antes do envio, tratada na Etapa 06.

## Decisões da Etapa 05

- **Gemini Live permanece como motor principal.**
- **Nenhuma API paga nova será adicionada para a v0.1.**
- **Billing não será requisito para desenvolvimento neste momento.**
- **DDG deve ser preferido quando a necessidade for apenas recuperar resultados/headlines.**
- **Gemini grounding será reservado para pesquisa/síntese que realmente agregue valor.**
- **ElevenLabs fica fora da v0.1.**
- **Voos, mensageria e dashboard não justificam custo/complexidade adicional agora.**
- **Não substituir soluções locais de STT/TTS sem evidência de necessidade.**
- **O consumo da Live API será medido novamente depois das Etapas 08–10 e 22.**

## Fontes externas verificadas

- Google AI for Developers — Gemini Developer API Pricing: `https://ai.google.dev/gemini-api/docs/pricing`
- Google AI for Developers — Grounding with Google Search: `https://ai.google.dev/gemini-api/docs/google-search`
- Google AI for Developers — Live API best practices: `https://ai.google.dev/gemini-api/docs/live-api/best-practices`

Consultadas em 04/09/2026. Preços e quotas são externos e podem mudar; devem ser revalidados antes de habilitar billing.

## Saída para as próximas etapas

### Etapa 06 — Segurança e limites

Definir matriz explícita de ações:

- autônoma;
- confirmação obrigatória;
- proibida.

Prioridade: arquivos, power/rede, mensagens, browser autenticado, automação visual e código gerado.

### Etapa 07 — Simplificação

Avaliar principalmente:

- redundância `desktop.py` × `computer_control.py` × `computer_settings.py`;
- remoção ou isolamento de `dev_agent.py` e `game_updater.py`;
- substituição de chamadas Gemini por lógica determinística quando possível.

### Etapa 08 — Configuração

Centralizar:

- modelo Live;
- modelos auxiliares;
- política free/paid;
- aliases de modelos;
- API keys;
- fallback;
- limites e logging de consumo.
