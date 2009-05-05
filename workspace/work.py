#!/usr/bin/python

from appscript import *

term = app('Terminal')
term.activate()

### Make sure we have windows open
# Can't make new window through 'new', so using keyboard commands, see: http://onrails.org/articles/2007/11/28/scripting-the-leopard-terminal

for i in range(1,5):
  if not term.windows[i].exists():
    app('System Events').processes['Terminal.app'].keystroke('n', using=k.command_down)

# TODO: Need to figure out what happens when 1, 2, 4, 5, 6 exists...
    
# Note, the order of the window stack is based on the last focus order
# Yes, this is stupid, hack: focus windows, this is more reliable than parsing
# the name() since one day I might change to title style...

### Resize Windows

app('System Events').processes['Terminal.app'].keystroke('2', using=k.command_down)
w = term.windows[1]
w.number_of_rows.set(82)
w.number_of_columns.set(80)
w.position.set([0,0])

## Test Command ##
## if bash (split)
# app('System Events').processes['Terminal.app'].keystroke('ls\n')


app('System Events').processes['Terminal.app'].keystroke('3', using=k.command_down)
w = term.windows[1]
w.number_of_rows.set(60)
w.number_of_columns.set(188)
w.position.set([583,0])

app('System Events').processes['Terminal.app'].keystroke('4', using=k.command_down)
w = term.windows[1]
w.number_of_rows.set(20)
w.number_of_columns.set(188)
w.position.set([583,889])



# Minimize 
windows = term.windows()
for i in range(4,len(windows)+1):
  # Note: while keystrokes can use application_processes, apparently buttons only exist in processes.  Thanks Apple!
  # This was a lucky guess, see: http://mail.python.org/pipermail/pythonmac-sig/2005-April/013791.html for when it broke
  # Works in 10.4 Tiger
  # app('System Events').click(app('System Events').processes['Terminal.app'].windows[i].buttons[3])

  # for 10.5 Leopard
  term.windows[i].miniaturized.set('True')

  # TODO: Move off to second monitor?
  # http://www.macosxhints.com/article.php?story=2007102012424539

# Hide Other Programs
app('System Events').processes['Terminal.app'].keystroke('h', using=[k.command_down, k.option_down])

# Focus 2
app('System Events').processes['Terminal.app'].keystroke('2', using=k.command_down)




### NOTES ###

# http://www.domodomo.com/iphoto_to_web.py
# http://aurelio.net/doc/as4pp.html
# http://mail.python.org/pipermail/pythonmac-sig/2006-January/015683.html
# http://www.mactech.com/articles/mactech/Vol.21/21.06/UserInterfaceScripting/index.html
# http://www.macgeekery.com/development/gui_automation_with_applescript
# http://www.macosxhints.com/article.php?story=20061228162454404
# http://osxhacker.com/2007/04/23/applescript-to-minimize-all-application-and-finder-windows/
# http://www.nach-vorne.de/2007/11/22/terminal-trick
# http://onrails.org/articles/2007/11/28/scripting-the-leopard-terminal
# http://forums.macosxhints.com/archive/index.php/t-2894.html
# http://www.macosxhints.com/article.php?story=20030327003233675
# http://matt.blogs.it/entries/00002722.html
# http://appscript.sourceforge.net/examples.html
# http://www.macdevcenter.com/pub/a/mac/2007/02/27/replacing-applescript-with-ruby.html
# http://blog.lathi.net/articles/2007/10/05/resizing-your-terminal
# http://www.macdevcenter.com/pub/a/mac/2007/05/08/using-python-and-applescript-to-get-the-most-out-of-your-mac.html?page=2

# http://pexpect.sourceforge.net/
# http://www.macosxhints.com/article.php?story=2007102012424539
# http://www.macosxhints.com/article.php?story=20060105082728937
# http://www.ithug.com/2007/09/applescript-moving-and-resizing-windows/
# http://forums.macnn.com/79/developer-center/345599/moving-windows-with-qs-and-applescript/

# if w.exists():
#   print w.name().encode('utf-8')
#   w.number_of_rows.set(82)
#   w.number_of_columns.set(80)
#   w.position.set(0,0);

# finder = app('Finder')

# w = finder.Finder_windows[1]

# if w.exists(): # is there a Finder window open?
#     if w.target.class_.get() == k.computer_object:
        # 'Computer' windows don't have a target folder, for obvious reasons.
#         raise RuntimeError, "Can't get path to 'Computer' window."
#     folder = w.target # get a reference to its target folder
# else:
#     folder = finder.desktop # get a reference to the desktop folder

# path = folder.get(resulttype=k.alias).path # get folder's path

# print path
# peopleRef = app('Address Book').people[its.emails != []]
# print zip(peopleRef.name.get(), peopleRef.emails.value.get())


# term = OSA.app 'Terminal'

# if frontwindow = term.windows.detect{|w|w.frontmost?}
#   suppress_display = frontwindow.title_displays_window_size?
#   if ARGV.size >= 2
#     cols, rows = ARGV[0..1].map{|a|a.to_i}
#     frontwindow.number_of_columns = cols
#     frontwindow.number_of_rows    = rows
#     suppress_display = false
#   end
#   puts "#{frontwindow.number_of_columns}x#{frontwindow.number_of_rows}" unless suppress_display
# else
#   puts "no frontmost window?" 
# end

