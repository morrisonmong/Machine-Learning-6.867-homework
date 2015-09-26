__author__ = 'manuelli'

import numpy as np
import pylab as pl
import scipy.optimize as opt
import scipy.io as sio


def getData(name):
    data = pl.loadtxt(name)
    # Returns column matrices
    X = data[0:1].T
    Y = data[1:2].T
    return X, Y

class LinearRegression:

    def __init__(self, x, y, M, phi=None):
        self.N = np.size(y)
        self.y = 1.0*np.reshape(y,(self.N,))
        self.x = 1.0*np.reshape(x,(np.size(x),))
        self.numFeatures = M+1

        # allow the user to pass in the feature matrix phi if so desired
        if phi is None:
            self.initializePhi()
        else:
            self.phi = phi
            self.numFeatures = np.shape(phi)[1]


    def initializePhi(self):
        self.phi = np.zeros((self.N,self.numFeatures))
        for i in range(0,self.numFeatures):
            self.phi[:,i] = np.power(self.x,i)

    # standard linear regression
    def reg(self):
        phi_pseudo_inverse = np.dot(np.linalg.inv(np.dot(np.transpose(self.phi), self.phi)),np.transpose(self.phi));
        w = np.dot(phi_pseudo_inverse, self.y)
        return w

    # compute ridge regression
    def ridge(self,lam):
        A = np.dot(np.linalg.inv(1.0*lam*np.eye(self.numFeatures) + np.dot(np.transpose(self.phi), self.phi)),np.transpose(self.phi));
        w = np.dot(A,self.y)
        return w

    # compute sum of squared error, can optionally pass in phi and y
    def SSE(self,w, phi=None, y=None):
        if phi is None:
            phi = self.phi

        if y is None:
            y = self.y

        s = np.dot(phi,w) - y
        sse = np.linalg.norm(s)**2
        return sse

    #computes the mean square error
    def MSE(self,w, phi=None, y=None):
        return 1/(1.0*self.N)*self.SSE(w, phi=phi, y=y)

    def SSE_gradient(self,w):
        return 2.0*np.dot(self.phi.transpose(),np.dot(self.phi,w) - self.y)

    def LASSO_objective(self,w,lam):
        return self.MSE(w) + lam*np.linalg.norm(w,ord=1)

    def Lasso(self,lam,w_0=None):
        if w_0 is None:
            w_0 = np.zeros((self.numFeatures))

        def objective(w):
            return self.LASSO_objective(w, lam)

        res = opt.minimize(objective, w_0)
        print res

        return res.x


    @staticmethod
    def getData(name):
        data = pl.loadtxt(name)
        # Returns column matrices
        X = 1.0*np.array(data[0:1].T)
        Y = 1.0*np.array(data[1:2].T)
        return X, Y

    @staticmethod
    def fromFile(filename, M):
        x,y = getData(filename)
        return LinearRegression(x,y,M)

    @staticmethod
    def fromBlog(type='train'):
        x_filename = 'BlogFeedback_data/x_' + type + '.csv'
        y_filename = 'BlogFeedback_data/y_' + type + '.csv'

        x = np.genfromtxt(x_filename, delimiter=',')
        y = np.genfromtxt(y_filename, delimiter=',')

        lr = LinearRegression(x,y,1,phi=x)
        return lr


    @staticmethod
    def fromLASSOData():
        data = sio.loadmat("regress-highdim.mat")
        phi_train = data['X_train'].transpose()
        y_train = data['Y_train']
        y_train = np.reshape(y_train,(np.size(y_train),))
        phi_test = data['X_test'].transpose()
        y_test = data['Y_test']
        y_test = np.reshape(y_test,(np.size(y_test),))

        lasso = LinearRegression(x_train,y_train,1,phi=phi_train)
        return (lasso, phi_train, y_train, phi_test, y_test)

    # @staticmethod
    # def computeLASSOFeatures(x):
    #     x = np.reshape(x,(x.size(),))
    #     phi = np.zeros((x.size(),12))
    #     for i in range(0,12):
    #         if i == 0:
    #             f = lambda t: t
    #         else:
    #             f = lambda t: np.sin(0.4*np.pi*i)
    #
    #         phi[:,i] = f(x)
    #
    #     return phi



if __name__ == "__main__":
    filename = "curvefitting.txt"
    lr = LinearRegression.fromFile(filename,4)
    w = lr.reg()
    print "linear regression "
    print w

    # sse = lr.SSE(w)
    # print "SSE is "
    # print lr.SSE(w)
    #
    # grad = lr.SSE_gradient(w)
    # print "SSE grad is "
    # print grad

    lam = 0
    w_ridge = lr.ridge(lam)
    print "ridge regression is"
    print w_ridge

    w_lasso = lr.Lasso(lam)
    print "lasso is"
    print w_lasso

    (lasso,_,_,_,_) = LinearRegression.fromLASSOData()



