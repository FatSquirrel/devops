from troposphere import (
    Base64,
    ec2,
    GetAtt,
    Join,
    Output,
    Parameter,
    Ref,
    Template,
)


applicateionPort = "3000"
t = Template()
t.add_description("Effective Devops in AWS: Helloworld web applicaion")
t.add_parameter(Parameter(
    "KeyPair",
    Description="Name of an existing EC2 KeyPair to SSH",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="Must be the name of an exisiting EC2 KeyPair.",
))

t.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="Allow SSH and TCP/{} access".format(applicateionPort),
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp="0.0.0.0/0",
        ),
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort=applicateionPort,
            ToPort=applicateionPort,
            CidrIp="0.0.0.0/0",
        )
    ]
))

"""skip UD parts"""

t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-05438a9ce08100b25",
    InstanceType="t2.micro",
    SecurityGroups=[Ref("SecurityGroup")],
    KeyName=Ref("KeyPair"),
))

t.add_output(Output(
    "InstancePublicIp",
    Description="Public Ip of our instance.",
    Value=GetAtt("instance", "PublicIp")
))

t.add_output(Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", [
        "http://", GetAtt("instance", "PublicDnsName"),
        ":", applicateionPort
    ])
))

print(t.to_json())
