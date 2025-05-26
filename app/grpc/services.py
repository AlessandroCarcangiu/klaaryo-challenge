import json
import grpc
from app.grpc import candidate_pb2, candidate_pb2_grpc
from screening.models import Candidate


class CandidateStatusService(candidate_pb2_grpc.CandidateStatusServiceServicer):
    def GetCandidateStatus(self, request, context):
        try:
            candidate = Candidate.objects.get(id=request.id)
            response = candidate_pb2.CandidateStatusResponse()
            response.status = candidate.status
            for item in candidate.screening_log:
                check = response.screening_log.add()
                check.name = str(item.get("name", ""))
                check.result = str(item.get("result", ""))
            return response
        except Candidate.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Candidate not found')
            return candidate_pb2.CandidateStatusResponse()
