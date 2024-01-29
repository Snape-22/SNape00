from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup

@csrf_exempt
def get_news_info_api(request):
    if request.method == 'GET':
        try:
            # Get URL input from the request
            news_url = request.GET.get('url', '')

            # Validate if the URL is provided
            if not news_url:
                return JsonResponse({'error': 'URL parameter is required'}, status=400)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Send a GET request to the provided URL with headers
            response = requests.get(news_url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'html.parser')

                # Initialize headline
                headline_tag = soup.find('h1')
                if not headline_tag or len(headline_tag.text.strip()) <= 20:
                    headline_tag = soup.find('h2')
                if not headline_tag or len(headline_tag.text.strip()) <= 20:
                    headline_tag = soup.find('h3')

                headline = headline_tag.text.strip() if headline_tag else "Heading not found"

                # Initialize description
                description = "Description not found"

                # Find all <p> tags
                paragraphs = soup.find_all('p')

                # Iterate through <p> tags to find suitable text
                for i, paragraph in enumerate(paragraphs):
                    # Get the text and strip leading/trailing whitespaces
                    paragraph_text = paragraph.text.strip()

                    # Check if the paragraph text is more than 100 characters
                    if len(paragraph_text) > 100:
                        # Take the first 200 characters
                        description = paragraph_text[:200]

                        # Check if the next paragraph exists
                        next_paragraph = paragraphs[i + 1] if i + 1 < len(paragraphs) else None

                        # If the next paragraph exists, append its text to the description
                        if next_paragraph:
                            description += " " + next_paragraph.text.strip()

                        break  # Stop searching after finding the first suitable paragraph

                # Return the extracted information along with the URL as JSON response
                return JsonResponse({'url': news_url, 'headline': headline, 'description': description})

            else:
                return JsonResponse({'error': 'Failed to fetch the content', 'status_code': response.status_code}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
