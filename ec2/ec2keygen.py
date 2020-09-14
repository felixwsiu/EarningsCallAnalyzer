import boto3
ec2 = boto3.resource("ec2")

# Create a new key pair and save it on disk
outfile = open('ec2-keypair.pem','w')
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)
