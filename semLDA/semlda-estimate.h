#ifndef LDA_ESTIMATE_H
#define LDA_ESTIMATE_H

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <float.h>
#include <string.h>
#include <time.h>

#include "semlda.h"
#include "semlda-data.h"
#include "semlda-inference.h"
#include "semlda-model.h"
#include "semlda-alpha.h"
#include "utils.h"
#include "cokus.h"

int LAG = 5;

float EM_CONVERGED;
int EM_MAX_ITER;
int ESTIMATE_ALPHA;
double INITIAL_ALPHA;
int NTOPICS;

double doc_e_step(document* doc,
                  double* gamma,
                  double** phi,
                  double** lambda,
                  lda_model* model,
                  lda_suffstats* ss);

void save_gamma(char* filename,
                double** gamma,
                int num_docs,
                int num_topics);

void save_phi(char* filename,
                double** phi,
                int num_docs,
                int n,
                int num_topics);

void save_lambda(char* filename,
                double** lambda,
                int num_docs,
                int n,
                int num_synsets);

void run_em(char* start,
            char* directory,
            corpus* corpus);

void read_settings(char* filename);

void infer(char* model_root,
           char* save,
           corpus* corpus);

void free_lambda(double** lambda, int doc);

#endif


