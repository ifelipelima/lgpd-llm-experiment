# Protocolo experimental

## Modelos

### Gemini

- Modelo: Gemini 3.5 Flash
- Identificador: gemini-3.5-flash
- Provedor: Google Gemini Developer API
- Thinking level: medium
- Max output tokens: 5000

### Llama

- Modelo: Llama 3.3 70B Instruct
- Identificador: @cf/meta/llama-3.3-70b-instruct-fp8-fast
- Desenvolvedor: Meta
- Provedor de inferência: Cloudflare Workers AI
- Quantização: FP8
- Max tokens: 5000

## Condições de execução

- Uma execução por cenário e por modelo.
- Mesmo system prompt para os dois modelos.
- Mesmo user prompt para os dois modelos.
- Mesma base normativa.
- Sem acesso à Web.
- Sem RAG.
- Sem ferramentas externas.
- Sem interação adicional após a resposta.
- Resposta textual.
- Parâmetros de amostragem mantidos nos valores padrão dos respectivos provedores.
- As respostas brutas são armazenadas sem edição antes da avaliação.

## Cenários

- 4 princípios da LGPD:
  - Finalidade
  - Necessidade
  - Transparência
  - Não discriminação

- 3 condições por princípio:
  - problema explícito;
  - situação aparentemente adequada;
  - informação insuficiente.

Total: 12 cenários.

Cada cenário será executado uma única vez em cada modelo.

Total de respostas oficiais: 24.

## Piloto

O cenário P0 foi utilizado exclusivamente para verificar:

- funcionamento das APIs;
- interpretação dos prompts;
- cumprimento da estrutura de resposta;
- limite de tokens;
- armazenamento das respostas.

O cenário P0 não fará parte dos resultados da pesquisa.

Após a execução do piloto, o protocolo foi congelado antes da coleta dos dados oficiais.
