Sphere-ob Airborne EM modelling 
====

Sphere-ob (sphere-overburden) is a python program developed to calculate and plot the airborne TDEM response of a sphere or ‘dipping sphere’ underlying conductive overburden. 
The response is calculated using the semi-analytic solution set presented in Desmerais & Smith (2016), this solution set is computationally efficient and allows the user to model a thin sheet in addition to a sphere, by artificially restricting current flow to parallel planes within an anisotropic sphere.

Installation
====

If you have python added to path and are familiar with pip, Sphere-ob may be installed with pip + git by opening a comand prompt as administrator and using::

	pip install git+https://github.com/anonseg2023/sphereob

Alternatively, the repository can be manually downloaded and installed using the install script, i.e., by navigating to the ShereOverburdenProject folder, opening a python / anaconda prompt in administrator and running::


	python setup.py install


Once these steps have been completed the program can be launched from the command line using::


	sphereob

For anaconda users or users who do not have python added to path, you may want to install sphere-ob into a separate Anaconda environment, this can be done easily by running the install_or_update.bat.

You can then switch to the newly installed environment using::

	conda activate sphereob

Or, if using git-bash::

	source activate sphereob

Note: By default, new terminals start in the 'base' environment, so you will have to enter the above command each time you open a new terminal. Alternatively, you may add the command to your ~/.bashrc file to have it run automatically. See the the `Anaconda Environemnent documentation <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_ for more details.

Once the environment has been activated the user may then navigate to the project directory in an anaconda prompt then launch the program using::


	python sphereob.py

Dependencies
====

* matplotlib
* numpy
* scipy
* pyqt5
* pandas


Documentation
====

Documentation, including explanations of the model parameters and data importers is included in SPHERE-OB.pdf
