from libs import logger


# handles different types of event
def get_app_mention_text(e):
    # app_mention: https://gist.github.com/Junyong-Suh/94fc948c8c1f7819a258101a23f169aa
    if is_event_type_app_mention(e) and 'text' in e:
        return e['text'], True

    if is_event_type_message(e):
        # message_changed: https://gist.github.com/Junyong-Suh/20e0291bc3ba230b2496ea2620cc66dd
        if is_message_subtype_message_changed(e):
            logger.info(f"Message changed: {e}")
            return e, False

        # message_deleted: https://gist.github.com/Junyong-Suh/385d2d68dd3ffbf88dad50f2032716c8
        if is_message_subtype_message_deleted(e):
            logger.info(f"Message deleted: {e}")
            return e, False

        if is_message_with_no_subtype(e):
            logger.info(f"Message in general: {e}")
            return e, False

    logger.error(f"Unexpected event: {e}")
    return e, False


def is_event_type_app_mention(e):
    return 'type' in e and e['type'] == 'app_mention'


def is_event_type_message(e):
    return 'type' in e and e['type'] == 'message'


def is_message_subtype_message_changed(e):
    return 'subtype' in e and e['subtype'] == 'message_changed'


def is_message_subtype_message_deleted(e):
    return 'subtype' in e and e['subtype'] == 'message_deleted'


def is_message_with_no_subtype(e):
    return not ('subtype' in e)


# progress percent
def progress_percent(count):
    percent = round(int(count) / int(21) * 100, 2)
    if int(count) == 1:
        return f"{count} time ({percent}%)"
    else:
        return f"{count} times ({percent}%)"
