import grpc
from concurrent import futures
from src.grpc.protobuf import (
    user_service_pb2 as user_service_pb2,
    user_service_pb2_grpc as user_service_pb2_grpc,
)
from src.helpers import customer
from src.settings.database import db
from src.security.jwt import verify_token
from fastapi import HTTPException, status
from src.schemas import CustomerPOSTRequestBody


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):

    def GetOrCreateCustomer(self, request, context):
        try:
            # Validate token, AUTH LOGIC
            # TODO: Implement auth logic
            token = request.token_data.token
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            token_data = verify_token(
                token=token, credentials_exception=credentials_exception
            )
            coffee_shop_id = token_data.coffee_shop_id

            # Fetch or create customer
            customer_details = CustomerPOSTRequestBody(
                phone_no=request.customer.phone_no, name=request.customer.name
            )
            customer_instance, status_code = customer.get_or_create_customer(
                request=customer_details, coffee_shop_id=coffee_shop_id, db=db
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

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error: {}".format(str(e)))
            return user_service_pb2.CustomerResponseWrapper()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
