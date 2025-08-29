import numpy as np

def identify_static(step_responses, poly_order = 3):
    '''
    Identify the parameters of the input nonlinearity
    
    ...
    
    In short summary, the identification is done in the following way:
    1) for each response the steady state values are paired (u_steady, y_steady)
    2) polyfit is done between pairs (u_steady, y_steady)
    3) return polynomial parameters
    
    Attributes
    ----------
    step_responses : 
        The list of StepResponse class (obtained by split tool).
    poly_order : float
        The order of the polynomial, which is applied to model the nonlinearity.        
         
    Returns
    ----------
    the polynomial parameters, polynomial object, list of points: u_static, y_static, y_model   
    '''    
    u_static = []
    y_static = []

    for step in step_responses:
        u_static.append(step.u_final)
        y_static.append(step.y_final)
    
    static_model = np.polyfit(u_static, y_static, poly_order)
    poly_static_model = np.poly1d(static_model)
    
    y_model = poly_static_model(u_static)
   
    # TODO - perform auto-evalution of identification results
   
    return static_model, poly_static_model, u_static, y_static, y_model
