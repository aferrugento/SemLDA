semlda_dir=$(pwd)"/semLDA"
dir=$(pwd)
echo "Running preprocessing_s.py ..." 
python preprocessing_s.py test_data.txt

echo "Running wsd_semcor.py ..."
python wsd_semcor.py test_data

cd $semlda_dir
echo "Running semLDA ..."
make
./semlda est 0.5 15 settings.txt $dir"/test_data_wsd.txt" random $dir"/results_exp2/"
echo "Obtaining topics with synsets ..."
python topics.py $dir"/results_exp2/final.beta" $dir"/test_data_synsetVoc.txt" 10 > $dir"/test_data_topics.txt"

cd ..

echo "Creating topics with words ..."
python choice_best_word_new.py test_data