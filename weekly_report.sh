#! /bin/bash
#--------------------------------------------
# git log to weekly report
# author:   zhnlk
# site:     github.com/zhnlk
# date:     2019-07-15
# desc:     put script in workspace directory
#           and pass location as 1st parameter.
# example:  ./weekly_report.sh $(pwd)
#--------------------------------------------

# $1 如果为空，则使用对应的路径
# echo "工作空间路径为:$1"

WORKSPACE_DIRECTORY=$1
WEEKLY_REPORT_NAME="weekly_report"
echo $WORKSPACE_DIRECTORY
mv $WEEKLY_REPORT_NAME `date +%Y%m%d%H%M%S` 
for PROJECT in `ls $WORKSPACE_DIRECTORY`;do 
    if [ -d $PROJECT ];then
        cd $PROJECT
        if [ -d '.git' ];then
            GIT_OUT=`git log --pretty="%cd-%h-%s" --author=$(git config --global user.name) --since=1.weeks --date=format:'%Y-%m-%d %H:%M:%S'`
            if [ -n "$GIT_OUT" ];then
                # echo $PROJECT $GIT_OUT
                echo $PROJECT >> ../$WEEKLY_REPORT_NAME
                echo $GIT_OUT >> ../$WEEKLY_REPORT_NAME
            fi
        fi
        cd ..
    fi
done
