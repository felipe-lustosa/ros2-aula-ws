import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/flca2/Documents/dev/programacao_robos/ros2_aula_ws/install/py_pubsub'
