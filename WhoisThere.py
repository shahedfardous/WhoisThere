import pandas as pd
import requests
from ipwhois import IPWhois
from ipaddress import ip_network
from tqdm import tqdm
from colorama import Fore, Style
import concurrent.futures
from functools import lru_cache
import argparse

# Configuration
MAX_WORKERS = 10  # Number of concurrent threads
CACHE_SIZE = 1000  # Number of lookups to cache

def clean_prefix(prefix):
    """Clean and validate the IP prefix"""
    if not isinstance(prefix, str):
        return None
    prefix = prefix.strip()
    if not prefix:
        return None
    if prefix.endswith('/'):
        prefix = prefix[:-1]
    if '/' not in prefix:
        prefix = f"{prefix}/32"
    return prefix

@lru_cache(maxsize=CACHE_SIZE)
def get_asn_info_cached(prefix):
    """Cached version of ASN lookup"""
    try:
        network = ip_network(prefix, strict=False)
        ip = str(network.network_address)
        obj = IPWhois(ip)
        results = obj.lookup_rdap()
        
        asn = results.get('asn', 'N/A')
        asn_desc = results.get('asn_description', 'N/A')
        
        if isinstance(asn_desc, (list, tuple)):
            asn_desc = ", ".join(asn_desc)
        if asn_desc == 'N/A':
            asn_desc = results.get('network', {}).get('name', 'N/A')
            
        return asn, asn_desc
    except Exception as e:
        return 'N/A', f'Error: {str(e)}'

def process_prefix(prefix):
    """Process a single prefix with error handling"""
    clean_pre = clean_prefix(prefix)
    if not clean_pre:
        return {'Prefix': prefix, 'ASN': 'N/A', 'Provider': 'Error: Invalid prefix format'}
    asn, provider = get_asn_info_cached(clean_pre)
    return {'Prefix': clean_pre, 'ASN': asn, 'Provider': provider}

def process_prefixes(input_file, output_file):
    """Main processing function with multithreading"""
    try:
        df = pd.read_excel(input_file)
        if 'Prefix' not in df.columns:
            print(f"{Fore.RED}Error: 'Prefix' column not found{Style.RESET_ALL}")
            return False

        prefixes = [p for p in df['Prefix'].unique() if pd.notna(p)]
        results = []

        with tqdm(total=len(prefixes), desc=f"{Fore.CYAN}Processing{Style.RESET_ALL}") as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                future_to_prefix = {
                    executor.submit(process_prefix, prefix): prefix 
                    for prefix in prefixes
                }
                for future in concurrent.futures.as_completed(future_to_prefix):
                    results.append(future.result())
                    pbar.update(1)

        pd.DataFrame(results).to_excel(output_file, index=False)
        print(f"\n{Fore.GREEN}Processed {len(results)} prefixes in {pbar.format_dict['elapsed']:.1f}s{Style.RESET_ALL}")
        return True

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fast ASN lookup for IP prefixes')
    parser.add_argument('input_file', help='Excel file with Prefix column')
    parser.add_argument('-o', '--output', default='asn_results.xlsx', help='Output file')
    parser.add_argument('-w', '--workers', type=int, default=MAX_WORKERS, help='Thread count')
    
    args = parser.parse_args()
    MAX_WORKERS = args.workers

    print(f"\n{Fore.YELLOW}ASN Lookup Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Threads: {MAX_WORKERS} | Cache: {CACHE_SIZE}{Style.RESET_ALL}")
    
    if process_prefixes(args.input_file, args.output):
        print(f"{Fore.GREEN}Results saved to {args.output}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Processing failed{Style.RESET_ALL}")