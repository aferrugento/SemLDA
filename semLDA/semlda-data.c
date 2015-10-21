#include "semlda-data.h"
#include "utils.h"

corpus* read_data(char* data_filename)
{
    FILE *fileptr, *fileptr2;
    int length, synset_size, synset_id, count, word, synset_word, n, n_synset, nd, nw, ne, s;
    double synset_prob;
    corpus* c;

    printf("reading data from %s\n", data_filename);

    c = malloc(sizeof(corpus));
    c->docs = 0;
    //c->eta = 0;
    c->num_terms = 0;
    c->num_docs = 0;
    c->num_synsets = 0;

    fileptr = fopen(data_filename, "r");
    nd = 0; nw = 0; ne = 0;
    /*
    while ((fscanf(fileptr, "%10d", &length) != EOF))
    {        
        c->docs = (document*) realloc(c->docs, sizeof(document)*(nd+1));
        c->docs[nd].length = length;
        c->docs[nd].total = 0;
        c->docs[nd].words = malloc(sizeof(int)*length);
        c->docs[nd].counts = malloc(sizeof(int)*length);
        for (n = 0; n < length; n++)
        {
            fscanf(fileptr, "%10d:%10d", &word, &count);
            word = word - OFFSET;
            c->docs[nd].words[n] = word;
            c->docs[nd].counts[n] = count;
            c->docs[nd].total += count;
            if (word >= nw) { nw = word + 1; }
        }
        nd++;
    }
    fclose(fileptr);
*/
    fscanf(fileptr, "%d", &ne);

    while ((fscanf(fileptr, "%10d", &length) != EOF))
    {        
        c->docs = (document*) realloc(c->docs, sizeof(document)*(nd+1));
        c->docs[nd].length = length;
        c->docs[nd].total = 0;
        c->docs[nd].words = malloc(sizeof(int)*length);
        c->docs[nd].counts = malloc(sizeof(int)*length);
        c->docs[nd].synsets = (synset*) malloc(sizeof(synset)*length);
        //printf("%d\n", length);
        for (n = 0; n < length; n++)
        {
            fscanf(fileptr, "%10d:%10d:%10d[", &word, &count, &synset_size);
            //printf("%d:%d:%d[", word, count, synset_size);
            word = word - OFFSET;
            c->docs[nd].words[n] = word;
            c->docs[nd].counts[n] = count;
            c->docs[nd].total += count;

            c->docs[nd].synsets[n].length = synset_size;
            c->docs[nd].synsets[n].ids = malloc(sizeof(int)*synset_size);
            c->docs[nd].synsets[n].log_prob_eta = malloc(sizeof(double)*synset_size);
            
            for (s = 0; s < synset_size; s++)
            {
                if (s == synset_size - 1)
                    fscanf(fileptr, "%10d:%lf]",  &synset_id, &synset_prob);
                else
                    fscanf(fileptr, "%10d:%lf",  &synset_id, &synset_prob);
                //printf("%d:%lf ", synset_id, synset_prob);
                c->docs[nd].synsets[n].ids[s] = synset_id;
                c->docs[nd].synsets[n].log_prob_eta[s] = log(synset_prob);
            }
            //printf("] ");
            if (word >= nw) { nw = word + 1; }
        }
        //return 0;
        
        nd++;
    }
    fclose(fileptr);
    /*for (s = 0; s < nd; s++){
        printf("DOC %d\n", s+1);
        printf("%d\n", c->docs[nd].length);
        for (n = 0;  n < c->docs[nd].length; n++){
            printf("%d:%d:%d[ ", c->docs[s].words[n], c->docs[s].counts[n], c->docs[s].synsets[n].length);
        }
        printf("\n");
    } */  
    printf("len %d\n", nd);
    //return 0;
printf("lolisss\n");
/*
    fileptr2 = fopen(eta_filename, "r");
    printf("reading eta from %s\n", eta_filename);
    c->synsets_per_word = (words*) malloc(sizeof(words)*nw);
    while ((fscanf(fileptr2, "%10d %10d", &synset_id, &synset_size) != EOF))
    {        
        /*
        c->eta = (synset*) realloc(c->eta, sizeof(synset)*(ne+1));
        c->eta[ne].length = synset_size;
        c->eta[ne].ID = synset_id;
        c->eta[ne].words = malloc(sizeof(double)*synset_size);
        c->eta[ne].log_prob_eta = malloc(sizeof(double)*synset_size);

        for (n_synset = 0; n_synset < synset_size; n_synset++)
        {
            fscanf(fileptr2, "%10d:%lf", &synset_word, &synset_prob);
            synset_word = synset_word - OFFSET;
            c->eta[ne].words[n_synset] = synset_word;
            c->eta[ne].log_prob_eta[n_synset] = log(synset_prob);
            //c->eta[ne].total += count;
            //if (word >= nw) { nw = word + 1; }
        }
        ne++;

        
        
        for (n_synset = 0; n_synset < synset_size; n_synset++)
        {
            fscanf(fileptr2, "%10d:%lf", &synset_word, &synset_prob);
            c->synsets_per_word[synset_word].length += 1;
            c->synsets_per_word[synset_word].log_prob_s = (double*) realloc(c->synsets_per_word[synset_word].log_prob_s, sizeof(double) * c->synsets_per_word[synset_word].length);
            c->synsets_per_word[synset_word].ids = (int*) realloc(c->synsets_per_word[synset_word].ids, sizeof(int) * c->synsets_per_word[synset_word].length);

            c->synsets_per_word[synset_word].ids[c->synsets_per_word[synset_word].length-1] = ne;  
            c->synsets_per_word[synset_word].log_prob_s[c->synsets_per_word[synset_word].length-1] = log(synset_prob);
        }
        
        //ne++;

        

    }

    fclose(fileptr2);*/
    /*for (n_synset = 0; n_synset < nw; n_synset++){
        printf("%d ", n_synset);
        for(n = 0; n < c->synsets[n_synset].length; n++){
            printf("%d:%lf ", c->synsets[n_synset].ids[n], c->synsets[n_synset].log_prob_s[n]);
        }
        printf("\n");
    }*/
    c->num_synsets = ne;
    c->num_docs = nd;
    c->num_terms = nw;
    printf("number of docs    : %d\n", nd);
    printf("number of terms   : %d\n", nw);
    printf("number of synsets   : %d\n", ne);
    return(c);
}

int max_corpus_length(corpus* c)
{
    int n, max = 0;
    for (n = 0; n < c->num_docs; n++)
    if (c->docs[n].length > max) max = c->docs[n].length;
    return(max);
}
