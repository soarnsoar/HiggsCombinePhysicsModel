from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class HighMassScalar(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        """Create POI out of signal strength """
        self.modelBuilder.doVar("mu[0,0,1000]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doSet("POI","mu")
        self.modelBuilder.factory_('expr::ggH_s_func("@0-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::ggH_b_func("1-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::ggH_sbi_func("sqrt(@0)", mu)')
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        if  "ggHWW" in process:
           
            
            if "_S_B_I" in process:
                return 'ggH_sbi_func'
            elif "_S" in process:
                return 'ggH_s_func'
            elif "_B" in process:
                return 'ggH_b_func'
            

        return 1
        
        
highmassscalar=HighMassScalar()
