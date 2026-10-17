# Security Policy

## Supported Versions

The current development version is `0.0.5`. Security fixes, where applicable, will be prioritized for the latest maintained version.

This is an early-stage, community-maintained project. No formal long-term support period or security response-time guarantee is provided.

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.** Do not publish credentials, API keys, exploitable details, or other sensitive information.

Project maintainer: Jan Reimen  
GitHub: https://github.com/janreimen

Use GitHub's **Report a vulnerability** feature in the repository's Security tab if private vulnerability reporting is enabled.

If private reporting is unavailable, contact the repository owner privately using the contact details available on their GitHub profile. Do not include real API keys, passwords, precise home coordinates, or unnecessary personal data.

Where possible, include:

- A description of the vulnerability.
- Its potential impact and affected components.
- The affected plugin version or commit.
- Reproduction steps or a proof of concept that does not expose real credentials or data.
- Any suggested mitigation.

Reports will be acknowledged and investigated as reasonably possible. The maintainer will coordinate remediation and disclosure where practical. No fixed response-time SLA is offered.

Please allow reasonable time for investigation and remediation before publicly disclosing an unpatched vulnerability.

## Security Practices

- **Secrets:** Keep `.env` files containing API keys or other secrets out of version control. Review `.gitignore` and check staged changes before committing.
- **Credentials in logs:** Do not log API keys, tokens, passwords, or complete credential-bearing URLs.
- **File permissions:** Restrict access to `.env` and other secret-bearing files to the Domoticz service account and authorized administrators.
- **Transport security:** Use HTTPS when communicating with `forecast.solar`. Do not disable TLS certificate verification to work around connection errors.
- **HTTP requests:** Use finite request timeouts and handle network failures and unsuccessful API responses safely.
- **External data:** Treat API responses and configuration values as external input. Validate data before using it in calculations or device updates.
- **Dependencies:** Keep dependencies limited to what the plugin needs, and review updates for relevant security fixes.
- **Diagnostics:** Redact credentials, personal data, public IP addresses, and precise location information before sharing logs or test output.

## Scope

This policy covers security issues in the Domoticz-SolarForecast plugin and its repository-maintained code. Issues in Domoticz, Python, operating systems, or external services should be reported to their respective maintainers when appropriate.
