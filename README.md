# wx-forecaster

Azure Function (Python) + Terraform + GitHub Actions to fetch forecasts from weather.gov.

## Quickstart
1. Set up Azure OIDC with GitHub.
2. Add repo secrets: AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID, AZURE_CLIENT_ID, WEATHERGOV_USER_AGENT, DEFAULT_POINTS.
3. Run Infra workflow to provision infra.
4. Run App workflow to deploy function.

## Usage
GET https://<function-app>.azurewebsites.net/api/<function-name>?latlon=33.4484,-112.0740&code=<function-key>

## Project layout

- `infra/` : Terraform infrastructure code for cloud resources.
- `function_app/` : Python Azure Function application source.
- `.github/workflows/` : GitHub Actions workflow definitions for CI/CD.
- `.gitignore` : Ignore rules for Python, Terraform, editors, and OS files.

## Notes

These folders are created as a starting scaffold. Add Terraform configs
under `infra/` and put your Azure Function code in `function_app/`.