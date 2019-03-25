# -*- coding: utf-8 -*-
import logging


# 创建一个日志用来记录当网站不存在时候的情况
logger = logging.getLogger('logging')
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler(filename='classification.log',encoding='utf-8')
fileHandler.setLevel(logging.DEBUG)

outputHandler = logging.StreamHandler()
outputHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
outputHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(outputHandler)