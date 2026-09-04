# Jarvis Mark 52 — Segurança e Limites

Data: 04/09/2026
Branch: `jarvis-dev`
Status: Etapa 06 concluída

## Objetivo

Definir claramente o que o Jarvis pode executar sozinho, o que exige confirmação humana e o que fica proibido na v0.1.

A regra central é simples: **autonomia somente quando o impacto é baixo, previsível e reversível**. Quanto maior o risco de perda de dados, interrupção, comunicação externa, gasto financeiro ou alteração de segurança, maior a exigência de confirmação.

## Níveis de execução

### A — Autônomo

Pode executar sem banner adicional quando a solicitação do usuário for clara e a ação for de baixo risco.

Exemplos:

- consultar clima, notícias, pesquisa e preços;
- consultar CPU, RAM, GPU, temperatura e status do PC;
- abrir aplicativos;
- listar arquivos e pastas permitidos;
- ler arquivos suportados;
- copiar arquivos dentro das áreas permitidas;
- criar arquivo ou pasta em área segura quando não sobrescrever dado importante;
- controlar volume, mute, brilho e janelas;
- alternar janelas e desktop;
- capturar screenshot ou câmera quando solicitado;
- navegar para URL e ler página;
- usar clipboard quando o usuário pediu a ação;
- executar pesquisa DDG/Gemini respeitando a política de custo.

### B — Autônomo somente se explicitamente solicitado e reversível

A instrução direta do usuário autoriza a ação, mas ela deve gerar undo quando tecnicamente possível.

Exemplos:

- mover ou renomear arquivo;
- editar/escrever arquivo existente dentro das raízes permitidas;
- organizar arquivos no Desktop;
- alterar wallpaper;
- excluir um arquivo para a Lixeira, nunca permanentemente;
- preencher campos locais ou formulários sem ainda submetê-los;
- alterações de configuração local reversíveis.

Se houver ambiguidade sobre alvo, escopo ou quantidade de itens, o Jarvis deve perguntar em vez de adivinhar.

### C — Confirmação humana obrigatória no HUD

A ação só é executada depois do usuário pressionar **CONFIRM** na interface. Confirmação por texto gerado pelo modelo não vale.

- desligar o computador;
- reiniciar o computador;
- logoff ou operação equivalente que encerre sessão;
- desligar/reconfigurar rede ou Wi-Fi;
- alterar firewall ou perfil de rede;
- instalar, atualizar ou remover software/dependências automaticamente;
- executar código gerado por LLM que escreva, mova, remova ou altere estado relevante;
- enviar mensagem, e-mail ou conteúdo para terceiro;
- publicar conteúdo em rede social;
- clicar em botão final de envio/submit quando houver consequência externa relevante;
- confirmar compra, assinatura, reserva, pagamento ou pedido;
- alterar senha, autenticação, conta ou permissões;
- excluir diretório ou conjunto de arquivos em massa, mesmo quando usando Lixeira;
- qualquer ação autenticada no navegador que altere dados do usuário ou de terceiros.

### D — Proibido na v0.1

Mesmo com pedido, não deve ser executado automaticamente pelo agente nesta versão.

- apagar permanentemente arquivos ou contornar a Lixeira;
- revelar, imprimir, transmitir ou registrar API keys, senhas, tokens ou credenciais em log;
- desabilitar antivírus, proteção do Windows ou controles de segurança para facilitar uma tarefa;
- alterar BIOS/UEFI, firmware ou configurações de baixo nível de hardware;
- executar comando destrutivo amplo sem alvo específico;
- fazer compra, pagamento ou transferência financeira de forma autônoma;
- aceitar contratos/termos em nome do usuário sem participação humana explícita;
- enviar mensagem em massa ou para destinatário não confirmado;
- elevar privilégios silenciosamente;
- modificar `main`/release do projeto sem aprovação humana.

## Confirmação técnica

`core/confirm.py` já implementa um mecanismo correto de confirmação: o token de autorização nasce na interface, não no modelo. O fluxo deve ser preservado.

Princípios:

1. o modelo solicita a ação;
2. a action registra o callable real em `confirm.request(...)`;
3. a UI mostra CONFIRM / CANCEL;
4. somente o clique humano em CONFIRM chama `resolve(True)`;
5. confirmação expira automaticamente;
6. em modo sem UI, ação crítica é recusada.

Nenhuma action crítica deverá voltar a usar parâmetros como `confirmed=yes`, pois o próprio modelo poderia fabricá-los.

## Undo

Undo é preferível a confirmação para ações simples e reversíveis.

O padrão atual de `file_controller.py` é adequado como base:

- delete usa Lixeira/Recycle Bin quando `send2trash` existe;
- exclusão permanente fica desabilitada;
- move/rename/create/write/copy registram undo quando suportado;
- raízes sensíveis são protegidas;
- operações fora das raízes autorizadas são recusadas.

A Etapa 13 validará na prática a cobertura e confiabilidade do undo.

## Gaps encontrados no código atual

### 1. Mensageria envia sem confirmação no HUD

`actions/send_message.py` abre o aplicativo, localiza o contato, cola o texto e pressiona Enter. Hoje isso pode enviar diretamente.

**Decisão:** manter módulo, mas impedir envio real sem confirmação obrigatória antes da ação final.

### 2. Código gerado pelo Gemini em `desktop.py`

O módulo solicita ao Gemini código Python e executa o resultado em sandbox limitado. Apesar das restrições, continua sendo código gerado dinamicamente.

**Decisão:** na simplificação, preferir funções determinísticas. Qualquer trecho gerado que altere estado relevante deverá passar por confirmação.

### 3. Auto-instalação / auto-upgrade

Há rotinas que podem instalar ou atualizar dependências automaticamente, incluindo fallback de TTS/Kokoro.

**Decisão:** na v0.1, instalação automática silenciosa não é permitida. Detectar falta de dependência é autônomo; instalar exige confirmação.

### 4. Dashboard e rede

O dashboard pode exigir operações de firewall/perfil de rede dependendo da configuração.

**Decisão:** nenhuma alteração de firewall, perfil Public/Private ou exposição de porta pode ocorrer sem confirmação humana.

### 5. Browser autenticado

Playwright pode atuar dentro de sessões reais do navegador.

**Decisão:** leitura e navegação podem ser autônomas; qualquer ação que envie, publique, compre, aceite, exclua ou altere dados externos exige confirmação.

## Regras de arquivos

- Raiz padrão atual: diretórios dentro de `Path.home()`.
- Não ampliar raízes de escrita sem configuração explícita.
- Leitura fora da raiz só poderá ser adicionada deliberadamente na Etapa 08/12.
- Nunca sobrescrever arquivo importante quando o alvo estiver ambíguo.
- Operações em lote devem mostrar escopo antes da execução.
- Para código do próprio Jarvis, trabalhar em `jarvis-dev`; merge/release continua humano.

## Regras de mensagens e conteúdo externo

Antes da confirmação, a UI deverá mostrar pelo menos:

- plataforma;
- destinatário;
- conteúdo ou preview suficientemente claro;
- ação final que será executada.

Alterar destinatário ou conteúdo invalida a confirmação anterior.

## Regras de custo

A ativação de billing, API paga, assinatura ou serviço externo pago é uma ação de nível C e sempre exige confirmação humana. Nenhum módulo pode habilitar faturamento sozinho.

## Regras de logs

Logs devem registrar:

- ação solicitada;
- action/tool usada;
- resultado ou erro;
- confirmação solicitada/aprovada/cancelada para ações críticas;
- serviço externo/modelo utilizado quando houver custo potencial.

Logs **não** devem registrar:

- API keys;
- senhas;
- tokens de sessão;
- conteúdo sensível desnecessário de clipboard;
- credenciais de sites.

## Matriz resumida

| Tipo de ação | Regra |
|---|---|
| Consulta / leitura | Autônoma |
| Controle simples do Windows | Autônoma |
| Arquivo reversível | Autônoma se pedido explícito + undo |
| Delete para Lixeira | Permitido se explícito; lote/pasta exige confirmação |
| Delete permanente | Proibido na v0.1 |
| Envio para terceiros | Confirmação obrigatória |
| Power / rede / firewall | Confirmação obrigatória |
| Instalação / update de software | Confirmação obrigatória |
| Código gerado alterando estado | Confirmação obrigatória |
| Browser somente leitura | Autônomo |
| Browser com efeito externo | Confirmação obrigatória |
| Compra/pagamento | Não autônomo; usuário executa ação final |
| Billing/API paga | Confirmação obrigatória |

## Critério de conclusão da Etapa 06

A política está definida. A implementação e os testes dos gates não pertencem a esta etapa:

- Etapa 07 simplifica módulos e remove sobreposição;
- Etapa 08 centraliza configuração e permissões;
- Etapa 12 valida ações Windows;
- Etapa 13 testa confirmação e undo.

Nenhuma função foi removida nesta etapa.
