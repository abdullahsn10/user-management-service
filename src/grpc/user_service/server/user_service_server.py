import grpc
from concurrent import futures
from src.grpc.user_service.protobuf import (
    user_service_pb2 as user_service_pb2,
    user_service_pb2_grpc as user_service_pb2_grpc,
)
from src.helpers import customer
from src.settings.database import db
from src.schemas import CustomerPOSTRequestBody
from src.grpc.user_service.server.user_service_helpers import _extract_token_data
from src.settings.settings import GRPC_SERVER_ADDRESS
from src.exceptions.exception import UserManagementServiceException


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    """
    This class is used to implement the gRPC server. It contains the implementation for
    all the methods defined in the user_service.proto file.
    """

    def GetOrCreateCustomer(self, request, context):
        """
        This method is used to get or create a customer. it receives a request from the
        gRPC client, validates the token, fetches or creates the customer, and returns
        the customer instance.
        *Args:
            request (user_service_pb2.CustomerRequest): the request from the client
            context: the context of the request
        *Returns:
            user_service_pb2.CustomerResponseWrapper: the response to the client
        """
        try:
            # Validate token, AUTH LOGIC
            token_data = _extract_token_data(token="ss")

            # Fetch or create customer
            customer_details = CustomerPOSTRequestBody(
                phone_no=request.customer.phone_no, name=request.customer.name
            )
            customer_instance, status_code = customer.get_or_create_customer(
                request=customer_details,
                coffee_shop_id=token_data.coffee_shop_id,
                db=db,
            )

            # Prepare the response
            customer_response = user_service_pb2.CustomerResponse(
                id=customer_instance.id,
                name=customer_instance.name,
                phone_no=customer_instance.phone_no,
                coffee_shop_id=customer_instance.coffee_shop_id,
            )
            return user_service_pb2.CustomerResponseWrapper(
                customer=customer_response, status_code=status_code
            )

        except UserManagementServiceException as ue:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(ue.message)
            return user_service_pb2.CustomerResponseWrapper()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return user_service_pb2.CustomerResponseWrapper()


def serve():
    """
    This function is used to start the gRPC server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port(GRPC_SERVER_ADDRESS)
    server.start()
    server.wait_for_termination()
