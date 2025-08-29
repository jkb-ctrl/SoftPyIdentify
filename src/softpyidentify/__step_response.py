import numpy as np

class SignalsHolder:
    """
    Holder to keep the parts (or whole) of signal: t, u, y (time, input, output).

    ...

    Attributes
    ----------
    t : ndarray
        Time.
    u : ndarray
        Input.        
    y : ndarray
        Output.
        
    """

    def __init__(self, t, u, y):
        self.t = t
        self.u = u
        self.y = y


class StepResponse:
    """
    Information of step response with its main features. The signals are before switch (t < 0) and after switch (t > 0).

    ...

    Attributes
    ----------
    t : ndarray
        The 1D array of the time (start before switch, and finished at the steady state)
    u : ndarray
        The 1D array of the input (before switch and after switch).        
    y : ndarray
        The 1D array of the output (before switch and after switch).     
    u_initial : float
        The initial (steady state) value of the input.        
    u_final : float
        The final (steady state) value of the input. 
    y_initial : float
        The initial (steady state) value of the output.     
    y_final : float
        The final (steady state) value of the output. 
    i_switch : int
        The auxiliary index (in the signal's array: t, u, y) of the switch moment. It should be t[i_switch] == 0.
    i_fast : int 
        The auxiliary index (in the signal's array: t, u, y) of the steady state of the fast response.
    idx : int 
        The identificator of the step reponse (for instance its order number)
    """
   
    def __init__(self, t:np.ndarray, u:np.ndarray, y:np.ndarray, u_initial:float, u_final:float, y_initial:float, y_final:float, i_switch:int, i_fast:int, idx:int):
        self.t = t
        self.u = u
        self.y = y
        self.u_initial = u_initial
        self.u_final = u_final
        self.y_initial = y_initial 
        self.y_final = y_final
        self.i_switch = i_switch
        self.i_fast = i_fast
        self.idx = idx
        self.after_holder = None
        self.fast_holder = None

    def get_after(self):
        '''
        Get the part of the response after switch to the end of the whole response
        
        ...
        
        Returns
        ----------
        SignalsHolder (data class with: t, u, y)
        '''
        if self.after_holder is None:
            self.after_holder = SignalsHolder(self.t[self.i_switch:], self.u[self.i_switch:], self.y[self.i_switch:] )
        return self.after_holder

    def get_fast(self):
        '''
        Get the part of the response after switch to the end of the fast response
        
        ...
        
        Returns
        ----------
        SignalsHolder (data class with: t, u, y)
        '''
        if self.fast_holder is None:
            self.fast_holder = SignalsHolder(self.t[self.i_switch:self.i_fast], self.u[self.i_switch:self.i_fast], self.y[self.i_switch:self.i_fast] )
        return self.fast_holder                
         
