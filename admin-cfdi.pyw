import sys
import os.path


ac_path = os.path.join(sys.path[0], "admin-cfdi")
exec(open(ac_path, encoding='utf-8').read())
