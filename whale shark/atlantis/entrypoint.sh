#!/bin/bash

atlantis server --gh-user="solon-the-explorer" --gh-token="$ATLANTIS_TOKEN" \
--gh-webhook-secret="$ATLANTIS_WEBHOOK_SECRET" \
--repo-allowlist="$REPO_ALLOWLIST" \
--atlantis-url="http://localhost" \
--port=4041
