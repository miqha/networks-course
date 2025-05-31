import json
import random
import ipaddress

class Router:
    def __init__(self, id, num_routers):
        self.id = id
        self.routing_table = {i: (-1, -1) for i in range(num_routers)}
        self.routing_table[self.id] = (self.id, 0)

    def update(self, edge):
        id1, id2 = edge
        if self.routing_table[id1][1] == -1:
            return
        
        if id1 == self.id:
            self.routing_table[id2] = (id2, 1)
        if self.routing_table[id2][1] == -1 or self.routing_table[id2][1] > self.routing_table[id1][1] + 1:
            self.routing_table[id2] = (self.routing_table[id1][0], self.routing_table[id1][1] + 1)

def generate_network(filename, n = 5):
    ip_list = []
    for i in range(n):
        ip = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
        ip_list.append(ip)
        
    routers = {ip: [ip_ for ip_ in ip_list if ip_ != ip and random.choice((True, False))] for ip in ip_list}
    
    with open(filename, 'w') as f:
        json.dump(routers, f, indent=4)

def load_network(filename):
    with open(filename, 'r') as f:
        routers = json.load(f)
    
    n = len(routers)
    ip_list = list(routers.keys())
    edges = [(ip_list.index(k), ip_list.index(i)) for k, v in routers.items() for i in v]

    return n, ip_list, edges

def print_router(step, router, ip_list):
    print(f"Router {ip_list[router.id]}. Step {step} routing table:")
    print("[Sourse IP]        [Destination IP]    [Next Hop]         [Metric]")
    for id, (next_hop, metric) in router.routing_table.items():
        print(f"{ip_list[router.id]:<18} {ip_list[id]:<18}  {(ip_list[next_hop] if next_hop != -1 else 'None'):<18}  {metric:>7}")
    print()

if __name__ == "__main__":
    generate_network('network.json', 10)
    n, ip_list, edges = load_network('network.json')

    routers = [Router(i, n) for i in range(n)]

    for j in range(n):
        print_router(0, routers[j], ip_list)

    for i in range(1, n):
        for j in range(n):
            for edge in edges:
                routers[j].update(edge)
            print_router(i, routers[j], ip_list)
