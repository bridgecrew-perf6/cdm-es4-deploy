#!/usr/bin/env bash


function set_exit_on_error() {
  # Exit when any command fails
  set -e
}

function run_init() {
  terraform init
}

function run_show() {
  terraform show -json "$REGION-$ENV-state.tfstate" | python3 -m json.tool >../outputs/"$REGION-$ENV-$DATE-$REPO-$1".json
}

function run_apply() {
  terraform apply -state="$REGION-$ENV-state.tfstate" -var="env=$ENV" -var="region=$REGION" -auto-approve
}

function run_plan() {
  terraform plan -var="env=$ENV" -var="region=$REGION"
}

function run_destroy() {
  terraform destroy -state="$REGION-$ENV-state.tfstate" -var="env=$ENV" -var="region=$REGION" -auto-approve
}

function terraform_show() {
  echo "################################### SHOW $project ###################################"
  cd "$project"
  run_show "$project"
  cd ..
}

function terraform_apply() {
  set_exit_on_error
  echo "################################### APPLY $project ###################################"

  cat ./template/ec2-tf-cdm-template-header.txt > "./$project/main.tf"
  python3 ./scripts/genEC2CDMTF.py "{\"url\": \"${albUrlMap[$ENV-$REGION]}\", \"ami\": \"${amiMap[$REGION]}\", \"baseip\": \"${baseIpMap[$ENV]}\", \"env\": \"$ENV\"}" >> "./$project/main.tf"

  ./scripts/buildUidIpMap.sh "${baseIpMap[$ENV]}" "${albUrlMap[$ENV-$REGION]}"

  cd "$project"
  run_init
  run_apply
  cd ..
}

function terraform_plan() {
  echo "################################### PLAN $project ###################################"
  cd "$project"
  run_init
  run_plan
  cd ..
}

function terraform_destroy() {
  echo "################################### DESTROY $project ###################################"
  cd "$project"
  run_destroy
  cd ..
}

function arg_exception() {
  echo "3 args are required"
  echo "arg 1: provision environment (dev|stage|prod)"
  echo "arg 2: terraform function (apply|plan|show|destroy)"
  echo "arg 3: region (gov-west|gov-east)"
  exit 0
}

#############################################################################

if [[ "$4" != "./provision.sh" ]]; then
  echo "This is script can only be executed by ./provision.sh"
  exit 0
fi

if [[ $# -ne 4
      || "$1" != @(dev|stage|prod)
      || "$2" != @(plan|apply|show|destroy)
      || "$3" != @(gov-west|gov-east) ]]; then
  arg_exception
fi

ENV=$1
REGION="$3"
DATE=$(date '+%Y%m%d%H%M%S')
REPO="cdm"
project="cdm-$ENV-$REGION"

if [[ ! -d "$project" ]]; then
  mkdir "$project"
fi

declare -A amiMap=(["gov-west"]="ami-0e8f77cwerwer912" ["gov-east"]="ami-0b803werwer42")
declare -A baseIpMap=(["prod"]="10.16.16." ["stage"]="172.31.16." ["dev"]="172.16.16.")
declare -A albUrlMap=(["prod-gov-west"]="train.foosource-training.com" ["stage-gov-east"]="s.com" ["dev-gov-west"]="dev-train.edgesource-training.com")


if [[ "$2" == "apply" ]]; then
  terraform_apply
elif [[ "$2" == "plan" ]]; then
  terraform_plan
elif [[ "$2" == "show" ]]; then
  terraform_show
elif [[ "$2" == "destroy" ]]; then
  terraform_destroy
fi
