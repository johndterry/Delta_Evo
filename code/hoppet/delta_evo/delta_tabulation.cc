#define _USE_MATH_DEFINES

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

double ymax = 12, dy = 0.01, asQ0 = 0.35, Q0 = 10, Q = 250, dlnlnQ = 0.01;
int    nloop = 1, order = -6;

// constants given default values that hoppet uses
double nf = 5, ca = 3, cf = 4.0/3.0, tr = 1.0/2.0, tf = 5.0/2.0;

// definition of the initial condition function
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf);

// for saving filenames
string to_string(double num);

//----------------------------------------------------------------------
int main () {
  
  // initialise
  hoppetStartExtended(ymax, dy, Q0, Q, dlnlnQ, nloop, order, factscheme_MSbar);
  
  // evolve the initial condition
  hoppetEvolve(asQ0, Q0, nloop, 1.0, heralhc_init, Q0);

  // output the results and save txt file
  double pdf[13];
  double xvals[12]={1e-5,1e-4,1e-3,1e-2,0.1,0.3,0.5,0.7,0.9,0.95,0.99,0.999};
 
  printf("           Evaluating PDFs at Q = %8.3f GeV\n",Q);
  ofstream outfile;
  string test = to_string(Q0);
  string filename = "../../data/test-" + to_string(Q0) + "-" + to_string(Q) + "-" + to_string(dy) + "-" + to_string(dlnlnQ) + ".txt";
  outfile.open(filename.c_str());

  // default hoppet output
  if (mode == 1) {
    printf("    x      u-ubar      d-dbar    2(ubr+dbr)    c+cbar       gluon\n");
  
    for (int ix = 0; ix < 12; ix++) {
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

  for (int ix = 0; ix < 12; ix++) {
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

double Pqq(const double & x, const double & a)
{
  return cf * ((1.0 + pow(x,2))/(1.0-x) + 3.0/2.0 * delta(x,a));
}

double Pgq(const double & x, const double & a)
{
  return cf * (1 + pow(1-x,2))/x;
}

double Pqg(const double & x, const double & a)
{
  return tr * (pow(x,2)  + pow(1-x,2)); 
}

double Pgg(const double & x, const double & a)
{
  return 2.0 * ca * (x/(1-x) + (1-x)/x + x*(1-x)) + (11.0*ca- 4.0*nf*tr)/6.0 * delta(x,a);
}

// gluon jet function
double gluon_jet(const double & x, const double & Q, const double & omega_j, const double & a, const double & R)
{
  if (x == 1) {
    return gluon_jet(0.999, Q, omega_j, a, R); }
  
  double as2pi;
  double L = log(pow(Q,2)/pow(omega_j * tan(R/2), 2));
  
  if (Q == Q0) {
    as2pi = asQ0/(2*M_PI); }
  else {
    as2pi = hoppetAlphaS(Q)/(2*M_PI); }

  return as2pi * (L * (Pgg(x,a) + 2*nf*Pqg(x,a))) - as2pi * (4 * ca * pow(1-x+pow(x,2),2)/x * log(1-x)/(1-x) - delta(x,a) * (ca * (67.0/9.0 - 2.0*pow(M_PI,2)/3.0) - tf*nf*(23.0/9.0)) + 4 * nf * (Pqg(x,a)*log(1-x) + tf*x*(1-x)));
}

// quark jet function
double quark_jet(const double & x, const double & Q, const double & omega_j, const double & a, const double & R)
{
  if (x == 1) {
    return gluon_jet(0.999, Q, omega_j, a, R); }
    
  double as2pi;
  double L = log(pow(Q,2)/pow(omega_j * tan(R/2), 2));
  
  if (Q == Q0) {
    as2pi = asQ0/(2*M_PI); }
  else {
    as2pi = hoppetAlphaS(Q)/(2*M_PI); }
  
  return as2pi * (L * (Pqq(x,a) + Pgq(x,a))) - as2pi * (cf * (2.0*(1+pow(x,2)) * log(1-x)/(1-x) + (1-x)) - delta(x,a) * cf * (13.0/2.0 - 2.0/3.0 * pow(M_PI,2)) + Pgq(x,a)*2*log(1-x) + cf*x);
}

// the initial condition
void heralhc_init(const double & x,
                   const double & Q,
                   double * pdf) {
  // double uv, dv;
  // double ubar, dbar;
  // double N_g=1.7, N_ls=0.387975;
  // double N_uv=5.107200, N_dv=3.064320;
  // double N_db=N_ls/2;

  // uv = N_uv * pow(x,0.8) * pow((1-x),3);
  // dv = N_dv * pow(x,0.8) * pow((1-x),4);
  // dbar = N_db * pow(x,-0.1) * pow(1-x,6);
  // ubar = dbar * (1-x);

  double R = 0.5;
  double omega_j = 1;
  double a = 0.01;
  
  // g = 0, d = 1, u = 2, s = 3, c = 4, b = 5, t = 6
  pdf[ 0+6] = x*gluon_jet(x, Q, omega_j, a, R);
  pdf[-3+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 3+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 2+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-2+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 1+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-1+6] = x*quark_jet(x, Q, omega_j, a, R);

  pdf[ 4+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 5+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 6+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-4+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-5+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-6+6] = x*quark_jet(x, Q, omega_j, a, R);
}
