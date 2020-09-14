import boto3
ec2 = boto3.resource("ec2")

#Details used for new instances
ImageId = "ami-0603cbe34fd08cb81" #Amazon Machine Image ID to use to create the instance
MinCount = 1				      #Number of EC2 instances to launch
MaxCount = 1
InstanceType = "t2.micro"	      #Size of the instance t2.micro, t2.small, m5.large
KeyName="ec2-keypair"


#Creates new AWS EC2 Instance based off set variables
# @returns {instance} instances : a list of EC2 instances 
def createNewInstances():
	print("Creating " + str(MaxCount) + " " + ImageId + " Instances with type " + InstanceType)
	instances = ec2.create_instances(
	     ImageId=ImageId, 	
	     MinCount=MinCount,						
	     MaxCount=MaxCount,
	     InstanceType=InstanceType,   		
	     KeyName=KeyName
	 )
	return instances



#Terminates all given EC2 instance by their id
# @params {[instance]} instances: a list of active EC2 instances
def terminateAllInstances(instances):
	for instance in instances:
	    print("Terminating Instance : " + instance.id)
	    ec2.instances.filter(InstanceIds=[instance.id]).terminate()
