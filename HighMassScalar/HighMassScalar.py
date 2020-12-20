from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT, os

##--GGF
class HighMassScalar(PhysicsModel):
    "assume the SM coupling but let the Higgs mass to float"
    def __init__(self,mass):
        #SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        #self.floatMass = False
        PhysicsModel.__init__(self)
        self.mass=mass

    def SetMass(self):
        ##
	HWW_XSEC={
            'GGF': {
                130: 11.546299999999999, 
                900: 0.1389804, 
                135: 14.343280000000002, 
                5000: 7.675e-08, 650: 0.762528, 
                140: 16.86576, 270: 7.753439999999999, 
                400: 5.481216, 145: 19.024289999999997, 
                150: 20.839519999999997, 
                155: 22.937921050954753, 
                160: 24.35391, 
                165: 24.25846849501213, 
                550: 1.642368, 
                170: 23.29497, 
                300: 6.787693, 
                175: 22.080719570671516, 
                180: 20.3112, 
                3000: 2.150228e-05, 
                700: 0.5300889999999999, 
                800: 0.264969, 
                450: 3.696966, 
                4000: 1.177038e-06, 
                2500: 0.00010916920000000001, 
                200: 13.39068, 
                2000: 0.000665576, 
                210: 12.004649999999998, 
                600: 1.11333, 
                1500: 0.005472582, 
                350: 6.9085, 
                230: 10.081819999999999, 
                1000: 0.0757062, 
                750: 0.3723636, 
                115: 4.046138999999999, 
                500: 2.455058, 
                120: 6.1841800000000005, 
                250: 8.748479999999999, 
                125: 8.731839999999998, 
                126: 9.467639794273635, 
                190: 15.53472,
            }, 
            'VBF': {
                130: 1.113035, 
                175: 2.600401651328187,
                900: 0.07127199999999999, 
                5000: 8.080239999999999e-06, 
                650: 0.15335159999999998, 
                140: 1.718064, 
                270: 1.03356, 
                400: 0.436608, 
                145: 1.986942, 
                150: 2.2284319999999997, 
                155: 2.50766007373293, 
                160: 2.7180299999999997, 
                165: 2.760077102560154, 
                550: 0.21703500000000003, 
                170: 2.698326, 
                300: 0.8678959999999999, 
                180: 2.4291600000000004, 
                3000: 0.0005067342, 
                700: 0.130585, 
                190: 1.91052, 
                800: 0.095698, 
                450: 0.32967480000000005, 
                4000: 6.45314e-05, 
                2500: 0.00144904, 
                200: 1.686398, 
                2000: 0.004329928, 
                210: 1.5414979999999998, 
                600: 0.18170700000000004, 
                1500: 0.01404832, 
                350: 0.6514884000000001, 
                230: 1.331988, 
                1000: 0.05361448, 
                750: 0.111453, 
                115: 0.3535905, 
                500: 0.2635752, 
                120: 0.5597820000000001, 
                250: 1.169969, 
                124: 0.7445578136647063, 
                125: 0.8163999999999999, 
                126: 0.8907425606102282,
                190:1.91052,
                135:1.422568,
            }
        }
        HWWLNUQQ_XSEC={
            'GGF': {
                130: 3.3810919445520002, 
                900: 0.04069749711081601, 
                135: 4.200128912851201, 
                5000: 2.247462882e-08, 
                650:0.22329034221312002,
                140: 4.938784309670401, 
                270: 2.2704323918976, 
                400: 1.6050592193126403, 
                145: 5.5708645773816, 
                150: 6.1024166356608, 
                155: 6.716889400946872, 
                160: 7.131532085546401, 
                165: 7.103584041264648, 
                550: 0.4809330447667201, 
                170: 6.821443701928801, 
                300: 1.9876336250047202, 175: 6.465875914388953,180: 5.947709197248001, 3000: 6.296492010211201e-06, 700: 0.15522545298456, 190: 4.5490171442688005, 800: 0.07759061789976002, 450: 1.0825790046926402, 4000: 3.4467090758352003e-07, 2500: 3.1967912033568006e-05, 200: 3.9211799693472003, 2000: 0.00019489998112704002, 210: 3.515310135036, 600: 0.3260153551032, 1500: 0.0016025309333812803, 350: 2.0230094228400004, 230: 2.9522496720528, 1000: 0.022168973868048003, 750: 0.10903887551894402, 115: 1.1848269990765599, 500: 0.7189122772843202, 120: 1.8109074925872004, 250: 2.5618089998592, 124: 2.3466716894041206, 125: 2.5569363246336, 126: 2.7723998720229464
            },
            
            'VBF': {
                130: 0.3259289705364, 900: 0.02087051133888, 135: 0.41656922177472006, 5000: 2.3661289221696e-06, 650: 0.044905801810464, 140: 0.5030990317785601, 270: 0.3026563825824001, 400: 0.12785150149632002, 145: 0.5818343183956801, 150: 0.65254960326528, 160: 0.7959181155912001, 165: 0.8082307282686716, 550: 0.06355415069640002, 170: 0.79014821218704, 300: 0.25414515249984, 175: 0.7614731191728479, 180:0.7113285908064002, 3000: 0.000148386489321168, 700: 0.038239080188400006, 190: 0.5594557375008, 800: 0.028023153469920004, 450: 0.09653835519619203, 4000: 1.8896667911856e-05, 2500: 0.00042432099212160005, 200: 0.4938263073979201, 2000: 0.0012679286595091203, 210: 0.45139537950192, 600: 0.053209086371280016, 1500: 0.0041137560592128, 350: 0.19077472274313606, 230: 0.39004476733152005, 1000: 0.015699876708499202, 750: 0.032636674995120005, 115: 0.10354156666812, 500: 0.077182472783808, 120: 0.16392042566928006, 250: 0.34260089909976005, 124: 0.21802814979993485, 125: 0.239065628256, 126: 0.26083528891063495,155:0.7343156920375432,
            }
        }
        
        
        mass=int(self.mass)
        #print "mass=",mass
        self.xsec_ggHlnuqq_sm=HWWLNUQQ_XSEC['GGF'][mass]
        self.xsec_qqHlnuqq_sm=HWWLNUQQ_XSEC['VBF'][mass]
        self.xsec_ggH_sm=HWW_XSEC['GGF'][mass]
        self.xsec_qqH_sm=HWW_XSEC['VBF'][mass]
        #print "SM Xsec ggHlnuqq=",self.xsec_ggHlnuqq_sm
        #print "SM Xsec qqHlnuqq=",self.xsec_qqHlnuqq_sm
        #print "SM Xsec ggH=",self.xsec_ggH_sm
        #print "SM Xsec qqH=",self.xsec_qqH_sm
    def doParametersOfInterest(self):
        #print "<doParametersOfInterest>"
        """Create POI out of signal strength """
        self.SetMass()
        if not self.sigstrength:
            self.modelBuilder.doVar("sigma[0,0,10]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.doVar("fvbf[0,0,1]") ##mu is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.factory_( 'expr::r_ggH(\"@0*(1-@1)'+'/'+str(self.xsec_ggH_sm)+'\", sigma,fvbf)')
            self.modelBuilder.factory_( 'expr::r_qqH(\"@0*@1'+'/'+str(self.xsec_qqH_sm)+'\", sigma,fvbf)')
            
            #self.modelBuilder.doSet("POI","sigma,fvbf")


        else:
            self.modelBuilder.doVar("r[0,0,10]") ##r is what we want to return (in string) name[starting_value,min,max] 
            self.modelBuilder.factory_( 'expr::r_ggH(\"@0\",r)')
            self.modelBuilder.factory_( 'expr::r_qqH(\"@0\",r)')            
            #self.modelBuilder.doSet("POI","r")

            #print 'expr::r_ggH(\"@0*(1-@1)'+'/'+str(self.xsec_ggHlnuqq_sm)+'\", sigma,fvbf)'
            #print 'expr::r_qqH(\"@0*@1'+'/'+str(self.xsec_qqHlnuqq_sm)+'\", sigma,fvbf)'
            #self.modelBuilder.factory_('expr::r_ggH(\"@0*(1-@1)\", r,fvbf)')
            #self.modelBuilder.factory_('expr::r_qqH(\"@0*@1\", r,fvbf)')
        if self.noInterference:
            self.modelBuilder.factory_('expr::ggH_s_func(\"@0\", r_ggH)')
            self.modelBuilder.factory_( 'expr::ggH_b_func(\"1\", r_ggH)')
            self.modelBuilder.factory_( 'expr::ggH_sbi_func(\"0\", r_ggH)')
            
            self.modelBuilder.factory_('expr::qqH_s_func(\"@0\", r_qqH)')
            self.modelBuilder.factory_( 'expr::qqH_b_func(\"1\", r_qqH)')
            self.modelBuilder.factory_( 'expr::qqH_sbi_func(\"0\", r_qqH)')
        else:
            self.modelBuilder.factory_('expr::ggH_s_func(\"@0-sqrt(@0)\", r_ggH)')
            self.modelBuilder.factory_( 'expr::ggH_b_func(\"1-sqrt(@0)\", r_ggH)')
            self.modelBuilder.factory_( 'expr::ggH_sbi_func(\"sqrt(@0)\", r_ggH)')
            
            self.modelBuilder.factory_('expr::qqH_s_func(\"@0-sqrt(@0)\", r_qqH)')
            self.modelBuilder.factory_( 'expr::qqH_b_func(\"1-sqrt(@0)\", r_qqH)')
            self.modelBuilder.factory_( 'expr::qqH_sbi_func(\"sqrt(@0)\", r_qqH)')
        
        if not self.sigstrength:
            self.modelBuilder.doSet("POI","sigma,fvbf")
        else:
            self.modelBuilder.doSet("POI","r")

    def setPhysicsOptions(self,physOptions):
        #print "<setPhysicsOptions>"
        print "physOptions=",physOptions
        self.noInterference=False
        self.sigstrength=False
        for po in physOptions:
            if 'KillInterference' in po:
                self.noInterference=True
            if 'SignalStrength' in po:
                self.sigstrength=True
        print "self.noInterference",self.noInterference
        print "self.sigstrength",self.sigstrength
    def getYieldScale(self,bin,process): ##bin process in datacard
        #print "<getYieldScale>"
        ###print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.mass)
        #if  "ggHWW" in process:
        #print process
        ##--ggH
        #if  "ggHWWlnuqq_M"+str(mass) in process:
        if  "ggH_hww"+str(mass) in process:
            if 'SBI' in process:
                #print "->ggH_sbi_func"
                return "ggH_sbi_func"
            elif 'S' in process:
                #print "->ggH_s_func"
                return "ggH_s_func"
        if 'ggWW' in process:
            #print "->ggH_b_func"
            return 'ggH_b_func'

        ##--qqH
        #if "vbfHWWlnuqq_M"+str(mass) in process:
        if "qqH_hww"+str(mass) in process:
            if 'SBI' in process:
                #print "->qqH_sbi_func"
                return "qqH_sbi_func"
            elif 'S' in process:
                #print '->qqH_s_func'
                return 'qqH_s_func'
        if 'qqWWqq' in process:
            #print '->qqH_b_func'
            return 'qqH_b_func'
        #print "->1"
        return 1

        #self.modelBuilder.doSet("POI","r_qqH")

        #self.modelBuilder.factory_('expr::qqH_s_func(\"@0-sqrt(@0)\", r_qqH)')
        #self.modelBuilder.factory_( 'expr::qqH_b_func(\"1-sqrt(@0)\", r_qqH)')
        #self.modelBuilder.factory_( 'expr::qqH_sbi_func(\"sqrt(@0)\", r_qqH)')
    
        
for m in [115,120,125,126,130,135,140,145,150,155,160,165,170,175,180,190,200,210,230,250,270,300,350,400,450,500,550,600,650,700,750,800,900,1000,1500,2000,2500,3000,4000,5000]:
    exec("XWW"+str(m)+"=HighMassScalar("+str(m)+")")
