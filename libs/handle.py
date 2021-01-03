from libs import commands_admin, commands_general, redis, slack, utils as u


KEYWORDS_MARK = ["done", "Done", "DONE", "인증", "ㅇㅈ"]
KEYWORDS_STATUS = ["status", "Status", "STATUS", "현황"]
KEYWORDS_CANCEL = ["cancel", "Cancel", "CANCEL", "취소", "ㅊㅅ"]
KEYWORDS_HELP = ["help", "Help", "HELP"]
KEYWORDS_DISABLE = ["긴급상황"]
KEYWORDS_ENABLE = ["돌아와줘"]
KEYWORDS_IS_ENABLED = ["살아있니"]


# handle only associated event
def event(e):
    event_text, should_process = u.get_app_mention_text(e)

    # do nothing if app mention text is not available
    if not should_process:
        return e

    # Admin Commands (process although the app is disabled)
    e, is_processed = admin_commands(e, event_text)
    if is_processed:
        return e

    # reject if the app is disabled hereafter
    if not redis.is_app_enabled():
        return reject(e)

    # General Commands (rejected if the app is disabled)
    e, is_processed = general_commands(e, event_text)
    if is_processed:
        return e

    return e


# Admin Commands (process although the app is disabled)
def admin_commands(e, event_text):
    # disable the app - emergency stop
    if any(tag in event_text for tag in KEYWORDS_DISABLE):
        return commands_admin.disable(e), True

    # enable the app
    if any(tag in event_text for tag in KEYWORDS_ENABLE):
        return commands_admin.enable(e), True

    # whether the app is enabled
    if any(tag in event_text for tag in KEYWORDS_IS_ENABLED):
        return commands_admin.is_enabled(e), True

    # not processed
    return e, False


# General Commands (rejected if the app is disabled)
def general_commands(e, event_text):
    # help
    if any(tag in event_text for tag in KEYWORDS_HELP):
        return commands_general.usage(e), True

    # mark
    if any(tag in event_text for tag in KEYWORDS_MARK):
        return commands_general.mark(e), True

    # status
    if any(tag in event_text for tag in KEYWORDS_STATUS):
        return commands_general.status(e), True

    # cancel
    if any(tag in event_text for tag in KEYWORDS_CANCEL):
        return commands_general.cancel(e), True

    # not processed
    return e, False


# reject if the app is disabled
def reject(e):
    message = {
        "channel": e['channel'],
        "text": "The app is disabled by admin :pray: - please contact admins"
    }
    slack.send_message(message)
    return e
