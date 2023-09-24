import subprocess, sys
import argparse
import yaml

parser = argparse.ArgumentParser(description="Maven project analyze")

parser.add_argument("--config",     help="y/n")

parser.add_argument("--type",       help="Gradle/Maven")
parser.add_argument("--path",       help="Path to the project")
parser.add_argument("--backend",    help="Backend server ip with port with http/s")


args = parser.parse_args()

def steady_send(backend: str, type: str, path: str):
    backendServer = f"-Dvulas.shared.backend.serviceUrl={backend}" # http://localhost:8033/backend/

    # mvn -Dsteady compile org.eclipse.steady:plugin-maven:3.2.5:app
    # mvn org.eclipse.steady:plugin-maven:3.2.5:report -Dvulas.report.reportDir=$(pwd)/../scans
    # mvn -Dsteady org.eclipse.steady:plugin-maven:3.2.5:clean
    if type.lower() == "maven":
        print("maven...")
        mvn_compile = [
            "mvn",
            "-f",
            path,
            "-Dsteady",
            "compile",
            "org.eclipse.steady:plugin-maven:3.2.5:app",
            backendServer
        ]

        mvn_report = [ 
            "mvn",
            "-f",
            path,
            "-Dsteady", 
            "org.eclipse.steady:plugin-maven:3.2.5:report",
            "-Dvulas.report.reportDir=./scans",
            backendServer
        ]

        mvn_clear = [
            "mvn",
            "-f",
            path,
            "-Dsteady",
            "org.eclipse.steady:plugin-maven:3.2.5:clean",
            backendServer
        ]

        try:
            print("mvn_compile...")
            subprocess.run(mvn_compile, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("mvn_report...")
            subprocess.run(mvn_report, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("mvn_clear...")
            subprocess.run(mvn_clear, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Success!")
        except subprocess.CalledProcessError as e:
            print("Произошла ошибка при выполнении команды Maven:", e)

    elif type.lower() == "gradle":
        print("gradle...")

if args.config == "n":
    steady_send(args.backend, args.type, args.path)
else:
    with open('config.yaml', 'r') as yaml_file:
        config_steady = yaml.safe_load(yaml_file)["steady"]
    
    steady_send(config_steady["backend"], config_steady["type"], config_steady["path"])

   

