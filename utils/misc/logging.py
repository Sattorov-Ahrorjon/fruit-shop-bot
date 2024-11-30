import os
import logging
from datetime import datetime

os.makedirs(name='data/logs', exist_ok=True)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    filename=f"data/logs/logs.log",
                    filemode='a'
                    # level=logging.DEBUG, # Можно заменить на другой уровень логгирования.
                    )
