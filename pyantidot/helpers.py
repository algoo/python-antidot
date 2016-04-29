# -*- coding: utf-8 -*-


def high_light(text_list: ['HighLightText'], surround: str='<span class="hight-light">{0}</span>') -> str:
    """
    Return high lighted text for list of HighLightText
    :param text_list: list of HighLightText
    :param surround: str expression to surround matched text, eg '<span class="hight-light">{0}</span>'
    :return: surrounded text
    """
    result = ''
    for text in text_list:
        if text.is_match:
            result += surround.format(str(text))
        else:
            result += str(text)
    return result
