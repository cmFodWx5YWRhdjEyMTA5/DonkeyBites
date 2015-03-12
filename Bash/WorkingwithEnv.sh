set -x

export LISTSUB=$($NEO_SH list-subscribed-accounts -a odp -b ${neoapp} -h neo.ondemand.com -u P1238713785 -p nirKoren123 | grep ${customerAccount})
export SUBAPP=$($NEO_SH subscribe -a ${customerAccount} -b odp:${neoapp} -h neo.ondemand.com -u P1238713785 -p nirKoren123)

# Check whether the tenant is already subscribed to  $customerAccount, if it is, the $TEST_RESULT will be equal to it
if [[ "$LISTSUB" == "" ]];
then
  $SUBAPP
  # Verify whether the tenant was subscribed successfuly to $customerAccount, if it is, the $VERIFY_RESULT will be equal to it
  export VERIFY_RESULT=$LISTSUB
  if [[ "$VERIFY_RESULT" == *"${customerAccount}"* ]];
  then
    echo Subscription SUCCEEDED! 
  else
    echo Subscription FAILED!
	exit 1
  fi  
else
  echo Already Subscribed
fi