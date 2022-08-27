import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.project_slug}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project slug (%s) is not a valid Python module name. Please do not use a - and use _ instead' % module_name)

    #Exit to cancel project
    sys.exit(1)

PYTHON_VERSION_REGEX = r'^(2|3)'

python_interpreter_version = '{{ cookiecutter.python_interpreter_version}}'

if not re.match(PYTHON_VERSION_REGEX, python_interpreter_version):
    print(f'ERROR: {python_interpreter_version} is an invalid Python version')
    sys.exit(1)
