# τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains

**Paper**: [https://arxiv.org/abs/2406.12045](https://arxiv.org/abs/2406.12045)

## Proof of Concepts for Shortcuts

Tau-bench evaluates the agents' actions based on 
1. whether the database state is correct
2. (optional) whether the agents' responses contain required text

Therefore, on tasks that do not change the database state and do not have 
required texts, agents can get positive evaluation results by doing nothing.
On tasks that do not change the database state and has a trivial required text,
such as "4", agents can get positive evaluation results by returning random 
responses or everything in the database.

To reproduce the do-nothing agent, run
```bash
git checkout do-nothing
python run.py \
      --agent-strategy tool-calling \
      --env retail \
      --model gpt-4o \
      --model-provider openai \
      --user-model gpt-4o \
      --user-model-provider openai \
      --user-strategy llm \
      --max-concurrency 10
python run.py \
      --agent-strategy tool-calling \
      --env airline \
      --model gpt-4o \
      --model-provider openai \
      --user-model gpt-4o \
      --user-model-provider openai \
      --user-strategy llm \
      --max-concurrency 10
```

To reproduce the output-everything agent, run
```
git checkout output
python run.py \
      --agent-strategy tool-calling \
      --env retail \
      --model gpt-4o \
      --model-provider openai \
      --user-model gpt-4o \
      --user-model-provider openai \
      --user-strategy llm \
      --max-concurrency 10
python run.py \
      --agent-strategy tool-calling \
      --env airline \
      --model gpt-4o \
      --model-provider openai \
      --user-model gpt-4o \
      --user-model-provider openai \
      --user-strategy llm \
      --max-concurrency 10
```

You will get the following pass^k or pass@k for any k:

|                  | Retail | Airline|
-------------------|--------|--------|
|do-nothing        | 6.0%   | 38% |
|output-everything | 9.6%   | 40% |