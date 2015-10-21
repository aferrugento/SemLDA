#include "semlda-model.h"

/*
 * compute MLE lda model from sufficient statistics
 *
 */

void lda_mle(lda_model* model, lda_suffstats* ss, int estimate_alpha)
{
    int k; int w;

    for (k = 0; k < model->num_topics; k++)
    {
        //ir ate ao numero de synsets
        for (w = 0; w < model->num_synsets; w++)
        {
            if (ss->class_word[k][w] > 0)
            {
                model->log_prob_w[k][w] =
                    log(ss->class_word[k][w]) -
                    log(ss->class_total[k]);
            }
            else
                model->log_prob_w[k][w] = -100;
        }
    }
    if (estimate_alpha == 1)
    {
        model->alpha = opt_alpha(ss->alpha_suffstats,
                                 ss->num_docs,
                                 model->num_topics);

        printf("new alpha = %5.5f\n", model->alpha);
    }
}

/*
 * allocate sufficient statistics
 *
 */

lda_suffstats* new_lda_suffstats(lda_model* model)
{
    int num_topics = model->num_topics;
    int num_terms = model->num_terms;
    int num_synsets = model->num_synsets;
    int i,j;

    lda_suffstats* ss = malloc(sizeof(lda_suffstats));
    ss->class_total = malloc(sizeof(double)*num_topics);
    ss->class_word = malloc(sizeof(double*)*num_topics);
    for (i = 0; i < num_topics; i++)
    {
	ss->class_total[i] = 0;
	ss->class_word[i] = malloc(sizeof(double)*num_synsets);
	for (j = 0; j < num_synsets; j++)
	{
	    ss->class_word[i][j] = 0;
	}
    }
    return(ss);
}


/*
 * various intializations for the sufficient statistics
 *
 */

void zero_initialize_ss(lda_suffstats* ss, lda_model* model)
{
    int k, w;
    for (k = 0; k < model->num_topics; k++)
    {
        ss->class_total[k] = 0;
        for (w = 0; w < model->num_synsets; w++)
        {
            ss->class_word[k][w] = 0;
        }
    }
    ss->num_docs = 0;
    ss->alpha_suffstats = 0;
}


void random_initialize_ss(lda_suffstats* ss, lda_model* model)
{
    int num_topics = model->num_topics;
    int num_synsets = model->num_synsets;
    int k, n;
    for (k = 0; k < num_topics; k++)
    {
        for (n = 0; n < num_synsets; n++)
        {
            ss->class_word[k][n] += 1.0/num_synsets + myrand();
            ss->class_total[k] += ss->class_word[k][n];
        }
    }
}


void corpus_initialize_ss(lda_suffstats* ss, lda_model* model, corpus* c)
{
    int num_topics = model->num_topics;
    int i, k, d, n;
    document* doc;

    for (k = 0; k < num_topics; k++)
    {
        for (i = 0; i < NUM_INIT; i++)
        {
            d = floor(myrand() * c->num_docs);
            printf("initialized with document %d\n", d);
            doc = &(c->docs[d]);
            for (n = 0; n < doc->length; n++)
            {
                ss->class_word[k][doc->words[n]] += doc->counts[n];
            }
        }
        for (n = 0; n < model->num_synsets; n++)
        {
            ss->class_word[k][n] += 1.0;
            ss->class_total[k] = ss->class_total[k] + ss->class_word[k][n];
        }
    }
}

/*
 * allocate new lda model
 *
 */

lda_model* new_lda_model(int num_terms, int num_topics, int num_synsets)
{
    int i,j;
    lda_model* model;

    model = malloc(sizeof(lda_model));
    model->num_topics = num_topics;
    model->num_terms = num_terms;
    model->num_synsets = num_synsets;
    model->alpha = 1.0;
    model->log_prob_w = malloc(sizeof(double*)*num_topics);
    for (i = 0; i < num_topics; i++)
    {
	model->log_prob_w[i] = malloc(sizeof(double)*num_synsets);
	for (j = 0; j < num_synsets; j++)
	    model->log_prob_w[i][j] = 0;
    }
    return(model);
}


/*
 * deallocate new lda model
 *
 */

void free_lda_model(lda_model* model)
{
    int i;

    for (i = 0; i < model->num_topics; i++)
    {
	free(model->log_prob_w[i]);
    }
    free(model->log_prob_w);
}


/*
 * save an lda model
 *
 */

void save_lda_model(lda_model* model, char* model_root)
{
    char filename[700];
    FILE* fileptr;
    int i, j;

    sprintf(filename, "%s.beta", model_root);
    fileptr = fopen(filename, "w");
    for (i = 0; i < model->num_topics; i++)
    {
    	for (j = 0; j < model->num_synsets; j++)
    	{
    	    fprintf(fileptr, " %5.10f", model->log_prob_w[i][j]);
    	}
	   fprintf(fileptr, "\n");
    }
    fclose(fileptr);

    sprintf(filename, "%s.other", model_root);
    fileptr = fopen(filename, "w");
    fprintf(fileptr, "num_topics %d\n", model->num_topics);
    fprintf(fileptr, "num_terms %d\n", model->num_terms);
    fprintf(fileptr, "num_synsets %d\n", model->num_synsets);
    fprintf(fileptr, "alpha %5.10f\n", model->alpha);
    fclose(fileptr);
}


lda_model* load_lda_model(char* model_root)
{
    char filename[700];
    FILE* fileptr;
    int i, j, num_terms, num_topics, num_synsets;
    float x, alpha;

    sprintf(filename, "%s.other", model_root);
    printf("loading %s\n", filename);
    fileptr = fopen(filename, "r");
    fscanf(fileptr, "num_topics %d\n", &num_topics);
    fscanf(fileptr, "num_terms %d\n", &num_terms);
    fscanf(fileptr, "num_synsets %d\n", &num_synsets);
    fscanf(fileptr, "alpha %f\n", &alpha);
    fclose(fileptr);

    lda_model* model = new_lda_model(num_terms, num_topics, num_synsets);
    model->alpha = alpha;

    sprintf(filename, "%s.beta", model_root);
    printf("loading %s\n", filename);
    fileptr = fopen(filename, "r");
    for (i = 0; i < num_topics; i++)
    {
        for (j = 0; j < num_synsets; j++)
        {
            fscanf(fileptr, "%f", &x);
            model->log_prob_w[i][j] = x;
        }
    }
    fclose(fileptr);
    return(model);
}
