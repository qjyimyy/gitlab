######## define color ########
# red color
_red = '\033[31m'

# blue color
_blue = '\033[34m'

# green color
_green = '\033[32m'

# yellow color
_yellow = '\033[33m'

# purple color
_purple = '\033[35m'

# end color
_ec = '\033[0m'

# sky blue color
_sky = '\033[36m'

# light green color
_lgreen = '\033[92m'

######## status of pipeline ########
running = _sky + 'running' + _ec
pending = _yellow + 'pending' + _ec
canceled = _red + 'canceled' + _ec
success = _green + 'success' + _ec
created = _lgreen + 'created' + _ec
# status = ['running', 'pending', 'canceled', 'success']


# ######## print color ########
# print(_red + 'hello world')
# print(_blue + 'hello world')
# print(_green + 'hello world')
# print(_yellow + 'hello world')
# print(_purple + 'hello world')
# print(_ec + 'hello world')