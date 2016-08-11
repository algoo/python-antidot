# -*- coding: utf-8 -*-


def highlight(
        text_list: ['HighlightText'],
        surround: str='<span class="hightlight">{0}</span>'
) -> str:
    """
    Return high lighted text for list of HighlightText
    :param text_list: list of HighlightText
    :param surround: str expression to surround matched text,
    eg '<span class="hightlight">{0}</span>'
    :return: surrounded text
    """
    result = ''
    for text in text_list:
        if text.is_match:
            result += surround.format(str(text))
        else:
            result += str(text)
    return result
