from setuptools import setup


setup(name='sphereob',
      version='0.0.83',
      description='GUI program to model the airborne EM response of a sphere underlying conductive overburden',
      url='https://github.com/adzamper71/SphereOverburden',
      author='Anon',
      author_email='anon@gmail.com',
      packages=['sphereob',
                'sphereob.GUI',
                'sphereob.utils',
                'sphereob.resources'],
      long_description=open('readme.rst').read(),
      scripts=[],
      entry_points={'console_scripts': ['sphereob = sphereob.GUI.sphere_overburden_gui:main']},
      install_requires=['numpy',
                        'pandas',
                        'matplotlib',
                        'qdarkstyle',
                        'scipy',
                        'pyqt5'
                       ],
      include_package_data=True)