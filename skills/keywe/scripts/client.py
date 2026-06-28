# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "requests>=2.31.0",
#   "python-dotenv>=1.0.0",
# ]
# ///

import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

def get_env_config():
    api_key = os.getenv("KEYWE_API_KEY")
    
    if not api_key:
        print("ERROR: KEYWE_API_KEY environment variable is not set.", file=sys.stderr)
        print("Ask the user to export their API key from /settings.", file=sys.stderr)
        sys.exit(1)
        
    return "https://keywe.cloud", {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def get_schlage_auth(base_url, headers):
    email = os.getenv("SCHLAGE_EMAIL")
    password = os.getenv("SCHLAGE_PASSWORD")
    if not email or not password:
        print("ERROR: SCHLAGE_EMAIL and SCHLAGE_PASSWORD environment variables must be set.", file=sys.stderr)
        print("Ask the user to export their Schlage account credentials.", file=sys.stderr)
        sys.exit(1)
    return email, password

def handle_response(response):
    try:
        response.raise_for_status()
        if response.status_code in [200, 201]:
            print(json.dumps(response.json(), indent=2))
        elif response.status_code == 302:
            print(json.dumps({"success": True, "redirect": response.headers.get("Location")}))
    except requests.exceptions.HTTPError as e:
        print(f"API HTTP Error ({response.status_code}): {response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="KeyWe Core API Client")
    parser.add_argument("--action", required=True, choices=[
        "add-property", "add-access-point", "add-lock", "add-template", "add-reservation", "add-automation",
        "schlage-login", "schlage-logout"
    ])
    parser.add_argument("--name")
    parser.add_argument("--address")
    parser.add_argument("--property-id")
    parser.add_argument("--room-type")
    parser.add_argument("--access-point-id")
    parser.add_argument("--device-id")
    parser.add_argument("--lock-type", default="schlage_encode")
    parser.add_argument("--category")
    parser.add_argument("--channel", choices=["sms", "email"])
    parser.add_argument("--content")
    parser.add_argument("--email")
    parser.add_argument("--phone")
    parser.add_argument("--notes")
    parser.add_argument("--triggers", type=str)
    
    args = parser.parse_args()
    base_url, headers = get_env_config()

    if args.action == "add-property":
        if not args.name:
            print("ERROR: --name is required.", file=sys.stderr)
            sys.exit(1)
        payload = {"name": args.name, "address": args.address}
        res = requests.post(f"{base_url}/api/properties", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "add-access-point":
        if not all([args.name, args.property_id]):
            print("ERROR: --name and --property-id are required.", file=sys.stderr)
            sys.exit(1)
        payload = {"name": args.name, "propertyId": args.property_id, "roomType": args.room_type}
        res = requests.post(f"{base_url}/api/access-points", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "add-lock":
        if not all([args.name, args.access_point_id]):
            print("ERROR: --name and --access-point-id are required.", file=sys.stderr)
            sys.exit(1)
        payload = {
            "name": args.name,
            "accessPointId": args.access_point_id,
            "deviceId": args.device_id,
            "lockType": args.lock_type
        }
        res = requests.post(f"{base_url}/api/locks", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "add-template":
        if not all([args.name, args.category, args.content]):
            print("ERROR: --name, --category, and --content are required.", file=sys.stderr)
            sys.exit(1)
        payload = {
            "name": args.name,
            "category": args.category,
            "channel": args.channel or "sms",
            "content": args.content,
            "status": "active"
        }
        res = requests.post(f"{base_url}/api/templates", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "add-reservation":
        if not args.name:
            print("ERROR: --name is required.", file=sys.stderr)
            sys.exit(1)
        payload = {
            "name": args.name,
            "email": args.email,
            "guestPhone": args.phone,
            "notes": args.notes
        }
        res = requests.post(f"{base_url}/api/reservations", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "add-automation":
        if not all([args.name, args.triggers]):
            print("ERROR: --name and --triggers are required.", file=sys.stderr)
            sys.exit(1)
        try:
            parsed_triggers = json.loads(args.triggers)
        except Exception as err:
            print(f"ERROR: --triggers must be valid JSON: {err}", file=sys.stderr)
            sys.exit(1)
            
        payload = {
            "name": args.name,
            "triggers": parsed_triggers,
            "conditions": [],
            "actions": []
        }
        res = requests.post(f"{base_url}/api/automations", headers=headers, json=payload)
        handle_response(res)

    elif args.action == "schlage-login":
        email, password = get_schlage_auth(base_url, headers)
        ct_headers = {**headers, "Content-Type": "application/x-www-form-urlencoded"}
        body = f"username={email}&password={password}"
        res = requests.post(f"{base_url}/api/schlage/auth/token", headers=ct_headers, data=body)
        handle_response(res)

    elif args.action == "schlage-logout":
        res = requests.post(f"{base_url}/api/schlage/auth/logout", headers=headers)
        handle_response(res)

if __name__ == "__main__":
    main()
