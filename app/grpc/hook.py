from app.grpc.services import CandidateStatusService
import app.grpc.candidate_pb2_grpc as candidate_pb2_grpc


def grpc_candidate_handlers(server):
    candidate_pb2_grpc.add_CandidateStatusServiceServicer_to_server(
        CandidateStatusService(), server
    )
