#ifndef LDA_H
#define LDA_H

typedef struct
{
    int* ids;
    double* log_prob_eta;
    int length;
}synset;

/*
typedef struct
{
    int* words;
    double* log_prob_eta;
    int length;
    int ID;
}synset;

typedef struct
{
    int* ids;
    double* log_prob_s;
    int length; 
}words;
*/

typedef struct
{
    synset* synsets;
    int* words;
    int* counts;
    int length;
    int total;
} document;


typedef struct
{
    //words* synsets_per_word;
    //synset* eta;
    document* docs;
    int num_terms;
    int num_docs;
    int num_synsets;
} corpus;


typedef struct
{
    double alpha;
    double** log_prob_w;
    int num_topics;
    int num_terms;
    int num_synsets;
} lda_model;


typedef struct
{
    double** class_word;
    double* class_total;
    double alpha_suffstats;
    int num_docs;
} lda_suffstats;

#endif
