#!/usr/bin/env python
# -*- coding: utf-8 -*-


def ms_str_2_date(ms_str):
    """
    Convert timeMs to js Date.
    :param ms_str: timeMs string.
    :return: js Date str.
    """
    return "new Date(%s * 1000)" % ms_str