# Ansible Collection - stevefulme1.openai

Ansible collection for the OpenAI API, auto-generated from the official OpenAPI specification.

## Modules

| Module | Description |
|--------|-------------|
| `assistant` | Manage OpenAI assistants |
| `batch` | Manage batch API jobs |
| `embedding` | Create embeddings |
| `file` | Manage files |
| `fine_tuning_job` | Manage fine-tuning jobs |
| `model` | Manage models |
| `moderation` | Create moderations |
| `thread` | Manage threads |
| `vector_store` | Manage vector stores |

Each module has a corresponding `_info` module for read-only queries.

## Installation

```bash
ansible-galaxy collection install stevefulme1.openai
```

## Authentication

All modules require `api_url` and `api_token` parameters, or the equivalent environment variables.

## License

GPL-3.0-or-later
