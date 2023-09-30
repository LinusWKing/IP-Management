import os, mysql.connector
from dotenv import load_dotenv


load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user':os.getenv('DB_USER'),
    'password':os.getenv('DB_PASSWORD'),
    'database':os.getenv('DB_DATABASE')
}

conn = mysql.connector.connect(**db_config)

def generate_ip(start_ip , end_ip):
    ip_address = []
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    
    while start <= end:
        ip_address.append('.'.join(map(str,start)))
        start[3] += 1
        for i in range (3,0,-1):
            if start[i] == 256:
                start[i] = 0
                start[i-1] += 1
                
    return ip_address


try:
    
    cur = conn.cursor()
    
    ips= generate_ip('192.168.0.0', '192.168.0.15') # Range limited for demonstartion purposes
    
    for ip in ips:
        if ip == '192.168.0.0':
           status = 'reserved'
        else:
            status = 'available'
    
        query = "INSERT INTO ip_addresses(ip_address, status) VALUES (%s, %s)"
        values = (ip, status)
        cur.execute(query,values)
    
    conn.commit()
    print(f'Successfully inserted {len(ips)} IP addresses')

except mysql.connector.Error as e:
    print(f'Error: {e}')

finally: 
    conn.close()

    