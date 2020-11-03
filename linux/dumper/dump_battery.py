import subprocess
import sys

class dump_battery:
    def battery_remaining(self):
        self.rem = subprocess.check_output("upower -i | grep -i 'percentage'", shell=True)
        
        #TESTING CODE - REMOVE WHEN DONE
        #self.file = open('/home/pi/dump-dev/dump/linux/dumper/battery_test.txt', 'r')   
        
        for i in self.rem:
            if 'percentage' in i:
                self.percentage = i.split()
            else:
                pass
        
        return (int(self.percentage[1].strip('%')))
        

    def battery_state(self):
        self.state = subprocess.check_output(["upower -i | grep -i 'state'", shell=True)
        
        #TESTING CODE - REMOVE WHEN DONE        
        #self.file = open('/home/pi/dump-dev/dump/linux/dumper/battery_test.txt', 'r')
        
        for i in self.state:
            if 'state' in i:
                self.status = i.split()
            else:
                pass
        
        return (str(self.status[1]))
        
