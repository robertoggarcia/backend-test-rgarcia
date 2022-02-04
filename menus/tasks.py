from datetime import datetime

from backend_test.celery import app
from celery.schedules import crontab

from backend_test.settings import SEND_MENU_SETTINGS
from core.slack import send_slack_message
from menus.models import Menu


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(**SEND_MENU_SETTINGS),
        send_menu.s(),
    )


@app.task
def send_menu():
    """Daily task to send the current menu by slack"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    menu = Menu.objects.filter(date=current_date)
    if not menu.exists():
        return None

    menu = menu.first()
    try:
        send_slack_message(menu.id)
    except AssertionError:
        raise Exception('Send menu task: Error to send slack message')
    return menu
