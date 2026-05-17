# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Base API client for OpenAI REST API."""

from __future__ import absolute_import, division, print_function
__metaclass__ = type
import json

from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.urls import open_url


class OpenAIError(Exception):
    """Exception raised for OpenAI API errors."""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class OpenAIClient:
    """REST client for the OpenAI API."""

    DEFAULT_BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key, organization=None, base_url=None, timeout=30):
        self.api_key = api_key
        self.organization = organization
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout

    def _headers(self, extra=None):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization
        if extra:
            headers.update(extra)
        return headers

    def _request(self, method, path, data=None, params=None, headers=None):
        url = "{}/{}".format(self.base_url, path.lstrip("/"))
        if params:
            url = f"{url}?{urlencode(params)}"
        body = None
        if data is not None:
            body = json.dumps(data)
        req_headers = self._headers(headers)
        try:
            resp = open_url(
                url,
                method=method,
                data=body,
                headers=req_headers,
                timeout=self.timeout,
            )
            resp_body = resp.read()
            if resp_body:
                return json.loads(resp_body)
            return {}
        except Exception as e:
            error_msg = str(e)
            status_code = getattr(e, "code", None)
            body = None
            fp = getattr(e, "read", None)
            if callable(fp):
                try:
                    body = json.loads(fp())
                    if "error" in body:
                        error_msg = body["error"].get("message", error_msg)
                except Exception:
                    pass
            raise OpenAIError(error_msg, status_code=status_code, response=body)

    def get(self, path, params=None):
        """Send a GET request."""
        return self._request("GET", path, params=params)

    def post(self, path, data=None):
        """Send a POST request."""
        return self._request("POST", path, data=data)

    def delete(self, path):
        """Send a DELETE request."""
        return self._request("DELETE", path)

    def list_paginated(self, path, params=None):
        """Fetch all pages using cursor-based pagination."""
        params = dict(params or {})
        results = []
        while True:
            resp = self.get(path, params=params)
            results.extend(resp.get("data", []))
            if not resp.get("has_more"):
                break
            last_id = resp.get("last_id")
            if not last_id:
                break
            params["after"] = last_id
        return results

    def upload_file(self, path, file_data, purpose, extra_fields=None):
        """Upload a file using multipart/form-data."""
        import os

        boundary = "----AnsibleOpenAIBoundary"
        body_parts = []

        body_parts.append(f"--{boundary}")
        body_parts.append('Content-Disposition: form-data; name="purpose"')
        body_parts.append("")
        body_parts.append(purpose)

        if extra_fields:
            for key, value in extra_fields.items():
                body_parts.append(f"--{boundary}")
                body_parts.append(f'Content-Disposition: form-data; name="{key}"')
                body_parts.append("")
                body_parts.append(str(value))

        filename = "upload"
        if isinstance(file_data, str) and os.path.isfile(file_data):
            filename = os.path.basename(file_data)
            with open(file_data, "rb") as f:
                content = f.read()
        elif isinstance(file_data, bytes):
            content = file_data
        else:
            content = file_data.encode("utf-8") if isinstance(file_data, str) else file_data

        body_parts.append(f"--{boundary}")
        body_parts.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"')
        body_parts.append("Content-Type: application/octet-stream")
        body_parts.append("")

        body_header = "\r\n".join(body_parts) + "\r\n"
        body_footer = f"\r\n--{boundary}--\r\n"

        body = body_header.encode("utf-8") + content + body_footer.encode("utf-8")

        url = "{}/{}".format(self.base_url, path.lstrip("/"))
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        }
        if self.organization:
            headers["OpenAI-Organization"] = self.organization

        try:
            resp = open_url(
                url,
                method="POST",
                data=body,
                headers=headers,
                timeout=self.timeout,
            )
            resp_body = resp.read()
            if resp_body:
                return json.loads(resp_body)
            return {}
        except Exception as e:
            raise OpenAIError(str(e), status_code=getattr(e, "code", None))


def openai_argument_spec():
    """Return shared argument spec for OpenAI modules."""
    return dict(
        api_key=dict(type="str", required=True, no_log=True),
        organization=dict(type="str", required=False, default=None),
        base_url=dict(type="str", required=False, default=None),
        timeout=dict(type="int", required=False, default=30),
    )
