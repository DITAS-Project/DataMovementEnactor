import grpc
import time
from concurrent import futures

import dal_pb2_grpc
import dal_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class DataMovementServicer(dal_pb2_grpc.DataMovementServiceServicer):

    def startDataMovement(self,  request, context):
        print(request)
        return dal_pb2.StartDataMovementReply()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dal_pb2_grpc.add_DataMovementServiceServicer_to_server(DataMovementServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
