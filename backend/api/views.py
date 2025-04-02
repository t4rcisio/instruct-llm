from rest_framework.response import Response
from rest_framework.decorators import api_view
import traceback

from api.services import embedding, models
from api.utils import params_check, log

@api_view(['GET'])
def info(request):

    try:
        dados = {
            "APP NAME": "INSTRUCT LLM",
            "VERSION": "1.0",
            "STATUS": "OK",
            "AUTHOR": "tarcisio.b.prates",
            "GIT": "https://github.com/t4rcisio/instruct-llm",
            "MESSAGE": "To view logs acess: /api/logs"
        }
        return Response(dados)
    except:

        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO GET INOF SYS"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())


@api_view(['GET'])
def getModels(request):
    try:
        models = embedding.getModels()
        return Response(models)
    except:
        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO GET MODELS"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())

@api_view(['POST'])
def embeddingData(request):

    try:

        data = request.data

        payload = {
            "PATH_DIR": {"VALUE": None, "TYPE": str},
            "MODEL_ID": {"VALUE": None, "TYPE": str} ,
            "MODEL_NAME": {"VALUE": None, "TYPE": str} ,
            "CHUNK_SIZE": {"VALUE": None, "TYPE": int, "DEFAULT": 300},
            "CHUNK_OVERLAP": {"VALUE": None, "TYPE": int , "DEFAULT": 100} ,
            "QUESTION": {"VALUE": None, "TYPE": str} ,
            "K": {"VALUE": None, "TYPE": int, "DEFAULT": 3} ,
        }

        erros, params = params_check.paramasVerify(payload, data)

        if len(erros) > 0:
            return Response(erros)

        embedding.genRAG_folder(params['PATH_DIR']["VALUE"], params['MODEL_ID']["VALUE"], params['MODEL_NAME']["VALUE"] , chunk_size=params['CHUNK_SIZE']["VALUE"], chunk_overlap=params['CHUNK_OVERLAP']["VALUE"])
        response = embedding.search(params['MODEL_ID']["VALUE"], params['QUESTION']["VALUE"], k=params['K']["VALUE"])

        return Response(response)
    except:
        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO RUN EMBEDDING MODEL"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())


@api_view(['GET'])
def logs(request):

    try:
    
        return Response(log.readLog())
    
    except:
        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO ACCESS LOG DATABSE"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())



@api_view(['POST'])
def chat(request):

    try:

        payload = {
            "MODEL_NAME": {"VALUE": None, "TYPE": str},
            "INPUT": {"VALUE": None, "TYPE": list} ,
        }

        erros, params = params_check.paramasVerify(payload, request.data)

        if len(erros) > 0:
            return Response(erros)
    
        return Response(models.ask(params['MODEL_NAME']["VALUE"], params['INPUT']["VALUE"]))
    
    except:
        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO CONNECT TO CHAT"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())




@api_view(['POST'])
def agent_chat(request):

    try:

        payload = {
            "MODEL_NAME": {"VALUE": None, "TYPE": str},
            "INPUT": {"VALUE": None, "TYPE": list} ,
            "TOOLS": {"VALUE": None, "TYPE": list} ,
        }

        erros, params = params_check.paramasVerify(payload, request.data)

        if len(erros) > 0:
            return Response(erros)
    
        return Response(models.agent(params['MODEL_NAME']["VALUE"], params['TOOLS']["VALUE"], params['INPUT']["VALUE"]))
    
    except:
        log.addLog("FATAL",traceback.format_exc())
        return Response({"error": "ERROR TO CONNECT TO AGENT"}, status=500)
    finally:
        log.addLog("INFO", request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')))
        log.addLog("INFO", request.build_absolute_uri())

