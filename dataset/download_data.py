import urllib.request
import os

# Create dataset folder if it doesn't exist
os.makedirs('dataset', exist_ok=True)

print("⏳ Downloading a real, balanced fake review dataset...")
url = "https://raw.githubusercontent.com/rajsiddarth/Text_Analytics/master/deceptive-opinion.csv"
output_path = "dataset/reviews.csv"

try:
    urllib.request.urlretrieve(url, output_path)
    print("✅ Download Complete! Dataset saved as 'dataset/reviews.csv'")
except Exception as e:
    print(f"❌ Download failed: {e}")