sed -n '1!p' training.csv | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > shuffled.csv
head -1 training.csv >> tmp & cat shuffled.csv >> tmp
mv tmp shuffled.csv