import requests

class Downloader():
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
    
    
    def download_image(self):
        try:
            # Send a GET request to the image URL
            response = requests.get(self.url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save the image to the specified file
            with open(self.save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image successfully downloaded: {self.save_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image: {e}")

# def download_image(url, save_path):
#     try:
#         # Send a GET request to the image URL
#         response = requests.get(url, stream=True)
#         response.raise_for_status()  # Raise an exception for HTTP errors

#         # Save the image to the specified file
#         with open(save_path, 'wb') as file:
#             for chunk in response.iter_content(1024):
#                 file.write(chunk)
#         print(f"Image successfully downloaded: {save_path}")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to download image: {e}")

# # Example usage
# image_url = "https://www.astria.ai/p/stylish-studio-portraits"  # Replace with the image URL
# save_location = "downloaded_image.jpg"  # Replace with the desired file name and location
# download_image(image_url, save_location)

