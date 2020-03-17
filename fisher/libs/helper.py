# _*_ coding: utf-8 _*_
import requests

__author__ = 'john'


def is_isbn_or_key(word):
    """
    判断用户输入为isbn或关键字搜索
    :param word:
    :return:
    """
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('_', '')
    if '_' in word and len(short_word) and word.short_word.isdigit:
        isbn_or_key = 'isbn'
    return isbn_or_key

