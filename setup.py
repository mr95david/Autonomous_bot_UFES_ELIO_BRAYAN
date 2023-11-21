import glob
from setuptools import find_packages, setup
import os

package_name = 'tb3_nav'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'worlds'), 
          [os.path.join('worlds', 'worldEndA.world'),
           os.path.join('worlds', 'worldEndB.world'),
           os.path.join('worlds', 'worldEndC.world')]),
        
        (os.path.join('share', package_name, 'launch'), 
          glob.glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Elio',
    maintainer_email='eliotrianar95@gmail.com',
    description='Assignment 1: Autonomous Robots - UFES',
    license='Apache 2.0 license',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'tb3_nav = tb3_nav.tb3_nav:main',
            'Detectar_Objetos = tb3_nav.nodo_objetos:main'
        ],
    },
)
