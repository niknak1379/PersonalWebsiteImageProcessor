from PIL import Image
from dotenv import load_dotenv
import boto3
import os
from io import BytesIO
import base64
import json

load_dotenv()

# Initialize S3 client outside handler for connection reuse
client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
)

def handler(event, context):
    base64Image = event.get("data")
    fieldname = event.get("fieldname")
    projectName = event.get("projectName")
    if base64Image is None or fieldname is None or projectName is None:
        return {
            'statusCode' : 500,
            'body' : json.dumps({'error': 'fields missing'})
        }
    
    try: 
       
        decodedImg = base64.b64decode(base64Image)

        img = Image.open(BytesIO(decodedImg))
        
        # Resize
        img.thumbnail((1200, 800))
        
        # Save to BytesIO as AVIF
        output = BytesIO()
        img.save(output, format='AVIF', quality=80)
        output.seek(0)
        
        objectURL = os.getenv('S3_PROJECT_DIR') + projectName + '/' + fieldname + '.avif'
        
        response = client.put_object(
            Body=output,
            Bucket=os.getenv('S3_BUCKET_NAME'),
            Key=objectURL
        )
        
        # Fix 4: Return properly formatted Lambda response
        if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'url': os.getenv('S3_PREFIX') + objectURL
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Error uploading to S3'})
            }
            
    except Exception as e:
        print(f"Error: {str(e)}")  # For CloudWatch logs
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }