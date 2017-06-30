# displaytools

This module is an experimental extension for IPython Notebook.

It enables the user to trigger the display the content of a newly assigned variable with a special comment
(`##` by default).

---

## Installation:

The file displaytools.py must be placed somewhere in $PYTHONPATH or simply
in the same directory as the notebook where it shall be included.

---

## Example:
See this [IPython notebook](http://nbviewer.ipython.org/github/cknoll/displaytools/blob/master/example1_python3.ipynb)

---

## Usage:

Load this extension with `%load_ext displaytools` or `%reload_ext displaytools`
The latter is usefull for debugging.
 
Example invocation:
 
`my_random_variable =  np.random.rand() ##`

Due to the special comment `##` the extension inserts the line `display(my_random_variable)` to the source code,
before it is passed to the interpreter, i.e. before its execution.

That way, additional output is generated, which makes the notebook is more comprehensible
(because the reader knows the content of `my_random_variable`). It saves the typing effort and the code
duplication of manually adding `display(my_random_variable)`.

Of course there can be several such in vocations within one cell.

If there is no assignment taking place, `##` nevertheless causes the display of the respective result.


The special comment `##:` additionally triggers the printing of the left hand side of the assignment.

---

## Security Advice

Because, the extension manipulates the source code before its execution it might cause unwanted and strange behavior.
Thus, this program is distributed in the hope that it will be useful, *but without any warrenty*.


