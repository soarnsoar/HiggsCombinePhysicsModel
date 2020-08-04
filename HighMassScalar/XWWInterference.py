from HiggsAnalysis.CombinedLimit.PhysicsModel import *
 
 
### This is the base python class to study the Higgs width
 
class XWWInterference(PhysicsModel):
    def __init__(self, mass):
        self.mass=mass
        self.categories=["of0j", "of1j", "of2j", "ofVBF", "ee", "mm"]
        pass
    
    def setModelBuilder(self, modelBuilder):
        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False
        print "setModelBuilder"
        for cat in self.categories:
          self.modelBuilder.doVar("r"+cat+"[1,0,10]")
          self.modelBuilder.factory_( "expr::s_scaling_ggH_"+cat+"(\"@0 - TMath::Sqrt(@0)\", r"+cat+")")
          self.modelBuilder.factory_( "expr::s_scaling_qqH_"+cat+"(\"@0 - TMath::Sqrt(@0)\", r"+cat+")")
          self.modelBuilder.factory_( "expr::b_scaling_ggH_"+cat+"(\"1.-TMath::Sqrt(@0)\",r"+cat+")")
          self.modelBuilder.factory_( "expr::b_scaling_qqH_"+cat+"(\"1.-TMath::Sqrt(@0)\",r"+cat+")")
          self.modelBuilder.factory_( "expr::sbi_scaling_ggH_"+cat+"(\"TMath::Sqrt(@0)\",r"+cat+")")
          self.modelBuilder.factory_( "expr::sbi_scaling_qqH_"+cat+"(\"TMath::Sqrt(@0)\",r"+cat+")")
    def preProcessNuisances(self,nuisances):
        nuisancesToRemove = []
        for n in nuisances:
          if "stat" in n[0] and "H_hww_" in n[0] and "c10brn00" in n[0]:
            if self.mass not in n[0]:
              print "removing nuisance", n[0]
              nuisancesToRemove.append(n[0])
        
        for nr in nuisancesToRemove:
          for n in nuisances:
            if n[0] == nr:
              nuisances.remove(n)
              break


    def getYieldScale(self,bin,process):
        scaling=1.
        postfix=""
        self.categories.append(bin)
        if self.manyR:
          for cat in self.categories:
            if cat in bin:
              postfix="_"+cat
              break
        if "hwwlnuqq" in bin and self.muAsPOI == False :
         postfix="2"

        if "ggH_hww_"+self.mass+"_"   in process: 
          scaling = "s_scaling_ggH"+postfix
        elif "qqH_hww_"+self.mass+"_" in process: 
          scaling = "s_scaling_qqH"+postfix
        elif process == 'ggWW' or process=="ggH_hww" : 
          scaling = "b_scaling_ggH"+postfix
        elif process == 'qqWWqq' or process=="qqH_hww" :
          scaling = "b_scaling_qqH"+postfix
        elif "ggH_hww_SBI"+self.mass+"_"   in process:
          scaling = "sbi_scaling_ggH"+postfix
        elif "qqH_hww_SBI"+self.mass+"_" in process:
          scaling = "sbi_scaling_qqH"+postfix
        elif "ggH_hww_" in process and self.mass+"_" not  in process:
           scaling = 0.
        elif "qqH_hww_" in process and self.mass+"_" not  in process:
           scaling = 0.
        else:
          scaling = 1.   

        print "Will scale",process,"in bin",bin,"by",scaling  
        return scaling

    def setXsec(self):

      self.BR2l2nu = (3*.108)*(3*.108)
      self.BRlnuqq = (3*.108)*.676*2

      masses = ['200','250','300','350','400','450','500','550','600','650','700','800','900','1000','1500','2000','2500','3000']  

      xsec_ggH = [ 1.812E+01*.739, 1.248E+01*.701, 9.823E+00*.691, 1.025E+01*.674, 9.516E+00*.576, 6.771E+00*.546, 4.538E+00*.541, 3.008E+00*.546, 2.006E+00*.555, 1.352E+00*.564, 9.235E-01*.574, 4.491E-01*.590, 2.301E-01*.604, 1.233E-01*.614, 8.913E-03*.614, 1.084E-03*.614, 1.778E-04*.614, 3.502E-05*.614]
  
      xsec_qqH = [ 2.282E+00*.739, 1.669E+00*.701, 1.256E+00*.691, 9.666E-01*.674, 7.580E-01*.576, 6.038E-01*.546, 4.872E-01*.541, 3.975E-01*.546, 3.274E-01*.555, 2.719E-01*.564, 2.275E-01*.574, 1.622E-01*.590, 1.180E-01*.604, 8.732E-02*.614, 2.288E-02*.614, 7.052E-03*.614, 2.360E-03*.614, 8.253E-04*.614]

      for index in range(len(masses)):
        if self.mass == masses[index]:
          self.xsec_ggH_2l2nu = xsec_ggH[index]*self.BR2l2nu
          self.xsec_qqH_2l2nu = xsec_qqH[index]*self.BR2l2nu
          self.xsec_ggH_lnuqq = xsec_ggH[index]*self.BRlnuqq
          self.xsec_qqH_lnuqq = xsec_qqH[index]*self.BRlnuqq
          return
                              
      raise RuntimeError, "Don't know this mass",  self.mass
      

    def setPhysicsOptions(self,physOptions):
        self.muAsPOI = True
        self.noInterference = False
        self.manyR = False  
        for po in physOptions:
            if po == "FloatVBFFraction":
              print "Will float  the VBF fraction, the limit is on the total  cross section"
              self.muAsPOI = False
            if po == "KillInterference":
              print "will neglect interference"
              self.noInterference = True
            if po == "ManyR":
              self.manyR = True
           
    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        if self.muAsPOI:
          poi="r"       
          if self.noInterference:
            self.modelBuilder.doVar("r[1,-10,10]")
        
            self.modelBuilder.factory_( "expr::s_scaling_ggH(\"@0\", r)")
            self.modelBuilder.factory_( "expr::s_scaling_qqH(\"@0\", r)")
            self.modelBuilder.factory_( "expr::b_scaling_ggH(\"1.\",r)")
            self.modelBuilder.factory_( "expr::b_scaling_qqH(\"1.\",r)")
            self.modelBuilder.factory_( "expr::sbi_scaling_ggH(\"0\", r)")
            self.modelBuilder.factory_( "expr::sbi_scaling_qqH(\"0\", r)")

          else:
            if self.manyR:
              poi=""
              for cat in self.categories:
                poi += "r"+cat+","
              poi.rstrip(",")  

            else:
              self.modelBuilder.doVar("r[1,0,10]")
              self.modelBuilder.factory_( "expr::s_scaling_ggH(\"@0 - TMath::Sqrt(@0)\", r)")
              self.modelBuilder.factory_( "expr::s_scaling_qqH(\"@0 - TMath::Sqrt(@0)\", r)")
              self.modelBuilder.factory_( "expr::b_scaling_ggH(\"1.-TMath::Sqrt(@0)\",r)")
              self.modelBuilder.factory_( "expr::b_scaling_qqH(\"1.-TMath::Sqrt(@0)\",r)")
              self.modelBuilder.factory_( "expr::sbi_scaling_ggH(\"TMath::Sqrt(@0)\",r)")
              self.modelBuilder.factory_( "expr::sbi_scaling_qqH(\"TMath::Sqrt(@0)\",r)")

        else:
          self.setXsec()
          self.modelBuilder.doVar("sigma[0,0,10]")
          self.modelBuilder.doVar("fvbf[0.5,0,1]")

          poi='sigma,fvbf'

          self.modelBuilder.factory_( "expr::rgg(\"(1.-@1)*@0*%f/%f\", sigma,fvbf)" %(self.BR2l2nu, self.xsec_ggH_2l2nu))
          self.modelBuilder.factory_( "expr::rqq(\"@1*@0*%f/%f\", sigma,fvbf)" %(self.BR2l2nu, self.xsec_qqH_2l2nu))       
          self.modelBuilder.factory_( "expr::s_scaling_ggH(\"@0 - TMath::Sqrt(@0)\", rgg)")
          self.modelBuilder.factory_( "expr::s_scaling_qqH(\"@0 - TMath::Sqrt(@0)\", rqq)")
          self.modelBuilder.factory_( "expr::b_scaling_ggH(\"1.-TMath::Sqrt(@0)\",  rgg)")
          self.modelBuilder.factory_( "expr::b_scaling_qqH(\"1.-TMath::Sqrt(@0)\", rqq)" )
          self.modelBuilder.factory_( "expr::sbi_scaling_ggH(\"TMath::Sqrt(@0)\", rgg)")
          self.modelBuilder.factory_( "expr::sbi_scaling_qqH(\"TMath::Sqrt(@0)\", rqq)")

          self.modelBuilder.factory_( "expr::rgg2(\"(1.-@1)*@0*%f/%f\", sigma,fvbf)" %(self.BRlnuqq, self.xsec_ggH_lnuqq))
          self.modelBuilder.factory_( "expr::rqq2(\"@1*@0*%f/%f\", sigma,fvbf)" %(self.BRlnuqq, self.xsec_qqH_lnuqq))      
          self.modelBuilder.factory_( "expr::s_scaling_ggH2(\"@0 - TMath::Sqrt(@0)\", rgg2)")
          self.modelBuilder.factory_( "expr::s_scaling_qqH2(\"@0 - TMath::Sqrt(@0)\", rqq2)")
          self.modelBuilder.factory_( "expr::b_scaling_ggH2(\"1.-TMath::Sqrt(@0)\",  rgg2)")
          self.modelBuilder.factory_( "expr::b_scaling_qqH2(\"1.-TMath::Sqrt(@0)\", rqq2)" )
          self.modelBuilder.factory_( "expr::sbi_scaling_ggH2(\"TMath::Sqrt(@0)\", rgg2)")
          self.modelBuilder.factory_( "expr::sbi_scaling_qqH2(\"TMath::Sqrt(@0)\", rqq2)")

        self.modelBuilder.doSet("POI",poi)
 
XWW200 = XWWInterference("200")
XWW210 = XWWInterference("210")
XWW230 = XWWInterference("230")
XWW250 = XWWInterference("250")
XWW270 = XWWInterference("270")
XWW300 = XWWInterference("300")
XWW350 = XWWInterference("350")
XWW400 = XWWInterference("400")
XWW450 = XWWInterference("450")
XWW500 = XWWInterference("500")
XWW550 = XWWInterference("550")    
XWW600 = XWWInterference("600")
XWW650 = XWWInterference("650")
XWW700 = XWWInterference("700")   
XWW750 = XWWInterference("750")
XWW800 = XWWInterference("800")    
XWW900 = XWWInterference("900")
XWW1000 = XWWInterference("1000")
XWW1500 = XWWInterference("1500")   
XWW2000 = XWWInterference("2000")
XWW2500 = XWWInterference("2500")
XWW3000 = XWWInterference("3000")
