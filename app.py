from flask import Flask, request, jsonify, send_file
from PIL import Image
from dotenv import load_dotenv
import boto3
import os
from io import BytesIO
import base64
load_dotenv()
app = Flask(__name__)

## setup AWS s3 client
client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
)



@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200



@app.route('/changeFormat', methods=['POST'])
def changeFormat():
    print(request)
    if not request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    print(request.files)
    # Get first file only
    file = request.files[list(request.files.keys())[0]]
    
    if not file.filename:
        return jsonify({'error': 'No filename'}), 400
    
    try:
        # Read and convert
        img = Image.open(BytesIO(file.read()))
        
        # Resize
        img.thumbnail((1200, 800))
        
        # Save to BytesIO as AVIF
        output = BytesIO()
        img.save(output, format='AVIF', quality=80)
        output.seek(0)
        objectURL = os.getenv('S3_PROJECT_DIR') + request.form.get('projectName')  + '/' + request.form.get('fieldname') + '.avif'
        response = client.put_object(
            Body=output,
            Bucket=os.getenv('S3_BUCKET_NAME'),
            Key=objectURL
        )
        # Return raw binary image
        if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            return { 's3_URL': os.getenv('S3_PREFIX') + objectURL}, 200
        else:
            return 'error in uploading to s3', 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)