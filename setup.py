from distutils.core import setup

VERSION = 'v0.4'

setup(
    name='lament',
    version=VERSION,
    author='Nic Roland',
    author_email='nicroland9@gmail.com',
    packages=['lament'],
    description='An easy way to handle application configuration (and open a schism to a dimention of endless pain and suffering).',
    url='https://github.com/nicr9/lament',
    download_url = 'https://github.com/nicr9/lament/tarball/%s' % VERSION,
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Other/Nonlisted Topic',
        ],
)
