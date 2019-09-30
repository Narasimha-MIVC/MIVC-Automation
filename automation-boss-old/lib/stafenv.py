'''This module is for adding modules as part of STAF env
'''

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "page"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "RobotKeywords"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "map"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Framework"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Framework",
                             "utils"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Framework","phone_wrappers","phone_4xx"))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Framework",
                             "db_connection"))
if 'PYTHONPATH' not in os.environ:
    os.environ['PYTHONPATH'] = os.path.join(os.path.dirname(os.path.dirname(
        os.path.dirname(__file__))), "Framework")

print(sys.path)