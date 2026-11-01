# jenkins_ui_tests

qa-guru homework: Jenkins + Selenoid + Selenium PageObject + Allure attachments (demoqa.com).

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
allure serve allure-results
```

Selenoid: `https://user1:1234@selenoid.qa.guru/wd/hub` (Chrome `156.0`).

## Jenkins

- Label: `python`
- Branch: `*/main`
- Execute shell:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest .
```

- Post-build: Allure Report → `allure-results`
