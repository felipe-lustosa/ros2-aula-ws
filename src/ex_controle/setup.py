from setuptools import find_packages, setup

package_name = 'ex_controle'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='flca2',
    maintainer_email='felipelustosaa6@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'cmd_turtle = ex_controle.control_turtle:main',
            'cmd_tiago = ex_controle.control_tiago:main',
            'cmd_arm = ex_controle.control_arm:main',
            'cmd_head = ex_controle.control_head:main',
            'cmd_laser = ex_controle.process_laser:main',
            'image_test = ex_controle.process_image:main',
        ],
    },
)
