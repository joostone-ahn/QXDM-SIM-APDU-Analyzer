def process(data, cmd):
    detail = ''
    if cmd == 'SELECT':
        if len(data) == 2:
            None

    return detail

cmd_name = dict()

# ETSI 102.221
cmd_name['A4'] = 'SELECT'
cmd_name['F2'] = 'STATUS'
cmd_name['B0'] = 'READ BINARY'
cmd_name['D6'] = 'UPDATE BINARY'
cmd_name['B2'] = 'READ RECORD'
cmd_name['DC'] = 'UPDATE RECORD'
cmd_name['A2'] = 'SEARCH RECORD'
cmd_name['32'] = 'INCREASE'
cmd_name['CB'] = 'RETRIEVE DATA'
cmd_name['DB'] = 'SET DATA'
cmd_name['20'] = 'VERIFY PIN'
cmd_name['24'] = 'CHANGE PIN'
cmd_name['26'] = 'DISABLE PIN'
cmd_name['28'] = 'ENABLE PIN'
cmd_name['2C'] = 'UNBLOCK PIN'
cmd_name['04'] = 'DEACTIVATE FILE'
cmd_name['44'] = 'ACTIVATE FILE'
cmd_name['88'] = 'AUTHENTICATE'
cmd_name['89'] = 'AUTHENTICATE'
cmd_name['84'] = 'GET CHALLENGE'
cmd_name['AA'] = 'TERMINAL CAPABILITY'
cmd_name['10'] = 'TERMINAL PROFILE'
cmd_name['C2'] = 'ENVELOPE'
cmd_name['12'] = 'FETCH'
cmd_name['14'] = 'TERMINAL RESPONSE'
cmd_name['70'] = 'MANAGE CHANNEL'
cmd_name['73'] = 'MANAGE SECURE CHANNEL'
cmd_name['75'] = 'TRANSACT DATA'
cmd_name['76'] = 'SUSPEND UICC'
cmd_name['78'] = 'GET IDENTITY'

# Global Platform v2.3.1
cmd_name['E4'] = 'DELETE'
cmd_name['CA'] = 'GET DATA'
cmd_name['CB'] = 'GET DATA'
cmd_name['F2'] = 'GET STATUS'
cmd_name['E6'] = 'INSTALL'
cmd_name['E8'] = 'LOAD'
cmd_name['D8'] = 'PUT KEY'
cmd_name['F0'] = 'SET STATUS'
cmd_name['E2'] = 'STORE DATA'

# # ISO7816-4
# cmd_name['D0'] = 'WRITE BIRARY'
# cmd_name['0E'] = 'ERASE BIRARY'
# cmd_name['D2'] = 'WRITE RECORD'
# cmd_name['E2'] = 'APPEND RECORD'
# cmd_name['CA'] = 'GET DATA'
# cmd_name['DA'] = 'PUT DATA'
# cmd_name['B4'] = 'GET CHALLENGE'
