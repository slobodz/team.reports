# team/reports/run.py

# # add to sys.path level below the folder containing this script
# import sys,os
# sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import os
from teamreports.gui import LoginForm


def main():
    a = LoginForm()
    a.mainloop()


if __name__ == '__main__':
    main()