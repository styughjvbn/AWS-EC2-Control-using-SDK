from pprint import pprint
import boto3

DISPLAY_WIDTH=80

class ControlPanel():
    def __init__(self) -> None:
        self.menu_list=[self.list_instance,self.available_zones,self.available_regions]
        self.ec2 = boto3.client('ec2')
    
    def print_menu(self):
        print("-"*DISPLAY_WIDTH)
        print(f"{'Amazon AWS Control Panel using SDK':^{DISPLAY_WIDTH}}")
        print("-"*DISPLAY_WIDTH,end="")
        for i in range(len(self.menu_list)):
            if i%2==0:
                print()
            print(f"{i:>3}. {self.menu_list[i].__name__:<{DISPLAY_WIDTH//2-5}}",end="")
        print(" "*(DISPLAY_WIDTH//2),end="")
        print(f"\n{' '*(DISPLAY_WIDTH//2)}{99:>3}. {'quit':<{DISPLAY_WIDTH//2-5}}")

    def available_regions(self):
        response = self.ec2.describe_regions()
        print("Available regions....")
        for i in response['Regions']:
            print(f"[region] {i['RegionName']:>20},  [endpoint]  {i['Endpoint']}")

    def available_zones(self):
        response = self.ec2.describe_availability_zones()
        print("Available zones....")
        for i in response['AvailabilityZones']:
            print(f"[id] {i['ZoneId']:>15},  [region]{i['RegionName']:>20},  [Zone]{i['ZoneName']:>20}")

    def run(self):
        while True:
            self.print_menu()
            print("Enter an integer: ",end="")
            menu=int(input())
            if menu==99:
                break
            self.menu_list[menu]()

    def list_instance(self):
        response = self.ec2.describe_instances()
        print("Listing instances....")
        for i in response['Reservations']:
            # pprint(i["Instances"])
            instance_info=i["Instances"][0]
            print(f"[id] {instance_info['InstanceId']},  [type]{instance_info['InstanceType']:>10},  [state]{instance_info['State']['Name']:>10}")
    
control_panel=ControlPanel()
control_panel.run()