import subprocess

def run_command(cmd):



    cmd = str(cmd).split(" ")
    cmd = [arg.replace("\\", "/") if isinstance(arg, str) else arg for arg in cmd]

    i_command = ["powershell", "-Command"]

    i_command.extend(cmd)

    try:
        process = subprocess.Popen(
            i_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # Capturar a saída de erro separadamente
            universal_newlines=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace", 
        )

        output, error = process.communicate()

        if process.returncode != 0:  # Houve erro na execução do comando
            if "No such file or directory" in error:
                return "Erro: O arquivo ou diretório especificado não existe."
            elif "Permission denied" in error:
                return "Erro: Permissão negada para acessar o diretório ou arquivo."
            elif "command not found" in error or "is not recognized" in error:
                return "Erro: O comando especificado não foi encontrado."
            else:
                return f"Erro desconhecido ao executar o comando: {error.strip()}"

        return str(output).strip()  # Retorna a saída normal do comando

    except FileNotFoundError:
        return "Erro: O comando não foi encontrado no sistema."
    except PermissionError:
        return "Erro: Permissão negada para executar o comando."
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
