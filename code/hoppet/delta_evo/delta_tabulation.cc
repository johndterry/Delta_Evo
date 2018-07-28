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

double ymax = 12, dy = 0.01, asQ0 = 0.1, Q0 = 12.5, Qmax = 250, dlnlnQ = 0.01;
int    nloop = 1, order = 6;

// constants given default values that hoppet uses
double nf = 5, ca = 3, cf = 4.0/3.0, tr = 1.0/2.0, tf = 1.0/2.0;

// definition of the initial condition function
void  heralhc_init(const double & x,
                   const double & Q,
                   double * pdf);

void  heralhc_init0(const double & x,
                   const double & Q,
		   double * pdf);

// for saving filenames
string to_string(double num);

//----------------------------------------------------------------------
int main () {
  double Q = Qmax;
  
  // initialise
  hoppetStartExtended(ymax, dy, Q0, Q, dlnlnQ, nloop, order, factscheme_MSbar);
  
  // evolve the initial condition
  hoppetEvolve(asQ0, Q0, nloop, 1.0, heralhc_init, Q0);

  // output the results and save txt file
  double pdf[13];
  double xvals[65]={1e-5,1e-4,1e-3,1e-2,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.17,0.18,0.19,0.2,0.21,0.22,0.23,0.24,0.25,0.26,0.27,0.28,0.29,0.3,0.31,0.32,0.33,0.34,0.35,0.36,0.37,0.38,0.39,0.4,0.42,0.44,0.46,0.48,0.5,0.55,0.6,0.7,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99,0.999,0.9999};
 
  printf("           Evaluating PDFs at Q = %8.3f GeV\n",Q);
  ofstream outfile;
  string test = to_string(Q0);
  string filename = "../../data/qNLO-" + to_string(Q0) + "-" + to_string(Q) + "-" + to_string(dy) + "-" + to_string(dlnlnQ) + ".txt";
  outfile.open(filename.c_str());

  // default hoppet output
  if (mode == 1) {
    printf("    x      u-ubar      d-dbar    2(ubr+dbr)    c+cbar       gluon\n");
  
    for (int ix = 0; ix < 65; ix++) {
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

  for (int ix = 0; ix < 65; ix++) {
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
double delta(const double x, const double a)
{
  if ((x > 1.0) or (x < 1.0 - a)) {
    return 0; }
  else {
    return 2/(a*a) * (x - 1.0 + a); }
}

double Pqq(const double & x, const double & a)
{
  return cf * ((1.0 + pow(x,2))/((1.0-x) - delta(x,a)*0.5) + 3.0/2.0 * delta(x,a));
}

double Pgq(const double & x, const double & a)
{
  return cf * (1.0 + pow(1-x,2))/x;
}

double Pqg(const double & x, const double & a)
{
  return tr * (pow(x,2)  + pow(1-x,2)); 
}

double Pgg(const double & x, const double & a)
{
  return 2.0 * ca * (x/((1.0-x) - delta(x,a)*0.5) + (1.0-x)/x + x*(1.0-x)) + (11.0*ca- 4.0*nf*tr)/6.0 * delta(x,a);
}

// gluon jet function
double gluon_jet(const double & x, const double & Q, const double & omega_j, const double & a, const double & R)
{
  //cout << x << endl;
 
  double as2pi;
  double L = log(pow(Q,2)/pow(omega_j * tan(R/2), 2));
 
  if (Q == Q0) {
    as2pi = asQ0/(2*M_PI); }
  else {
    as2pi = hoppetAlphaS(Q)/(2*M_PI); }
  
  if (x == 1) {
    return -6e4; }
    //return as2pi * L * (Pgg(x,a) + 2*nf*Pqg(x,a)) - as2pi * (0 - delta(x,a) * (ca * (67.0/9.0 - 2.0*pow(M_PI,2)/3.0) - tf*nf*(23.0/9.0)) + 4 * nf * (Pqg(x,a)*log(1-x+1e-10) + tf*x*(1-x))); }
  
  return as2pi * L * (Pgg(x,a) + 2*nf*Pqg(x,a)) - as2pi * (4 * ca * pow(1-x+pow(x,2),2)/x * (log(1-x)/(1-x) - delta(x,a) * (-0.5)*pow(log(1e-10),2)) - delta(x,a) * (ca * (67.0/9.0 - 2.0*pow(M_PI,2)/3.0) - tf*nf*(23.0/9.0)) + 4 * nf * (Pqg(x,a)*log(1-x) + tf*x*(1-x)));
}

// quark jet function
double quark_jet(const double & x, const double & Q, const double & omega_j, const double & a, const double & R)
{
  double as2pi;
  double L = log(pow(Q,2)/pow(omega_j * tan(R/2), 2));

  if (Q == Q0) {
    as2pi = asQ0/(2*M_PI); }
  else {
    as2pi = hoppetAlphaS(Q)/(2*M_PI); }

   if (x == 1) {
     return 0; }
     //return as2pi * L * (Pqq(x,a) + Pgq(x,a)) - as2pi * (cf * (2.0*(1+pow(x,2)) * (1-x)) - delta(x,a) * cf * (13.0/2.0 - 2.0/3.0 * pow(M_PI,2)) + Pgq(x,a)*2*log(1-x+1e-10) + cf*x); }

  return as2pi * L * (Pqq(x,a) + Pgq(x,a)) - as2pi * (cf * (2.0*(1+pow(x,2)) * (log(1-x)/(1-x) - delta(x,a) * (-0.5)*pow(log(1e-10),2)) + (1-x)) - delta(x,a) * cf * (13.0/2.0 - 2.0/3.0 * pow(M_PI,2)) + Pgq(x,a)*2*log(1-x) + cf*x);
}

// the initial condition
void heralhc_init(const double & x,
                   const double & Q,
                   double * pdf) {
  
  double R = Q0/Qmax;
  double omega_j = Q/tan(R/2);
  double a = 1e-10;
  
  // g = 0, d = 1, u = 2, s = 3, c = 4, b = 5, t = 6
  pdf[ 0+6] = 0*x*gluon_jet(x, Q, omega_j, a, R);
  pdf[-3+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 3+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 2+6] = x*quark_jet(x, Q, omega_j, a, R);
  pdf[-2+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 1+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[-1+6] = 0*x*quark_jet(x, Q, omega_j, a, R);

  pdf[ 4+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 5+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[ 6+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[-4+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[-5+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
  pdf[-6+6] = 0*x*quark_jet(x, Q, omega_j, a, R);
}

void heralhc_init0(const double & x,
                   const double & Q,
                   double * pdf) {

  double a = 1e-2;
  
  // g = 0, d = 1, u = 2, s = 3, c = 4, b = 5, t = 6
  pdf[ 0+6] = x*delta(x,a);
  pdf[-3+6] = x*delta(x,a);
  pdf[ 3+6] = x*delta(x,a);
  pdf[ 2+6] = x*delta(x,a);
  pdf[-2+6] = x*delta(x,a);
  pdf[ 1+6] = x*delta(x,a);
  pdf[-1+6] = x*delta(x,a);

  pdf[ 4+6] = x*delta(x,a);
  pdf[ 5+6] = x*delta(x,a);
  pdf[ 6+6] = x*delta(x,a);
  pdf[-4+6] = x*delta(x,a);
  pdf[-5+6] = x*delta(x,a);
  pdf[-6+6] = x*delta(x,a);
}
