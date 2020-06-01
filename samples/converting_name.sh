
file_directory="./test"
save_directory="./output"


files=$( ls $file_directory )


for i in $files
do
  var=$(echo $i | awk -F"." '{print $1,$2}')
  set -- $var
 
  current_file_directory="$file_directory/$i"
  save_file_directory="$save_directory/$1_lp.png"
  cp $current_file_directory $save_file_directory

done
