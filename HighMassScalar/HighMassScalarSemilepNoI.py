from HiggsAnalysis.CombinedLimit.PhysicsModel import *
#from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
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
        self.modelBuilder.doVar("r[1,0,100]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doSet("POI","r")
        #self.modelBuilder.factory_('expr::ggH_s_func("@0-sqrt(@0)", mu)')
        #self.modelBuilder.factory_( 'expr::ggH_b_func("1-sqrt(@0)", mu)')
        #self.modelBuilder.factory_( 'expr::ggH_sbi_func("sqrt(@0)", mu)')
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:

        if  "ggHWWlnuqq_M" in process:
            this_mass=int(process.split("M")[1])
            if this_mass==mass:
                print "signal",process
                return "r"      
            elif this_mass=="125":
                print "[SMHIGGS]",process
                return 1
            else:
                print "[Other Mass points]",process
                return 0
        if "vbfHWWlnuqq_M" in process:
            this_mass=process.split("M")[1]
            
            if this_mass=="125":
                print "[SMHIGGS]",process
            else:
                print "vbf,->0",process
                
        else:
            print "[BKG]",process
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
        
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:            
        
        if "vbfHWWlnuqq_M"+str(mass)+"_M"+str(mass) in process:
            return 'mu'



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
        self.modelBuilder.factory_('expr::ggH_s_func("(@0-sqrt(@0))*(1.-@1)", mu,Fvbf)')
        self.modelBuilder.factory_('expr::vbfH_s_func("(@0-sqrt(@0))*(@1)", mu,Fvbf)')

        

        
 

    def getYieldScale(self,bin,process): ##bin process in datacard
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.options.mass)
        #if  "ggHWW" in process:            
        if  "ggHWWlnuqq_M"+str(mass) in process:            
            return 'ggH_s_func'
        if "vbfHWWlnuqq_M"+str(mass)+"_M"+str(mass) in process:
            return 'vbfH_s_func'
        return 1
        
        


GGFONLY=HighMassScalar_GGFOnly()##this should be use when text2workspace
VBFONLY=HighMassScalar_VBFOnly()
FLOATINGFVBF=HighMassScalar_FloatingFvbf()
