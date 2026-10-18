# Security Policy

## Supported versions

The current development/release line is `0.0.5`. Security fixes, if any, will be prioritized for the latest maintained version. This early-stage project does not promise a formal long-term support window or response-time SLA.

## Reporting a vulnerability

Please do not publish credentials, API keys, exploitable details, or other sensitive information in a public issue.

Use GitHub's **Report a vulnerability** feature in the repository's Security tab if private vulnerability reporting is enabled. If it is unavailable, contact the repository owner privately through the contact details on the [maintainer's GitHub profile](https://github.com/janreimen). Include the affected version, impact, steps to reproduce, and any suggested mitigation. Do not include real API keys, precise home coordinates, or other personal data.

Reports will be acknowledged and investigated when reasonably possible. Coordinated disclosure will be preferred where practical, but no fixed response-time SLA is offered.

## Security practices

- Keep `.env` out of version control; it may contain an API key.
- Restrict `.env` permissions to the Domoticz service account and administrators (for example, `chmod 600 .env`).
- Do not put credentials in URLs or log tokens and secrets.
- Use HTTPS to access forecast.solar.
- Use finite HTTP timeouts and treat API responses as external input.
- Keep dependencies and the Domoticz installation updated.
- Redact private data and tokens before sharing logs or configuration snippets.
