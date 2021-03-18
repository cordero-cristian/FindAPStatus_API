from pathlib import Path
import logging.config

currentDir = Path().cwd() / 'LoggingFunctions'
iniFile = currentDir / 'logging.ini'
logging.config.fileConfig(iniFile)
