import vim as vim_module

class VariableWrapper(object):
    """ Provides a dict-like interface which can be used to access variables.
    
    Overrides __getitem__ and __setitem__ in order to allow developers to
    get and set the values of vimscript variables via a dict-like interface
    using the vimpy.settings['variable_name']

    """

    # TODO: Verify that the proper prefixes are working.
    def __init__(self, prefix=''):
       self.prefix = prefix

    def make_name(self, key):
        return '{0}{1}'.format(self.prefix, key)

    def __contains__(self, key):
        """ Allows us to check if a variable exists in this scope. """

        command = 'exists("{0}")'.format(self.make_name(key))
        return vim_module.eval(command) == '1'

    def __getitem__(self, key):
        """ Returns the value of a variable. """

        return vim_module.eval(self.make_name(key))

    def __setitem__(self, key, value):
        """ Modifies the value of the provided variable. """

        # Attempt to escape provided values to be safely provided to vim
        final_value = str(value)
        final_value = final_value.replace('\\', '\\\\')
        final_value = final_value.replace('"', '\\"')

        variable = self.make_name(key)

        command = 'islocked("{0}")'.format(variable)
        is_locked = vim_module.eval(command)

        if int(is_locked) > 0:
            raise TypeError('Tried to alter {0} but it is locked.'.format(variable))

        command = 'let {0}="{1}"'.format(self.make_name(key), final_value)
        return vim_module.command(command)

globals = VariableWrapper(prefix='g:')
window = VariableWrapper(prefix='w:')
tab = VariableWrapper(prefix='t:')
buffer = VariableWrapper(prefix='b:')
vim = VariableWrapper(prefix='v:')
options = VariableWrapper(prefix='&')
registers = VariableWrapper(prefix='@')
environment = VariableWrapper(prefix='$')

