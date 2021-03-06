import numpy as np
import theano.tensor as T
import math

def GaussianMarginalLogDensity(incomings, normal_priori=False, return_by_units=False):
    '''
    sum along the last axis of incomings
    p(z|x) = N(z| z_mu, z_var), p0(z) = N(0,I)
    crossentropy mode: True, \int_z{ p(z|x)log[p0(z)] }
                       False,\int_z{ p(z|x)log[p(z|x)] }
    '''
    mu, logvar = incomings
    if normal_priori:
        density = -0.5 * (T.log(2 * np.pi) + (T.sqr(mu) + T.exp(1e-8 + logvar)))
    else:
        density = -0.5 * (T.log(2 * np.pi) + 1 + logvar)
    if return_by_units:
        return density.mean(0)
    else:
        return density.sum(-1)

def GaussianQLogPDensity(incomings, return_by_units=False):
    '''
    \int_z{ q(z|z_mu1,z_logvar1)log[p(z|z_mu2,z_logvar2)] }
    reference: https://www.semanticscholar.org/paper/Approximating-the-Kullback-Leibler-Divergence-Hershey-Olsen
    /4f8deabc58014eae708c3e6ee27114535325067b/pdf
    '''
    mu1, logvar1, mu2, logvar2 = incomings
    density = -0.5 * (T.log(2 * np.pi) + logvar2 +
                      T.sqr(mu2 - mu1) / (1e-8 + T.exp(logvar2)) +
                      T.exp(logvar1)/(1e-8 + T.exp(logvar2)))
    if return_by_units:
        return density.mean(0)
    else:
        return density.sum(-1)


def GaussianLogDensity(incomings):
    x, mu, logvar = incomings
    density = -0.5 * ( np.log(2 * np.pi) + logvar + T.sqr(x-mu)/T.exp(1e-8 + logvar) )
    return density.sum(-1)