

"""
 Main routine used to calculate the sphere-overburden response using the semi-analytical solution described in Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
 This script is called by sphereexe when the "plot response" button is clicked in the GUI
"""




#imports
import numpy as np
import math

class sphereresponse(object):
    def __init__(self):

        self.mu = 1.256637e-6  # permeability of free space
        self.dipole_m = 1847300  # dipole moment of tx
        self.rtx = np.array([0, 0, 120],dtype=np.int64)  # Tx co-ordinates in array
        self.radar = self.rtx[2]  # height of transmitter above ground surface=
        self.offset_tx_rx = np.array([12.5, 0, 56],dtype=np.int64)  # offset from transmitter to receiver array

        self.rrx = np.array([self.rtx[0] - self.offset_tx_rx[0], self.rtx[1] - self.offset_tx_rx[1],
                        self.rtx[2] - self.offset_tx_rx[2]],dtype=np.int64)  # receiver co-ordinate array


        self.rsp = np.array([-200],dtype=np.int64) # sphere position array
        self.a = 60.0  # sphere radius
        self.sigma_sp = 0.5  # sphere conductivity
        self.mtx = np.array([0, 0, 1],dtype=np.int64)  # unit vector of transmitter dipole moment
        self.interval = 101
        self.profile_length = 1000
        self.profile = np.zeros((1, self.interval))  # profile position vector
        self.profile_rrx = np.zeros((1, self.interval))
        self.PlottingPoint = 'Rx'
        self.Xsign = "+ve"

        # Default HELITEM window centers

        self.wc = np.array([0.000154600000000000, 0.000236000000000000, 0.000333700000000000, 0.000447600000000000,
                       0.000577800000000000, 0.000740600000000000, 0.000944000000000000, 0.00118820000000000,
                       0.00151370000000000, 0.00192060000000000, 0.00253090000000000, 0.00334470000000000,
                       0.00456540000000000, 0.00619300000000000, 0.00901430000000000])




        self.nw = len(self.wc)  # Number of windows

        self.P = 3.65 * 1E-3  # Pulse length

        self.bfreq = 25  # Frequency of transmitter waveform

        self.T = 1 / self.bfreq  # Period

        self.H_tot_x = np.zeros((self.nw, self.interval))  # Response vectors
        self.H_tot_y = np.zeros((self.nw, self.interval))
        self.H_tot_z = np.zeros((self.nw, self.interval))

        self.C_x = np.zeros((self.nw, self.interval))  # Induced sphere moment vectors
        self.C_z = np.zeros((self.nw, self.interval))

        self.H_ob1 = np.zeros((self.nw, self.interval))  # Overburden response vectors
        self.H_ob2 = np.zeros((self.nw, self.interval))
        self.H_ob3 = np.zeros((self.nw, self.interval))

        self.sigma_ob = 1 / 30  # Conductivity of overburden in S/m
        self.thick_ob = 2  # Thickness of overburden in m

        self.apply_dip = 0  # if 1 then apply dipping sphere model
        self.strike = 90  # Strike of sphereS
        self.dip = 135  # Dip of sphere
        self.wave = 1
        self.windows = 1








    def calculate(self):




        def dh_obdt_xyz(mtx, dipole_m, rtx, rrx, O, mu, sigma_ob, thick_ob):

            """
             Function evaluates the time-derivative of the x,y,z component of the overburden field
             see equations Eq A-5 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """


            m_x = dipole_m * mtx[0]
            m_y = dipole_m * mtx[1]
            m_z = dipole_m * mtx[2]
            rtx_x = rtx[0]
            rtx_y = rtx[1]
            rtx_z = rtx[2]
            rrx_x = rrx[0]
            rrx_y = rrx[1]
            rrx_z = rrx[2]


            if rrx_z > 0:
                dh_obx = (-1 / (4 * math.pi)) * ((m_z * (6 * rrx_x - 6 * rtx_x)) / (mu * sigma_ob * thick_ob * (
                        (rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (6 * m_x * (rrx_z + rtx_z + (2 *O) / (
                                mu * sigma_ob * thick_ob))) / (mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                    rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O)/ (
                                        mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) + (5 * (6 * rrx_x - 6 * rtx_x) * (
                                            rrx_z + rtx_z + (2 *O) / (mu * sigma_ob * thick_ob)) * (
                                                m_x * (rrx_x - rtx_x) - m_z * (rrx_z + rtx_z +(2 *O) / (
                                                    mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                                        mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                                            rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O) / (
                                                                mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))

            else:
                dh_obx1 = ((m_z * (6 * rrx_x - 6 * rtx_x)) / (
                        mu * sigma_ob * thick_ob * ((
                            rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                                mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (6 * m_x * (rtx_z - rrx_z + (2 * O) / (
                                    mu * sigma_ob * thick_ob))) / (mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                        rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
                dh_obx2 =  (5 * (6 * rrx_x - 6 * rtx_x) * (
                                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                                                    m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                                        rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                                            mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                                                rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                                                                    mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))
                dh_obx = (-1 / (4 * math.pi))* (dh_obx1 + dh_obx2)

            if rrx_z > 0:
                dh_oby = (-1 / (4 * math.pi)) * ((m_z * (6 * rrx_y - 6 * rtx_y)) / (mu * sigma_ob * thick_ob * (
                    (rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (6 * m_y * (rrx_z + rtx_z + (2 *O) / (
                                mu * sigma_ob * thick_ob))) / (mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                    rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O)/ (
                                        mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) + (5 * (6 * rrx_y - 6 * rtx_y) * (
                                            rrx_z + rtx_z + (2 *O) / (mu * sigma_ob * thick_ob)) * (
                                                m_x * (rrx_x - rtx_x) - m_z * (rrx_z + rtx_z +(2 *O) / (
                                                    mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                                        mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                                            rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 *O) / (
                                                                mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))

            else:
                #(-1 / (4 * math.pi))
                dh_oby1 = ((m_z * (6 * rrx_y - 6 * rtx_y)) / (
                            mu * sigma_ob * thick_ob * ((
                                    rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                                        mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (6 * m_y * (rtx_z - rrx_z + (2 * O) / (
                                            mu * sigma_ob * thick_ob))) / (mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                                rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
                dh_oby2 =  (5 * (6 * rrx_y - 6 * rtx_y) * (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) * (
                                                            m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                                                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                                                    mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                                                        rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                                                                            mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))
                dh_oby = (-1 / (4 * math.pi))* (dh_oby1 + dh_oby2)






            if rrx_z > 0:
                dh_obz = (-1 / (4 * math.pi)) * ((6 * m_z * (rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                            mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                                rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (6 * (
                                    m_x * (rrx_x - rtx_x) - m_z * (rrx_z + rtx_z + (2 *O) / (
                                        mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (mu * sigma_ob * thick_ob * ((
                                            rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                                                mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) + (m_z * (6 * rrx_z + 6 * rtx_z + (
                                                    12 * O) / (mu * sigma_ob * thick_ob))) / (mu * sigma_ob * thick_ob * (
                                                       (rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O)

                        / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) + (5 * (
                            6 * rrx_z + 6 * rtx_z + (12 * O) / (mu * sigma_ob * thick_ob)) * (rrx_z + rtx_z + (2 * O) / (
                                mu * sigma_ob * thick_ob)) * (m_x * (rrx_x - rtx_x) - m_z * (rrx_z + rtx_z + (
                                    2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                        mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                                            rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))
            else:
                dh_obz = (-1 / (4 * math.pi)) * ((6 * (m_x * (rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (mu * sigma_ob * thick_ob * (
                                (rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                                    rtx_z - rrx_z + (2 *O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (m_z * (
                                        6 * rtx_z - 6 * rrx_z + (12 * O) / (mu * sigma_ob * thick_ob))) / (
                                            mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                                                rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (
                                                    6 * m_z * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob))) / (
                                                        mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (

                        rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)) - (
                            5 * (6 * rtx_z - 6 * rrx_z + (12 * O) / (mu * sigma_ob * thick_ob)) * (rtx_z - rrx_z + (
                                2 * O) / (mu * sigma_ob * thick_ob)) * (m_x * (rrx_x - rtx_x) + m_y * (
                                    rrx_y - rtx_y) - m_z * (rtx_z - rrx_z + (2 *O) / (mu * sigma_ob * thick_ob)))) / (
                                        mu * sigma_ob * thick_ob * ((rrx_x - rtx_x) ** 2 + (
                                            rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                                                mu * sigma_ob * thick_ob)) ** 2) ** (7 / 2)))

            return np.array([dh_obx,dh_obz,dh_oby])







        def h_ob_xyz(mtx, dipole_m, rtx, rrx, O, mu, sigma_ob, thick_ob):

            """
            Function evaluates the x,y,z component of the overburden field
            see equations Eq A-3 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            m_x = dipole_m * mtx[0]
            m_y = dipole_m * mtx[1]
            m_z = dipole_m * mtx[2]
            rtx_x = rtx[0]
            rtx_y = rtx[1]
            rtx_z = rtx[2]
            rrx_x = rrx[0]
            rrx_y = rrx[1]
            rrx_z = rrx[2]

            if rrx_z > 0:
                h_obx = (-1 / (4 * math.pi)) * (
                            m_x / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) - (
                                        3 * (2 * rrx_x - 2 * rtx_x) * (m_x * (rrx_x - rtx_x) - m_z * (
                                        rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                        2 * ((
                                                     rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                                        mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
            else:
                h_obx = (-1 / (4 * math.pi)) * (
                            m_x / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) - (3 * (2 * rrx_x - 2 * rtx_x) * (m_x * (
                            rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (rtx_z - rrx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)))) / (2 * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))

            if rrx_z > 0:
                h_oby = (-1 / (4 * math.pi)) * (
                            m_y / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) - (
                                        3 * (2 * rrx_y - 2 * rtx_y) * (m_x * (rrx_x - rtx_x) - m_z * (
                                        rrx_z + rtx_z + (2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (
                                        2 * ((
                                                     rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                                        mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
            else:
                h_oby = (-1 / (4 * math.pi)) * (
                            m_y / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) - (3 * (2 * rrx_y - 2 * rtx_y) * (m_x * (
                            rrx_x - rtx_x) + m_y * (rrx_y - rtx_y) - m_z * (rtx_z - rrx_z + (2 * O) / (
                            mu * sigma_ob * thick_ob)))) / (2 * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (
                            rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))


            if rrx_z > 0:
                h_obz = (-1 / (4 * math.pi)) * (- m_z / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (
                            2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) - (3 * (2 * rrx_z + 2 * rtx_z + (
                                4 * O) / (mu * sigma_ob * thick_ob)) * (m_x * (rrx_x - rtx_x) - m_z * (rrx_z + rtx_z + (
                                    2 * O) / (mu * sigma_ob * thick_ob)) + m_y * (rrx_y - rtx_y))) / (2 * ((
                                        rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rrx_z + rtx_z + (2 * O) / (
                                            mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
            else:
                h_obz = (-1 / (4 * math.pi)) * (m_z / ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (
                            2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (3 / 2) + (3 * (2 * rtx_z - 2 * rrx_z + (
                                4 * O) / (mu * sigma_ob * thick_ob)) * (m_x * (rrx_x - rtx_x) + m_y * (
                                    rrx_y - rtx_y) - m_z * (rtx_z - rrx_z + (2 * O) / (mu * sigma_ob * thick_ob)))) / (
                                        2 * ((rrx_x - rtx_x) ** 2 + (rrx_y - rtx_y) ** 2 + (rtx_z - rrx_z + (
                                            2 * O) / (mu * sigma_ob * thick_ob)) ** 2) ** (5 / 2)))
            return np.array([h_obx,h_obz,h_oby])




        def static(m, r):
            """
            Function calculates the field of a dipole
            see Eq A-5a from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
             m is the magnetic field vector
             r is the vector from the dipole to the field location
             m is the dipole moment vector
             multiply all components of mm by mu0 to get b field
            """
            one_over_4pi = 1 / (4 * math.pi)
            r2 = np.dot(r, r)
            if r2 < 1.e-20:
                h = 0.0
            else:
                a = one_over_4pi / (math.sqrt(r2) * r2)
                b = np.dot(r, m) * 3 / r2
                h = (b * r - m) * a
            return h



        def thetafunction_step(t, O, o, mu, sigma_sp, a, T):

            """
            Function calculates the time-dependant part of a step-response of the sphere alone
            see equations Eq 12-13 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            ss = mu * sigma_sp * a * a
            theta = 0
            solver = 0
            k = 0

            while solver < 1:

                k = k + 1

                temp = (1 / (1 + np.exp(-(T/2) * ((k * math.pi) ** 2) / ( self.mu * self.sigma_sp * (self.a ** 2))))) * (
                            (6 / ((k * math.pi) ** 2)) * np.exp((o + O - t) * ((k * math.pi) ** 2) / (self.mu * self.sigma_sp *(self.a**2))))

                theta = theta + temp

                solver = np.linalg.lstsq(np.transpose(np.atleast_2d(temp)),np.transpose(np.atleast_2d(theta)),rcond=-1)[0]


            return theta



        def dh_tot_step(mtx, dipole_m, rtx, rsp, mu, sigma_ob, thick_ob, t, o, sigma_sp, a, T):

            """
            Function calculates the x,y,z component of the first order induced moment at the sphere
            see equations Eq 16 from Desmarais and Smith, 2016. Geophysics 81(4), P. E265-E277
            """

            s = 0.0
            b = t
            n = 10
            start_points = np.linspace(s, b, n, endpoint=False)
            h = (b - s) / n
            end_points = start_points + h
            intervals = np.array([start_points, end_points])
            ob_array = h_ob_xyz(self.mtx, self.dipole_m, self.rtx, self.rsp, -o, self.mu, self.sigma_ob, self.thick_ob)
            thetaz = thetafunction_step(t, 0, o, self.mu, self.sigma_sp, self.a, self.T)

            def my_function_x(x):
                return -dh_obdt_xyz(self.mtx, self.dipole_m, self.rtx, self.rsp, x, self.mu, self.sigma_ob,
                                    self.thick_ob)[0] * \
                       thetafunction_step(t, x, o, self.mu, self.sigma_sp, self.a, self.T)

            def my_function_z(x):
                return -dh_obdt_xyz(self.mtx, self.dipole_m, self.rtx, self.rsp, x, self.mu, self.sigma_ob,
                                    self.thick_ob)[1] * \
                       thetafunction_step(t, x, o, self.mu, self.sigma_sp, self.a, self.T)

            def my_function_y(x):
                return -dh_obdt_xyz(self.mtx, self.dipole_m, self.rtx, self.rsp, x, self.mu, self.sigma_ob,
                                    self.thick_ob)[2] * \
                       thetafunction_step(t, x, o, self.mu, self.sigma_sp, self.a, self.T)

            from scipy.integrate import fixed_quad


            resultx, _ = fixed_quad(my_function_x, 0, t - o, n=100)
            resultz, _ = fixed_quad(my_function_z, 0, t - o, n=100)
            resulty, _ = fixed_quad(my_function_y, 0, t - o, n=100)


            return np.array([resultx + (ob_array[0] * thetaz), resultz + (ob_array[1] * thetaz), resulty + (ob_array[2]*thetaz)])





        def h_total_step_1storder(
                mtx, dipole_m, rtx, offset_tx_rx, rsp, t, mu, sigma_ob, thick_ob, sigma_sp, a, P, apply_dip, dip, strike, wave, T):

            """
            Function checks if waveform is being convolved and calls previous functions to calculate sphere-overburden response
            """

            if hasattr(self.wave,"__len__"):
                N = len(self.wave)
                temp_z = 0
                temp_x = 0
                tempy_xyz = 0
                tempy_z = 0
                tempy_y = 0
                temp_y = 0
                H2x = 0
                H2z = 0
                H2y = 0
                H_xyz = 0
                for i in list(range(0, N - 1, 25)):

                    temp_xyz = tempy_xyz + 2 * math.pi * (a ** 3) * (self.P/45) *(
                    dh_tot_step(self.mtx, self.dipole_m,[0, 0, self.rtx[2]], [-self.rtx[0], -self.rtx[1], self.rsp[2]],self.mu, self.sigma_ob, self.thick_ob, t,
                                          (-self.P * (i-1) / (N - 2)), self.sigma_sp, self.a, self.T) + H2x) * ((self.wave[i+1]) - (self.wave[i])/(8.14*1e-6))
                    tempy_xyz = temp_xyz

                    H_xyz = H_xyz + ((self.P / N) * h_ob_xyz(self.mtx, self.dipole_m, [0, 0, self.rtx[2]],
                                                             [-self.offset_tx_rx[0], -self.offset_tx_rx[1],
                                                              self.rtx[2] - self.offset_tx_rx[2]],
                                                             t + (self.P * (i-1) / (N - 2)), self.mu, self.sigma_ob,
                                                             self.thick_ob) * (
                                         (self.wave[i + 1] - self.wave[i]) / (8.14 * 1e-6)))



                convo_x = temp_xyz[0]

                convo_z = temp_xyz[1]

                convo_y = temp_xyz[2]

                H_z = 0

                H_y = 0


                    # This loop convolves the tx waveform with x component



                    # store sphere moment

                msp = np.array([convo_x, convo_y, convo_z])

                    # dipping sphere model if applydip=1

                if apply_dip == 1:
                    norm = np.array([(math.cos((90-dip)*(math.pi/180))) * (math.cos((strike-90)*(math.pi/180))),
                                        math.sin((strike-90)*(math.pi/180)) * math.cos(((90-dip))*(math.pi/180)),
                                            math.sin((90-dip)*(math.pi/180))])

                    # make the dip normal vector a unit vector

                    normt = math.sqrt(np.dot(norm, norm))
                    norm = norm/normt
                    mspdotnorm = np.dot(msp, norm)

                    # now scale the normal to have this strength and redirect the sphere
                    # moment to be in the dip direction

                    msp = mspdotnorm * norm

                statics = static(msp, (np.array([-offset_tx_rx[0], -offset_tx_rx[1], rtx[2] - offset_tx_rx[2]]) -
                                       (np.array([-rtx[0], -rtx[1], rsp[2]]))))

                    # calculate field using induced moment

                if self.Xsign == "-ve":
                    H_tot_x = (np.dot([1, 0, 0], statics))
                else:
                    H_tot_x = -(np.dot([1, 0, 0], statics))

                H_tot_z = np.dot([0, 0, 1], statics)
                H_tot_y = np.dot([0, 1, 0], statics)

                if self.Xsign == "-ve":
                    final_lst = np.array([(H_tot_x + H_xyz[0]), -H_tot_z - H_xyz[1], H_tot_y + H_xyz[2]])  # + z?

                final_lst = np.array([-H_tot_x + H_xyz[0], -H_tot_z - H_xyz[1], H_tot_y + H_xyz[2]]) # + z?

                return final_lst






            else:


            # This loop convolves the tx waveform with x component

                temp = (2 * math.pi * (self.a ** 3)) * dh_tot_step(
                self.mtx, self.dipole_m, [0, 0, self.rtx[2]], [-self.rtx[0], -self.rtx[1], self.rsp[2]], self.mu, self.sigma_ob, self.thick_ob, t, 0, self.sigma_sp, self.a, self.T)



                # store sphere moment
                msp = np.array([temp[0], temp[2], temp[1]])
               # msp = np.array([(2 * math.pi * (self.a ** 3)) * temp[0], (2 * math.pi * (self.a ** 3)) * temp[2], (2 * math.pi * (self.a ** 3)) * temp[1]])

                # dipping sphere model if applydip=1

                if apply_dip == 1:
                    norm = np.array([(math.cos((90-dip)*(math.pi/180))) * (math.cos((strike-90)*(math.pi/180))),
                                      math.sin((strike-90)*(math.pi/180)) * math.cos(((90-dip))*(math.pi/180)),
                                         math.sin((90-dip)*(math.pi/180))])

                # make the dip normal vector a unit vector

                    normt = math.sqrt(np.dot(norm, norm))
                    norm = norm/normt
                    mspdotnorm = np.dot(msp, norm)


                # now scale the normal to have this strength and redirect the sphere
                # moment to be in the dip direction

                    msp = mspdotnorm * norm


                statics = static(msp, (np.array([-offset_tx_rx[0], -offset_tx_rx[1], rtx[2] - offset_tx_rx[2]]) -
                                   (np.array([-rtx[0], -rtx[1], rsp[2]]))))


                # calculate field using induced moment

                if self.Xsign == "-ve":
                    H_tot_x = (np.dot([1, 0, 0], statics))
                else:
                    H_tot_x = -(np.dot([1, 0, 0], statics))

                H_tot_z = np.dot([0, 0, 1], statics)
                H_tot_y = np.dot([0, 1, 0], statics)

                # calculate 0th order term (field of overburden alone)
                H_field = h_ob_xyz(self.mtx, self.dipole_m, [0, 0, self.rtx[2]],
                               [-self.offset_tx_rx[0], -self.offset_tx_rx[1], self.rtx[2] - self.offset_tx_rx[2]],
                               t, self.mu, self.sigma_ob, self.thick_ob)

                if self.Xsign == "-ve":
                    final_lst = np.array([-(H_tot_x + H_field[0]), H_tot_z - H_field[1], H_tot_y - H_field[2]])  # + z?

                final_lst = np.array([H_tot_x + H_field[0], H_tot_z - H_field[1], H_tot_y - H_field[2]]) # + z?

                return final_lst

        if hasattr(self.wave, "__len__"):
            self.wc = self.windows
            self.nw = len(self.wc)
            self.H_tot_x = np.zeros((self.nw, self.interval))  # Response vectors
            self.H_tot_y = np.zeros((self.nw, self.interval))
            self.H_tot_z = np.zeros((self.nw, self.interval))

            self.C_x = np.zeros((self.nw, self.interval))  # Induced sphere moment vectors
            self.C_z = np.zeros((self.nw, self.interval))

            self.H_ob1 = np.zeros((self.nw, self.interval))  # Overburden response vectors
            self.H_ob2 = np.zeros((self.nw, self.interval))
            self.H_ob3 = np.zeros((self.nw, self.interval))

        self.delta_x = math.floor(abs((self.profile_length)) / (self.interval - 1))
        for j in list(range(0, self.nw)):  # iterate time
            i = -1
            t = self.wc[j]
            print(j)
            for x in list(range((-self.profile_length//2), (self.profile_length//2) + self.delta_x, self.delta_x)):  # iterate along profile
                i += 1
                if self.PlottingPoint == "Rx":
                    self.profile[0, i] = x - self.offset_tx_rx[0]
                if self.PlottingPoint == "Tx":
                    self.profile[0, i] = x
                if self.PlottingPoint == "Mid point":
                    self.profile[0, i] = x - ((self.offset_tx_rx[0]) / 2)

                self.rtx[0] = x
                self.rrx[0] = self.rtx[0] - self.offset_tx_rx[0]
                # calculate response
                response_array = (
                    h_total_step_1storder(self.mtx, self.dipole_m, self.rtx, self.offset_tx_rx, self.rsp, t,
                                          self.mu, self.sigma_ob,
                                          self.thick_ob, self.sigma_sp, self.a, self.P, self.apply_dip, self.dip, self.strike, self.wave,self.T))


                self.H_tot_x[j, i] = (self.mu / 1e-12) * response_array[0]
                self.H_tot_z[j, i] = (self.mu / 1e-12) * response_array[1]
                self.H_tot_y[j, i] = (self.mu / 1e-12) * response_array[2]