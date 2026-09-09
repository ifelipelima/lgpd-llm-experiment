# Avaliação de LLMs como Suporte Informacional à LGPD

Este repositório contém os artefatos e scripts utilizados em uma experiência exploratória sobre o uso de Large Language Models (LLMs) como suporte informacional à avaliação de aspectos da Lei Geral de Proteção de Dados Pessoais (LGPD) em cenários de software.

A experiência busca observar como diferentes LLMs identificam, contextualizam, justificam e comunicam aspectos relacionados à LGPD a partir de situações sintéticas de software.

## Objetivo

Investigar as potencialidades e limitações das análises produzidas por LLMs quando utilizadas como suporte informacional à avaliação de aspectos da LGPD em cenários de software.

## Modelos utilizados

Foram selecionados modelos pertencentes a duas famílias distintas de LLMs.

### Gemini 3.5 Flash

- Modelo: Gemini 3.5 Flash
- Identificador: `gemini-3.5-flash`
- Provedor: Google Gemini Developer API
- Thinking level: `medium`
- Limite máximo de saída: `5000` tokens

### Llama 3.3 70B Instruct

- Modelo: Llama 3.3 70B Instruct
- Identificador: `@cf/meta/llama-3.3-70b-instruct-fp8-fast`
- Desenvolvedor: Meta
- Provedor de inferência: Cloudflare Workers AI
- Quantização: FP8
- Limite máximo de saída: `5000` tokens

## Cenários

Foram construídos 12 cenários sintéticos de software relacionados a quatro princípios da LGPD:

- Finalidade;
- Necessidade;
- Transparência;
- Não discriminação.

Para cada princípio foram definidas três condições:

1. problema explícito;
2. situação aparentemente adequada;
3. informação insuficiente.

A organização dos cenários é apresentada abaixo:

| ID  | Princípio         | Condição                        |
| --- | ----------------- | ------------------------------- |
| F1  | Finalidade        | Problema explícito              |
| F2  | Finalidade        | Situação aparentemente adequada |
| F3  | Finalidade        | Informação insuficiente         |
| N1  | Necessidade       | Problema explícito              |
| N2  | Necessidade       | Situação aparentemente adequada |
| N3  | Necessidade       | Informação insuficiente         |
| T1  | Transparência     | Problema explícito              |
| T2  | Transparência     | Situação aparentemente adequada |
| T3  | Transparência     | Informação insuficiente         |
| D1  | Não discriminação | Problema explícito              |
| D2  | Não discriminação | Situação aparentemente adequada |
| D3  | Não discriminação | Informação insuficiente         |

Cada cenário foi executado uma única vez em cada modelo, totalizando **24 respostas oficiais**.

## Cenário piloto

Antes da coleta oficial foi utilizado o cenário `P0`.

O piloto teve como objetivo verificar:

- funcionamento das APIs;
- interpretação dos prompts;
- cumprimento da estrutura solicitada;
- adequação do limite máximo de saída;
- registro do consumo das execuções;
- armazenamento das respostas.

O cenário piloto não integra o conjunto de 12 cenários oficiais da experiência e não faz parte dos resultados da pesquisa.

Durante o piloto, o limite máximo de saída foi ajustado até `5000` tokens, evitando o truncamento das respostas antes do início da coleta oficial.

## Prompts

Todas as execuções utilizaram os mesmos prompts padronizados.

Os arquivos estão disponíveis em:

```text
prompts/
├── system_prompt.md
└── user_prompt.md
```

O arquivo `system_prompt.md` define o papel da LLM, a base normativa considerada e as restrições gerais da análise.

O arquivo `user_prompt.md` contém o template utilizado para inserir cada cenário e determina a estrutura esperada da resposta.

Entre as execuções, apenas os campos correspondentes ao cenário analisado são substituídos.

## Condições de execução

Durante a coleta foram mantidas as seguintes condições:

- uma execução por cenário e por modelo;
- mesmo system prompt para os dois modelos;
- mesmo user prompt para os dois modelos;
- mesma base normativa;
- sem acesso à Web;
- sem RAG;
- sem ferramentas externas;
- sem interação adicional após a resposta;
- respostas exclusivamente textuais;
- parâmetros de amostragem não configurados explicitamente mantidos nos valores padrão dos respectivos provedores;
- armazenamento das respostas brutas sem edição antes de qualquer análise posterior.

O protocolo completo da experiência está disponível em [`protocol.md`](protocol.md).

## Estrutura do repositório

```text
.
├── prompts/
│   ├── system_prompt.md
│   └── user_prompt.md
│
├── scenarios/
│   ├── P0.md
│   ├── F1.md
│   ├── F2.md
│   ├── F3.md
│   ├── N1.md
│   ├── N2.md
│   ├── N3.md
│   ├── T1.md
│   ├── T2.md
│   ├── T3.md
│   ├── D1.md
│   ├── D2.md
│   └── D3.md
│
├── results/
│   ├── gemini/
│   └── llama/
│
├── prompt_builder.py
├── run_gemini.py
├── run_llama.py
├── protocol.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuração do ambiente

O experimento foi desenvolvido em Python.

### Windows

Para criar um ambiente virtual:

```powershell
python -m venv .venv
```

Para ativá-lo no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux

Para criar um ambiente virtual:

```bash
python3 -m venv .venv
```

Para ativá-lo:

```bash
source .venv/bin/activate
```

### Instalação das dependências

Com o ambiente virtual ativo, instale as dependências:

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

As credenciais utilizadas para acesso às APIs devem ser armazenadas em um arquivo `.env`.

Exemplo:

```env
GEMINI_API_KEY=sua_chave_do_gemini

CLOUDFLARE_API_TOKEN=seu_token_cloudflare
CLOUDFLARE_ACCOUNT_ID=seu_account_id
```

## Execução

Os executores recebem o identificador do cenário pela linha de comando.

### Gemini

Para visualizar o prompt montado sem realizar uma chamada à API:

```bash
python run_gemini.py F1 --dry-run
```

Para executar o cenário:

```bash
python run_gemini.py F1
```

### Llama

Para visualizar o prompt montado sem realizar uma chamada à API:

```bash
python run_llama.py F1 --dry-run
```

Para executar o cenário:

```bash
python run_llama.py F1
```

Os executores impedem a sobrescrita de uma resposta já existente para a mesma combinação de cenário e modelo.

## Resultados

As respostas produzidas pelos modelos são armazenadas em formato JSON.

A organização dos resultados segue a estrutura:

```text
results/
├── gemini/
│   ├── F1_gemini-3.5-flash.json
│   ├── F2_gemini-3.5-flash.json
│   └── ...
│
└── llama/
    ├── F1_llama-3.3-70b-instruct-fp8-fast.json
    ├── F2_llama-3.3-70b-instruct-fp8-fast.json
    └── ...
```

Cada registro contém informações como:

- identificador do cenário;
- modelo utilizado;
- provedor;
- data e horário da execução;
- configurações utilizadas;
- métricas de uso disponibilizadas pelo provedor;
- system prompt;
- user prompt final;
- resposta bruta produzida pela LLM.

As respostas armazenadas correspondem diretamente às saídas obtidas durante a coleta e não foram editadas antes da etapa posterior de análise.

## Observação

Os cenários utilizados no experimento são sintéticos e foram construídos exclusivamente para fins de investigação.

As análises produzidas pelas LLMs não devem ser interpretadas como certificações jurídicas de conformidade de sistemas com a LGPD.
