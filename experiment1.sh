lda_dir=$(pwd)"/semLDA"
dir=$(pwd)
echo "Running preprocessing_s.py ..." 
python preprocessing_s.py test_data.txt

echo "Running preprocessing_semanticLDA.py ..."
python preprocessing_semanticLDA.py test_data

echo "Creating input for SemLDA ..."
python new_format.py test_data

python synset_vocab.py test_data

cd $lda_dir
echo "Running semLDA ..."
make
./semlda est 0.5 15 settings.txt $dir"/test_data_newformat.txt" random $dir"/results_exp1/"
echo "Obtaining topics with synsets ..."
python topics.py $dir"/results_exp1/final.beta" $dir"/test_data_synsetvocab.txt" 10 > $dir"/test_data_topics.txt"

cd ..

echo "Creating topics with words ..."
python choice_best_word.py test_data