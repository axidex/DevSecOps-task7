#!/bin/sh

root=$(pwd)
d=$1
echo "traversing ${d}";
# if [ -f "${d}/${report_file}" ]; then
#     echo "${d}/${report_file} exists, skipping analysis";
# else
cd $d
echo "running steady analysis on ${d}"
mvn -Dsteady compile org.eclipse.steady:plugin-maven:3.2.5:app
mvn org.eclipse.steady:plugin-maven:3.2.5:report -Dvulas.report.reportDir=$(pwd)/../scans
mv ../scans/vulas-report.json ../
# rm -rf ../scans
mvn -Dsteady org.eclipse.steady:plugin-maven:3.2.5:clean
cd $root
# fi

