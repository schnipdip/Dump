import subprocess

class dump_wifi():
    def __init__(self, state):
        '''
            Params: state   - state of WiFi (on/off)
        '''
        
        self.state = str(state)
        
        if self.state.lower() == 'on':
            wifi_enable()
        elif self.state.lower() == 'off':
            wifi_disable()
        else:
            print('Invalid Wifi State. Valid states: on, off')

    def wifi_enable(self):
        #Enable Wifi Connection using rfkill. More information 'man rfkill'
        subprocess.check_output(["rfkill", "unblock", "wifi"], shell=True)
        
    def wifi_disable(self):
        #Disable Wifi Connection using rfkill. More information 'man rfkill'
        subprocess.check_output(["rfkill", "block", "wifi"], shell=True)
    
