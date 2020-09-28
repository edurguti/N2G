import sys
sys.path.insert(0,'..')

# after updated sys path, can do N2G import from parent dir
from N2G import drawio_diagram as create_drawio_diagram
from N2G import yed_diagram as create_yed_diagram
from N2G import cdp_lldp_drawer

def test_cdp_drawing_yed_data_dict():
    data = {"Cisco_IOS": ["""
switch-1#show cdp neighbors detail 
-------------------------
Device ID: switch-2
Entry address(es): 
  IP address: 10.2.2.2
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP 
Interface: GigabitEthernet4/6,  Port ID (outgoing port): GigabitEthernet1/5

-------------------------
Device ID: switch-3
Entry address(es): 
  IP address: 10.3.3.3
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/1,  Port ID (outgoing port): GigabitEthernet0/1

-------------------------
Device ID: switch-4
Entry address(es): 
  IP address: 10.4.4.4
Platform: cisco WS-C3560-48TS,  Capabilities: Switch IGMP 
Interface: GigabitEthernet1/2,  Port ID (outgoing port): GigabitEthernet0/10

switch-1#show run
interface GigabitEthernet4/6
 description switch-2: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
!
interface GigabitEthernet1/1
 description switch-3:Gi0/1
 switchport
 switchport trunk allowed vlan 1771,1887
 switchport mode trunk
 mtu 9216
!
interface GigabitEthernet1/2
 description SW4 Routing Peering
 vrf forwarding VRF1
 ip address 10.0.0.1 255.255.255.0
    """,
    """
switch-2#show cdp neighbors detail 
-------------------------
Device ID: switch-1
Entry address(es): 
  IP address: 10.1.1.1
Platform: cisco WS-C6509,  Capabilities: Router Switch IGMP 
Interface: GigabitEthernet1/5,  Port ID (outgoing port): GigabitEthernet4/6    

switch-2#show run
interface GigabitEthernet1/5
 description switch-1: access
 switchport
 switchport access vlan 2150
 switchport mode access
 spanning-tree portfast edge
    """
        ]
    }
    config = {}
    drawing = create_yed_diagram()
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                           'src_label': 'Ge4/6',
                                           'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                           'trgt_label': 'Ge1/5'},
                                          {'source': 'switch-1',
                                           'src_label': 'Ge1/1',
                                           'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                           'trgt_label': 'Ge0/1'},
                                          {'source': 'switch-1',
                                           'src_label': 'Ge1/2',
                                           'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                           'trgt_label': 'Ge0/10'}],
                            'interfaces': {'Ge1/1': {'description': 'switch-3:Gi0/1',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'mtu': '9216',
                                                     'trunk_vlans': '1771,1887'},
                                           'Ge1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                           'Ge4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
               'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                           'src_label': 'Ge1/5',
                                           'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                           'trgt_label': 'Ge4/6'}],
                            'interfaces': {'Ge1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_dict.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_dict.graphml") as produced:
        with open("./Output/test_cdp_drawing_yed_data_dict_should_be.graphml") as should_be:
            assert produced.read() == should_be.read()
            
# test_cdp_drawing_yed_data_dict()


def test_cdp_drawing_yed_data_path():
    data = "./Data/SAMPLE_CDP_LLDP/"
    config = {}
    drawing = create_yed_diagram()
    drawer = cdp_lldp_drawer(drawing, config)
    drawer.work(data)
    assert drawer.parsed_data == {'Cisco_IOS': {'switch-1': {'cdp_peers': [{'source': 'switch-1',
                                           'src_label': 'Ge4/6',
                                           'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-2', 'top_label': '10.2.2.2'},
                                           'trgt_label': 'Ge1/5'},
                                          {'source': 'switch-1',
                                           'src_label': 'Ge1/1',
                                           'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-3', 'top_label': '10.3.3.3'},
                                           'trgt_label': 'Ge0/1'},
                                          {'source': 'switch-1',
                                           'src_label': 'Ge1/2',
                                           'target': {'bottom_label': 'cisco WS-C3560-48TS', 'id': 'switch-4', 'top_label': '10.4.4.4'},
                                           'trgt_label': 'Ge0/10'}],
                            'interfaces': {'Ge1/1': {'description': 'switch-3:Gi0/1',
                                                     'is_l2': True,
                                                     'l2_mode': 'trunk',
                                                     'mtu': '9216',
                                                     'trunk_vlans': '1771,1887'},
                                           'Ge1/2': {'description': 'SW4 Routing Peering', 'ip': '10.0.0.1 255.255.255.0', 'vrf': 'VRF1'},
                                           'Ge4/6': {'access_vlan': '2150', 'description': 'switch-2: access', 'is_l2': True, 'l2_mode': 'access'}}},
               'switch-2': {'cdp_peers': [{'source': 'switch-2',
                                           'src_label': 'Ge1/5',
                                           'target': {'bottom_label': 'cisco WS-C6509', 'id': 'switch-1', 'top_label': '10.1.1.1'},
                                           'trgt_label': 'Ge4/6'}],
                            'interfaces': {'Ge1/5': {'access_vlan': '2150', 'description': 'switch-1: access', 'is_l2': True, 'l2_mode': 'access'}}}}}
    drawer.drawing.dump_file(filename="test_cdp_drawing_yed_data_path.graphml", folder="./Output/")
    with open ("./Output/test_cdp_drawing_yed_data_path.graphml") as produced:
        with open("./Output/test_cdp_drawing_yed_data_path_should_be.graphml") as should_be:
            assert produced.read() == should_be.read()
    
# test_cdp_drawing_yed_data_path()