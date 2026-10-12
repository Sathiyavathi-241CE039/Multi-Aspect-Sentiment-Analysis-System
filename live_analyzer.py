import requests


API_URL = "http://127.0.0.1:5000/predict"


def analyze_review(review):

    try:

        response = requests.post(
            API_URL,
            json={
                "review": review
            },
            timeout=10
        )

        if response.status_code == 200:

            return response.json()

        return {
            "error": f"API Error: {response.status_code}"
        }

    except requests.exceptions.ConnectionError:

        return {
            "error": (
                "Flask API is not running. "
                "Please run: python api.py"
            )
        }

    except requests.exceptions.Timeout:

        return {
            "error": "API request timed out."
        }

    except Exception as e:

        return {
            "error": str(e)
        }