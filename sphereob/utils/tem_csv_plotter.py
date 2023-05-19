if (
        self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked()) and self.options_menu.sphere_y.isChecked():

    self.axes = self.fig.add_subplot(3, 1, 1)
    x = sphere.H_tot_x
    i = 0
    while i < len(sphere.H_tot_x):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('x-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.axes = self.fig.add_subplot(3, 1, 2)
    z = sphere.H_tot_z
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('z-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.axes = self.fig.add_subplot(3, 1, 3)
    y = sphere.H_tot_y
    i = 0
    while i < len(sphere.H_tot_y):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('y-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.canvas.draw()



elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_y.isChecked() == False:

    self.axes = self.fig.add_subplot(2, 1, 1)
    x = sphere.H_tot_x
    i = 0
    while i < len(sphere.H_tot_x):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('x-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.axes = self.fig.add_subplot(2, 1, 2)
    z = sphere.H_tot_z
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('z-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.canvas.draw()

elif self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_y.isChecked():

    self.axes = self.fig.add_subplot(2, 1, 1)
    x = sphere.H_tot_x
    i = 0
    while i < len(sphere.H_tot_x):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('x-component (A/m)')
    self.axes.grid(True, which='both', ls='-')
    # the first subplot in the first figure

    self.axes = self.fig.add_subplot(2, 1, 2)
    y = sphere.H_tot_y
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('y-component (A/m)')
    self.axes.grid(True, which='both', ls='-')
    # self.canvas.addWidget(self.navi_toolbar)

    self.canvas.draw()
elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked():

    self.axes = self.fig.add_subplot(2, 1, 1)
    z = sphere.H_tot_z
    i = 0
    while i < len(sphere.H_tot_x):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('z-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.axes = self.fig.add_subplot(2, 1, 2)
    y = sphere.H_tot_y
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('y-component (A/m)')
    self.axes.grid(True, which='both', ls='-')

    self.canvas.draw()


elif self.options_menu.sphere_x.isChecked() and self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_y.isChecked() == False:

    self.fig.clf()
    self.axes = self.fig.add_subplot(111)
    x = sphere.H_tot_x
    i = 0
    while i < len(sphere.H_tot_x):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_x[i],
                       color='0.4')  # will have to change x axis for changing param
        i += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('x-component (A/m)')
    self.axes.grid(True, which='both', ls='-')
    self.canvas.draw()


elif self.options_menu.sphere_z.isChecked() and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked() == False:

    self.fig.clf()
    self.axes = self.fig.add_subplot(111)
    z = sphere.H_tot_z
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_z[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('z-component (A/m)')
    self.axes.grid(True, which='both', ls='-')
    self.canvas.draw()
elif self.options_menu.sphere_z.isChecked() == False and self.options_menu.sphere_x.isChecked() == False and self.options_menu.sphere_y.isChecked():

    self.fig.clf()
    self.axes = self.fig.add_subplot(111)
    y = sphere.H_tot_y
    k = 0
    while k < len(sphere.H_tot_z):
        self.axes.plot(np.linspace(sphere.profile[0][0], sphere.profile[0][100], 101), sphere.H_tot_y[k],
                       color='0.4')  # will have to change x axis for changing param
        k += 1

    self.axes.set_xlabel('Profile (m)')
    self.axes.set_ylabel('y-component (A/m)')
    self.axes.grid(True, which='both', ls='-')
    self.canvas.draw()