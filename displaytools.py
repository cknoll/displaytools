# -*- coding: utf-8 -*-

# Issues: SyntaxError points to the wrong line (due to display insertion)
# Note: this is vulnerable by keywordargs: x = func(a, b=2)


"""
This module is an experimental ipython extension.

Background: insert some logic to display the 'result' of an assignment




# load it with %reload_ext displaytools

 usage:
 
`my_random_variable =  np.random.rand() ##`

inserts the source line `display(my_random_variable)` to the source code,
that is actually executed.

That way, the notebook is more comprehensible beacause the reader knows
the content of `my_random_variable`. It saves the typing effort and the code
duplication of manually adding `display(my_random_variable)`.
"""

# todo maybe use sp.Eq(sp.Symbol('Z1'), theta, evaluate=False) to get better formatting


import new

from IPython.display import display

special_comment = '##'
special_comment_lhs = '##:'

def insert_disp_lines(raw_cell):
    lines = raw_cell.split('\n')
    N = len(lines)
    
    # iterate from behind -> insert does not change the lower indices
    for i in xrange(N-1, -1, -1):
        line = lines[i]
        if line.endswith(special_comment) and line.count(' = ') == 1 and not line[0] in [' ', '#']:
            idx = line.index(' = ')
            var_str = line[:idx].strip()

            #!! try ... eval(...) except SyntaxError
            new_line = 'display(%s); print("---")' % var_str
            lines.insert(i+1, new_line)
        
        # also allow to display the return value (without assignment)
        elif line.endswith(special_comment) and not line[0] in [' ', '#']:
            if not line.index('#') == line.index('##'):
                continue
            
            idx = line.index('##')
            lines[i] = 'display(%s); print("___")' % line[:idx]
            
        elif line.endswith(special_comment_lhs) and line.count(' = ') == 1 and not line[0] in [' ', '#']:
            idx = line.index(' = ')
            var_str = line[:idx].strip()

            new_line = 'custom_display("%s", %s); print("---")' % (var_str, var_str)
            lines.insert(i+1, new_line)
            
            

    new_raw_cell = "\n".join(lines)

    return new_raw_cell

def custom_display(lhs, rhs):
    """
    lhs: left hand side
    rhs: right hand side
    
    This function serves to inject the string for the left hand
    """
    
    # This code is mainly copied from IPython/display.py
    # (IPython version 2.3.0)
    kwargs = {}
    raw = kwargs.get('raw', False)
    include = kwargs.get('include')
    exclude = kwargs.get('exclude')
    metadata = kwargs.get('metadata')

    from IPython.core.interactiveshell import InteractiveShell
    from IPython.core.displaypub import publish_display_data

    format = InteractiveShell.instance().display_formatter.format
    format_dict, md_dict = format(rhs, include=include, exclude=exclude)
    
    # exampl format_dict (for a sympy expression):
    # {u'image/png': '\x89PNG\r\n\x1a\n\x00 ...\x00\x00IEND\xaeB`\x82',
    #  u'text/latex': '$$- 2 \\pi \\sin{\\left (2 \\pi t \\right )}$$',
    # u'text/plain': u'-2\u22c5\u03c0\u22c5sin(2\u22c5\u03c0\u22c5t)'}
    
    # it is up to IPython which item value is finally used
    
    # now merge the lhs into the dict:
    
    if not isinstance(lhs, basestring):
        raise TypeError('unexpexted Type for lhs object: %s' %type(lhs))
    
    new_format_dict = {}
    for key, value in format_dict.items():
        if 'text/' in key:
            new_value = lhs+' := '+value
            new_format_dict[key] = new_value
        else:
            # this happens e.g. for mime-type (i.e. key) 'image/png'
            new_format_dict = format_dict
    publish_display_data('display', new_format_dict, md_dict)


def load_ipython_extension(ip):

    def new_run_cell(self, raw_cell, *args, **kwargs):

        new_raw_cell = insert_disp_lines(raw_cell)

        if 0:
            #debug
            print "cell:"
            print raw_cell
            print "new_cell:"
            print new_raw_cell

        ip.old_run_cell(new_raw_cell, *args, **kwargs)

    # prevent unwanted overwriting when the extension is reloaded
    if not 'new_run_cell' in str(ip.run_cell):
        ip.old_run_cell = ip.run_cell
        
    ip.run_cell = new.instancemethod(new_run_cell, ip)
    ip.user_ns['display'] = display
    ip.user_ns['custom_display'] = custom_display

