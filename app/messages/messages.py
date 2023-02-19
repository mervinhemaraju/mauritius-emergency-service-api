CONTENT_NOT_FOUND_SERVICES = {
    "services": [],
    "message": "No services found under this identifier. Check the docs at https://github.com/mervinhemaraju/mauritius-emergency-service-api",
    "success": False,
}

CONTENT_NOT_FOUND_REPORT = {
    "services": [],
    "message": "An error occurred while getting the report: {}",
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

def content_cyclone_report(level, next_bulletin):
    return {
        "report": {
            "class": level,
            "next_bulletin": next_bulletin
        },
        "message": "",
        "success": True,
    }

def content_services(services):
    return {"services": services, "message": "", "success": True}
