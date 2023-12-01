from pprint import pprint
import time
import boto3

DISPLAY_WIDTH=80

class ControlPanel():
    def __init__(self) -> None:
        self.menu_list=[self.list_instance,self.available_zones,self.start_instance,self.available_regions,self.stop_instance,self.create_instance,self.reboot_instance,self.list_images,self.condor_status,self.create_image,self.delete_image,self.list_security_groups,self.create_security_group,self.add_security_group_inegress,self.change_security_group]
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
            instance_info=i["Instances"][0]
            print(f"[id] {instance_info['InstanceId']}, [AMI] {instance_info['ImageId']}, [type]{instance_info['InstanceType']:>10}, [state]{instance_info['State']['Name']:>10}, [monitoring state] {instance_info['Monitoring']['State']}, [security group] {' ,'.join(map(lambda a: a['GroupId'],instance_info['SecurityGroups']))}")

    def start_instance(self):
        print("Enter instance id: ",end="")
        instance_id=input()
        response = self.ec2.start_instances(InstanceIds=[instance_id])
        print("Starting .... %s"%(instance_id))
        print("Successfully started instance %s"%(instance_id))

    def stop_instance(self):
        print("Enter instance id: ",end="")
        instance_id=input()
        response = self.ec2.stop_instances(InstanceIds=[instance_id])
        print("Successfully stop instance %s"%(instance_id))

    def reboot_instance(self):
        print("Enter instance id: ",end="")
        instance_id=input()
        response = self.ec2.reboot_instances(InstanceIds=[instance_id])
        print("Rebooting .... %s"%(instance_id))
        print("Successfully rebooted instance %s"%(instance_id))

    def create_instance(self):
        print("Enter ami id: ",end="")
        ami_id=input()
        response=self.ec2.run_instances(ImageId=ami_id, InstanceType='t2.micro',MaxCount=1,MinCount=1)
        print("Successfully started EC2 instance %s based on AMI %s"%(response['Instances'][0]['InstanceId'],response['Instances'][0]['ImageId']))

    def delete_image(self):
        print("Enter ami id: ",end="")
        ami_id=input()
        response=self.ec2.deregister_image(ImageId=ami_id)

        print("Successfully deleted image %s"%(ami_id))
    
    def create_image(self):
        print("Enter instance id: ",end="")
        instance_id=input()
        print("Enter image name: ",end="")
        iamge_name=input()
        print("Enter image description : ",end="")
        iamge_description=input()
        response=self.ec2.create_image(InstanceId =instance_id, Description =iamge_description,Name=iamge_name)

        print("Successfully created image %s based on instance %s"%(response['ImageId'],instance_id))

    def list_images(self):
        response = self.ec2.describe_images(Owners=['self'])
        print("Listing images....")
        for i in response['Images']:
            print(f"[ImageID] {i['ImageId']},  [Name]{i['Name']:>20},  [Hypervisor]{i['Hypervisor']:>10}")
    
    def condor_status(self):
        # AWS 인증 및 서비스 클라이언트 생성
        ssm_client = boto3.client('ssm')
        print("Enter instance id: ",end="")
        instance_id=input()

        # Run Command 실행
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWS-RunShellScript',  # 실행할 문서 (Shell 스크립트 실행을 위해 AWS-RunShellScript 사용)
            Parameters={'commands': ['condor_status']},
        )
        command_id = response['Command']['CommandId']
        # 명령이 완료될 때까지 대기
        while True:
            command_status = ssm_client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,  # 결과를 받을 인스턴스 ID
            )
            if command_status['Status'] in ['Success', 'Failed', 'Cancelled']:
                break
            time.sleep(5)  # 일정 시간을 대기한 후에 상태를 확인합니다.

        # 실행 결과 확인
        if command_status['Status'] == 'Success':
            output = command_status['StandardOutputContent']
            print(output)  # 명령어 실행 결과 출력
        else:
            print("Command execution failed or was cancelled.")

    def list_security_groups(self):
        response=self.ec2.describe_security_groups()
        for i in response['SecurityGroups']:
            print(f"[GroupId] {i['GroupId']},  [Name]{i['GroupName']:>20},  [Description]  {i['Description']}")
            for j in i['IpPermissions']:
                if j['IpProtocol']=='-1':
                    print(f"    ingress : [protocol] {'all':>7}, [ipv4Range]{j['IpRanges'][0]['CidrIp'] if len(j['IpRanges']) else 'None':>10},  [UserIdGroupPairs]{j['UserIdGroupPairs'][0]['GroupId'] if len(j['UserIdGroupPairs']) else 'None':>25}")
                else:
                    print(f"    ingress : [protocol] {j['IpProtocol']:>7},  [portRange]{str(j['FromPort'])+'-'+str(j['ToPort']):>13},  [ipv4Range]{j['IpRanges'][0]['CidrIp'] if len(j['IpRanges']) else 'None':>10},  [UserIdGroupPairs]{j['UserIdGroupPairs'][0]['GroupId'] if len(j['UserIdGroupPairs']) else 'None':>25}")
            print()
    def create_security_group(self):
        print("Enter security group name: ",end="")
        name=input()
        print("Enter security group description : ",end="")
        description=input()
        response=self.ec2.create_security_group(Description=description,GroupName=name)
        print("Successfully created security group %s"%(response['GroupId']))

    def add_security_group_inegress(self):
        request={}
        print("Enter security group id: ",end="")
        request['GroupId']=input()
        print("choice egress protocol [ 1.TCP  2.UDP  3.ICMP  4.ICMPv6 ] : ",end="")
        IpPermissions={}
        protocol=int(input())
        if protocol == 1:
            IpPermissions["IpProtocol"]="tcp"
            print("choice port range ex) 0 - 65535: ",end="")
            port=input()
            IpPermissions["FromPort"]=int(port.split("-")[0])
            IpPermissions["ToPort"]=int(port.split("-")[1])
        elif protocol == 2:
            IpPermissions["IpProtocol"]="udp"
            print("choice port range ex) 0 - 65535: ",end="")
            port=input()
            IpPermissions["FromPort"]=int(port.split("-")[0])
            IpPermissions["ToPort"]=int(port.split("-")[1])
        elif protocol==3:
            IpPermissions["IpProtocol"]="icmp"
            IpPermissions["FromPort"]=-1
            IpPermissions["ToPort"]=-1
        elif protocol==4:
            IpPermissions["IpProtocol"]="icmpv6"
            IpPermissions["FromPort"]=-1
            IpPermissions["ToPort"]=-1
        print("choice ipv4 range or user group pair ex) 0.0.0.0/0 or sg-4b51a32f : ",end="")
        input_value=input()
        if 'sg' in input_value:
            IpPermissions["UserIdGroupPairs"]=[{'GroupId':input_value}]
        else:
            IpPermissions["IpRanges"]=[{'CidrIp':input_value}]
        request['IpPermissions']=[IpPermissions]
        response=self.ec2.authorize_security_group_ingress(**request)
        if response['Return']:
            print("Successfully add security group ingress %s"%(request['GroupId']))
        else:
            print("Failed")

    def change_security_group(self):
        print("Enter instance id: ",end="")
        instance_id=input()
        interfaceId=self.ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]["Instances"][0]['NetworkInterfaces'][0]['NetworkInterfaceId']
        print("Enter security group id: ",end="")
        security_group_id=input()
        response = self.ec2.modify_network_interface_attribute(
        Groups=[security_group_id],
        NetworkInterfaceId=interfaceId,
        )
        print("Successfully change security group")

    
control_panel=ControlPanel()
control_panel.run()