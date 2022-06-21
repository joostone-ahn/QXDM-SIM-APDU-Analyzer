def process(data, cmd):
    detail = ''
    if cmd == 'SELECT':
        if len(data) == 2:
            None

    return detail

cmd_name = dict()
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