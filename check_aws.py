import boto3
import sys

def check_credentials():
    print("------------------------------------------------")
    print("Checking AWS Credentials...")
    print("------------------------------------------------")
    
    try:
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        print("✅ SUCCESS! Credentials are valid.")
        print(f"Account: {identity['Account']}")
        print(f"ARN: {identity['Arn']}")
        print("------------------------------------------------")
        return True
    except Exception as e:
        print("❌ FAILURE! Could not verify credentials.")
        print(f"Error: {e}")
        print("------------------------------------------------")
        print("Please run 'aws configure' in your terminal and enter valid keys.")
        return False

if __name__ == "__main__":
    if check_credentials():
        # Try to list the bucket
        s3 = boto3.client('s3')
        bucket_name = "us-traffic-accidents-datalake"
        print(f"\nChecking access to bucket: {bucket_name}...")
        try:
            s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
            print(f"✅ SUCCESS! Can access bucket '{bucket_name}'.")
        except Exception as e:
            print(f"❌ FAILURE! Cannot access bucket '{bucket_name}'.")
            print(f"Error: {e}")
