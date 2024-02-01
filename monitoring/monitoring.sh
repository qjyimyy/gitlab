#!/bin/zsh

# 调用Python脚本，获取项目列表并将其输出作为变量值
projects=$(python3 ./gitlab/get_projects.py)
print "$projects"

# 将项目列表的第一个项目的ID作为GITLAB_PROJECT_ID变量的值
echo "$projects" | head -n $(($(echo "$projects" | wc -l))) | awk '{print $3}'
export GITLAB_PROJECT_ID=$(echo "$projects" | head -n $(($(echo "$projects" | wc -l))) | awk '{print $3}')

# 输出当前运行的pipeline和正在使用的runner
echo "Current pipeline: $CI_PIPELINE_ID"
echo "Current runner: $CI_RUNNER_DESCRIPTION"
