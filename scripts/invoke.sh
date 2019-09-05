#!/bin/sh
# usage via make: "make id=foo invoke"

aws lambda invoke --function-name "$1" out --log-type Tail
