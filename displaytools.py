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


import new

from IPython.display import display

special_comment = '##'

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

    new_raw_cell = "\n".join(lines)

    return new_raw_cell



def load_ipython_extension(ip):
    #print "hello world"
    #print dir(ip)

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

