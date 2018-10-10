#upgrade
python -m pip install --user --upgrade setuptools wheel

# build
python setup.py sdist bdist_wheel

#install whl
pip install *.whl

pip install C:\Project\team.datasync\dist\team.reports-0.0.1-py3-none-any.whl