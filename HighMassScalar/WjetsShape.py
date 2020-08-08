from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os

##--GGF
class WjetsShape(PhysicsModel):
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
        POI_LIST=[]
        if self.simple:
            self.modelBuilder.doVar("w_min[0.9,0.5,1.5]")
            self.modelBuilder.doVar("w_max[1.1,0.5,1.5]")
            POI_LIST.append('w_min')
            POI_LIST.append('w_max')
            #
            self.modelBuilder.factory_( 'expr::r_slope0j(\"@1 - @0\", w_min,w_max)')
            self.modelBuilder.factory_( 'expr::r_nominal0j(\"@0\", w_min)')
            self.modelBuilder.factory_( 'expr::r_slope1j(\"@1 - @0\", w_min,w_max)')
            self.modelBuilder.factory_( 'expr::r_nominal1j(\"@0\", w_min)')
            self.modelBuilder.factory_( 'expr::r_slope2j(\"@1 - @0\", w_min,w_max)')
            self.modelBuilder.factory_( 'expr::r_nominal2j(\"@0\", w_min)')

        elif self.slope012j:
            self.modelBuilder.doVar("w_min0j[0.9,0.5,1.5]")
            self.modelBuilder.doVar("w_max0j[1.1,0.5,1.5]")
            self.modelBuilder.doVar("w_min1j[0.9,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.doVar("w_max1j[1.1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210



            POI_LIST.append('w_min0j')
            POI_LIST.append('w_max0j')
            POI_LIST.append('w_min1j')
            POI_LIST.append('w_max1j')
            self.modelBuilder.doVar("w_min2j[0.9,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.doVar("w_max2j[1.1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210
            POI_LIST.append('w_min2j')
            POI_LIST.append('w_max2j')



            self.modelBuilder.factory_( 'expr::r_slope0j(\"@1 - @0\", w_min0j,w_max0j)')
            self.modelBuilder.factory_( 'expr::r_nominal0j(\"@0\", w_min0j)')

            self.modelBuilder.factory_( 'expr::r_slope1j(\"@1 - @0\", w_min1j,w_max1j)')
            self.modelBuilder.factory_( 'expr::r_nominal1j(\"@0\", w_min1j)')
        
            self.modelBuilder.factory_( 'expr::r_slope2j(\"@1 - @0\", w_min2j,w_max2j)')
            self.modelBuilder.factory_( 'expr::r_nominal2j(\"@0\", w_min2j)')

        elif self.slope12j:
            self.modelBuilder.doVar("w_0j[1,0.5,1.5]")
            self.modelBuilder.doVar("w_min1j[0.9,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.doVar("w_max1j[1.1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210

            POI_LIST.append('w_0j')
            POI_LIST.append('w_min1j')
            POI_LIST.append('w_max1j')
            self.modelBuilder.doVar("w_min2j[0.9,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.doVar("w_max2j[1.1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210
            POI_LIST.append('w_min2j')
            POI_LIST.append('w_max2j')



            self.modelBuilder.factory_( 'expr::r_slope0j(\"0\",w_0j)')
            self.modelBuilder.factory_( 'expr::r_nominal0j(\"@0\",w_0j)')

            self.modelBuilder.factory_( 'expr::r_slope1j(\"@1 - @0\", w_min1j,w_max1j)')
            self.modelBuilder.factory_( 'expr::r_nominal1j(\"@0\", w_min1j)')
        
            self.modelBuilder.factory_( 'expr::r_slope2j(\"@1 - @0\", w_min2j,w_max2j)')
            self.modelBuilder.factory_( 'expr::r_nominal2j(\"@0\", w_min2j)')

        elif self.slope2j:
            self.modelBuilder.doVar("w_0j[1,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max]
            self.modelBuilder.doVar("w_1j[1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210 
            POI_LIST.append('w_0j')
            POI_LIST.append('w_1j')
            self.modelBuilder.doVar("w_min2j[0.9,0.5,1.5]") ##mu is what we want to return (in string) name[starting_value,min,max]
            self.modelBuilder.doVar("w_max2j[1.1,0.5,1.5]") ## slope shape's signal strength (250-mass)/210
            POI_LIST.append('w_min2j')
            POI_LIST.append('w_max2j')


            self.modelBuilder.factory_( 'expr::r_slope0j(\"0\",w_0j)')
            self.modelBuilder.factory_( 'expr::r_nominal0j(\"@0\",w_0j)')

            self.modelBuilder.factory_( 'expr::r_slope1j(\"0\",w_1j)')
            self.modelBuilder.factory_( 'expr::r_nominal1j(\"@0\",w_1j)')

            self.modelBuilder.factory_( 'expr::r_slope2j(\"@1 - @0\", w_min2j,w_max2j)')
            self.modelBuilder.factory_( 'expr::r_nominal2j(\"@0\", w_min2j)')

        

        ##totalw = r_nominal+r_slope*(250-mass)/210
        ##totalw 's max = r_nominal + r_slope
        ##totalw 's min = r_nominal
        POIS=",".join(POI_LIST)
        self.modelBuilder.doSet("POI",POIS)


    def setPhysicsOptions(self,physOptions):
        print "<setPhysicsOptions>"
        print str(physOptions)

        self.slope12j=False
        self.simple=False
        self.slope2j=False
        self.slope012j=False
        for po in physOptions:
            if 'slope12j'==po:
                self.slope12j=True
            elif 'simple'==po:
                self.simple=True
            elif 'slope2j'==po:
                self.slope2j=True
            elif 'slope012j'==po:
                self.slope012j=True
        
    def getYieldScale(self,bin,process): ##bin process in datacard
        print "<getYieldScale>"
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        #mass=int(self.mass)
        #if  "ggHWW" in process:
        print process
        if 'Wjets0j' in process:
            if 'slope' in process: #slope
                return 'r_slope0j'
            else: ##nominal
                return 'r_nominal0j'


        elif 'Wjets1j' in process:
            if 'slope' in process: #slope
                return 'r_slope1j'
            else: ##nominal
                return 'r_nominal1j'


        elif 'Wjets2j' in process:
            if 'slope' in process: #slope
                return 'r_slope2j'
            else: ##nominal
                return 'r_nominal2j'

        else: ## other bkg
            return 1

    
WjetsShapeFit=WjetsShape()
#for m in [115,120,125,126,130,135,140,145,150,155,160,165,170,175,180,190,200,210,230,250,270,300,350,400,450,500,550,600,650,700,750,800,900,1000,1500,2000,2500,3000,4000,5000]:
#    exec("XWW"+str(m)+"=HighMassScalar("+str(m)+")")
