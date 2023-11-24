# import boto3

# ec2 = boto3.client('ec2',region_name='us-east-1')

# # Retrieves all regions/endpoints that work with EC2
# response = ec2.describe_regions()
# print('Regions:', response['Regions'])
DISPLAY_WIDTH=80

class ControlPanel():
    def __init__(self) -> None:
        self.menu_list=[self.temp]
    
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

    def temp():
        print("hihi")

    def temp2():
        print("hihi223")

    def temp4():
        print("hihi5534543")
    
control_panel=ControlPanel()
control_panel.print_menu()