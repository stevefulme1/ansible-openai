# Copyright: (c) 2026, Steve Fulmer
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
---
event_source: openai_events
short_description: >-
  Poll OpenAI usage API and audit logs for EDA events
description:
  - >-
    Polls the OpenAI organization usage and audit log
    endpoints at a configurable interval and emits events
    for automation triggers.
version_added: "1.1.0"
author: Steve Fulmer (@stevefulme1)
options:
  api_key:
    description: OpenAI API key.
    type: str
    required: true
  organization:
    description: OpenAI organization ID.
    type: str
    required: false
  poll_interval:
    description: Seconds between polling cycles.
    type: int
    default: 60
  event_types:
    description: >-
      List of event types to emit. Defaults to all.
    type: list
    elements: str
    default:
      - usage_threshold_exceeded
      - fine_tuning_completed
      - fine_tuning_failed
      - model_deployed
      - rate_limit_hit
      - api_key_expiring
"""

EXAMPLES = r"""
- name: Poll OpenAI for usage events
  stevefulme1.openai.openai_events:
    api_key: "{{ openai_api_key }}"
    organization: "org-abc123"
    poll_interval: 120
    event_types:
      - usage_threshold_exceeded
      - fine_tuning_completed
"""

import asyncio
import json
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen

_BASE_URL = "https://api.openai.com/v1"


def _api_get(endpoint, api_key, organization=None):
    """Make a GET request to the OpenAI API."""
    url = f"{_BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if organization:
        headers["OpenAI-Organization"] = organization
    req = Request(url, headers=headers, method="GET")
    try:
        resp = urlopen(req, timeout=30)
        return json.loads(resp.read().decode("utf-8"))
    except URLError:
        return None


def _check_usage(api_key, organization):
    """Check usage and return events if thresholds exceeded."""
    events = []
    data = _api_get("organization/usage", api_key, organization)
    if not data:
        return events
    total = data.get("total_usage", 0)
    if total > 0:
        events.append(
            {
                "type": "usage_threshold_exceeded",
                "total_usage": total,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    return events


def _check_fine_tuning(api_key, organization):
    """Check fine-tuning jobs for completed/failed."""
    events = []
    data = _api_get("fine_tuning/jobs?limit=10", api_key, organization)
    if not data or "data" not in data:
        return events
    for job in data["data"]:
        status = job.get("status", "")
        if status == "succeeded":
            events.append(
                {
                    "type": "fine_tuning_completed",
                    "job_id": job.get("id"),
                    "model": job.get("fine_tuned_model"),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
        elif status == "failed":
            events.append(
                {
                    "type": "fine_tuning_failed",
                    "job_id": job.get("id"),
                    "error": job.get("error"),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
    return events


def _check_audit_logs(api_key, organization):
    """Check audit logs for key events."""
    events = []
    data = _api_get(
        "organization/audit_logs?limit=20",
        api_key,
        organization,
    )
    if not data or "data" not in data:
        return events
    for entry in data["data"]:
        etype = entry.get("type", "")
        if "model.deployed" in etype:
            events.append(
                {
                    "type": "model_deployed",
                    "details": entry,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
        elif "rate_limit" in etype:
            events.append(
                {
                    "type": "rate_limit_hit",
                    "details": entry,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
        elif "api_key" in etype and "expir" in etype:
            events.append(
                {
                    "type": "api_key_expiring",
                    "details": entry,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
    return events


async def main(queue, args):
    """Entry point for the EDA event source plugin."""
    api_key = args.get("api_key")
    organization = args.get("organization")
    poll_interval = int(args.get("poll_interval", 60))
    event_types = args.get(
        "event_types",
        [
            "usage_threshold_exceeded",
            "fine_tuning_completed",
            "fine_tuning_failed",
            "model_deployed",
            "rate_limit_hit",
            "api_key_expiring",
        ],
    )

    seen_events = set()

    while True:
        all_events = []
        all_events.extend(_check_usage(api_key, organization))
        all_events.extend(_check_fine_tuning(api_key, organization))
        all_events.extend(_check_audit_logs(api_key, organization))

        for event in all_events:
            if event["type"] not in event_types:
                continue
            event_key = "{}-{}".format(
                event["type"],
                event.get("job_id", event.get("timestamp")),
            )
            if event_key in seen_events:
                continue
            seen_events.add(event_key)
            await queue.put(event)

        await asyncio.sleep(poll_interval)


if __name__ == "__main__":

    class _MockQueue:
        async def put(self, event):
            print(json.dumps(event, indent=2))

    asyncio.run(
        main(
            _MockQueue(),
            {"api_key": "test", "poll_interval": 5},
        )
    )
