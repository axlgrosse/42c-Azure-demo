#! /bin/sh

check_api() {
    apiJobStatusUrl="https://photo-demo.westeurope.cloudapp.azure.com/scand/api/job/$scanJob"
    headers='Accept: */*'

    # Perform curl request and store output in a variable
    response=$(curl -s -X GET $apiJobStatusUrl -H "$headers")
    echo "API response: $response"

    # Property to check for
    property="status"

    # Expected value
    expected_value="succeeded"

    # Extract the property value from the JSON response
    actual_value=$(echo "$response" | jq -r ".${property}")

    # Check if the actual value matches the expected value
    if [ "$actual_value" = "$expected_value" ]; then
        echo "The value of '$property' matches the expected value: $actual_value"
        return 0
    else
        echo "The value of '$property' does not match the expected value."
        echo "Actual value: $actual_value"
        return 1
    fi
}

scanJob='scan'

if [ "$1" ]; then
    scanJob=$1
fi

index=0
# Retry logic using 'until'
until check_api; do
    if [ $(($index % 3)) -eq 0 ]; then
      echo "Waiting for Scan job..."
    fi
    index=$((index+1))
    sleep 2
done

echo "Scan job completed."