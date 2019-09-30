from threading import  Thread
#import multiprocessing
import ManhattanComponent
import time
from robot.api.logger import console
obj_list = []
lthreads1 = []
lthreads2 = []
lthreads3 = []
lthreads4 = []

def parallel_launch(dict, obj):    
    obj.launch_client(dict)    
    
def parallel_login(user, obj):    
    obj.client_login(**user)
    
def parallel_logout(obj):
    obj.close_browser()

def parallel_hookup(obj):
    obj.end_voicemail_call()    
    
def launch_login(**params):
    global obj_list
    client1 = ManhattanComponent.ManhattanComponent("parallel")
    obj_list.append(client1)
    client2 = ManhattanComponent.ManhattanComponent("parallel")
    obj_list.append(client2)
    client3 = ManhattanComponent.ManhattanComponent("parallel")
    obj_list.append(client3)
    client4 = ManhattanComponent.ManhattanComponent("parallel")
    obj_list.append(client4)    
    launch(**params)
    login(**params)
    end_calls(**params)
    console(obj_list)
    return obj_list


def launch(**params): 
    global lthreads1
    dicts = [
    {'server':'localhost', 'component_type':'manhattancomponent', 'port':'4444', 'browserName':'chrome', 'aut':'connect_client', 'isDevScript':'true'}
    ,{'server':'localhost', 'component_type':'manhattancomponent', 'port':'5555', 'browserName':'chrome', 'aut':'connect_client', 'isDevScript':'true'}
    ,{'server':'localhost', 'component_type':'manhattancomponent', 'port':'6666', 'browserName':'chrome', 'aut':'connect_client', 'isDevScript':'true'}
    ,{'server':'localhost', 'component_type':'manhattancomponent', 'port':'7777', 'browserName':'chrome', 'aut':'connect_client', 'isDevScript':'true'}
    ]   
    
    import Queue
    q = Queue.Queue()
    for i in range(int(params['client_count'])):
        t = Thread(target=parallel_launch, args=[dicts[i], obj_list[i]])
        t.start()
        lthreads1.append(t)
    
    for t in lthreads1:
        t.join()
    
    
def login(**params):
    global lthreads2
    users = [{'username':params['user1'].client_id, 'password':params['user1'].client_password, 'server_address':params['user1'].server}
    ,{'username':params['user2'].client_id, 'password':params['user2'].client_password, 'server_address':params['user2'].server}
    ,{'username':params['user3'].client_id, 'password':params['user3'].client_password, 'server_address':params['user3'].server}
    ,{'username':params['user4'].client_id, 'password':params['user4'].client_password, 'server_address':params['user4'].server}]

    for i in range(int(params['client_count'])):
        t = Thread(target=parallel_login, args=[users[i], obj_list[i]])
        t.start()
        lthreads2.append(t)
    
    for t in lthreads2:
        t.join()

def end_calls(**params):
    global lthreads4
    for i in range(int(params['client_count'])):
        t = Thread(target=parallel_hookup, args=[obj_list[i]])
        t.start()
        lthreads4.append(t)
    
    for t in lthreads4:
        t.join()

    
def close_applications(params):    
    global lthreads3
    for i in range(int(params)):
        t = Thread(target=parallel_logout, args=[obj_list[i]])
        t.start()
        lthreads3.append(t)
    
    for t in lthreads3:
        t.join()
       
