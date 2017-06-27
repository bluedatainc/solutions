 #/bin/bash
  export node=`bdmacro node --get_self_index`
  if [[ $node == 0 ]]; then
  ls -l /usr/lib/spark
  fi
