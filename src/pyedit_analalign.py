"""
This module is a Pydev extension written in python targetting Jython within the context
of the PyDev and Eclipse Java frameworks.

Setup: Put this file in eclipse/plugins/org.python.pydev.jython_1.4.7.2843/jysrc
Usage: Ctrl + 2 'ea' ENTER
(Ctrl + 2 lets you enter commands... we are using tt for now because it is easier to type
 and it is not clear what other keybinding would be better)

Use cases:
---------------- EQUAL ALIGN : Ctrl + 2 ea <ENTER> ----------------------
vara = 5
varb = 10
myvariable = 20
my_really_long_variable = 44

** BECOMES **

vara                      = 5
varb                      = 10
myvariable                = 20
my_really_long_variable   = 44

---------------- DICT ALIGN : Ctrl + 2 da <ENTER> -----------------------
mydict = {
    'key': value,
    'longer_key': 'some_str_value'
    55: 'Yet Another Value!',
}

** BECOMES **

mydict = {
    'key'        : value,
    'longer_key' : 'some_str_value'
    55           : 'Yet Another Value!',
}


"""
DEBUG = False

if False: # Standard issue hack
    from org.python.pydev.editor import PyEdit #@UnresolvedImport
    cmd = 'command string'
    editor = PyEdit

# Make sure we have something to work with
assert cmd is not None 
assert editor is not None

if cmd == 'onCreateActions': # Bind when an editor is created
    from org.eclipse.jface.action import Action #@UnresolvedImport
    from org.eclipse.jface.dialogs import MessageDialog #@UnresolvedImport
    from org.python.pydev.core.docutils import PySelection #@UnresolvedImport
    from org.python.pydev.core.docutils import StringUtils #@UnresolvedImport

    def pad_right(string, length, padchar=' '):
        return string + padchar * max(0, (length - len(string)))
    
    def align_on_character(lines, character):
        # first pass, find the offset to use
        max_offset = 0
        for line in lines:
            if character in line:
                max_offset = max(max_offset, line.index(character))
        
        # second pass... do the alignment (just '=' for now)
        adjusted_lines = []
        for line in lines:
            if character in line:
                parts = line.split(character)
                head, tail = parts[0].rstrip(), character.join(parts[1:]).lstrip() # in case there are multiple equals?
                adjusted_lines.append((' %s ' % character).join([pad_right(head, max_offset), tail]))
            else:
                adjusted_lines.append(line)
        return adjusted_lines

    def align_selected_code_on_character(character):
            selection = PySelection(editor)
            selection.selectCompleteLine() # change selection to entire lines
            lines = StringUtils.splitInLines(selection.getSelectedText())
            adjusted_lines = align_on_character(lines, character)
            replacement = ''.join(adjusted_lines)
            selection.getDoc().replace(selection.getStartLine().getOffset(), selection.getSelLength(), replacement)
    
    class EqualsAlign(Action):
        def run(self):
            align_selected_code_on_character('=')
            
    class DictionaryAlign(Action):
        def run(self):
            align_selected_code_on_character(':')
        
    def bindInInterface():
        editor.addOfflineActionListener("ea", EqualsAlign(), 'Anally Align Equal Signs', True) 
        editor.addOfflineActionListener("da", DictionaryAlign(), 'Anally Align Dictionary Declaration', True)
    
    class RunInUi(Runnable):
        '''Helper class that implements a Runnable (just so that we
        can pass it to the Java side). It simply calls some callable.
        '''
    
        def __init__(self, c):
            self.callable = c
        def run(self):
            self.callable ()
    
    def runInUi(callable):
        '''
        @param callable: the callable that will be run in the UI
        '''
        Display.getDefault().asyncExec(RunInUi(callable))
    
    runInUi(bindInInterface)
