%pip install dnspython

import dns.resolver
import time
import subprocess
import platform


def measure_dns_resolution_time(domain, record_type='A'):
    """Measures the time taken to resolve a DNS record."""

    resolver = dns.resolver.Resolver()
    start_time = time.perf_counter()  # Use perf_counter for accurate timing
    try:
        answers = resolver.resolve(domain, record_type)
        end_time = time.perf_counter()
        resolution_time = end_time - start_time
        print(f"Resolved {domain} ({record_type}) in {resolution_time:.4f} seconds")
        for rdata in answers:
            print(f"  {rdata}")
        return resolution_time

    except dns.exception.DNSException as e:
        print(f"Error resolving {domain}: {e}")
        return None



def traceroute_to_server(hostname):
    """Performs a traceroute to the given hostname using the system's traceroute."""
    try:
        if platform.system().lower() == 'windows':
            process = subprocess.run(['tracert', hostname], capture_output=True, text=True, check=True)
        else:
            process = subprocess.run(['traceroute', hostname], capture_output=True, text=True, check=True)
        output = process.stdout
        print(output)  
        # You can further process the output here (e.g., extract hop timings)

    except subprocess.CalledProcessError as e:
        print(f"Traceroute to {hostname} failed: {e.stderr if e.stderr else e}")



def get_authoritative_nameservers(domain):

    resolver = dns.resolver.Resolver()

    try:
      answers = resolver.resolve(domain, 'NS')
      nameservers = [ns.to_text() for ns in answers]
      print(f"Authoritative nameservers for {domain}:")
      for ns in nameservers:
          print(ns)
      return nameservers

    except dns.exception.DNSException as e:
        print(f"Error getting nameservers for {domain}: {e}")
        return []

# Example Usage
domain = 'google.com'  # Replace with the domain you want to test
measure_dns_resolution_time(domain)
measure_dns_resolution_time(domain, 'MX')
get_authoritative_nameservers(domain)
traceroute_to_server(domain)
