##responsible for creating the app as a package. It can be installed and used.


from setuptools import find_packages,setup
from typing import List 

HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path, 'r') as file_obj:
        for line in file_obj:
            req = line.strip()
            if req and req != HYPHEN_E_DOT:
                requirements.append(req)
    return requirements

setup(
    name='dscproject',
    version='0.0.1',
    author='ShawnT',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)


##when find packages is running it looks for init.py in all folders.
##It considers that folder a package.