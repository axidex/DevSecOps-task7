import subprocess, sys
import argparse
import yaml

parser = argparse.ArgumentParser(description="Maven project analyze")

parser.add_argument("--config",     help="y/n")

parser.add_argument("--type",       help="Gradle/Maven")
parser.add_argument("--path",       help="Path to the project")
parser.add_argument("--backend",    help="Backend server ip with port with http/s")

args = parser.parse_args()

# gradle_app/gradlew assemble vulasApp -p gradle_app -Pgroup=group -Pversion=1.2.3 -Pvulas.shared.backend.serviceUrl=http://localhost:8033/backend/
def gradle_send(backend: str, path: str):
    backendServer = f"-Pvulas.shared.backend.serviceUrl={backend}" 
    gradle_compile = [
        f"{path}/gradlew",
        "assemble",
        "vulasApp",
        "-p", "gradle_app",
        "-Pgroup=group",
        "-Pversion=1.2.3",
        backendServer
    ]

    gradle_report = [ 
        f"{path}/gradlew",
        "assemble",
        "vulasReport",
        "-p", "gradle_app",
        "-Pgroup=group",
        "-Pversion=1.2.3",
        backendServer
    ]

    gradle_clear = [
        f"{path}/gradlew",
        "assemble",
        "vulasClean",
        "-p", "gradle_app",
        "-Pgroup=group",
        "-Pversion=1.2.3",
        backendServer
    ]

    try:
        print("gradle_compile...")
        subprocess.run(gradle_compile, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("gradle_report...")
        subprocess.run(gradle_report, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("gradle_clear...")
        subprocess.run(gradle_clear, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Success!")
    except subprocess.CalledProcessError as e:
        print("Произошла ошибка при выполнении команды Maven:", e)

# mvn -f ./mvn_app -Dsteady compile org.eclipse.steady:plugin-gradle:3.2.5:app -Dvulas.shared.backend.serviceUrl=http://localhost:8033/backend/
def mvn_send(backend: str, path: str):
    backendServer = f"-Dvulas.shared.backend.serviceUrl={backend}"

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

def steady_send(backend: str, type: str, path: str):
    # http://localhost:8033/backend/

    # mvn -Dsteady compile org.eclipse.steady:plugin-maven:3.2.5:app
    # mvn org.eclipse.steady:plugin-maven:3.2.5:report -Dvulas.report.reportDir=$(pwd)/../scans
    # mvn -Dsteady org.eclipse.steady:plugin-maven:3.2.5:clean
    if type.lower() == "maven":
        print("maven...")
        mvn_send(backend=backend, path=path)
    elif type.lower() == "gradle":
        print("gradle...")
        gradle_send(backend=backend, path=path)

# python3.10 maven.py --path ./gradle_app --type gradle --backend http://localhost:8033/backend/ --config n
if __name__ == "__main__":
    if args.config == "n":
        print(args.backend, args.type, args.path)
        steady_send(args.backend, args.type, args.path)
    else:
        with open('config.yaml', 'r') as yaml_file:
            config_steady = yaml.safe_load(yaml_file)["steady"]
        
        steady_send(config_steady["backend"], config_steady["type"], config_steady["path"])

   

