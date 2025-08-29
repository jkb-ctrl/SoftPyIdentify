import numpy as np
from scipy.optimize import minimize

def __calculate_slow_model_response(time, s0, z0):
    return z0/s0 - ((z0-s0)/s0)*np.exp(-s0*time)

def get_slow_model_y(step, s0, z0, poly_static_model, k_fast):
    dv = poly_static_model(step.u_final) - poly_static_model(step.u_initial)
    y_model = step.y_initial + k_fast*__calculate_slow_model_response(step.get_after().t, s0, z0)*dv
    return y_model

def __opt_goal(x, step, poly_static_model, k_fast):
    
    s0 = x[0]
    z0 = s0/k_fast
    
    y_model = get_slow_model_y(step, s0, z0, poly_static_model, k_fast)
    
    J = np.mean(np.abs(y_model - step.get_after().y))
             
    return J

def identify_slow(step_responses, static_model, k_fast, s0_initial = 0.2):
    
    poly_static_model = np.poly1d(static_model)
    
    s0_list = []
    
    x0 = [s0_initial]
    for step in step_responses:
        args = (step, poly_static_model, k_fast)
        res = minimize(__opt_goal, x0, args=args, method='Nelder-Mead', options = {'disp': False})
  
        if res.success:
            s0_list.append(res.x[0])
 
    s0_list = np.array(s0_list)
    s0 = np.median(s0_list)
    z0 = s0/k_fast
     
    return s0, z0
