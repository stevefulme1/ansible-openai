# Ansible Collection - stevefulme1.openai

Manage OpenAI platform resources and AI operations with Ansible -- assistants, fine-tuning, embeddings, vector stores, images, audio, organization governance, and more.

This collection provides **99 modules** and an **Event-Driven Ansible (EDA) event source** for full lifecycle automation of the OpenAI API.

## Requirements

| Dependency | Version |
|---|---|
| Python | >= 3.10 |
| Ansible Core | >= 2.16 |

No additional Python libraries are required -- all API calls use `ansible.module_utils.urls`.

## Installation

```bash
ansible-galaxy collection install stevefulme1.openai
```

Install from source:

```bash
ansible-galaxy collection install git+https://github.com/stevefulme1/ansible-openai.git
```

## Authentication

Every module requires an `api_key` parameter. Optional parameters include `organization` and `base_url` (for Azure OpenAI or compatible endpoints).

```yaml
# group_vars/all.yml
openai_api_key: "{{ vault_openai_api_key }}"
openai_organization: "org-abc123"  # optional
```

| Parameter | Description | Required | Env Variable |
|---|---|---|---|
| `api_key` | OpenAI API key | Yes | `OPENAI_API_KEY` |
| `organization` | Organization ID | No | `OPENAI_ORGANIZATION` |
| `base_url` | API base URL (default: `https://api.openai.com/v1`) | No | -- |
| `timeout` | Request timeout in seconds (default: `30`) | No | -- |

## Quick Start

### Create a chat completion

```yaml
- name: Generate a summary using GPT-4o
  stevefulme1.openai.chat_completion:
    api_key: "{{ openai_api_key }}"
    model: gpt-4o
    messages:
      - role: system
        content: "You are a helpful assistant."
      - role: user
        content: "Summarize the benefits of infrastructure as code."
  register: completion

- name: Show response
  ansible.builtin.debug:
    msg: "{{ completion.choices[0].message.content }}"
```

### Create an assistant with a vector store

```yaml
- name: Create a vector store for documentation
  stevefulme1.openai.vector_store:
    api_key: "{{ openai_api_key }}"
    state: present
    name: product-docs
  register: vs

- name: Create a support assistant
  stevefulme1.openai.assistant:
    api_key: "{{ openai_api_key }}"
    state: present
    name: support-bot
    model: gpt-4o
    instructions: "You are a product support assistant. Use the attached knowledge base."
    tools:
      - type: file_search
    tool_resources:
      file_search:
        vector_store_ids:
          - "{{ vs.id }}"
```

### Launch a fine-tuning job

```yaml
- name: Upload training data
  stevefulme1.openai.file_upload:
    api_key: "{{ openai_api_key }}"
    file: /data/training.jsonl
    purpose: fine-tune
  register: upload

- name: Start fine-tuning
  stevefulme1.openai.fine_tuning_job:
    api_key: "{{ openai_api_key }}"
    model: gpt-4o-mini-2024-07-18
    training_file: "{{ upload.id }}"
    suffix: "custom-support-v1"
  register: ft_job

- name: Show job status
  ansible.builtin.debug:
    msg: "Fine-tuning job {{ ft_job.id }} status: {{ ft_job.status }}"
```

## Module Index

### Chat & Responses

| Module | Description |
|---|---|
| `chat_completion` | Create an OpenAI chat completion |
| `chat_completion_structured` | Chat completion with JSON schema response format |
| `chat_completion_vision` | Chat completion with image inputs |
| `chat_completion_with_tools` | Chat completion with function/tool calling |
| `response` | Create a response via the Responses API |
| `response_info` | Get response details |
| `response_input_item` | Manage response input items |
| `response_stream` | Create a streaming response |

### Assistants & Threads

| Module | Description |
|---|---|
| `assistant` | Create, update, or delete an OpenAI assistant |
| `assistant_info` | List OpenAI assistants |
| `assistant_file` | Manage files attached to assistants |
| `assistant_tool` | Manage assistant tools |
| `assistant_vector_store` | Attach vector store to assistant |
| `thread` | Create or delete an OpenAI thread |
| `thread_message` | Create a message in an OpenAI thread |
| `thread_message_info` | List messages in an OpenAI thread |
| `thread_run` | Create a run on an OpenAI thread |
| `thread_run_info` | Get OpenAI thread run status and details |
| `thread_run_cancel` | Cancel an OpenAI thread run |
| `thread_run_step_info` | Get run step details |
| `thread_run_tool_output` | Submit tool outputs for a run |

### Embeddings

| Module | Description |
|---|---|
| `embedding` | Create OpenAI embeddings |
| `embedding_batch` | Batch create OpenAI embeddings |
| `embedding_dimension` | Configure embedding dimensions |
| `embedding_model_info` | Get embedding model details |
| `embedding_usage_info` | Get embedding usage statistics |

### Vector Stores

| Module | Description |
|---|---|
| `vector_store` | Create, update, or delete an OpenAI vector store |
| `vector_store_info` | List OpenAI vector stores |
| `vector_store_file` | Add or remove a file from an OpenAI vector store |
| `vector_store_file_info` | List files in an OpenAI vector store |
| `vector_store_file_batch` | Batch add files to an OpenAI vector store |

### Fine-Tuning

| Module | Description |
|---|---|
| `fine_tuning_job` | Create an OpenAI fine-tuning job |
| `fine_tuning_job_info` | List OpenAI fine-tuning jobs |
| `fine_tuning_job_detail_info` | Get details of a specific fine-tuning job |
| `fine_tuning_job_cancel` | Cancel an OpenAI fine-tuning job |
| `fine_tuning_event_info` | List events for an OpenAI fine-tuning job |
| `fine_tuning_checkpoint_info` | List fine-tuning checkpoints |
| `fine_tuning_dataset_validate` | Validate fine-tuning training data |
| `fine_tuning_hyperparameters` | Configure fine-tuning hyperparameters |
| `fine_tuning_wandb_integration` | Configure W&B integration for fine-tuning |

### Images

| Module | Description |
|---|---|
| `image_generate` | Generate images with OpenAI DALL-E |
| `image_edit` | Edit an image with OpenAI DALL-E |
| `image_variation` | Create image variations with OpenAI DALL-E |
| `image_batch` | Batch image generation |
| `image_download` | Download generated images to local path |
| `image_model_info` | Get image model details |

### Audio

| Module | Description |
|---|---|
| `audio_transcription` | Transcribe audio with OpenAI Whisper |
| `audio_translation` | Translate audio to English with OpenAI Whisper |
| `audio_speech` | Generate speech from text with OpenAI TTS |
| `audio_batch_transcription` | Batch audio transcription |
| `audio_model_info` | List audio models |
| `audio_voice_info` | List available TTS voices |

### Files & Batches

| Module | Description |
|---|---|
| `file_upload` | Upload a file to OpenAI |
| `file_info` | List files in the OpenAI account |
| `file_detail_info` | Get metadata for a specific OpenAI file |
| `file_content_info` | Retrieve file content |
| `file_purpose_info` | List files by purpose |
| `file_delete` | Delete an OpenAI file |
| `file_wait` | Wait for file processing to complete |
| `batch` | Create an OpenAI batch job |
| `batch_info` | List or get details of OpenAI batch jobs |
| `batch_cancel` | Cancel an OpenAI batch job |

### Models

| Module | Description |
|---|---|
| `model_info` | List available OpenAI models |
| `model_detail_info` | Get details of a specific OpenAI model |
| `model_delete` | Delete a fine-tuned OpenAI model |
| `model_policy` | Define allowed or blocked models per project |
| `model_policy_info` | List model policies |

### Moderation & Content Safety

| Module | Description |
|---|---|
| `moderation` | Run content moderation check |
| `moderation_info` | Get moderation model categories |
| `moderation_batch` | Run batch content moderation |
| `content_filter_policy` | Manage content filter policies |

### Realtime API

| Module | Description |
|---|---|
| `realtime_session` | Create a realtime session |
| `realtime_session_info` | List realtime sessions |
| `realtime_session_config` | Configure realtime session parameters |
| `realtime_token` | Generate ephemeral realtime token |

### MCP (Model Context Protocol)

| Module | Description |
|---|---|
| `mcp_server_config` | Configure AAP MCP server connection |
| `mcp_tool_policy` | Define which tools AI agents can access |
| `mcp_audit_log_info` | Get MCP action audit trail |

### Organization & Governance

| Module | Description |
|---|---|
| `org_api_key` | Manage OpenAI API keys |
| `org_api_key_info` | List OpenAI API keys |
| `org_project` | Manage OpenAI organization projects |
| `org_project_info` | List OpenAI organization projects |
| `org_project_api_key` | Manage per-project API keys |
| `org_project_member` | Manage project membership |
| `org_user_info` | List OpenAI organization users |
| `org_user_role` | Manage OpenAI organization user roles |
| `org_user_invite_info` | List pending organization invites |
| `org_invite` | Send or manage OpenAI organization invites |
| `org_service_account` | Manage organization service accounts |
| `org_billing_info` | Get organization billing details |
| `org_usage_info` | Get OpenAI organization usage data |
| `org_rate_limit_info` | Get OpenAI rate limit status |
| `org_audit_log_info` | Get OpenAI organization audit logs |
| `org_cost_budget` | Set organization spending limits |
| `api_key_rotation` | Automated API key rotation |
| `usage_alert` | Configure usage threshold alerts |
| `usage_report` | Generate usage reports |
| `compliance_audit` | Generate compliance audit reports |
| `governance_dashboard_info` | Get governance metrics dashboard |

## Event-Driven Ansible (EDA)

The collection includes an EDA event source plugin that polls OpenAI usage and audit log endpoints.

### Event Source: `openai_events`

Emits events for usage spikes, audit log entries, and quota alerts.

```yaml
# eda-rulebook.yml
- name: React to OpenAI events
  hosts: all
  sources:
    - stevefulme1.openai.openai_events:
        api_key: "{{ openai_api_key }}"
        organization: "{{ openai_org }}"
        poll_interval: 60
        event_types:
          - usage_spike
          - audit_log
          - quota_warning
  rules:
    - name: Alert on high spend
      condition: event.type == "usage_spike" and event.cost_usd > 100
      action:
        run_playbook:
          name: notify_cost_alert.yml
```

## Contributing

Contributions are welcome. Please open an issue or pull request on
[GitHub](https://github.com/stevefulme1/ansible-openai).

## License

GNU General Public License v3.0 or later.
