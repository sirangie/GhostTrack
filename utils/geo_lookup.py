import requests
import json
from typing import Optional, Dict, Any


def get_ip_info(ip: str, timeout: int = 10) -> Optional[Dict[str, Any]]:
    """
    Fetch geolocation and network info for a given IP address.
    Uses ip-api.com as the primary source (free, no key needed).
    
    Args:
        ip: The IP address to look up
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with IP info or None if lookup failed
    """
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "fail":
            print(f"[!] ip-api error: {data.get('message', 'unknown error')}")
            return None

        return data

    except requests.exceptions.ConnectionError:
        print("[!] Connection error — check your internet connection.")
    except requests.exceptions.Timeout:
        print(f"[!] Request timed out after {timeout}s.")
    except requests.exceptions.HTTPError as e:
        print(f"[!] HTTP error: {e}")
    except json.JSONDecodeError:
        print("[!] Failed to parse response from ip-api.")
    except Exception as e:
        print(f"[!] Unexpected error during IP lookup: {e}")

    return None


def format_ip_info(data: Dict[str, Any]) -> str:
    """
    Format the raw IP info dict into a readable string for terminal output.
    
    Args:
        data: Dictionary returned by get_ip_info()
    
    Returns:
        Formatted string with all available fields
    """
    fields = [
        ("IP",          data.get("query",      "N/A")),
        ("Country",     f"{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})"),
        ("Region",      f"{data.get('regionName', 'N/A')} ({data.get('region', 'N/A')})"),
        ("City",        data.get("city",       "N/A")),
        ("ZIP",         data.get("zip",        "N/A")),
        ("Latitude",    str(data.get("lat",    "N/A"))),
        ("Longitude",   str(data.get("lon",    "N/A"))),
        ("Timezone",    data.get("timezone",   "N/A")),
        ("ISP",         data.get("isp",        "N/A")),
        ("Org",         data.get("org",        "N/A")),
        ("AS",          data.get("as",         "N/A")),
    ]

    lines = []
    for label, value in fields:
        lines.append(f"  {label:<12}: {value}")

    return "\n".join(lines)


def get_map_link(lat: float, lon: float) -> str:
    """
    Generate a Google Maps link for the given coordinates.
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        URL string pointing to the location on Google Maps
    """
    return f"https://www.google.com/maps?q={lat},{lon}"


def lookup_and_display(ip: str) -> bool:
    """
    High-level helper: look up an IP and print formatted results.
    Used by GhostTR.py's IP_Track function.
    
    Args:
        ip: Target IP address
    
    Returns:
        True if lookup succeeded, False otherwise
    """
    print(f"\n[*] Looking up: {ip}")
    data = get_ip_info(ip)

    if not data:
        print("[-] Could not retrieve information for this IP.")
        return False

    print("\n" + "-" * 40)
    print(format_ip_info(data))

    lat = data.get("lat")
    lon = data.get("lon")
    if lat and lon:
        print(f"  {'Map':<12}: {get_map_link(lat, lon)}")

    print("-" * 40 + "\n")
    return True
