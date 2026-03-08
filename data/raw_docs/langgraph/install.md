---
title: Install LangGraph
sidebarTitle: Install
---



To install the base LangGraph package:

:::python

```bash pip
pip install -U langgraph
```

```bash uv
uv add langgraph
```

:::

:::js

```bash npm
npm install @langchain/langgraph @langchain/core
```

```bash pnpm
pnpm add @langchain/langgraph @langchain/core
```

```bash yarn
yarn add @langchain/langgraph @langchain/core
```

```bash bun
bun add @langchain/langgraph @langchain/core
```

:::

To use LangGraph you will usually want to access LLMs and define tools.
You can do this however you see fit.

One way to do this (which we will use in the docs) is to use [LangChain](/oss/langchain/overview).

Install LangChain with:

:::python

```bash pip
pip install -U langchain
# Requires Python 3.10+
```

```bash uv
uv add langchain
# Requires Python 3.10+
```

:::

:::js

```bash npm
npm install langchain
```

```bash pnpm
pnpm add langchain
```

```bash yarn
yarn add langchain
```

```bash bun
bun add langchain
```

:::

To work with specific LLM provider packages, you will need install them separately.

Refer to the [integrations](/oss/integrations/providers/overview) page for provider-specific installation instructions.
