find ./test_cases -iname '*.sh' -print0 | xargs -0 -i bash run-a-test.sh {}
