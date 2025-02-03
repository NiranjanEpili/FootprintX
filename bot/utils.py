import socket
import ssl
import requests
import json
from datetime import datetime
import dns.resolver

def get_ssl_info(domain):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                # Format certificate information
                cert_info = {
                    'Subject': dict(x[0] for x in cert['subject']),
                    'Issuer': dict(x[0] for x in cert['issuer']),
                    'Version': cert['version'],
                    'Serial Number': cert['serialNumber'],
                    'Not Before': cert['notBefore'],
                    'Not After': cert['notAfter'],
                    'SANS': cert.get('subjectAltName', [])
                }
                return cert_info
    except ssl.SSLError as e:
        return f"SSL Error: {str(e)}"
    except socket.gaierror as e:
        return f"DNS Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_dns_records(domain):
    """Query different DNS record types for a domain."""
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    results = {}
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = []
            for rdata in answers:
                if record_type == 'MX':
                    results[record_type].append(f"{rdata.exchange} (priority: {rdata.preference})")
                elif record_type == 'SOA':
                    results[record_type].append(f"{rdata.mname} {rdata.rname}")
                else:
                    results[record_type].append(str(rdata))
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            return f"Domain {domain} does not exist"
        except Exception as e:
            continue
    
    return results

def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        return response.json()
    except:
        return None

def traceroute(domain):
    import subprocess
    try:
        output = subprocess.check_output(['traceroute', domain]).decode()
        return output
    except:
        return "Traceroute failed"

def check_haveibeenpwned(email):
    # Note: Requires API key from haveibeenpwned.com
    try:
        response = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={"hibp-api-key": "your-api-key"}
        )
        return response.json() if response.status_code == 200 else []
    except:
        return []

def generate_report_data(domain, results):
    return {
        "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "domain": domain,
        "results": results
    }
