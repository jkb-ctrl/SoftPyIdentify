import numpy as np

from .__step_response import StepResponse


def split_signal(t, u, y, period_switch, duration_fast, relative_start_extension = 0.01, steady_end_window = 0.01):
    '''
    Split signals t, u, y for single step responses.
    
    ...
    
    The signals are split every period_switch. The response is taken before switch and until steady state. 
    Currently, the period_switch must be constant. The first 0..period_switch is ommited.
    The fast response is also extracted between switch time and switch time + duration_fast
    
    
    Attributes
    ----------
    t, u, y : ndarray
        The array with time, input, and output
    period_switch : float
        The period of switching in the input signal
    duration_fast : float
        The duriotion of the fast reponse in the step response.    
    relative_start_extension : float
        Applied to calculate the time before switch -> start = t_switch - relative_start_extension*period_switch
    steady_end_window : float
        Applied to calculate the window of steady state value -> t_steady = 2*t_switch - steady_end_window*period_switch
    
    Returns
    ----------
    the list of step responses.   
    '''

    step_rsp_list = []

    counter = 0

    t_final = t[-1]
    t_switch = period_switch
    while t_switch < t_final - period_switch:
        
        t_start = t_switch - relative_start_extension*period_switch
        t_end = t_switch + period_switch
        t_fast = t_switch + duration_fast
        t_steady = t_end - steady_end_window*period_switch
        
        # TODO in future: checks if i_s, i_e, i_switch, i_fast, i_final differ by minimal value;
        # for instance relative_start_extension*period_switch is less than sampling time
        
        i_s = np.argmin(np.abs(t - t_start))
        i_e = np.argmin(np.abs(t - t_end))
        
        i_switch = np.argmin(np.abs(t - t_switch))
        i_fast = np.argmin(np.abs(t - t_fast))
        i_final = np.argmin(np.abs(t - t_steady))
        
        # initial and final value of input
        u_initial = np.mean(u[i_s:i_switch])
        u_final = np.mean(u[i_final:i_e])
        # initial and final value of output
        y_initial = np.mean(y[i_s:i_switch])
        y_final = np.mean(y[i_final:i_e])
              
        step_rsp_list.append(StepResponse(t[i_s:i_e] - t_switch, u[i_s:i_e], y[i_s:i_e], u_initial, u_final, y_initial, y_final, i_switch-i_s, i_fast-i_s, counter))
                
        t_switch = t_switch + period_switch
        
        counter = counter + 1
        
    return step_rsp_list
