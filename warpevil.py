import platform, subprocess, os, datetime, base64, json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
import requests
   
   
temphi={
  "outbounds": 
  [


            
        {
            "type": "wireguard",
            "server": "",
            "server_port": 0,
            "local_address": [
                "172.16.0.2/32",
                ""
            ],
            "private_key": "",
            "peer_public_key": "",
            "reserved": [],
            "mtu": 1300,
            "workers": 2,
            "detour": "",
            "tag": "",
            "fake_packets": "1-3",
            "fake_packets_size": "10-30",
            "fake_packets_delay": "10-30",
            "fake_packets_mode": "m4"
        }
  ]
}
temp2hi={
  "outbounds": 
  [


            
        {
            "type": "wireguard",
            "server": "",
            "server_port": 0,
            "local_address": [
                "172.16.0.2/32",
                ""
            ],
            "private_key": "",
            "peer_public_key": "",
            "reserved": [],
            "mtu": 1300,
            "workers": 2,
            "detour": "",
            "tag": "",
            "fake_packets_mode": "m4"
        }
  ]
}

temp={
  "outbounds": 
  [
        {
            "type": "wireguard",
            "server": "",
            "server_port": 0,
            "local_address": [
                "172.16.0.2/32",
                ""
            ],
            "private_key": "",
            "peer_public_key": "",
            "reserved": [],
            "mtu": 1330,
            "workers": 2,
            "detour": "",
            "tag": ""
        }
  ]
}
temp2={
  "outbounds": 
  [
        {
            "type": "wireguard",
            "server": "",
            "server_port": 0,
            "local_address": [
                "172.16.0.2/32",
                ""
            ],
            "private_key": "",
            "peer_public_key": "",
            "reserved": [],
            "mtu": 1330,
            "workers": 2,
            "detour": "",
            "tag": ""
        }
  ]
}



    
def byte_to_base64(myb):
    return base64.b64encode(myb).decode('utf-8')
     

def generate_public_key(key_bytes):
    # Convert the private key bytes to an X25519PrivateKey object
    private_key = X25519PrivateKey.from_private_bytes(key_bytes)
    
    # Perform the scalar multiplication to get the public key
    public_key = private_key.public_key()
    
    # Serialize the public key to bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )    
    return public_key_bytes



def generate_private_key():
    key = os.urandom(32)    
    # Modify random bytes using algorithm described at:
    # https://cr.yp.to/ecdh.html.
    key = list(key) # Convert bytes to list for mutable operations
    key[0] &= 248
    key[31] &= 127
    key[31] |= 64    
    return bytes(key) # Convert list back to bytes




def register_key_on_CF(pub_key):
    url = 'https://api.cloudflareclient.com/v0a4005/reg'
    # url = 'https://api.cloudflareclient.com/v0a2158/reg'
    # url = 'https://api.cloudflareclient.com/v0a3596/reg'

    body = {"key": pub_key,
            "install_id": "",
            "fcm_token": "",
            "warp_enabled": True,
            "tos": datetime.datetime.now().isoformat()[:-3] + "+07:00",
            "type": "Android",
            "model": "PC",
            "locale": "en_US"}

    bodyString = json.dumps(body)

    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'Host': 'api.cloudflareclient.com',
               'Connection': 'Keep-Alive',
               'Accept-Encoding': 'gzip',
               'User-Agent': 'okhttp/3.12.1',
               "CF-Client-Version": "a-6.30-3596"
               }

    r = requests.post(url, data=bodyString, headers=headers)
    return r




def bind_keys():
    priv_bytes = generate_private_key()
    priv_string = byte_to_base64(priv_bytes)
    
    
    
    
    pub_bytes = generate_public_key(priv_bytes)
    pub_string = byte_to_base64(pub_bytes)
    
    



    result = register_key_on_CF(pub_string)
    
    if result.status_code == 200:
        try:
            z = json.loads(result.content)
            client_id = z['config']["client_id"]      
            cid_byte = base64.b64decode(client_id)
            reserved = [int(j) for j in cid_byte]
            
            
            return '2606:4700:110:846c:e510:bfa1:ea9f:5247/128',priv_string,reserved, 'bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo='
            
        except Exception as e:
            print('Something went wronge with api')
            exit()
def arch_suffix():
    machine = platform.machine().lower()
    if machine.startswith('i386') or machine.startswith('i686'):
        return '386'
    elif machine.startswith(('x86_64', 'amd64')):
        return 'amd64'
    elif machine.startswith(('armv8', 'arm64', 'aarch64')):
        return 'arm64'
    elif machine.startswith('s390x'):
        return 's390x'
    else:
        raise ValueError("Unsupported CPU architecture")


def export_bestIPS(path):
    Bestip = []

    with open(path, 'r') as csv_file:
        next(csv_file)
        c = 0
        for line in csv_file:
            Bestip.append(line.split(',')[0])
            c += 1
            if c == 2:
                break

    with open('Bestip.txt', 'w') as f:
        for ip in Bestip:
            f.write(f"{ip}\n")

    return Bestip
def export_bestIPS2(path):
    Bestip = []

    with open(path, 'r') as csv_file:
        csv_file2=csv_file.readlines()
        c = 0
        for line in csv_file2:
            Bestip.append(line[:len(line)-1])
            c += 1
            if c == 2:
                break

    return Bestip


def export_Hiddify(t_ips, f_ips):
    creation_time = os.path.getctime(f_ips)
    formatted_time = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M:%S")
    config_prefix = f'warp://{t_ips[0]}?ifp=10-20&ifps=20-60&ifpd=5-10#𓄂𓆃-IR&&detour=warp://{t_ips[1]}?ifp=10-20&ifps=20-60&ifpd=5-10#WoW-🗽-DE'

    title = "//profile-title: base64:" + base64.b64encode('𓄂𓆃 🗽 ÐΛɌ₭ᑎΞ𐒡𐒡 '.encode('utf-8')).decode(
        'utf-8') + "\n"
    update_interval = "//profile-update-interval: 1\n"
    sub_info = "//subscription-userinfo: upload=0; download=0; total=10737418240000000; expire=2546249531\n"
    profile_web = "//profile-web-page-url: https://github.com/darknessm427\n"
    last_modified = "//last update on: " + formatted_time + "\n"

    with open('warp.json', 'w') as op:
        op.write(title + update_interval + sub_info + profile_web + last_modified + config_prefix)


def toSingBox1(tag, clean_ip, detour):
    print("Generating Warp Conf")


    data = bind_keys()
    wg = temp["outbounds"][0]
    wg['private_key']=data[1]
    wg['peer_public_key']=data[3]
    wg['reserved']=data[2]
    wg['local_address'][1]=data[0]
    wg['server'] = clean_ip.split(':')[0]
    wg['server_port'] = int(clean_ip.split(':')[1])
    wg['mtu'] = 1300
    wg['workers'] = 2
    wg['detour'] = detour
    wg['tag'] = tag
    return wg
def toSingBox11(tag, clean_ip, detour):
    print("Generating Warp Conf")


    data = bind_keys()
    wg = temp2["outbounds"][0]
    wg['private_key']=data[1]
    wg['peer_public_key']=data[3]
    wg['reserved']=data[2]
    wg['local_address'][1]=data[0]
    wg['server'] = clean_ip.split(':')[0]
    wg['server_port'] = int(clean_ip.split(':')[1])
    wg['mtu'] = 1300
    wg['workers'] = 2
    wg['detour'] = detour
    wg['tag'] = tag
    return wg
def toSingBox2(tag, clean_ip, detour):
    print("Generating Warp Conf")


    data = bind_keys()
    wg = temphi["outbounds"][0]
    wg['private_key']=data[1]
    wg['peer_public_key']=data[3]
    wg['reserved']=data[2]
    wg['local_address'][1]=data[0]
    wg['server'] = clean_ip.split(':')[0]
    wg['server_port'] = int(clean_ip.split(':')[1])
    wg['mtu'] = 1300
    wg['workers'] = 2
    wg['detour'] = detour
    wg['tag'] = tag
    return wg
def toSingBox22(tag, clean_ip, detour):
    print("Generating Warp Conf")


    data = bind_keys()
    wg = temp2hi["outbounds"][0]
    wg['private_key']=data[1]
    wg['peer_public_key']=data[3]
    wg['reserved']=data[2]
    wg['local_address'][1]=data[0]
    wg['server'] = clean_ip.split(':')[0]
    wg['server_port'] = int(clean_ip.split(':')[1])
    wg['mtu'] = 1300
    wg['workers'] = 2
    wg['detour'] = detour
    wg['tag'] = tag
    return wg


def export_SingBox(t_ips, arch):
    with open('edge/assets/singbox-template.json', 'r') as f:
        data = json.load(f)

    warp_go_url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-go/warp-go-latest-linux-{arch}"
    subprocess.run(["wget", warp_go_url, "-O", "warp-go"])
    os.chmod("warp-go", 0o755)

    main_wg = toSingBox1('WARP-MAIN', t_ips[0], "direct")
    data["outbounds"].insert(1, main_wg)
    wow_wg = toSingBox11('WARP-WOW', t_ips[1], "WARP-MAIN")
    data["outbounds"].insert(2, wow_wg)

    with open('sing-box.json', 'w') as f:
        f.write(json.dumps(data, indent=4))


    os.remove("warp-go")
def export_SingBox2(t_ips, arch):
    with open('edge/assets/singbox-template.json', 'r') as f:
        data = json.load(f)

    warp_go_url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-go/warp-go-latest-linux-{arch}"
    subprocess.run(["wget", warp_go_url, "-O", "warp-go"])
    os.chmod("warp-go", 0o755)

    main_wg = toSingBox2('WARP-MAIN', t_ips[0], "direct")
    data["outbounds"].insert(3, main_wg)
    wow_wg = toSingBox22('WARP-WOW', t_ips[1], "WARP-MAIN")
    data["outbounds"].insert(4, wow_wg)  

    with open('sing-box-hiddify.json', 'w') as f:
        f.write(json.dumps(data, indent=4))


    os.remove("warp-go")

 
def main(script_dir):
    arch = arch_suffix()
    print("Fetch warp program...")
    url = f"https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/warp-yxip/warp-linux-{arch}"
    subprocess.run(["wget", url, "-O", "warp"])
    os.chmod("warp", 0o755)
    command = "./warp >/dev/null 2>&1"
    print("Scanning ips...")
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        print("Error: Warp execution failed.")
    else:
        print("Warp executed successfully.")

    result_path = os.path.join(script_dir, 'result.csv')
    top_ips = export_bestIPS(result_path)

    export_SingBox(t_ips=top_ips, arch=arch)
    export_SingBox2(t_ips=top_ips, arch=arch)
   
    os.remove("result.csv")
    os.remove("warp")


if __name__ == '__main__':
    script_directory = os.path.dirname(__file__)
    main(script_directory)
