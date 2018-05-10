#include "../src/hoppet_v1.h"
#include <fstream>
#include <iostream>
#include <cmath>
#include <cstdio>

using namespace std;

// set to 1 if using hoppet default, 2 to see all individual PDFs
int mode = 2;

// definition of the initial condition function
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf);


//----------------------------------------------------------------------
int main () {

  double dy    = 0.5;
  int    nloop = 1;

  // initialise with NNLO, VFN
  hoppetStart(dy, nloop);
  // hoppetSetPoleMassVFN(1.414213563, 4.5, 175.0);
  
  // evolve the initial condition
  double asQ0 = 0.35, Q0=10.0;
  hoppetEvolve(asQ0, Q0, nloop, 1.0, heralhc_init, Q0);
  // alternatively preprepare an evolution and then use its cached version.
  //hoppetPreEvolve(asQ0, Q0, nloop, 1.0, Q0);
  //hoppetCachedEvolve(heralhc_init);

  // output the results and save in pdf.txt
  double pdf[13];
  double xvals[9]={1e-5,1e-4,1e-3,1e-2,0.1,0.3,0.5,0.7,0.9};
  double Q = 100;
 
  printf("           Evaluating PDFs at Q = %8.3f GeV\n",Q);
  ofstream outfile;
  outfile.open("../../Python/pdf.txt");

  // default hoppet output
  if (mode == 1) {
    printf("    x      u-ubar      d-dbar    2(ubr+dbr)    c+cbar       gluon\n");
  
    for (int ix = 0; ix < 9; ix++) {
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

  for (int ix = 0; ix < 9; ix++) {
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

// delta function
double delta(const double z, const double a)
{
  if ((z > 1.0 - a) and (z <= 1.0)) {
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
  double a = 0.000001;

  uv = N_uv * pow(x,0.8) * pow((1-x),3);
  dv = N_dv * pow(x,0.8) * pow((1-x),4);
  dbar = N_db * pow(x,-0.1) * pow(1-x,6);
  ubar = dbar * (1-x);

  // g = 0, d = 1, u = 2, s = 3, c = 4, b = 5, t = 6
  pdf[ 0+6] = 0;  
  pdf[-3+6] = 0;
  pdf[ 3+6] = 0;
  pdf[ 2+6] = x*delta(1-x,a);
  pdf[-2+6] = 0;
  pdf[ 1+6] = 0;
  pdf[-1+6] = 0;

  pdf[ 4+6] = 0;
  pdf[ 5+6] = 0;
  pdf[ 6+6] = 0;
  pdf[-4+6] = 0;
  pdf[-5+6] = 0;
  pdf[-6+6] = 0;
}
