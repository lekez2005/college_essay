import endpoints
from api.question import ObjectiveApi, EssayApi
from api.exam import ExamApi
from api.subject import SubjectApi
from api.examiner import ExaminerApi

application = endpoints.api_server([ObjectiveApi,
                                    EssayApi,
                                    ExamApi,
                                    SubjectApi,
                                    ExaminerApi],
                                    restricted=False)
