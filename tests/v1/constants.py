def error_404_response():
    return {
        "code": 404,
        "message": "You've landed on a non-existant page. Please check our docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
        "success": False,
    }
