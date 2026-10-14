# Security Policy

## Supported versions

The current release line is `0.0.3`. Security fixes, if any, will be prioritized for the latest maintained version. This early-stage project does not promise a formal long-term support window.

## Reporting a vulnerability

Please do not publish credentials, API keys, exploitable details, or other sensitive information in a public issue.

Project maintainer: Jan Reimen (GitHub: https://github.com/janreimen). Until a private security contact is configured in the repository, use GitHub's **Report a vulnerability** feature (Security tab / private vulnerability reporting) if it is enabled. If that feature is unavailable, contact the repository owner privately through the contact details on their GitHub profile. Include a description, impact, affected version, reproduction steps, and any suggested mitigation. Avoid sending real API keys or personal data.

We will acknowledge reports when reasonably possible, investigate, and coordinate a fix or disclosure. No fixed response-time SLA is offered for this community project.

## Security practices

- Keep `.env` out of version control; it may contain an API key.
- Do not log credential-bearing URLs or tokens.
- Restrict `.env` permissions to the Domoticz service account and administrators.
- Use HTTPS to access forecast.solar.
- Treat API responses as external input and use finite HTTP timeouts.
- Redact personal data and tokens before sharing logs.
