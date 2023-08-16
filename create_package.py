import os
import re
import shutil
import subprocess
import sys

PREINSTALLED = {'botocore', 'boto3', 's3transfer'}

with open('./requirements.txt', 'r') as requirements:
    for req in requirements.readlines():
        module = re.search(r'\w+', req).group()
        if module not in PREINSTALLED:
            subprocess.check_call([
                sys.executable, '-m',
                'pip', 'install',
                '--target', './package',
                '--upgrade', req
            ])
        else:
            print(f'Skipping: {req}')

os.makedirs('./package/src')
src_dir = f'{os.getcwd()}/src_py'
for ele in os.listdir(src_dir):
    if ele.endswith('.py'):
        shutil.copy(f'src_py/{ele}', './package/src')

shutil.make_archive('./package', 'zip', './package')
shutil.rmtree('./package')
