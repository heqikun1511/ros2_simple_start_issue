from setuptools import find_packages, setup

package_name = 'py_pkg'

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
    maintainer='amoy',
    maintainer_email='3669308367@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "py_node=py_pkg.my_firstnode:main",
            "news_station=py_pkg.news_station:main",
            "smartphone=py_pkg.smartphone:main",
            "add_two_int_server=py_pkg.add_two_int_server:main",
            "add_two_ints_client_no_oop=py_pkg.add_two_ints_client_no_oop:main",
           "add_two_ints_client_oop=py_pkg.add_two_ints_client_oop:main",
           "number_publisher=py_pkg.number_publisher:main",
        ],
    },
)
