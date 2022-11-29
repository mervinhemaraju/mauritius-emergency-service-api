CONTENT_NOT_FOUND = {
    "services": [],
    "message": "No services found under this identifier. Check the docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
    "success": False,
}

CONTENT_BAD_REQUEST = {
    "services": [],
    "message": "Your browser sent a request that this server could not understand. Check the docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
    "success": False,
}

def content_service(service):
    return {
        "services": service,
        "message": "",
        "success": True,
    }


def content_services(services):
    return {"services": services, "message": "", "success": True}
