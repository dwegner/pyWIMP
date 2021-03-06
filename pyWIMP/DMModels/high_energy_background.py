import ROOT
from base_model import BaseModel
import gamma_line_model 
import background_model 
import math

def get_sigma(energy_in_eV):
    noise = 70.4843
    energy_par = 6.49228e-2
    return math.sqrt(noise*noise + 2.96*2.96*energy_par*energy_in_eV)
class FittingModel(BaseModel):
    def __init__(self, \
                 basevars,
                 use_rel = False,
                 erfc_on = False,
                 use_ratio = False):
        BaseModel.__init__(self, basevars)
        self.use_ratio = use_ratio
        self.initialize(basevars)

    def initialize(self, basevars):
        mean_list = [("Ge", 10.367, 0.10, 0.1, 0.04, 0), 
                     ("Ga", 9.659, 0.10, 0.1, 0.04, 0), 
                     ("Zn", 8.979, 0.1, 0.1, 0.04, 0), 
                     ("As", 11.103, 0.1, 0.1, 0.04, 0), 
                     ("Ge-Low", 1.299, 0.0, 0.1, 0.0, 0), 
                     ("ZN-Low", 1.10, 0.0, 0.0, 0.0, 0) ]
                     #("Unknown", 0.9, 0.05, 0.1, 0.04, 0), 
        
        self.gamma_list = []
        max = basevars.get_energy().getMax()
        min = basevars.get_energy().getMin()
        print min, max
        for name,mean,mean_error,sigma, sigma_error, atime in mean_list:
            if mean > max or mean < min: continue
            print mean
            agamma = gamma_line_model.GammaLineFactory.generate(mean, 
                mean_error, get_sigma(mean*1e3)*1e-3, 
                sigma_error, atime, basevars,name)
            self.gamma_list.append((agamma, agamma.get_model()))
          
        self.saved_pdf = [] # Hack to keep this from dying
        self.pdf_list = ROOT.RooArgList()
        self.coefficienct_list = ROOT.RooArgList()
        for _,gamma in self.gamma_list:
            new_var = ROOT.RooRealVar("%s_ampl" % gamma.GetName(), 
                                      "%s_ampl" % gamma.GetName(), 
                                      1e-15, 10000)
            self.pdf_list.add(gamma)
            self.coefficienct_list.add(new_var)
            self.saved_pdf.append((gamma, new_var))

        tag = ""
        self.exp_constant_one = ROOT.RooRealVar("expo_const_one%s" % tag,
                                            "expo_const_one%s" % tag,
                                            #1./3, 0, 500)
                                            -3., -10, -0.8)
        #self.exp_constant_one.removeMax()
        self.exp_constant_one.setError(0.5)
        self.exp_constant_time = ROOT.RooRealVar("expo_const_time_%s" % tag,
                                            "expo_const_time_%s" % tag,
                                            -0.2, -1, 0.5)

        self.exp_coef = ROOT.RooRealVar("exp_coef_%s" % tag,
                                        "exp_coef_%s" % tag,
                                        1e-15, 20000)
        self.flat_coef = ROOT.RooRealVar("flat_coef_%s" % tag,
                                         "flat_coef_%s" % tag,
                                         1e-15, 10000)
        # Flat pdf
        self.time_pdf = ROOT.RooPolynomial("time_pdf_exp_%s" % tag, 
                                           "time_pdf_exp_%s" % tag, 
                                           basevars.get_time())
        self.energy_pdf_flat = ROOT.RooPolynomial("energy_pdf_flat_%s" % tag, 
                                           "energy_pdf_flat_%s" % tag, 
                                           basevars.get_energy())
        self.energy_exp_pdf = ROOT.RooExponential("energy_pdf_exp", 
                                           "energy_pdf_exp", 
                                           basevars.get_energy(),
                                           self.exp_constant_one)
        self.pdf_list.add(self.energy_pdf_flat)
        self.coefficienct_list.add(self.flat_coef)

        if basevars.get_energy().getMin() < 1.5:
            self.pdf_list.add(self.energy_exp_pdf)
            self.coefficienct_list.add(self.exp_coef)



    def get_model(self):
        return self.final_pdf
    def get_list_components(self):
        return (self.pdf_list, self.coefficienct_list)


class HighEnergyBackgroundModel(FittingModel):
    def initialize(self, basevars):
        mean_list = [("Ge-Low",   1.299, 0.2, 0.1, 1, 0),
                     ("ZN-Low",   1.100, 0.2, 0.1, 1, 0),
                     ("Unknown1", 2.350, 0.2, 0.1, 1, 0), 
                     ("Unknown2", 3.000, 0.2, 0.1, 1, 0),
                     ("Unknown3", 3.600, 0.2, 0.1, 1, 0),
                     ("49V",      4.970, 0.2, 0.1, 1, 0),
                     ("51Cr",     5.460, 0.2, 0.1, 1, 0),
                     ("54Mn",     5.990, 0.2, 0.1, 1, 0),
                     ("55Fe",     6.540, 0.2, 0.1, 1, 0),
                     ("Co",       7.110, 0.2, 0.1, 1, 0),
                     ("56Ni",     7.710, 0.2, 0.1, 1, 0),
                     #("Unknown4", 8.000, 0.2, 0.1, 0, 0),
                     ("Zn",       8.979, 0.2, 0.1, 1, 0),
                     ("Ga",       9.659, 0.2, 0.1, 1, 0),
                     ("Ge",      10.367, 0.2, 0.1, 1, 0),
                     ("As",      11.103, 0.2, 0.1, 1, 0),   ]
        
        self.gamma_list = []
        max = basevars.get_energy().getMax()
        min = basevars.get_energy().getMin()
        for name,mean,mean_error,sigma, sigma_error, atime in mean_list:
            if mean > max or mean < min: continue
            agamma = gamma_line_model.GammaLineFactory.generate(mean, mean_error, get_sigma(mean*1e3)*1e-3, 
                sigma_error*get_sigma(mean*1e3)*4e-4, 
                atime, basevars,name)
            #print name
            self.gamma_list.append((agamma, agamma.get_model()))
        
        #print self.gamma_list
        self.expm = background_model.FlatWithExponentialModel(basevars)
        self.exp_pdf = self.expm.get_model()
        self.final_pdf = self.exp_pdf 
        self.added_pdf = self.final_pdf
        self.saved_pdf = [] # Hack to keep this from dying
        ratio  = 0.331511
        self.zn_ge_relative_amplitude = ROOT.RooRealVar(
                                             "l_ratio",
                                             "l_ratio",
                                             ratio/(1 + ratio))
               
        for _,gamma in self.gamma_list:
            print gamma.GetName()
            new_var = ROOT.RooRealVar("%s_ampl" % gamma.GetName(), 
                                      "%s_ampl" % gamma.GetName(), 
                                      1e-15, 10000)
            self.saved_pdf.append((gamma, new_var))
        self.pdf_list = ROOT.RooArgList()
        self.coefficienct_list = ROOT.RooArgList()
        zn = self.saved_pdf[1][0]
        ge = self.saved_pdf[0][0]
        if self.use_ratio:
            ratio_pdf = ROOT.RooAddPdf("Ge+Zn", "Ge+Zn", zn, ge, 
                                        self.zn_ge_relative_amplitude)
            new_amplitude = ROOT.RooRealVar("lline_amp", "lline_amp",
                                                 1e-15, 10000) 
            self.saved_pdf.append((ratio_pdf, new_amplitude))
            self.pdf_list.add(ratio_pdf)
            self.coefficienct_list.add(new_amplitude)
        else:
            #self.pdf_list.add(zn)
            #self.coefficienct_list.add(self.saved_pdf[1][1])
            #self.pdf_list.add(ge)
            #self.coefficienct_list.add(self.saved_pdf[0][1])
            for index in range(len(self.gamma_list)):
                self.pdf_list.add(self.saved_pdf[index][0])
                self.coefficienct_list.add(self.saved_pdf[index][1])


        #self.pdf_list.Print()
        tag = ""
        self.exp_constant_one = ROOT.RooRealVar("expo_const_one%s" % tag,
                                            "expo_const_one%s" % tag,
                                            #1./3, 0, 500)
                                            -1., -100, 0)
        #self.exp_constant_one.removeMax()
        self.exp_constant_one.setError(0.5)
        self.exp_constant_time = ROOT.RooRealVar("expo_const_time_%s" % tag,
                                            "expo_const_time_%s" % tag,
                                            -0.2, -1, 0.5)

        self.exp_coef = ROOT.RooRealVar("exp_coef_%s" % tag,
                                        "exp_coef_%s" % tag,
                                        1., 1e-15, 20000)
        self.flat_coef = ROOT.RooRealVar("flat_coef_%s" % tag,
                                         "flat_coef_%s" % tag,
                                         1., 1e-15, 10000)
        self.flat_coef_cut = ROOT.RooRealVar("flat_coef_cut_%s" % tag,
                                         "flat_coef_cut_%s" % tag,
                                         1., 1e-15, 10000)
        # Flat pdf
        self.time_pdf = ROOT.RooPolynomial("time_pdf_exp_%s" % tag, 
                                           "time_pdf_exp_%s" % tag, 
                                           basevars.get_time())
        self.energy_pdf_flat = ROOT.RooPolynomial("energy_pdf_flat_%s" % tag, 
                                           "energy_pdf_flat_%s" % tag, 
                                           basevars.get_energy())
        self.energy_pdf_flat_cut = ROOT.RooGenericPdf("energy_pdf_flat_cut_%s" % tag,
                                           "energy_pdf_flat_cut_%s" % tag,
                                           "1-1/(1+exp(-8*(ee_energy1-9)))",
                                           ROOT.RooArgList(basevars.get_energy()))
        self.energy_exp_pdf = ROOT.RooExponential("energy_pdf_exp", 
                                           "energy_pdf_exp", 
                                           basevars.get_energy(),
                                           self.exp_constant_one)
        self.pdf_list.add(self.energy_pdf_flat)
        self.coefficienct_list.add(self.flat_coef)
        self.pdf_list.add(self.energy_pdf_flat_cut)
        self.coefficienct_list.add(self.flat_coef_cut)
        self.pdf_list.add(self.energy_exp_pdf)
        self.coefficienct_list.add(self.exp_coef)


    def get_list_components(self):
        return (self.pdf_list, self.coefficienct_list)

class TestModel(HighEnergyBackgroundModel):
    def initialize(self, basevars):
       
        self.pdf_list = ROOT.RooArgList()
        self.coefficienct_list = ROOT.RooArgList()

        tag = ""
        self.exp_constant_one = ROOT.RooRealVar("expo_const_one%s" % tag,
                                            "expo_const_one%s" % tag,
                                            #1./3, 0, 500)
                                            -3, -100, -0.5)
        #self.exp_constant_one.removeMax()
        self.exp_constant_one.setError(0.5)

        self.exp_coef = ROOT.RooRealVar("exp_coef_%s" % tag,
                                        "exp_coef_%s" % tag,
                                        1e-15, 2000)
        self.flat_coef = ROOT.RooRealVar("flat_coef_%s" % tag,
                                         "flat_coef_%s" % tag,
                                         1e-15, 1000)
        # Flat pdf
        self.energy_pdf_flat = ROOT.RooPolynomial("energy_pdf_flat_%s" % tag, 
                                           "energy_pdf_flat_%s" % tag, 
                                           basevars.get_energy())
        self.energy_exp_pdf = ROOT.RooExponential("energy_pdf_exp", 
                                           "energy_pdf_exp", 
                                           basevars.get_energy(),
                                           self.exp_constant_one)
        self.pdf_list.add(self.energy_pdf_flat)
        self.coefficienct_list.add(self.flat_coef)
        self.pdf_list.add(self.energy_exp_pdf)
        self.coefficienct_list.add(self.exp_coef)


