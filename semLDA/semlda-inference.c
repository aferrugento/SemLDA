#include "semlda-inference.h"

/*
 * variational inference
 *
 */

double lda_inference(document* doc, lda_model* model, double* var_gamma, double** phi, double** lambda)
{
    double converged = 1;
    double phisum = 0, lambdasum = 0, likelihood = 0;
    double likelihood_old = 0, oldphi[model->num_topics];
    int k, s, j, n, m, var_iter;
    double digamma_gam[model->num_topics];

    // compute posterior dirichlet
    // F: initilization of the standard LDA algorithm

    for (k = 0; k < model->num_topics; k++)
    {
		// F: initilize gamma_k = alpha + N/K (Step 2 of Figure 6 of Blei2003)
        var_gamma[k] = model->alpha + (doc->total/((double) model->num_topics));
        digamma_gam[k] = digamma(var_gamma[k]);
        for (n = 0; n < doc->length; n++)
            // F: initilize phi_nk = 1/K (Step 1 of Figure 6 of Blei2003)
            phi[n][k] = 1.0/model->num_topics;
    }

    for (n = 0; n < doc->length; n++)
    {
        for (j = 0; j < model->num_synsets; j++)
            // initilize lambda_nj = 1/S 
            lambda[n][j] = 1.0/model->num_synsets;
    }
    
    var_iter = 0;

    while ((converged > VAR_CONVERGED) && ((var_iter < VAR_MAX_ITER) || (VAR_MAX_ITER == -1)))
    {
    	var_iter++;
    	for (n = 0; n < doc->length; n++) // STEP 4 FIGURE 6 OF LDA 
    	{
                phisum = 0;
                lambdasum = 0;
                for (k = 0; k < model->num_topics; k++) // STEP 5 FIGURE 6 OF LDA
                {
                    oldphi[k] = phi[n][k];
                    phi[n][k] = 0;

                    for (s = 0; s < doc->synsets[n].length; s++)
                    {
                        phi[n][k] += lambda[n][doc->synsets[n].ids[s]] * model->log_prob_w[k][doc->synsets[n].ids[s]];
                    }

                    phi[n][k] += digamma_gam[k];

                    // F: standard phi update from Figure 6, Step 6 of Blei2003, but IN LOG SPACE! hence the product becomes a sum...
                    //phi[n][k] = digamma_gam[k] + model->log_prob_w[k][doc->words[n]];

                    // F: this computes the normalization constant of phi; for example the digamma(sum_j phi_j) comes from here...
                    if (k > 0)
                        phisum = log_sum(phisum, phi[n][k]);
                    else
                        phisum = phi[n][k]; // note, phi is in log space
                    //printf("word %d topic %d %lf\n", n, k, phi[n][k]);
                }

                // F: normalize the phis and update the gammas (Step 8 from Figure 6 of Blei2003)
                for (k = 0; k < model->num_topics; k++)
                {
                    // F: normalize and move back from log space, by exponentiating...
                    phi[n][k] = exp(phi[n][k] - phisum);

                    // F: this update is in a sequencial form; to verify that it is correct notice the following:
                    // gamma^(t+1) = alpha + sum_n phi_n^(t+1) = alpha + sum_n phi_n^(t+1) + sum_n phi_n^t - sum_n phi_n^t = gamma^t + sum(phi_n^(t+1) - phi_n^t)
                    var_gamma[k] = var_gamma[k] + doc->counts[n]*(phi[n][k] - oldphi[k]);
                    // !!! a lot of extra digamma's here because of how we're computing it
                    // !!! but its more automatically updated too.
                    digamma_gam[k] = digamma(var_gamma[k]);
                }

                for (s = 0; s < doc->synsets[n].length; s++)
                {
                    lambda[n][doc->synsets[n].ids[s]] = 0;
                    for (k = 0; k < model->num_topics; k++)
                    {
                        lambda[n][doc->synsets[n].ids[s]] += phi[n][k] * model->log_prob_w[k][doc->synsets[n].ids[s]];                   
                    }

                    lambda[n][doc->synsets[n].ids[s]] += doc->synsets[n].log_prob_eta[s];
                    /*
                    int found = 0;
                    for (m = 0; m < synsets_per_word[n].length; m++)
                    {
                        if (synsets_per_word[n].ids[m] == s)
                        {
                            lambda[n][s] += synsets_per_word[n].log_prob_s[m];
                            found = 1;
                            break;
                        }
                    }

                    if(!found)
                        lambda[n][s] += -100;

                    int found = 0;
                    for (m = 0; m < eta[s].length; m++)
                    {
                        if (n == eta[s].words[m])
                        {
                            lambda[n][s] += eta[s].log_prob_eta[m];
                            found = 1;
                            break;
                        }
                    }
                    
                    if(!found)
                        lambda[n][s] += -100;
                    */
                    if (s > 0)
                        lambdasum = log_sum(lambdasum, lambda[n][doc->synsets[n].ids[s]]);
                    else
                        lambdasum = lambda[n][doc->synsets[n].ids[s]]; // note, lambda is in log space
                    if (isnan(lambda[n][s]))
                        printf("LOL %lf %lf\n", lambda[n][s], lambdasum);

                }
                for (s = 0; s < doc->synsets[n].length; s++)
                {
                    lambda[n][doc->synsets[n].ids[s]] = exp(lambda[n][doc->synsets[n].ids[s]] - lambdasum);

                }
                
            }

            likelihood = compute_likelihood(doc, model, phi, var_gamma, lambda);
            assert(!isnan(likelihood));
            converged = (likelihood_old - likelihood) / likelihood_old;
            likelihood_old = likelihood;

            // printf("[LDA INF] %8.5f %1.3e\n", likelihood, converged);
    }
    return(likelihood);
}


/*
 * compute likelihood bound
 *
 */

double
compute_likelihood(document* doc, lda_model* model, double** phi, double* var_gamma, double** lambda)
{
    double likelihood = 0, digsum = 0, var_gamma_sum = 0, dig[model->num_topics];
    int k, n, s, m;

    for (k = 0; k < model->num_topics; k++)
    {
    	dig[k] = digamma(var_gamma[k]);
    	var_gamma_sum += var_gamma[k];
    }
    digsum = digamma(var_gamma_sum);

    likelihood = lgamma(model->alpha * model -> num_topics)	- model -> num_topics * lgamma(model->alpha) - (lgamma(var_gamma_sum));

    for (k = 0; k < model->num_topics; k++)
    {
	   likelihood += (model->alpha - 1)*(dig[k] - digsum) + lgamma(var_gamma[k]) - (var_gamma[k] - 1)*(dig[k] - digsum);

    	for (n = 0; n < doc->length; n++)
    	{
            if (phi[n][k] > 0)
            {
                likelihood += doc->counts[n]* (phi[n][k]*((dig[k] - digsum) - log(phi[n][k])));

                for (s = 0; s < doc->synsets[n].length; s++)
                {                
                    likelihood += doc->counts[n] * (phi[n][k] * lambda[n][doc->synsets[n].ids[s]] * model->log_prob_w[k][doc->synsets[n].ids[s]]);

                }
            }
        }    
    }
    for (n = 0; n < doc->length; n++)
    {
        for (s = 0; s < doc->synsets[n].length; s++)
        {
            likelihood += doc->counts[n] * (lambda[n][doc->synsets[n].ids[s]] * (doc->synsets[n].log_prob_eta[s] - log(lambda[n][doc->synsets[n].ids[s]])));
            /*int found = 0;
            for (m = 0; m < eta[s].length; m++)
            {
                if (n == eta[s].words[m])
                {
                    likelihood += doc->counts[n] * lambda[n][s] * eta[s].log_prob_eta[m];
                    found = 1;
                    break;
                }
            
            }
            if(!found)
                likelihood += doc->counts[n] * lambda[n][s] * -100;
            */
            /*
            int found = 0;
            for (m = 0; m < synsets_per_word[n].length; m++)
            {
                if (synsets_per_word[n].ids[m] == s)
                {
                    likelihood += doc->counts[n] * lambda[n][s] * synsets_per_word[n].log_prob_s[m];
                    found = 1;
                    break;
                }
            }

            if(!found)
                likelihood += doc->counts[n] * lambda[n][s] * -100;


            //printf("LOL %lf\n", likelihood);
            */
        }    
    }

    return(likelihood);
}
