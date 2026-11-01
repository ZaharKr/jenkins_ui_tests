import os
from urllib.parse import quote, urlparse

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://demoqa.com",
        help="Адрес тестируемого сайта",
    )
    parser.addoption(
        "--remote-url",
        action="store",
        default="https://selenoid.qa.guru/wd/hub",
        help="Адрес удалённого браузера (Selenoid)",
    )
    parser.addoption(
        "--browser",
        action="store",
        choices=["chrome", "firefox"],
        default="chrome",
        help="Браузер",
    )
    parser.addoption(
        "--browser-version",
        action="store",
        default="156.0",
        help="Версия браузера",
    )
    parser.addoption(
        "--headless",
        action="store",
        choices=["true", "false"],
        default="false",
        help="Headless: true/false",
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920x1080",
        help="Разрешение экрана, например 1920x1080",
    )


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def _parse_window_size(value: str) -> tuple[int, int]:
    try:
        width, height = value.lower().split("x")
        return int(width), int(height)
    except ValueError as exc:
        raise pytest.UsageError("--window-size должен быть в формате 1920x1080") from exc


@pytest.fixture(scope="function")
def setup_browser(request):
    base_url = request.config.getoption("--base-url").rstrip("/")
    remote_url = request.config.getoption("--remote-url")
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser-version")
    headless = request.config.getoption("--headless") == "true"
    window_size = request.config.getoption("--window-size")
    width, height = _parse_window_size(window_size)

    login = os.getenv("SELENOID_LOGIN")
    password = os.getenv("SELENOID_PASSWORD")
    if not login or not password:
        pytest.fail(
            "В .env должны быть SELENOID_LOGIN и SELENOID_PASSWORD "
            "(см. .env.example)"
        )

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={width},{height}")
    else:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

    options.capabilities.update(
        {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": f"{width}x{height}x24",
            },
        }
    )

    encoded_login = quote(login, safe="")
    encoded_password = quote(password, safe="")
    command_executor = remote_url.replace(
        "://",
        f"://{encoded_login}:{encoded_password}@",
        1,
    )

    driver = webdriver.Remote(command_executor=command_executor, options=options)
    driver.set_window_size(width, height)
    driver.base_url = base_url
    driver.selenoid_url = f"{urlparse(remote_url).scheme}://{urlparse(remote_url).hostname}"

    yield driver

    attach.add_screenshot(driver)
    attach.add_page_source(driver)
    attach.add_console_logs(driver)
    attach.add_video(driver)

    driver.quit()
