class Utils:
    @staticmethod
    def sort_queried_service(args, services):

        # Checks if an order was queried
        if "order" in args:
            order = args["order"]

            # Checks order type
            if order == "asc":
                return sorted(services, key=lambda x: x["name"], reverse=False)

            if order == "dsc":
                return sorted(services, key=lambda x: x["name"], reverse=True)

        return services
