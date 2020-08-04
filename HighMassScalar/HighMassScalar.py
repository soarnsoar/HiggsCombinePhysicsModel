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
                126: 9.467639794273635}, 
            'VBF': {
                130: 1.113035, 
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
                126: 0.8907425606102282
            }
        }
        HWWLNUQQ_XSEC={
            'GGF': {
                130: 5.071637916827999, 
                900: 0.061046245666224, 
                135: 6.3001933692768, 
                5000: 3.3711943229999994e-08, 
                650: 0.33493551331967997, 
                140: 7.4081764645056, 
                270: 3.4056485878464, 
                400: 2.4075888289689598, 
                145: 8.356296866072398, 
                150: 9.153624953491198, 
                155: 10.075334101420307, 
                160: 10.697298128319598, 
                165: 10.65537606189697, 
                550: 0.72139956715008, 
                170: 10.2321655528932, 
                300: 2.98145043750708, 
                175: 9.698813871583427, 
                180: 8.921563795871998, 
                3000: 9.4447380153168e-06, 
                700: 0.23283817947683996, 
                800: 0.11638592684964, 
                450: 1.62386850703896, 
                4000: 5.170063613752799e-07, 
                2500: 4.7951868050352006e-05, 
                200: 5.8817699540207995, 
                2000: 0.00029234997169055995, 
                210: 5.272965202553999, 
                600: 0.48902303265479996, 
                1500: 0.0024037964000719197, 
                350: 3.0345141342599997, 
                230: 4.428374508079199, 
                1000: 0.033253460802072, 
                750: 0.163558313278416, 
                115: 1.7772404986148396, 
                500: 1.07836841592648, 
                120: 2.7163612388808, 
                250: 3.8427134997887995, 
                125: 3.835404486950399, 
                126: 4.158599808034419}, 
            'VBF': {
                130: 0.4888934558046, 
                900: 0.031305767008319996, 
                5000: 3.5491933832543992e-06, 
                650: 0.06735870271569598, 
                140: 0.75464854766784, 
                270: 0.4539845738736, 
                400: 0.19177725224448, 
                145: 0.8727514775935199, 
                150: 0.9788244048979199, 
                155: 1.1014735380563145, 
                160: 1.1938771733867999, 
                165: 1.2123460924030072, 
                550: 0.09533122604460001, 
                170: 1.18522231828056, 
                300: 0.38121772874975995, 
                180: 1.0669928862096, 
                3000: 0.00022257973398175196, 
                700: 0.0573586202826, 
                190: 0.8391836062511999, 
                800: 0.04203473020488, 
                450: 0.144807532794288, 
                4000: 2.8345001867783997e-05, 
                2500: 0.0006364814881823999, 
                200: 0.7407394610968799, 
                2000: 0.00190189298926368, 
                210: 0.6770930692528799, 
                600: 0.07981362955692001, 
                1500: 0.0061706340888192, 
                350: 0.286162084114704, 
                230: 0.5850671509972799, 
                1000: 0.023549815062748797, 
                750: 0.04895501249267999, 
                115: 0.15531235000218, 
                500: 0.115773709175712, 
                120: 0.24588063850392003, 
                250: 0.51390134864964, 
                124: 0.32704222469990224, 
                125: 0.35859844238399996, 
                126: 0.39125293336595235
            }
        }
        
        mass=int(self.mass)
        print "mass=",mass
        self.xsec_ggHlnuqq_sm=HWWLNUQQ_XSEC['GGF'][mass]
        self.xsec_qqHlnuqq_sm=HWWLNUQQ_XSEC['VBF'][mass]
        self.xsec_ggH_sm=HWW_XSEC['GGF'][mass]
        self.xsec_qqH_sm=HWW_XSEC['VBF'][mass]
        print "SM Xsec ggHlnuqq=",self.xsec_ggHlnuqq_sm
        print "SM Xsec qqHlnuqq=",self.xsec_qqHlnuqq_sm
        print "SM Xsec ggH=",self.xsec_ggH_sm
        print "SM Xsec qqH=",self.xsec_qqH_sm
    def doParametersOfInterest(self):
        print "<doParametersOfInterest>"
        """Create POI out of signal strength """
        self.SetMass()
        self.modelBuilder.doVar("sigma[0,0,10]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        self.modelBuilder.doVar("fvbf[0,0,1]") ##mu is what we want to return (in string) name[starting_value,min,max] 
        
        #self.modelBuilder.factory_( 'expr::r_ggH(\"@0*(1-@1)'+'/'+str(self.xsec_ggHlnuqq_sm)+'\", sigma,fvbf)')
        #self.modelBuilder.factory_( 'expr::r_qqH(\"@0*@1'+'/'+str(self.xsec_qqHlnuqq_sm)+'\", sigma,fvbf)')
        self.modelBuilder.factory_( 'expr::r_ggH(\"@0*(1-@1)'+'/'+str(self.xsec_ggH_sm)+'\", sigma,fvbf)')
        self.modelBuilder.factory_( 'expr::r_qqH(\"@0*@1'+'/'+str(self.xsec_qqH_sm)+'\", sigma,fvbf)')

        print 'expr::r_ggH(\"@0*(1-@1)'+'/'+str(self.xsec_ggHlnuqq_sm)+'\", sigma,fvbf)'
        print 'expr::r_qqH(\"@0*@1'+'/'+str(self.xsec_qqHlnuqq_sm)+'\", sigma,fvbf)'
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
        
        
        self.modelBuilder.doSet("POI","sigma,fvbf")

    def setPhysicsOptions(self,physOptions):
        print "<setPhysicsOptions>"
        self.noInterference=False
        
        for po in physOptions:
            if 'KillInterference'==po:
                self.noInterference=True

        
    def getYieldScale(self,bin,process): ##bin process in datacard
        print "<getYieldScale>"
        ##print "self.options.mass=",self.options.mass :: get this value using -m
        mass=int(self.mass)
        #if  "ggHWW" in process:
        print process
        ##--ggH
        if  "ggHWWlnuqq_M"+str(mass) in process:
            if 'SBI' in process:
                print "->ggH_sbi_func"
                return "ggH_sbi_func"
            elif 'S' in process:
                print "->ggH_s_func"
                return "ggH_s_func"
        if 'ggWW' in process:
            print "->ggH_b_func"
            return 'ggH_b_func'

        ##--qqH
        if "vbfHWWlnuqq_M"+str(mass) in process:
            if 'SBI' in process:
                print "->qqH_sbi_func"
                return "qqH_sbi_func"
            elif 'S' in process:
                print '->qqH_s_func'
                return 'qqH_s_func'
        if 'qqWWqq' in process:
            print '->qqH_b_func'
            return 'qqH_b_func'
        print "->1"
        return 1

        #self.modelBuilder.doSet("POI","r_qqH")

        #self.modelBuilder.factory_('expr::qqH_s_func(\"@0-sqrt(@0)\", r_qqH)')
        #self.modelBuilder.factory_( 'expr::qqH_b_func(\"1-sqrt(@0)\", r_qqH)')
        #self.modelBuilder.factory_( 'expr::qqH_sbi_func(\"sqrt(@0)\", r_qqH)')
    
        
for m in [115,120,125,126,130,135,140,145,150,155,160,165,170,175,180,190,200,210,230,250,270,300,350,400,450,500,550,600,650,700,750,800,900,1000,1500,2000,2500,3000,4000,5000]:
    exec("XWW"+str(m)+"=HighMassScalar("+str(m)+")")
