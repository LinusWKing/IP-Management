from flask import Flask, request, jsonify
from model import IPAddr,db
from dotenv import load_dotenv
import os, ipaddress

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

db.init_app(app)

API_KEY = os.getenv('API_KEY')

@app.before_request
def check_api_key():
    api_key = request.headers.get('API-Key')
    if api_key != API_KEY:
        return jsonify({'messsage': 'Unauthorized. Invalid API Key'}), 401

@app.route('/ip/allocate', methods=['POST'])
def allocate_ip():
    
    data = request.get_json()
    cust_name = data.get('customer_name')
    email = data.get('email')
    
    if not cust_name or not email:
        return jsonify({'status': 'error', 'message':'Bad Request'}), 400
    
    available_ip = IPAddr.query.filter_by(status='available').first()
    if available_ip:
        
        # Check if IP is allocated 
        if available_ip.status == 'allocated':
            return jsonify({'status':'error', 
                        'messsage': 'IP Already Allocated'}), 400
        
        available_ip.status = 'allocated'
        available_ip.customer_name = cust_name
        available_ip.email = email
        
        db.session.commit()
        
        return jsonify({'status':'success',
                        'message': f'Allocated IP: {available_ip.ip_address}'}),201
    
    else:
        return jsonify({'status':'error', 'message':'No available IPs'}), 500
    

@app.route('/ip/release/<ip_address>', methods=['PUT'])
def release_ip(ip_address):
    ip_for_release = IPAddr.query.filter_by(ip_address=ip_address).first()
    
    if not ip_for_release:
        return jsonify({'status':'error', 
                        'messsage': 'IP Not Found'}), 404

    elif ip_for_release.status != 'allocated':
        return jsonify({'status':'error', 
                        'messsage': 'IP Not allocated'}), 404
    else:
        ip_for_release.status = 'available'
        ip_for_release.customer_name = None
        ip_for_release.email = None
        
        db.session.commit()
        
        return jsonify({'status':'success', 
                        'messsage':f'IP Released:{ip_for_release.ip_address}'}), 200

@app.route('/ip/allocated', methods=['GET'])
def list_allocated():
    
  
    available_ips = IPAddr.query.filter_by(status='allocated').all()
    
    ip_list = [{'ip_address':ip.ip_address, 
                'customer':ip.customer_name,
                'email':ip.email} for ip in available_ips]
    
    return jsonify({'status':'success', 'allocated adresses':ip_list }), 200

@app.route('/ip/available', methods=['GET'])
def list_available():
    
   
    available_ips = IPAddr.query.filter_by(status='available').all()
    
    
    ip_list = [ip.ip_address for ip in available_ips]
    
    return jsonify({'status':'success', 'available adresses':ip_list }), 200


@app.route('/ip/subnet_calculator', methods=['GET'])
def subnet_calc():
    ip_address = request.args.get('ip_address')
    subnet_mask = request.args.get('subnet_mask')
    
    if not ip_address or not subnet_mask:
        return jsonify({'status':'error', 
                        'messsage': 'Provide IP address and Subnet mask'}), 400
    
    try:
        
        details = ipaddress.IPv4Network(f'{ip_address}/{subnet_mask}')
        
        network_addr = str(details.network_address)
        broadcast_addr = str(details.broadcast_address)
        valid_ip_range = [str(ip) for ip in details.hosts()]
    

        return jsonify({
            'status':'success',
            'network_address':network_addr,
            'broadcast_address':broadcast_addr,
            'valid_ip_range': valid_ip_range
        }), 200
    except ValueError:
        return jsonify({'status':'error', 
                        'messsage': 'Invalid IP address or Subnet mask format'}), 400

    
    
    
if __name__ == '__main__':
    app.run(debug=True)
    