/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
 * This code was autogenerated by RooClassFactory                            * 
 * This implements a generic beta decay function without any fermi corrections.
 *****************************************************************************/

#ifndef _MGMBetaDecayFunction_hh_
#define _MGMBetaDecayFunction_hh_

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "TMath.h"
 
class MGMBetaDecayFunction : public RooAbsPdf {
public:
  MGMBetaDecayFunction() {} 
  MGMBetaDecayFunction(const char *name, const char *title,
	      RooAbsReal& _energy,
	      RooAbsReal& _mass_of_electron,
	      RooAbsReal& _qvalue);
  MGMBetaDecayFunction(const MGMBetaDecayFunction& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new MGMBetaDecayFunction(*this,newname); }
  inline virtual ~MGMBetaDecayFunction() { }

protected:

  RooRealProxy fEnergy ;
  RooRealProxy fMassOfElectron ;
  RooRealProxy fQValue ;
  
  Double_t evaluate() const ;

private:

  ClassDef(MGMBetaDecayFunction,1) // Your description goes here...
};
 
#endif
