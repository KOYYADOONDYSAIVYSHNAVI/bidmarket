from concurrent import futures
import grpc
import user_pb2 as user_pb2
import user_pb2_grpc as user_pb2_grpc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.user import User  


engine = create_engine('mysql://root:root@localhost/userdb')  
Session = sessionmaker(bind=engine)
db = Session()

def block_user_logic(user_id):
    try:
        user = db.query(User).filter_by(user_id=user_id).first()
        if user:
            user.is_active = False  
            user.is_blocked = True  
            db.commit()  
            return True
        return False
    except Exception as e:
        print(f"Error blocking user: {e}")
        db.rollback()  
        return False

class UserService(user_pb2_grpc.UserServiceServicer):
    def RemoveAndBlockUser(self, request, context):
        user_id = request.user_id
        if block_user_logic(user_id):
            return user_pb2.UserResponse(message="User removed and blocked successfully")
        return user_pb2.UserResponse(message="Failed to remove and block user")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50053")  
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
