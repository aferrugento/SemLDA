semlda_dir=$(pwd)"/semLDA"
dir=$(pwd)
echo "Running preprocessing_s.py ..." 
python preprocessing_s.py test_data_pt.txt

echo "Running wsd.py ..."
python newformat_pt.py test_data_pt

cd $semlda_dir
echo "Running semLDA ..."
make
./semlda est 0.5 15 settings.txt $dir"/test_data_pt_newformat.txt" random $dir"/results_exp5/"
echo "Obtaining topics with synsets ..."
python topics.py $dir"/results_exp5/final.beta" $dir"/test_data_pt_synsetVoc.txt" 10 > $dir"/test_data_pt_topics.txt"

cd ..

echo "Creating topics with words ..."
python choice_best_word_pt.py test_data_pt