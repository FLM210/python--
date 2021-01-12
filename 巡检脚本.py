from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time,os

m = PyMouse()
k = PyKeyboard()
os.startfile('H:\soft_center\FSCapture.exe')



def switchWindow(num=1): ###窗口切换
    k.press_key(k.alt_key)
    k.tap_key(k.tab_key,n=num)
    k.release_key(k.alt_key)

def cleanPrsc(): ###清屏
    k.press_key(k.control_l_key)
    k.tap_key("l")
    k.release_key(k.control_l_key)

def openTer(ipaddress):  ###打开终端
    os.startfile('H:\Program Files\CRT\SecureCRT.exe')
    time.sleep(1)
    m.click(x=84,y=122,button=1)
    time.sleep(1)
    k.type_string(ipaddress)
    time.sleep(1)
    k.tap_key(k.enter_key)
    time.sleep(1)

def runcmd(command):  ###运行命令
    m.click(479,253)
    k.type_string(command)
    k.tap_key(k.enter_key)

def prsc(startx,starty,endx,endy):  ###区域截屏
    k.press_key(k.control_l_key)
    k.tap_key(k.print_screen_key)
    k.release_key(k.control_l_key)
    time.sleep(1)
    #m.move(startx,starty)
    m.click(startx,starty)
    time.sleep(1)
    m.move(endx,endy)
    time.sleep(1)
    m.click(endx,endy)

def longprsc():    ###长截屏
    k.press_key(k.control_l_key)
    time.sleep(1)
    k.press_key(k.alt_l_key)
    time.sleep(1)
    k.tap_key(k.print_screen_key)
    time.sleep(1)
    k.release_key(k.control_l_key)
    time.sleep(1)
    k.release_key(k.alt_l_key)
    time.sleep(1)
    m.click(553,580)

def startPrsc(cmd,clean=1,close=0,startx=295,starty=94,endx=1417,endy=710):
    if clean == 1 :
        cleanPrsc()
    time.sleep(0.5)
    runcmd(cmd)
    if cmd == 'kubectl get po -n henanbill | grep -v Running':
        time.sleep(5)
    else:
        time.sleep(1.5)
    prsc(startx,starty,endx,endy)
    time.sleep(0.5)
    if close == 1 :
        os.system('taskkill /IM SecureCRT.exe /F')   

def startLongPrsc(cmd,close=0):
    runcmd(cmd)
    time.sleep(1)
    longprsc()
    if close == 1 :
        os.system('taskkill /IM SecureCRT.exe /F')


def startCheck(address,commandList,longScTime=10):
    openTer(address)
    startLongPrsc('kubectl get no')
    time.sleep(longScTime)
    switchWindow()
    startPrsc('kubectl get cs',close=1)
    openTer(address)
    startLongPrsc('kubectl top nodes')
    time.sleep(longScTime)
    switchWindow()
    startPrsc('kubectl get pod -n kube-system  | grep -v Running')
    switchWindow()
    startPrsc('kubectl get ev -n kube-system')
    switchWindow()
    for comm in commandList:
        startPrsc(comm)
        switchWindow()


clusterList = { 
    'crm': ['etcdctl --endpoint=https://10.218.127.70:2379 --cert-file=/etc/ssl/etcd/ssl/member-BH14F-F10-7U-R4700G3.pem --ca-file=/etc/ssl/etcd/ssl/ca.pem  --key-file=/etc/ssl/etcd/ssl/member-BH14F-F10-7U-R4700G3-key.pem cluster-health','kubectl get pod -n 62eb100d-5079-4430-86ff-d625f2e44bab|grep -v Running','kubectl get pod -n 8cb41151-68f0-47b8-99d4-80cbac44c48e|grep -v Running','kubectl get ev -n 62eb100d-5079-4430-86ff-d625f2e44bab','kubectl get ev -n 8cb41151-68f0-47b8-99d4-80cbac44c48e'],
    'jifei': ['etcdctl --endpoint=https://10.218.126.45:2379 --cert-file=/etc/ssl/etcd/ssl/member-BH14F-G07-7U-R4700G3.pem --ca-file=/etc/ssl/etcd/ssl/ca.pem  --key-file=/etc/ssl/etcd/ssl/member-BH14F-G07-7U-R4700G3-key.pem cluster-health','kubectl get po -n henanbill | grep -v Running','kubectl get ev -n henanbill'],
    'esb': ['etcdctl --endpoint=https://10.96.170.72:2379 --cert-file=/etc/kubernetes/ssl/kubernetes.pem --ca-file=/etc/kubernetes/ssl/ca.pem --key-file=/etc/kubernetes/ssl/kubernetes-key.pem cluster-health','kubectl get pod -n esb-jf  | grep -v Running','kubectl get pod -n esb-jf  | grep -v 2/2','kubectl get pod -n esb-llgj| grep -v Running','kubectl get pod -n esb-llgj| grep -v 2/2','kubectl get ev -n esb-jf','kubectl get ev -n esb-llgj']
}

#crm = 
#jifei = ['etcdctl --endpoint=https://10.218.126.45:2379 --cert-file=/etc/ssl/etcd/ssl/member-BH14F-G07-7U-R4700G3.pem --ca-file=/etc/ssl/etcd/ssl/ca.pem  --key-file=/etc/ssl/etcd/ssl/member-BH14F-G07-7U-R4700G3-key.pem cluster-health','kubectl get po -n henanbill | grep -v Running','kubectl get ev -n henanbill']
#esb = ['etcdctl --endpoint=https://10.96.170.72:2379 --cert-file=/etc/kubernetes/ssl/kubernetes.pem --ca-file=/etc/kubernetes/ssl/ca.pem --key-file=/etc/kubernetes/ssl/kubernetes-key.pem cluster-health','kubectl get pod -n esb-jf  | grep -v Running','kubectl get pod -n esb-jf  | grep -v 2/2','kubectl get pod -n esb-llgj| grep -v Running','kubectl get pod -n esb-llgj| grep -v 2/2','kubectl get ev -n esb-jf','kubectl get ev -n esb-llgj']

#startCheck('10.218.127.70',crm,13)
#startCheck('10.218.126.45-master',jifei,25)
#startCheck('10.96.170.72-Master(DockerBuild)',esb,7)


cluster = input("请输入需要巡检的集群【crm/jifei/esb】：")
if cluster in clusterList:
    if cluster == 'crm':
        startCheck('10.218.127.70',clusterList['crm'],13)
    elif cluster == 'jifei':
        startCheck('10.218.126.45-master',clusterList['jifei'],25)
    elif cluster == 'esb':
        startCheck('10.96.170.72-Master(DockerBuild)',clusterList['esb'],7)
else:
    print ('请输入正确的集群名称')
