#include "semlda-estimate.h"

/*
 * perform inference on a document and update sufficient statistics
 *
 */

double doc_e_step(document* doc, double* gamma, double** phi, double** lambda,
                  lda_model* model, lda_suffstats* ss)
{
    double likelihood;
    int n, k, j;

    // posterior inference
    likelihood = lda_inference(doc, model, gamma, phi, lambda);

    // update sufficient statistics

    double gamma_sum = 0;
    for (k = 0; k < model->num_topics; k++)
    {
        gamma_sum += gamma[k];
        ss->alpha_suffstats += digamma(gamma[k]);
    }
    ss->alpha_suffstats -= model->num_topics * digamma(gamma_sum);

    for (n = 0; n < doc->length; n++)
    {
        for (k = 0; k < model->num_topics; k++)
        {
            for (j = 0; j < doc->synsets[n].length; j++)
            {
                // F: compute the number of times word n appears associated with topic k (KxN matrix);
                // these are soft counts! since phi is not zeros and ones (it's a probability of assigning topic k to word n);
                // notice how this corresponds to eq. 9 of Blei2003 (except for the outer sum over all documents)

                ss->class_word[k][doc->synsets[n].ids[j]] += doc->counts[n]*lambda[n][doc->synsets[n].ids[j]]*phi[n][k];
                
                // F: compute the number of times topic k appears associated with any word (K vector)
                
                ss->class_total[k] += doc->counts[n]*lambda[n][doc->synsets[n].ids[j]]*phi[n][k];

            }
            /*

            for (j = 0; j < synsets_per_word[n].length; j++)
            {
            // F: compute the number of times word n appears associated with topic k (KxN matrix);
            // these are soft counts! since phi is not zeros and ones (it's a probability of assigning topic k to word n);
            // notice how this corresponds to eq. 9 of Blei2003 (except for the outer sum over all documents)
                ss->class_word[k][synsets_per_word[n].ids[j]] += doc->counts[n]*lambda[n][synsets_per_word[n].ids[j]]*phi[n][k];
            // F: compute the number of times topic k appears associated with any word (K vector)
                ss->class_total[k] += doc->counts[n]*lambda[n][synsets_per_word[n].ids[j]]*phi[n][k];
            }
            //ss->class_word[k][doc->words[n]] += doc->counts[n]*phi[n][k];
            //ss->class_total[k] += doc->counts[n]*phi[n][k];*/
        }
    }

    ss->num_docs = ss->num_docs + 1;

    return(likelihood);
}


/*
 * writes the word assignments line for a document to a file
 *
 */

void write_word_assignment(FILE* f, document* doc, double** phi, lda_model* model)
{
    int n;

    fprintf(f, "%03d", doc->length);
    for (n = 0; n < doc->length; n++)
    {
        fprintf(f, " %04d:%02d", doc->words[n], argmax(phi[n], model->num_topics));
    }
    fprintf(f, "\n");
    fflush(f);
}

void write_synset_assignment(FILE* f, document* doc, double** lambda, lda_model* model)
{
    int n;

    fprintf(f, "%03d", doc->length);
    for (n = 0; n < doc->length; n++)
    {
        fprintf(f, " %04d:%02d", doc->words[n], argmax(lambda[n], model->num_synsets));
    }
    fprintf(f, "\n");
    fflush(f);
}


/*
 * saves the gamma parameters of the current dataset
 *
 */

void save_gamma(char* filename, double** gamma, int num_docs, int num_topics)
{
    FILE* fileptr;
    int d, k;
    fileptr = fopen(filename, "w");

    for (d = 0; d < num_docs; d++)
    {
    	fprintf(fileptr, "%5.10f", gamma[d][0]);
    	for (k = 1; k < num_topics; k++)
    	{
    	    fprintf(fileptr, " %5.10f", gamma[d][k]);
    	}
    	fprintf(fileptr, "\n");
    }
    fclose(fileptr);
}

void save_phi(char* filename, double** phi, int num_docs, int n, int num_topics)
{
    FILE* fileptr;
    int d, k;
    fileptr = fopen(filename, "w");
    for (d = 0; d < n; d++)
    {
        for (k = 0; k < num_topics; k++)
        {
            fprintf(fileptr, " %5.10f", phi[d][k]);
        }
        fprintf(fileptr, "\n");
    }
    fclose(fileptr);
}

void save_lambda(char* filename, double** lambda, int num_docs, int n, int num_synsets)
{
    FILE* fileptr;
    int d, k;
    fileptr = fopen(filename, "w");

    for (d = 0; d < n; d++)
    {
        for (k = 0; k < num_synsets; k++)
        {
            fprintf(fileptr, " %5.10f", lambda[d][k]);
        }
        fprintf(fileptr, "\n");
    }
    fclose(fileptr);
}

/*
 * run_em
 *
 */

void run_em(char* start, char* directory, corpus* corpus)
{
    //printf("Assim funciona\n");
    int d, n;
    lda_model *model = NULL;
    double **var_gamma, **phi, **lambda;

    // allocate variational parameters

    var_gamma = malloc(sizeof(double*)*(corpus->num_docs));
    for (d = 0; d < corpus->num_docs; d++)
	var_gamma[d] = malloc(sizeof(double) * NTOPICS);

    int max_length = max_corpus_length(corpus);
    phi = malloc(sizeof(double*)*max_length);
    for (n = 0; n < max_length; n++)
	   phi[n] = malloc(sizeof(double) * NTOPICS);

    //new variational parameter lambda (concept)   
    lambda = malloc(sizeof(double*)*max_length);
    for (n = 0; n < max_length; n++)
        lambda[n] = malloc(sizeof(double) * corpus->num_synsets);    

    // initialize model

    char filename[700], filename2[700];

    lda_suffstats* ss = NULL;
    if (strcmp(start, "seeded")==0)
    {
        model = new_lda_model(corpus->num_terms, NTOPICS, corpus->num_synsets);
        ss = new_lda_suffstats(model);
        corpus_initialize_ss(ss, model, corpus);
        lda_mle(model, ss, 0);
        model->alpha = INITIAL_ALPHA;
    }
    else if (strcmp(start, "random")==0)
    {
        model = new_lda_model(corpus->num_terms, NTOPICS, corpus->num_synsets);
        ss = new_lda_suffstats(model);
        random_initialize_ss(ss, model);
        lda_mle(model, ss, 0);
        model->alpha = INITIAL_ALPHA;
    }
    else
    {
        model = load_lda_model(start);
        ss = new_lda_suffstats(model);
    }

    sprintf(filename,"%s/000",directory);
    save_lda_model(model, filename);

    // run expectation maximization

    int i = 0;
    double likelihood, likelihood_old = 0, converged = 1;
    sprintf(filename, "%s/likelihood.dat", directory);
    FILE* likelihood_file = fopen(filename, "w");

    while (((converged < 0) || (converged > EM_CONVERGED) || (i <= 2)) && (i <= EM_MAX_ITER))
    {
        i++; printf("**** em iteration %d ****\n", i);
        likelihood = 0;
        zero_initialize_ss(ss, model);

        // e-step
        printf("e-step\n");
        for (d = 0; d < corpus->num_docs; d++)
        {

            if ((d % 1000) == 0) printf("document %d\n",d);
            likelihood += doc_e_step(&(corpus->docs[d]),
                                     var_gamma[d],
                                     phi,
                                     lambda,
                                     model,
                                     ss);
        }

        // m-step

        printf("m-step\n");
        lda_mle(model, ss, ESTIMATE_ALPHA);

        // check for convergence

        converged = (likelihood_old - likelihood) / (likelihood_old);
        if (converged < 0) VAR_MAX_ITER = VAR_MAX_ITER * 2;
        likelihood_old = likelihood;

        // output model and likelihood

        fprintf(likelihood_file, "%10.10f\t%5.5e\n", likelihood, converged);
        fflush(likelihood_file);
        if ((i % LAG) == 0)
        {
            sprintf(filename,"%s/%03d",directory, i);
            save_lda_model(model, filename);
            sprintf(filename,"%s/%03d.gamma",directory, i);
            save_gamma(filename, var_gamma, corpus->num_docs, model->num_topics);
            sprintf(filename,"%s/%03d.phi",directory, i);
            save_phi(filename, phi, corpus->num_docs, max_length, model->num_topics);
            //sprintf(filename,"%s/%03d.lambda",directory, i);
            //save_lambda(filename, lambda, corpus->num_docs, max_length, model->num_synsets);
        }
    }

    // output the final model

    sprintf(filename,"%s/final",directory);
    save_lda_model(model, filename);
    sprintf(filename,"%s/final.gamma",directory);
    save_gamma(filename, var_gamma, corpus->num_docs, model->num_topics);
    sprintf(filename,"%s/final.phi",directory);
    save_phi(filename, phi, corpus->num_docs, max_length, model->num_topics);
    //sprintf(filename,"%s/final.lambda",directory);
    //save_lambda(filename, lambda, corpus->num_docs, max_length, model->num_synsets);
    
    // output the word assignments (for visualization)

    sprintf(filename, "%s/word-assignments.dat", directory);
    FILE* w_asgn_file = fopen(filename, "w");

    sprintf(filename2, "%s/synset-assignments.dat", directory);
    FILE* s_asgn_file = fopen(filename2, "w");

    for (d = 0; d < corpus->num_docs; d++)
    {
        if ((d % 100) == 0) printf("final e step document %d\n",d);
        likelihood += lda_inference(&(corpus->docs[d]), model, var_gamma[d], phi, lambda);

        //necessario alterar? 
        write_word_assignment(w_asgn_file, &(corpus->docs[d]), phi, model);
        write_synset_assignment(s_asgn_file, &(corpus->docs[d]), lambda, model);
    }
    fclose(w_asgn_file);
    fclose(s_asgn_file);
    fclose(likelihood_file);
}


/*
 * read settings.
 *
 */

void read_settings(char* filename)
{
    FILE* fileptr;
    char alpha_action[100];
    fileptr = fopen(filename, "r");
    fscanf(fileptr, "var max iter %d\n", &VAR_MAX_ITER);
    fscanf(fileptr, "var convergence %f\n", &VAR_CONVERGED);
    fscanf(fileptr, "em max iter %d\n", &EM_MAX_ITER);
    fscanf(fileptr, "em convergence %f\n", &EM_CONVERGED);
    fscanf(fileptr, "alpha %s", alpha_action);
    if (strcmp(alpha_action, "fixed")==0)
    {
	ESTIMATE_ALPHA = 0;
    }
    else
    {
	ESTIMATE_ALPHA = 1;
    }
    fclose(fileptr);
}


/*
 * inference only
 *
 */

void infer(char* model_root, char* save, corpus* corpus)
{
    FILE* fileptr;
    char filename[700];
    int i, d, n;
    lda_model *model;
    double **var_gamma, likelihood, **phi, **lambda;
    document* doc;

    model = load_lda_model(model_root);
    var_gamma = malloc(sizeof(double*)*(corpus->num_docs));
    for (i = 0; i < corpus->num_docs; i++)
	var_gamma[i] = malloc(sizeof(double)*model->num_topics);
    sprintf(filename, "%s-lda-lhood.dat", save);
    fileptr = fopen(filename, "w");
    for (d = 0; d < corpus->num_docs; d++)
    {
    	if (((d % 100) == 0) && (d>0)) printf("document %d\n",d);

    	doc = &(corpus->docs[d]);
    	phi = (double**) malloc(sizeof(double*) * doc->length);
    	for (n = 0; n < doc->length; n++)
    	    phi[n] = (double*) malloc(sizeof(double) * model->num_topics);
        lambda = (double**) malloc(sizeof(double*) * doc->length);
        for (n = 0; n < doc->length; n++)
            lambda[n] = (double*) malloc(sizeof(double) * model->num_synsets);
    	likelihood = lda_inference(doc, model, var_gamma[d], phi, lambda);

    	fprintf(fileptr, "%5.5f\n", likelihood);
        free_lambda(lambda, doc->length);
    }
    fclose(fileptr);
    sprintf(filename, "%s-gamma.dat", save);
    save_gamma(filename, var_gamma, corpus->num_docs, model->num_topics);
}

void free_lambda(double** lambda, int doc)
{
    int i;

    for (i = 0; i < doc; i++)
    {
    free(lambda[i]);
    }
    free(lambda);
}

/*
 * update sufficient statistics
 *
 */



/*
 * main
 *
 */

int main(int argc, char* argv[])
{
    // (est / inf) alpha k settings data (random / seed/ model) (directory / out)

    corpus* corpus;

    long t1;
    (void) time(&t1);
    seedMT(t1);
    // seedMT(4357U);

    if (argc > 1)
    {
        
        if (strcmp(argv[1], "est")==0)
        {
            INITIAL_ALPHA = atof(argv[2]);
            NTOPICS = atoi(argv[3]);
            read_settings(argv[4]);

            corpus = read_data(argv[5]);
            
            //corpus = read_data(argv[5], argv[6]);
            make_directory(argv[7]);
            run_em(argv[6], argv[7], corpus);
        }
        if (strcmp(argv[1], "inf")==0)
        {
            read_settings(argv[2]);
            corpus = read_data(argv[4]);
            //corpus = read_data(argv[4], argv[5]);
            infer(argv[3], argv[5], corpus);
        }
    }
    else
    {
        printf("usage : lda est [initial alpha] [k] [settings] [data] [eta] [random/seeded/*] [directory]\n");
        printf("        lda inf [settings] [model] [data] [eta] [name]\n");
    }
    return(0);
}
