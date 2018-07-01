#include "../src/hoppet_v1.h"
#include <fstream>
#include <iostream>
#include <cmath>
#include <cstdio>
#include <string>
#include <sstream>

using namespace std;

// set to 1 if using hoppet default, 2 to see all individual PDFs
int mode = 2;

// definition of the initial condition function
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf);

// for saving filenames
string to_string(double num);

//----------------------------------------------------------------------
int main () {
  
  double ymax = 12, dy = 0.01, asQ0 = 0.35, Q0 = 10, Q = 1000, dlnlnQ = 0.01;
  int    nloop = 1, order = -6; 


  // initialise
  hoppetStartExtended(ymax, dy, Q0, Q, dlnlnQ, nloop, order, factscheme_MSbar);
  
  // evolve the initial condition
  hoppetEvolve(asQ0, Q0, nloop, 1.0, heralhc_init, Q0);

  // output the results and save txt file
  double pdf[13];
  double xvals[13]={1e-5,1e-4,1e-3,1e-2,0.1,0.3,0.5,0.7,0.9,0.95,0.99,0.999,1};
 
  printf("           Evaluating PDFs at Q = %8.3f GeV\n",Q);
  ofstream outfile;
  string test = to_string(Q0);
  string filename = "../../data/bbar-" + to_string(Q0) + "-" + to_string(Q) + "-" + to_string(dy) + "-" + to_string(dlnlnQ) + ".txt";
  outfile.open(filename.c_str());

  // default hoppet output
  if (mode == 1) {
    printf("    x      u-ubar      d-dbar    2(ubr+dbr)    c+cbar       gluon\n");
  
    for (int ix = 0; ix < 13; ix++) {
      hoppetEval(xvals[ix], Q, pdf);

      printf("%7.1E %11.4E %11.4E %11.4E %11.4E %11.4E\n",xvals[ix],
	     pdf[6+2]-pdf[6-2], 
	     pdf[6+1]-pdf[6-1], 
	     2*(pdf[6-1]+pdf[6-2]),
	     (pdf[6-4]+pdf[6+4]),
	     pdf[6+0]);

        outfile << xvals[ix] << "  "
	      << pdf[6+2]-pdf[6-2] << "  "
	      << pdf[6+1]-pdf[6-1] << "  "
	      << 2*(pdf[6-1]+pdf[6-2]) << "  "
	      << pdf[6-4]+pdf[6+4] << "  "
	      << pdf[6+0] << endl;
    
    }
    
    outfile.close();
    return 0;
  }
  
  // individual PDF output
  printf("    x         t        tbar          b          bbar         c         cbar          s         sbar          u        ubar          d         dbar         gluon\n");

  for (int ix = 0; ix < 13; ix++) {
    hoppetEval(xvals[ix], Q, pdf);
    printf("%7.1E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E %11.4E\n",xvals[ix],
           pdf[6+6], pdf[6-6], 
           pdf[6+5], pdf[6-5], 
           pdf[6+4], pdf[6-4],
           pdf[6+3], pdf[6-3],
	   pdf[6+2], pdf[6-2],
	   pdf[6+1], pdf[6-1],
	   pdf[6+0]);

    outfile << xvals[ix] << "  "
	    << pdf[6+6] << "  " << pdf[6-6] << "  "
   	    << pdf[6+5] << "  " << pdf[6-5] << "  "
    	    << pdf[6+4] << "  " << pdf[6-4] << "  "
    	    << pdf[6+3] << "  " << pdf[6-3] << "  "
    	    << pdf[6+2] << "  " << pdf[6-2] << "  "
    	    << pdf[6+1] << "  " << pdf[6-1] << "  "
    	    << pdf[6+0] << endl;
    
  }
  
  outfile.close();
  }

// converting doubles to strings
string to_string(double num)
{
  ostringstream str;
  str << num;
  return str.str();
}

// delta function
double delta(const double z, const double a)
{
  if ((z > 1.0) or (z < 1.0 - a)) {
    return 0; }
  else {
    return 2/(a*a) * (z - 1.0 + a); }
}

// the initial condition
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf) {
  double uv, dv;
  double ubar, dbar;
  double N_g=1.7, N_ls=0.387975;
  double N_uv=5.107200, N_dv=3.064320;
  double N_db=N_ls/2;
  double a = 0.01;

  uv = N_uv * pow(x,0.8) * pow((1-x),3);
  dv = N_dv * pow(x,0.8) * pow((1-x),4);
  dbar = N_db * pow(x,-0.1) * pow(1-x,6);
  ubar = dbar * (1-x);

  // g = 0, d = 1, u = 2, s = 3, c = 4, b = 5, t = 6
  pdf[ 0+6] = 0;  
  pdf[-3+6] = 0;
  pdf[ 3+6] = 0;
  pdf[ 2+6] = 0;
  pdf[-2+6] = 0;
  pdf[ 1+6] = 0;
  pdf[-1+6] = 0;

  pdf[ 4+6] = 0;
  pdf[ 5+6] = 0;
  pdf[ 6+6] = 0;
  pdf[-4+6] = 0;
  pdf[-5+6] = x*delta(x,a);
  pdf[-6+6] = 0;
}
