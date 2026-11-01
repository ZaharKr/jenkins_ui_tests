# jenkins_ui_tests

qa-guru: Jenkins UI + Selenoid + Allure + параметризация.

## Параметры CLI

| Параметр | Пример | Описание |
|----------|--------|----------|
| `--base-url` | `https://demoqa.com` | сайт |
| `--remote-url` | `https://selenoid.qa.guru/wd/hub` | Selenoid |
| `--browser` | `chrome` / `firefox` | браузер |
| `--browser-version` | `156.0` | версия |
| `--headless` | `true` / `false` | headless |
| `--window-size` | `1920x1080` | разрешение |

Логин/пароль Selenoid — в `.env` (`SELENOID_LOGIN`, `SELENOID_PASSWORD`).

## Локальный запуск

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # если ещё нет

pytest -v \
  --base-url=https://demoqa.com \
  --remote-url=https://selenoid.qa.guru/wd/hub \
  --browser=chrome \
  --browser-version=156.0 \
  --headless=false \
  --window-size=1920x1080
```

## Jenkins

Параметризованная job: Choice / String / Boolean → передаются в `pytest`.
Перед shell создаётся `.env` с логином/паролем Selenoid.

## Telegram notifications

См. `notifications/config.json.example` и `Selenium 1/lesson_14/NOTES.md`.
Jar: `allure-notifications-4.11.1` (скачивается в Jenkins).
