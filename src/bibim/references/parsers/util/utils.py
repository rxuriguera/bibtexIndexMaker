# -*- coding: utf-8 -*-

# $Copy$

""" Collection of python utility-methodes commonly used by other
    bibliograph packages.

$Id$
"""
__docformat__ = 'reStructuredText'
__author__ = 'Tom Gross <itconsense@gmail.com>'

_default_encoding = 'utf-8'
_entity_mapping = {'&mdash;':'{---}',
                   '&ndash;':'{--}',
                   }

def _encode(s, encoding=_default_encoding):
    ur""" Try to encode a string

        >>> from bibliograph.core.utils import _encode

        ASCII is ASCII is ASCII ...
        >>> _encode(u'ascii', 'utf-8')
        'ascii'

        This is normal
        >>> _encode(u'öl', 'utf-8')
        '\xc3\xb6l'

        Don't fail on this ...
        >>> _encode('öl', 'utf-8')
        '\xc3\xb6l'

        Don't fail on this also
        >>> _encode(None, 'utf-8')
        ''

        Still throw an exception on unknown encodings
        >>> _encode(u'öl', 'bogus')
        Traceback (most recent call last):
        ...
        LookupError: unknown encoding: bogus

    """
    if not s:
        return ''
    try:
        return s.encode(encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s

def _decode(s, encoding=_default_encoding):
    ur""" Try to decode a string

        >>> from bibliograph.core.utils import _decode

        ASCII is ASCII is ASCII ...
        >>> _decode('ascii', 'utf-8')
        u'ascii'

        This is normal
        >>> _decode('öl', 'utf-8')
        u'\xf6l'

        Don't fail on this ...
        >>> _decode(u'öl', 'utf-8')
        u'\xf6l'

        Still throw an exception on unknown encodings
        >>> _decode('öl', 'bogus')
        Traceback (most recent call last):
        ...
        LookupError: unknown encoding: bogus

    """
    try:
        return unicode(s, encoding)
    except (TypeError, UnicodeDecodeError, ValueError):
        return s
