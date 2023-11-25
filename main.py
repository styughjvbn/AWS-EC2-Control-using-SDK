import boto3

DISPLAY_WIDTH=80

class ControlPanel():
    def __init__(self) -> None:
        self.menu_list=[self.available_zone]
        self.ec2 = boto3.client('ec2',region_name='us-east-1')
    
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

    def available_zone(self):
        response = self.ec2.describe_regions()
        print("Available regions....")
        for i in response['Regions']:
            print(f"[region] {i['RegionName']:>20},  [endpoint]  {i['Endpoint']}")

    def run(self):
        while True:
            self.print_menu()
            print("Enter an integer: ",end="")
            menu=int(input())
            if menu==99:
                break
            self.menu_list[menu]()

        print("hihi223")

    def temp4():
        print("hihi5534543")
    
control_panel=ControlPanel()
control_panel.run()