import requests
import os

def count_files_in_folder(folder_path):
    """
    Find the count how many image files are available in pexels_images folder.
    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    file_count = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count


def download_img():
    folder_path = "pexels_images"
    file_count = count_files_in_folder(folder_path)
    if file_count==None:
        file_count = 1
    else:
        file_count = file_count + 1

    # Create a folder to save the downloaded images
    os.makedirs('pexels_images', exist_ok=True)

    # Set your API key
    api_key = '<YOUR-PEXELS-API-KEY>' # API Key can be generated from official website of Pexels.com (https://www.pexels.com/api/)

    # Set the URL for searching images
    url = 'https://api.pexels.com/v1/search'

    # Set the search query and parameters
    query = 'indian boys'
    per_page = 80  # Number of images to retrieve per request
    total_images = 100  # Total number of images to download

    # Calculate the number of requests required
    num_requests = total_images // per_page

    # Make the API requests
    for i in range(num_requests+1):
        # Set the parameters for each request
        params = {
            'query': query,
            'per_page': per_page,
            'page': i + 1  # Page number of the request
        }

        # Make the API request with the proper headers
        headers = {
            'Authorization': api_key
        }
        response = requests.get(url, headers=headers, params=params)

        # Process the response
        if response.status_code == 200:
            data = response.json()
            for photo in data['photos']:
                image_url = photo['src']['original']

                image_name = f"img-{file_count}.jpg"
                image_path = os.path.join('pexels_images', image_name)

                image_response = requests.get(image_url)
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                print(f'Saved image: {image_path}')
                file_count += 1
        else:
            print('Error:', response.status_code)


if __name__ == "__main__":
    download_img()