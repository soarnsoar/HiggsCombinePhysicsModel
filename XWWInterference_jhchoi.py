from array import array
import CombineHarvester.CombineTools.plotting as plot
from HiggsAnalysis.CombinedLimit.PhysicsModel import *
import ROOT
from copy import deepcopy 
 
### This is the base python class to study the Higgs width
 
class XWWInterference(PhysicsModel):
    def __init__(self):
        print "<init>"
        self.NuisanceNamesToAdd=set()
        pass
    
    def setModelBuilder(self, modelBuilder):
        print "<setModelBuilder>"
        PhysicsModel.setModelBuilder(self,modelBuilder)

    def preProcessNuisances(self,nuisances):
        print "<preProcessNuisances>"
        print "---preProcessNuisances---"
        print "--nuisances--"
        #for Nuisance in self.NuisanceNamesToAdd:
        #    nuisances.append((Nuisance,"",False, "param", [ "0", "1"], [] ) )
        #for n in nuisances:
        #    #if 'deltaTheoryXsec' in n[0]:
        #    #    print "!!!![deltaTheoryXsec] in preProcessNuisances"
        #        print n
        #    #print n[0]
        



    def getYieldScale(self,bin,process):
        print "<getYieldScale>"
        print bin
        print process
        addsemilep="2" if "qq" in bin else ""
        if "ggH_hww" in process and "SBI" not in process and (not process=="ggH_hww"):
          scaling = "S_SCALE_ggH" +addsemilep
        elif "qqH_hww" in process and "SBI" not in process and (not process=="qqH_hww"):
          scaling = "S_SCALE_qqH" +addsemilep
        elif process in ["ggWW", "ggH_hww"]:
          scaling = "B_SCALE_ggH" +addsemilep
        elif process in ["qqWWqq", "qqH_hww"]:
          scaling = "B_SCALE_qqH" +addsemilep
        elif "ggH_hww" in process and "SBI" in process:
          scaling = "SBI_SCALE_ggH" +addsemilep
        elif "qqH_hww" in process and "SBI" in process:
          scaling = "SBI_SCALE_qqH" +addsemilep
        else:
          scaling = 1

        print "Will scale",process,"in bin",bin,"by",scaling  
        return scaling

    def setPhysicsOptions(self,physOptions):
        print "<setPhysicsOptions>"
        self.noInterference = False
        self.theory_xsec_ggH=False
        self.theory_xsec_qqH=False
        self.delta_theory_xsec_ggH=False
        self.delta_theory_xsec_qqH=False
        #self.addNuisance=False
        for po in physOptions:
            if po == "noInterference":
                print "will neglect interference"
                self.noInterference = True
            if "input_ggH_xsec" in po:
                self.theory_xsec_ggH=float(po.split(':')[1])
            if "input_qqH_xsec" in po:
                self.theory_xsec_qqH=float(po.split(':')[1])

            if "delta_ggH_xsec" in po:
                self.delta_theory_xsec_ggH=(po.split(':')[1])
            if "delta_qqH_xsec" in po:
                self.delta_theory_xsec_qqH=(po.split(':')[1])

            #if "addNuisance" in po:
            #    self.addNuisance=po.split(":")[1:]
           
    def doParametersOfInterest(self):
        print "<doParametersOfInterest>"
        """Create POI and other parameters, and define the POI set."""
        if not self.theory_xsec_ggH and not self.theory_xsec_qqH :
            poi='sigma'
            self.modelBuilder.doVar("sigma[1,0,10]")
            self.modelBuilder.doVar("fvbf[0.5,0,1]")
        
            if self.noInterference:
            
                
                self.modelBuilder.factory_("expr::rgg2(\"(1.-@1)*@0\", sigma,fvbf)")
                self.modelBuilder.factory_("expr::rqq2(\"@1*@0\", sigma,fvbf)")
                self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0\", rgg2)")
                self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0\", rqq2)")
                self.modelBuilder.factory_("expr::B_SCALE_ggH2(\"1.\", rgg2)")
                self.modelBuilder.factory_("expr::B_SCALE_qqH2(\"1.\", rqq2)")
                self.modelBuilder.factory_("expr::SBI_SCALE_ggH2(\"0\", rgg2)")
                self.modelBuilder.factory_("expr::SBI_SCALE_qqH2(\"0\", rqq2)")
                self.modelBuilder.out.function('rgg').Print('')
                self.modelBuilder.out.function('rqq').Print('')
                
            else: ########## This is what is used for ggF-only, VBF-only and floating f_VBF scenarios!!
            
                self.modelBuilder.factory_("expr::rgg2(\"(1.-@1)*@0\", sigma,fvbf)")
                self.modelBuilder.factory_("expr::rqq2(\"@1*@0\", sigma,fvbf)")  
                self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0 - TMath::Sqrt(@0)\", rgg2)")
                self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0 - TMath::Sqrt(@0)\", rqq2)")
                self.modelBuilder.factory_("expr::B_SCALE_ggH2(\"1.-TMath::Sqrt(@0)\",  rgg2)")
                self.modelBuilder.factory_("expr::B_SCALE_qqH2(\"1.-TMath::Sqrt(@0)\", rqq2)" )
                self.modelBuilder.factory_("expr::SBI_SCALE_ggH2(\"TMath::Sqrt(@0)\", rgg2)")
                self.modelBuilder.factory_("expr::SBI_SCALE_qqH2(\"TMath::Sqrt(@0)\", rqq2)")
            



        else:
            poi='r'
            self.modelBuilder.doVar("r[1,0,10]")
            ##--parameter for theory xsec
            ##---sigma = sigma0*(1+delta)
            self.modelBuilder.doVar("deltaTheory_ggH_hww_xsec[0,0,0]")
            self.modelBuilder.doVar("deltaTheory_qqH_hww_xsec[0,0,0]")

            
            #self.modelBuilder.factory_("BifurGauss::deltaTheory_ggH_hww_xsec_pdf(deltaTheory_ggH_hww_xsec,deltaTheory_ggH_hww_xsec_In[0,-1,1],-0.5,0.6")
            #self.out.var("deltaTheory_ggH_hww_xsec_In").setConstant(True)
            ##--enable

            if self.delta_theory_xsec_ggH!=False:

                self.modelBuilder.out.var("deltaTheory_ggH_hww_xsec").setMax(7.)
                self.modelBuilder.out.var("deltaTheory_ggH_hww_xsec").setMin(-7.)
                print "[set AsymGausssian Constraint to theroy ggH xsec]"
                sigmaL=self.delta_theory_xsec_ggH.split(',')[0]
                if sigmaL.replace(" ","").split()[0]!="-": sigmaL="-"+sigmaL ##must be negative value for low error
                sigmaR=self.delta_theory_xsec_ggH.split(',')[1]
                self.modelBuilder.doObj("deltaTheory_ggH_hww_xsec_Pdf", "BifurGauss", "deltaTheory_ggH_hww_xsec, deltaTheory_ggH_hww_xsec_In[0,-7,7], {0}, {1}".format(sigmaL,sigmaR),False) ##
                self.modelBuilder.out.var("deltaTheory_ggH_hww_xsec_In").setConstant(True)
            if self.delta_theory_xsec_qqH!=False:
                self.modelBuilder.out.var("deltaTheory_qqH_hww_xsec").setMax(7.)
                self.modelBuilder.out.var("deltaTheory_qqH_hww_xsec").setMin(-7.)
                print "[set AsymGausssian Constraint to theroy ggH xsec]"
                sigmaL=self.delta_theory_xsec_qqH.split(',')[0]
                sigmaR=self.delta_theory_xsec_qqH.split(',')[1]
                self.modelBuilder.doObj("deltaTheory_qqH_hww_xsec_Pdf", "BifurGauss", "deltaTheory_qqH_hww_xsec, deltaTheory_qqH_hww_xsec_In[0,-1,1], {0}, {1}".format(sigmaL,sigmaR),False) ##
                self.modelBuilder.out.var("deltaTheory_qqH_hww_xsec_In").setConstant(True)
                


            ##--
            #self.modelBuilder.doObj("deltaTheory_ggH_hww_xsec_Pdf", "BifurGauss", "deltaTheory_ggH_hww_xsec, deltaTheory_ggH_hww_xsec_In[0,-1,1], -0.5, 0.6",False) ##min max = -1 ,1 sigmaL = -0.5 sigmaR=0.6
            #self.modelBuilder.doObj("deltaTheory_qqH_hww_xsec_Pdf", "BifurGauss", "deltaTheory_qqH_hww_xsec, deltaTheory_qqH_hww_xsec_In[0,-1,1], -0.5, 0.6",False) ##min max = -1 ,1 sigmaL = -0.5 sigmaR=0.6
            #deltaTheoryXsec_ggH_var=self.modelBuilder.out.var("deltaTheory_ggH_hww_xsec").setVal(0)
            #deltaTheoryXsec_qqH_var=self.modelBuilder.out.var("deltaTheory_qqH_hww_xsec").setError(1)
            #self.NuisanceNamesToAdd.add("deltaTheory_ggH_hww_xsec")
            #self.NuisanceNamesToAdd.add("deltaTheory_qqH_hww_xsec")
            #self.modelBuilder.doVar("deltaTheoryXsec_ggH[1,0,10]")
            #self.modelBuilder.doVar("deltaTheoryXsec_qqH[1,0,10]")
            #asym = ROOT.AsymPow("deltaTheoryXsec_ggH","","0.9","1.1")

            if self.noInterference:

                #self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0"+str(self.theory_xsec_ggH)+"\", r)")
                #self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0"+str(self.theory_xsec_qqH)+"\", r)")
                self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0*(1.+@1)"+str(self.theory_xsec_ggH)+"\", r,deltaTheory_ggH_hww_xsec)")
                self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0*(1.+@1)"+str(self.theory_xsec_qqH)+"\", r,deltaTheory_qqH_hww_xsec)")
                self.modelBuilder.factory_("expr::B_SCALE_ggH2(\"1.\", r)")
                self.modelBuilder.factory_("expr::B_SCALE_qqH2(\"1.\", r)")
                self.modelBuilder.factory_("expr::SBI_SCALE_ggH2(\"0\", r)")
                self.modelBuilder.factory_("expr::SBI_SCALE_qqH2(\"0\", r)")
                self.modelBuilder.out.function('r').Print('')
                #self.modelBuilder.out.function('deltaTheoryXsec_ggH').Print('')
                #self.modelBuilder.out.function('deltaTheoryXsec_qqH').Print('')

            else: ########## This is what is used for ggF-only, VBF-only and floating f_VBF scenarios!!                                                                           


                #self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0*"+str(self.theory_xsec_ggH)+" - TMath::Sqrt(@0*"+str(self.theory_xsec_ggH)+")\", r)")
                #self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0*"+str(self.theory_xsec_qqH)+" - TMath::Sqrt(@0*"+str(self.theory_xsec_qqH)+")\", r)")
                #self.modelBuilder.factory_("expr::B_SCALE_ggH2(\"1.-TMath::Sqrt(@0*"+str(self.theory_xsec_ggH)+")\",  r)")
                #self.modelBuilder.factory_("expr::B_SCALE_qqH2(\"1.-TMath::Sqrt(@0*"+str(self.theory_xsec_qqH)+")\", r)" )
                #self.modelBuilder.factory_("expr::SBI_SCALE_ggH2(\"TMath::Sqrt(@0*"+str(self.theory_xsec_ggH)+")\", r)")
                #self.modelBuilder.factory_("expr::SBI_SCALE_qqH2(\"TMath::Sqrt(@0*"+str(self.theory_xsec_qqH)+")\", r)") #deltaTheory_qqH_hww_xsec
                self.modelBuilder.factory_("expr::S_SCALE_ggH2(\"@0*(1.+@1)*"+str(self.theory_xsec_ggH)+" - TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_ggH)+")\", r,deltaTheory_ggH_hww_xsec)")
                self.modelBuilder.factory_("expr::S_SCALE_qqH2(\"@0*(1.+@1)*"+str(self.theory_xsec_qqH)+" - TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_qqH)+")\", r,deltaTheory_qqH_hww_xsec)")
                self.modelBuilder.factory_("expr::B_SCALE_ggH2(\"1.-TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_ggH)+")\",  r,deltaTheory_ggH_hww_xsec)")
                self.modelBuilder.factory_("expr::B_SCALE_qqH2(\"1.-TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_qqH)+")\", r,deltaTheory_qqH_hww_xsec)" )
                self.modelBuilder.factory_("expr::SBI_SCALE_ggH2(\"TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_ggH)+")\", r,deltaTheory_ggH_hww_xsec)")
                self.modelBuilder.factory_("expr::SBI_SCALE_qqH2(\"TMath::Sqrt(@0*(1.+@1)*"+str(self.theory_xsec_qqH)+")\", r,deltaTheory_qqH_hww_xsec)")
                self.modelBuilder.out.function('r').Print('')
                self.modelBuilder.out.function('deltaTheory_ggH_hww_xsec').Print('')
                self.modelBuilder.out.function('deltaTheory_qqH_hww_xsec').Print('')


            
        self.modelBuilder.out.function('S_SCALE_ggH2').Print('')
        self.modelBuilder.out.function('S_SCALE_qqH2').Print('')
        self.modelBuilder.out.function('B_SCALE_ggH2').Print('')
        self.modelBuilder.out.function('B_SCALE_qqH2').Print('')
        self.modelBuilder.out.function('SBI_SCALE_ggH2').Print('')
        self.modelBuilder.out.function('SBI_SCALE_qqH2').Print('')
        self.modelBuilder.doSet("POI",poi)


 
XWW = XWWInterference()

