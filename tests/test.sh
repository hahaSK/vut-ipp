declare -a arr=("complex" "empty" "read_test" "simple_tag" "write_test" "invalid_opcode" "header_error_1" "header_error_2" "parse_error_1" "parse_error_2" "parse_error_3")

for i in "${arr[@]}"
do
  echo $i
  ../interpret/php.exe ../parse.php < "./parse-only/$i.src" > "../test_results/$i.out"
  echo $? > "../test_results/$i.rc"
  diff -Z -q "../test_results/$i.rc" "./parse-only/$i.rc"
done