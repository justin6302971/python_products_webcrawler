from os import environ

DEFAULT_ENDPOINT_URL=environ.get("LINE_NOTIFY_API_ENDPOINT")

LOGIN_URL = f'{DEFAULT_ENDPOINT_URL}/api/v1/auth/login'
MESSAGE_URL = f'{DEFAULT_ENDPOINT_URL}/api/v1/linenotify/send'

