"""
The file contains simple functions to collect information 
from BrianObjects and represent them in a standard 
dictionary format. The parts of the file shall be reused 
with standard format exporter.
"""

def collect_NeuronGroup(group):
    """
    Collect information from `brian2.groups.neurongroup.NeuronGroup`
    and return them in a dictionary format
    
    Parameters
    ----------
    group : brian2.groups.neurongroup.NeuronGroup
        NeuronGroup object

    Returns
    -------
    neuron_dict : dict
        Dictionary with extracted information
    """
    neuron_dict = {}
    
    # get name
    neuron_dict['name'] = group.name

    # get size
    neuron_dict['N'] = group._N

    # get user defined stateupdation method
    if isinstance(group.method_choice, str):
        neuron_dict['user_method'] = group.method_choice
    # if not specified by user
    else: 
        neuron_dict['user_method'] = None
    
    # get equations
    neuron_dict['user_equations'] = collect_Equations(group.user_equations)

    # check spike event is defined
    if bool(group.events):
        neuron_dict['events'] = collect_Events(group)

    return neuron_dict

def collect_Equations(equations):
    """
    Collect model equations of the NeuronGroup

    Parameters
    ----------
    equations : brian2.equations.equations.Equations
        model equations object

    Returns
    -------
    eqn_dict : dict
        Dictionary with extracted information
    """

    eqn_dict = {}

    # get DIFFERENTIAL_EQUATIONS and SUBEXPRESSIONS
    for names in equations.diff_eq_names.union(equations.subexpr_names):
        
        eqn_dict[names] = {'expr': equations[names].expr, 
                                'unit': equations[names].unit, 
                                'type': equations[names].type, 
                                'dtype': equations[names].var_type}
        
        if equations[names].flags:
            eqn_dict[names]['flags'] = equations[names].flags
    
    # get PARAMETERS
    for param_names in equations.parameter_names:
        
        eqn_dict[param_names] = {'unit': equations[param_names].unit, 
                                'type': equations[param_names].type, 
                                'dtype': equations[param_names].var_type}
        
        if equations[param_names].flags:
            eqn_dict[param_names]['flags'] = equations[param_names].flags

    return eqn_dict

def collect_Events(group):

    """
    Collect Events (spiking) of the NeuronGroup

    Parameters
    ----------
    group : brian2.groups.neurongroup.NeuronGroup
        NeuronGroup object

    Returns
    -------
    event_dict : dict
        Dictionary with extracted information
    """

    event_dict = {}
    
    # add threshold
    event_dict['spike'] = {'threshold': group.events['spike']}
    
    #check reset is defined
    if bool(group.event_codes):
        event_dict['spike'].update({'reset': group.event_codes['spike']})

    #check refractory is defined
    if group._refractory:
        event_dict['spike'].update({'refractory': group._refractory})
    
    return event_dict