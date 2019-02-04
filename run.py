# team/reports/run.py

import os
from teamreports.gui import LoginForm


def main():
    """This function runs application gui"""
    a = LoginForm()
    a.mainloop()


if __name__ == '__main__':
    main()