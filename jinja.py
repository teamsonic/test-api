from jinja2 import Environment, FileSystemLoader


def getThreads():
    loader = FileSystemLoader('templates/', encoding='utf-8')
