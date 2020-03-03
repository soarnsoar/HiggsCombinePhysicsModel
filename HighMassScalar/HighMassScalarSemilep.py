from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

##--GGF
class HighMassScalar_GGFOnly(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        """Create POI out of signal strength """
        self.modelBuilder.doVar("mu[1,0,100]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doSet("POI","mu")
        self.modelBuilder.factory_('expr::ggH_s_func("@0-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::ggH_b_func("1-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::ggH_sbi_func("sqrt(@0)", mu)')
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:
        print bin,process
        #print "check whether:","ggHWWlnuqq_M"+str(mass)
        #if  "ggHWWlnuqq_M"+str(mass) in process:            
        if  "ggHWWlnuqq_M" in process:            
            if "_S_B_I" in process:
                print 'gghww s b i'
                #return 0
                return 'ggH_sbi_func'
            elif "_S" in process:
                print 'gghww s'
                return 'ggH_s_func'
            elif "ggWW_MELA" in process:
                print 'ggww bkg'
                return 'ggH_b_func'
                #return 1
        if "VBFHToWWToLNuQQ" in process:
            #print 'vbf = 0'
            return 0

        return 1

##--VBF
class HighMassScalar_VBFOnly(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        """Create POI out of signal strength """
        self.modelBuilder.doVar("mu[0,0,1000]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doSet("POI","mu")
        self.modelBuilder.factory_('expr::vbfH_s_func("@0-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::vbfH_b_func("1-sqrt(@0)", mu)')
        self.modelBuilder.factory_( 'expr::vbfH_sbi_func("sqrt(@0)", mu)')
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:            
        if  "ggHWWlnuqq_M" in process:
            return 0
        if "VBFHToWWToLNuQQ_M"+str(mass) in process:
            if "_S_B_I" in process:
                return 'vbfH_sbi_func'
            elif "_S" in process:
                return 'vbfH_s_func'
            elif "qqWW_MELA" in process:
                return 'vbfH_b_func'



        return 1



##--Floating f_vbf
class HighMassScalar_FloatingFvbf(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)

    def doParametersOfInterest(self):
        """Create POI out of signal strength """
        ''' ref : physicsmodel -> rvf
        self.modelBuilder.out.var("MH").setRange(float(self.mHRange[0]),float(self.mHRange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
        '''

        self.modelBuilder.doVar("mu[0,0,1000]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doVar("Fvbf[0,0,1]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doSet("POI","mu,Fvbf")
        self.modelBuilder.doVar("")
        self.modelBuilder.factory_('expr::ggH_s_func("(@0-sqrt(@0))*(1.-@1)", mu,Fvbf)')
        self.modelBuilder.factory_( 'expr::ggH_b_func("(1-sqrt(@0))*(1.-@1)", mu,Fvbf)')
        self.modelBuilder.factory_( 'expr::ggH_sbi_func("sqrt(@0)*(1.-@1)", mu,Fvbf)')

        self.modelBuilder.factory_('expr::vbfH_s_func("(@0-sqrt(@0))*(@1)", mu,Fvbf)')
        self.modelBuilder.factory_( 'expr::vbfH_b_func("(1-sqrt(@0))*(@1)", mu,Fvbf)')
        self.modelBuilder.factory_( 'expr::vbfH_sbi_func("sqrt(@0)*(@1)", mu,Fvbf)')


 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:            
        if  "ggHWWlnuqq_M"+str(mass) in process:            
            if "_S_B_I" in process:
                return 'ggH_sbi_func'
            elif "_S" in process:
                return 'ggH_s_func'
            elif "ggWW_MELA" in process:
                return 'ggH_b_func'
        if "VBFHToWWToLNuQQ"+str(mass) in process:
            if "_S_B_I" in process:
                return 'vbfH_sbi_func'
            elif "_S" in process:
                return 'vbfH_s_func'
            elif "qqWW_MELA" in process:
                return 'vbfH_b_func'

        return 1
        
        


GGFONLY=HighMassScalar_GGFOnly()
VBFONLY=HighMassScalar_VBFOnly()
FLOATINGFVBF=HighMassScalar_FloatingFvbf()
