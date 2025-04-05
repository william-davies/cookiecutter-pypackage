import sys

REQUIRED_PYTHON_VERSION = "{{ cookiecutter.python_interpreter_version }}"


def main():
    system_major = sys.version_info.major
    required_major = int(REQUIRED_PYTHON_VERSION.split('.')[0])

    if system_major != required_major:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                required_major, sys.version))
    else:
        print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()
