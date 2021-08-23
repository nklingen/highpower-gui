import psutil
import os, signal
for proc in psutil.process_iter():
    print(proc.cmdline())
    if '4GruppeHP.py' in proc.cmdline() or "ppd" in proc.name():

        print('Found existing PPP session on pid: %s' % proc.pid)
        

        
        #this_process = os.getpgid(0)
        #process.kill()
        print(str(os.getpid()) + " "+ str(proc.pid))
        if ((int(proc.pid)-int(os.getpid())) != 0):
            print('Killing pid %s now' % proc.pid)
            process = psutil.Process(int(proc.pid))
            process.kill()
            #os.system('sudo kill -9 {pid}'.format(pid=proc.pid))

