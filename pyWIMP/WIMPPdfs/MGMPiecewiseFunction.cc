 /***************************************************************************** 
  * Project: RooFit                                                           * 
  *                                                                           * 
  * This code was autogenerated by RooClassFactory                            * 
  *****************************************************************************/ 

 // Your description goes here... 

#include "MGMPiecewiseFunction.hh" 
#include "RooMsgService.h" 
#include "MGMPiecewiseRegions.hh"

 ClassImp(MGMPiecewiseFunction) 

 MGMPiecewiseFunction::MGMPiecewiseFunction(const char *name, 
                        const char *title, 
                        RooAbsReal& _var) :
   RooAbsPdf(name,title), 
   fVariable("variable","variable",this,_var),
   fRegions(0)
 { 
 } 


 MGMPiecewiseFunction::MGMPiecewiseFunction(const MGMPiecewiseFunction& other, const char* name) :  
   RooAbsPdf(other,name), 
   fVariable("variable",this,other.fVariable),
   fRegions(other.fRegions)
 { 
 } 

 Double_t MGMPiecewiseFunction::evaluate() const 
 { 
   if (!fRegions) return 1; 
   if ( fRegions->IsInAcceptedRegion( fVariable ) ) return 1; 
   // Otherwise it is in a region which we have inserted, return 0
   //return 0;
   return 1e-16;
 } 

Int_t MGMPiecewiseFunction::getAnalyticalIntegral(RooArgSet& allVars, RooArgSet& analVars, const char* /*rangeName*/) const
{
   if (matchArgs(allVars, analVars, fVariable)) return 1;
   return 0;
} 

Double_t MGMPiecewiseFunction::analyticalIntegral(Int_t code, const char* rangeName) const
{
   assert(code==1);
   if (!fRegions) return 1; 
   Double_t max = fVariable.max(rangeName);
   Double_t min = fVariable.min(rangeName);

   Double_t sum = 0.0;
   fRegions->InitializeRegionIterator(min, max);
   const MGMPiecewiseRegions::MGMRegion* reg;
   while ( (reg = fRegions->GetNextRegion()) ) sum += reg->fEnd - reg->fBegin;
   return sum; 
}

