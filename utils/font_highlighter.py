#!/usr/bin/env python
# coding=utf-8
'''
Date         : 2022-09-03 20:12:45
LastEditors  : Chen Chengshuai
LastEditTime : 2022-09-03 20:12:46
FilePath     : /NERAnnotator/utils/font_highlighter.py
Description  : 
'''

from PyQt5.QtGui import QFont
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QTextCharFormat
from PyQt5.QtGui import QSyntaxHighlighter



class FontHighlighter(QSyntaxHighlighter):
    """字体高亮类
    """
    
    rules = []
    formats = dict()
    
    def __init__(self, parent=None):
        super(FontHighlighter, self).__init__(parent)
        
        self.initializeFormats()
        
        #! Qt 不支持 .*? 这种非贪婪匹配语法。
        #! 只要使用了 setMinimal(true) 之后，所有的匹配都会变成非贪婪的。
        self.taggedEntity = QRegExp(r'\[\@.*\#.*\*\](?!\#)')
        self.taggedEntity.setMinimal(True)
        self.recommendEntity = QRegExp(r'\[\$.*\#.*\*\](?!\#)')
        self.recommendEntity.setMinimal(True)
        
        FontHighlighter.rules.append((self.taggedEntity, 'taggedEntity'))
        FontHighlighter.rules.append((self.recommendEntity, 'recommendEntity'))

    @classmethod
    def initializeFormats(cls):
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily('黑体')
        baseFormat.setFontPointSize(18)
        
        for name, color in [
            ['taggedEntity', QColor(255, 106, 106)],
            ['recommendEntity', QColor(60, 179, 113)]
        ]:
            format = QTextCharFormat(baseFormat)
            format.setFontWeight(QFont.Bold)
            format.setBackground(color)            # 设置背景色
            # format.setForeground(QColor(color))  # 设置字体色
            format.setFontWeight(QFont.Bold)
            format.setFontItalic(True)
            cls.formats[name] = format
    
    def highlightBlock(self, text: str) -> None:
        for regex, format in FontHighlighter.rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(
                    i,
                    length,
                    FontHighlighter.formats[format]
                )
                i = regex.indexIn(text, i + length)