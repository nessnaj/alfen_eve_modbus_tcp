# Reminder for package creation

## Pre-requisites
1. Make sure to have an account on PyPI.org.

2. In order to upload the package to be created, you need to install ```twine```:

    ```pip3 install twine```

## Package Creation
Make sure to update the version number in ```setup.cfg``` before creating the package
```commandline
make clean # To remove old code and folders.
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
Now anyone that wants to make use of the newly created package can do:

```pip3 install alfen-eve-modbus-tcp```

