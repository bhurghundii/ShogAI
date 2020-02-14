
cd ml

python3 processData.py

python2 sortfiles.py

cd ..

python3 generateCSVHeaders.py $file

for entry in "ml/black/storage"/*

do
    if [[ $entry =~ ".csa.txt" ]];
    then
    root=$(pwd)
    file="$root/$entry" 
    echo $file  
    echo "python3 generateDataset.py $file"  
    timeout 30 python3 generateDataset.py $file
    fi
done

mv training.csv black_training.csv


python3 generateCSVHeaders.py $file

for entry in "ml/white/storage"/*

do
    if [[ $entry =~ ".csa.txt" ]];
    then
    root=$(pwd)
    file="$root/$entry" 
    echo $file  
    echo "python3 generateDataset.py $file"  
    timeout 30 python3 generateDataset.py $file
    fi
done

mv training.csv white_training.csv
# EXAMPLE: python3.7 generateDataset.py /home/ubuntu/Documents/Shogi-DISS/src/ml/storage/tmp-2-6.csa.txt


