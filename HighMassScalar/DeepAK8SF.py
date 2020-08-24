from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os


class DeepAK8SF(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)
        #self.mass=mass


    def doParametersOfInterest(self):
        print "<doParametersOfInterest>"
        """Create POI out of signal strength """
        #####---POIs -> slope/intercept  -> slopeshape's signal strength & nominal shape's signal strength.
        ####Contraint ->  totalweight=[0,2]
        self.modelBuilder.doVar('SF_eff[0.9,0.5,1.5]')
        #self.modelBuilder.doVar('r_match_pass[0.9,0.5,1.5]') ##r_match_pass = r_match_total * SF
        self.modelBuilder.doVar('r_match_total[0.9,0.5,1.5]')
        self.modelBuilder.doVar('r_notW_pass[0.9,0.5,1.5]')
        self.modelBuilder.doVar('r_notW_total[0.9,0.5,1.5]')



        self.modelBuilder.factory_( 'expr::r_match_pass(\"@0*@1\", SF_eff,r_match_total)')

        POI_LIST=['SF_eff']

        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print "<setPhysicsOptions>"
        print str(physOptions)
        
    def getYieldScale(self,bin,process): ##bin process in datacard
        print "<getYieldScale>"

        print process,bin

        if 'DATA' in process:
            return 1
        elif '_NotMatched': ##bkg
            if 'Pass' in bin: ## bkg pass the WP
                return 'r_notW_pass'
            else: ## bkg all
                return 'r_notW_total'
        else:
            if 'Pass' in bin : ## matched to W and pass WP
                return 'r_matched_pass'
            else:
                return 'r_matched_total'
    
EvalDeepAK8SF=DeepAK8SF()
