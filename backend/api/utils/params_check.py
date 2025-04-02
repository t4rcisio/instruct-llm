
import traceback
from api.utils import log
import ollama

def paramasVerify(params, request):


    erros = []
    for item in params:

        try:
            
            if item in request:
                
                if isinstance(request[item], params[item]["TYPE"]):
                    params[item]["VALUE"] = request[item]
                else:
                    erros.append("Datatype error > Requested: " + str(params[item]["TYPE"]) + " | Recived: " + str(type(request[item])))
                    log.addLog("WARNING", erros[-1])
            else:

                if "DEFAULT" in params[item]:
                    params[item]["VALUE"] = params[item]['DEFAULT']
                else:
                    erros.append("Missing param > " + str(item))
                    log.addLog("WARNING", erros[-1])

        except:
            erros.append(traceback.format_exc())
            log.addLog("ERROR", erros[-1])

    return erros, params
    


def checkModel(model_name, maxTry=2):

    if maxTry == 0:
        return False

    models = ollama.list().get("models", [])

    ctrl = False

    for model in models:
     
        if model.model == model_name +":latest" :
            ctrl = model_name+":latest"
            break

        if model.model == model_name:
            ctrl = model_name
            break
    
    if not ctrl:
        ollama.pull(model_name)
        return checkModel(model_name, maxTry-1)

    return ctrl