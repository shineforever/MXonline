#!/bin/bash

#获得本机所有tomcat路径
tomcatlist=`ps -ef | grep -v grep | egrep -o '\-Dcatalina.home=[^ ]+' | cut -d'=' -f2`

printf "{\n"
printf "\t\"data\":[\n\n"

for tomcat in $tomcatlist
do
  tomcatpath=${tomcat}
  #获得tomcat进程文件
  tomcatpid=`ps -ef | grep "${tomcat} " | grep -v grep | awk '{print $2}'`

  if [ -n ${tomcatpid} ]; then
    #获得tomcatHTTP端口，规则可以根据需要修改
    httpport=`netstat -tnlp | grep "${tomcatpid}" | awk '$4!~/127\.0\.0\.1/ {print $4}' | cut -d':' -f2 | egrep '[5678]0[1-9][0-9]'`
    httpportnum=`netstat -tnlp | grep "${tomcatpid}" | awk '$4!~/127\.0\.0\.1/ {print $4}' | cut -d':' -f2 | egrep '[5678]0[1-9][0-9]' | wc -l`

    if [ $httpportnum -eq 1 ]; then
      printf "\t{"
      printf "\t\"{#TOMCATPORT}\":\"${httpport}\","
      printf "\t\"{#TOMCATPATH}\":\"${tomcatpath}\""
      printf "\t},\n"
    elif [ $httpportnum -gt 1 ]; then
      continue
    elif [ $httpportnum -eq 0 ]; then
      continue
    else
      continue
    fi

  fi

done

printf "\n\t]\n"
printf "}\n"
