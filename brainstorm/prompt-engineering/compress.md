# compress.jsonl

Paired examples of prompt compression: an input prompt and one or more shorter rewrites with commentary.

## Purpose

Training data and reference for prompt compression. Each entry records what was tried, what worked, and what broke — including regressions where shorter text lost necessary meaning.

## Schema

JSONL. One object per line.

```
{
  "input": Prompt,
  "outputs": Prompt[]
}
```

```
interface Prompt {
  prompt: string;
  comment?: string;
}
```

`input` — the original text. `outputs` — compressed alternatives, best first. Comments note token counts, reasoning, and regressions.
