import subprocess, sys
import argparse

path = sys.argv[1]
# path = "app2"

parser = argparse.ArgumentParser(description="Maven project analyze")

parser.add_argument("--type",       help="Gradle/Maven")

parser.add_argument("--path",       help="Path to the project")
parser.add_argument("--backend",    help="Backend server ip with port with http/s")



args = parser.parse_args()

backendServer = f"-Dvulas.shared.backend.serviceUrl={args.backend}" # http://localhost:8033/backend/

# mvn -Dsteady compile org.eclipse.steady:plugin-maven:3.2.5:app
# mvn org.eclipse.steady:plugin-maven:3.2.5:report -Dvulas.report.reportDir=$(pwd)/../scans
# mvn -Dsteady org.eclipse.steady:plugin-maven:3.2.5:clean
if args.type.lower() == "maven":
    print("maven...")
    mvn_compile = [
        "mvn",
        "-f",
        args.path,
        "-Dsteady",
        "compile",
        "org.eclipse.steady:plugin-maven:3.2.5:app",
        backendServer
    ]

    mvn_report = [ 
        "mvn",
        "-f",
        args.path,
        "-Dsteady",
        "org.eclipse.steady:plugin-maven:3.2.5:report",
        "-Dvulas.report.reportDir=./scans",
        backendServer
    ]

    mvn_clear = [
        "mvn",
        "-f",
        args.path,
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

elif args.type.lower() == "gradle":
    print("gradle...")

