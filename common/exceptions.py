# -*- coding: utf-8 -*-
# @Author  : Windy.Gu
# @Software: PyCharm
# @Time    : 2022/6/30 20:53
# @File    : exceptions.py


"""
Exceptions that may happen in all the poium code.
"""


class PoiumException(Exception):
    """
    Base poium exception.
    """

    def __init__(self, msg=None, screen=None, stacktrace=None):
        self.msg = msg
        self.screen = screen
        self.stacktrace = stacktrace

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        if self.screen is not None:
            exception_msg += "Screenshot: available via screen\n"
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg


class PageSelectException(PoiumException):
    """
    Thrown when using a select box error
    """
    pass


class PageElementError(PoiumException):
    """
    Raises an error using the PagElement class
    """
    pass


class FindElementTypesError(PoiumException):
    """
    Find element types Error
    """
    pass


class CSSFindElementError(PoiumException):
    """
    Find element types Error
    """
    pass


class FindElementTimedOutException(PoiumException):
    """
    Find element timeout exception
    """
    pass


class ElementException(PoiumException):
    """
    Element exception
    """
    pass


class ElementNoFindException(PoiumException):
    """
    Element no find exception
    """
    pass


class AssertNoEqualException(PoiumException):
    """
    Assert no equal exception
    """
    pass
