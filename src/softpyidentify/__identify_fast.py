import numpy as np
from scipy.optimize import minimize

def __calculate_response_fast(time, gain, alpha, omega):
    phi_z = np.arctan2(-omega, -alpha) - np.pi/2.0
    transient = np.multiply(np.cos(omega*time + phi_z), np.exp(-alpha*time))
    a = np.sqrt(alpha**2 + omega**2)/omega
    return gain*(1.0 + a*transient)

def get_fast_model_y(step, poly_static_model, gain, alpha, omega):
    dv = poly_static_model(step.u_final) - poly_static_model(step.u_initial)
    y_model = step.y_initial + __calculate_response_fast(step.get_fast().t, gain, alpha, omega)*dv
    return y_model

def __opt_goal(x, step, poly_static_model):
    
    gain = x[0]
    alpha = x[1]
    omega = x[2]
   
    y_model = get_fast_model_y(step, poly_static_model, gain, alpha, omega)
    J = np.mean(np.abs(y_model - step.get_fast().y))
    return J

def identify_fast(step_responses, static_model, k_initial = 0.5, alpha_initial = 10.0, omega_initial = 10.0, bounds=[(0.0, 1.0), (1.0e-3, 1.0e3), (1.0e-3, 1.0e3)], algorithm='fixed'):
    '''
    Identify the parameters of Gfast(s) for the step responses.
    
    ...
    
    In short summary, the identification is done in the following way:
    1) two possibilities:
       - fixed: for each response minimize Gfast paramters and store parameters in list
       - random: many times (5 x len(step responses)) random choose step response and initial parameters, minimize Gfast paramters and store parameters in list
    2) take the median from the list for each parameter
    3) return parameters
    
    Attributes
    ----------
    step_responses : 
        The list of StepResponse class (obtained by split tool).
    static_model : ndarray
        The static model of the nonlinear input (suitable for np.poly1d).        
    k_initial : float
        The initial value for the minimize tool of the Gfast's gain.
    alpha_initial : float
        The initial value for the minimize tool of the Gfast's damping.    
    omega_initial : float
        The initial value for the minimize tool of the Gfast's angular frequency.    
    bounds : array
        The bounds on k, alpha, omega for minize tool.    
    algorithm : string
        The algorithm of analyzing step responses. 
    
    Returns
    ----------
    the optimized three parameters: k, alpha, omega     
    '''
    
    # initialize input nonlinearity
    poly_static_model = np.poly1d(static_model)
    
    k_list = []
    alpha_list = []
    omega_list = []
    
    if algorithm == 'fixed':
        # minimize and store in the list
        x0 = [k_initial, alpha_initial, omega_initial]
        for step in step_responses:
            # run for fixed initial conditions and all steps
            args = (step, poly_static_model)
            res = minimize(__opt_goal, x0, args=args, method='Nelder-Mead', options = {'disp': False}, bounds=bounds)
            # retrive result
            if res.success:
                k_list.append(res.x[0])
                alpha_list.append(res.x[1])
                omega_list.append(res.x[2])
    elif algorithm == 'random':
         # minimize and store in the list
        Ns = len(step_responses)
        for i in range(5*Ns):
            # choose step
            s = np.random.randint(low=0, high=Ns-1)
            # choose initial conditions
            k_random = np.random.uniform(low=bounds[0][0], high=bounds[0][1])
            alpha_random = np.random.uniform(low=bounds[1][0], high=bounds[1][1])
            omega_random = np.random.uniform(low=bounds[2][0], high=bounds[2][1])
            # run algorithm
            x0 = [k_random, alpha_random, omega_random]
            args = (step_responses[s], poly_static_model)
            res = minimize(__opt_goal, x0, args=args, method='Nelder-Mead', options = {'disp': False}, bounds=bounds)
            # retrive result
            if res.success:
                k_list.append(res.x[0])
                alpha_list.append(res.x[1])
                omega_list.append(res.x[2])   
    
    # take median for each list
    k_list = np.array(k_list)
    k = np.median(k_list)
    alpha_list = np.array(alpha_list)
    alpha = np.median(alpha_list)
    omega_list = np.array(omega_list)
    omega = np.median(omega_list)
    
    # return result
    return k, alpha, omega
 