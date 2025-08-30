import requests
import sys
import os
import uuid

BASE_URL = "https://filebin.net"

def upload_folder(folder_path):
    if not os.path.isdir(folder_path):
        print("❌ Not a folder:", folder_path)
        return

    # Create a random bin ID so all files go into the same bin
    bin_id = str(uuid.uuid4())

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            url = f"{BASE_URL}/{bin_id}/{filename}"
            print(f"⬆️ Uploading {filename} ...")

            # Stream upload instead of buffering into memory
            with open(file_path, "rb") as f:
                headers = {"Content-Type": "application/octet-stream"}
                resp = requests.post(url, data=f, headers=headers)

            if resp.status_code in (200, 201):
                print(f"✅ Uploaded: {filename}")
            else:
                print(f"❌ Failed: {filename} ({resp.status_code})")

    print("\n🔗 Bin link:", f"{BASE_URL}/{bin_id}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <folder_path>")
        sys.exit(1)

    upload_folder(sys.argv[1])
