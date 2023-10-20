#!/usr/bin/env python

from biasUtils import *
#from os import *
from os import path
from os import system
#import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--datacard",default="Datacard.root")
parser.add_option("-o","--outfile",default="Out file name")
parser.add_option("-w","--workspace",default="w")
parser.add_option("-t","--toys",action="store_true", default=False)
parser.add_option("-n","--nToys",default=1000,type="int")
parser.add_option("-f","--fits",action="store_true", default=False)
parser.add_option("-p","--plots",action="store_true", default=False)
parser.add_option("-e","--expectSignal",default=1.,type="float")
parser.add_option("-m","--mH",default=125.,type="float")
parser.add_option("-c","--combineOptions",default="")
parser.add_option("-s","--seed",default=-1,type="int")
parser.add_option("--dryRun",action="store_true", default=False)
parser.add_option("--poi",default="r")
parser.add_option("--split",default=500,type="int")
parser.add_option("--selectFunction",default=None)
parser.add_option("--gaussianFit",action="store_true", default=False)
(opts,args) = parser.parse_args()
print
if opts.nToys>opts.split and not opts.nToys%opts.split==0: raise RuntimeError('The number of toys %g needs to be smaller than or divisible by the split number %g'%(opts.nToys, opts.split))

import ROOT as r
r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(2211)

ws = r.TFile(opts.datacard).Get(opts.workspace)

pdfs = rooArgSetToList(ws.allPdfs())
multipdfName = None
for pdf in pdfs:
    if pdf.InheritsFrom("RooMultiPdf"):
        if multipdfName is not None: raiseMultiError()
        multipdfName = pdf.GetName()
        print 'Conduct bias study for multipdf called %s'%multipdfName
multipdf = ws.pdf(multipdfName)
print

varlist = rooArgSetToList(ws.allCats())
indexName = None
for var in varlist:
    if var.GetName().startswith('pdfindex'):
        if indexName is not None: raiseMultiError()
        indexName = var.GetName()
        print 'Found index called %s'%indexName
print

from collections import OrderedDict as od
indexNameMap = od()
for ipdf in range(multipdf.getNumPdfs()):
    if opts.selectFunction is not None:
        if not multipdf.getPdf(ipdf).GetName().count(opts.selectFunction): continue
    indexNameMap[ipdf] = multipdf.getPdf(ipdf).GetName()

if opts.toys:
    #if not path.isdir('BiasToys'): system('mkdir -p BiasToys')
    if not path.isdir('BiasToys_%s'%(opts.outfile)): system('mkdir -p BiasToys_%s'%(opts.outfile))#bing
    toyCmdBase = 'combine -m %.4f -d %s -M GenerateOnly --expectSignal %.4f --rMax=1 --rMin=0 -s %g --saveToys %s '%(opts.mH, opts.datacard, opts.expectSignal, opts.seed, opts.combineOptions)
    for ipdf,pdfName in indexNameMap.iteritems():
        print pdfName
        name = shortName(pdfName)
        if opts.nToys > opts.split:
            for isplit in range(opts.nToys//opts.split):
                toyCmd = toyCmdBase + ' -t %g -n _%s_%s_split%g --setParameters %s=%g --freezeParameters %s'%(opts.split, opts.outfile, name, isplit, indexName, ipdf, indexName)
                print toyCmd
                run(toyCmd, dry=opts.dryRun)
                #system('mv higgsCombine_%s* %s'%(name, toyName(name,split=isplit)))
                #print 'mv higgsCombine_%s_%s* %s'%(opts.outfile, name, toyName(name,split=isplit,n=opts.outfile))
                system('mv higgsCombine_%s_%s* %s'%(opts.outfile, name, toyName(name,split=isplit,n=opts.outfile)))#bing
        else:
            toyCmd = toyCmdBase + ' -t %g -n _%s --setParameters %s=%g --freezeParameters %s'%(opts.nToys, name, indexName, ipdf, indexName)
            run(toyCmd, dry=opts.dryRun)
            #system('mv higgsCombine_%s* %s'%(name, toyName(name))
            system('mv higgsCombine_%s* %s'%(name, toyName(name,n=opts.outfile)))
print

if opts.fits:
    #if not path.isdir('BiasFits'): system('mkdir -p BiasFits')
    if not path.isdir('BiasFits_%s'%(opts.outfile)): system('mkdir -p BiasFits_%s'%(opts.outfile))
    fitCmdBase = 'combine -m %.4f -d %s -M MultiDimFit --rMax=1 --rMin=0 -P %s --algo singles %s '%(opts.mH, opts.datacard, opts.poi, opts.combineOptions)
    for ipdf,pdfName in indexNameMap.iteritems():
        name = shortName(pdfName)
        #if pdfName != "env_pdf_0_13TeV_bern2": continue
        #if "bern" in pdfName: continue
        if opts.nToys > opts.split:
            for isplit in range(opts.nToys//opts.split):
                #fitCmd = fitCmdBase + ' -t %g -n _%s_split%g --toysFile=%s'%(opts.split, name, isplit, toyName(name,split=isplit))
                fitCmd = fitCmdBase + ' -t %g -n _%s_%s_split%g --toysFile=%s'%(opts.split, opts.outfile, name, isplit, toyName(name,split=isplit,n=opts.outfile))
                
                run(fitCmd, dry=opts.dryRun)
                #system('mv higgsCombine_%s* %s'%(name, fitName(name,split=isplit)))
                system('mv higgsCombine_%s_%s* %s'%(opts.outfile, name, fitName(name,split=isplit,n=opts.outfile)))
            #run('hadd %s BiasFits/*%s*split*.root'%(fitName(name),name), dry=opts.dryRun)
            run('hadd -f %s BiasFits_%s/*%s*split*.root'%(fitName(name,n=opts.outfile),opts.outfile,name), dry=opts.dryRun)#bing
        else:
            #fitCmd = fitCmdBase + ' -t %g -n _%s --toysFile=%s'%(opts.nToys, name, toyName(name))
            fitCmd = fitCmdBase + ' -t %g -n _%s_%s --toysFile=%s'%(opts.nToys, opts.outfile, name, toyName(name,n=opts.outfile))
            run(fitCmd, dry=opts.dryRun)
            #system('mv higgsCombine_%s* %s'%(name, fitName(name)))
            system('mv higgsCombine_%s_%s* %s'%(opts.outfile, name, fitName(name,n=opts.outfile)))

if opts.plots:
    file = open('./Bias_%s.txt'%(opts.outfile), 'w')
    mean = ''
    out_name = ''
    #if not path.isdir('BiasPlots'): system('mkdir -p BiasPlots')
    if not path.isdir('BiasPlots_%s'%(opts.outfile)): system('mkdir -p BiasPlots_%s'%(opts.outfile))#bing
    for ipdf,pdfName in indexNameMap.iteritems():
	print pdfName
        name = shortName(pdfName)
        #if "bern" in pdfName: continue
        #if pdfName == "env_pdf_0_13TeV_exp3_gauxexp3": continue
        #tfile = r.TFile(fitName(name))
        tfile = r.TFile(fitName(name,n=opts.outfile))
        tree = tfile.Get('limit')
        pullHist = r.TH1F('pullsForTruth_%s'%name, 'Pull distribution using the envelope to fit %s'%name, 80, -4., 4.)
        pullHist.GetXaxis().SetTitle('Pull')
        pullHist.GetYaxis().SetTitle('Entries')
        print tree
        for itoy in range(opts.nToys):
            tree.GetEntry(3*itoy)
            if not getattr(tree,'quantileExpected')==-1:
                raiseFailError(itoy,True)
                continue
            bf = getattr(tree, 'r')
            tree.GetEntry(3*itoy+1)
            if not abs(getattr(tree,'quantileExpected')--0.32)<0.001:
                raiseFailError(itoy,True)
                continue
            lo = getattr(tree, 'r')
            tree.GetEntry(3*itoy+2)
            if not abs(getattr(tree,'quantileExpected')-0.32)<0.001:
                raiseFailError(itoy,True)
                continue
            hi = getattr(tree, 'r')
            diff = bf - opts.expectSignal
            unc = 0.5 * (hi-lo)
            if unc > 0.:
                pullHist.Fill(diff/unc)
        canv = r.TCanvas()
        pullHist.Draw()
        if opts.gaussianFit:
           r.gStyle.SetOptFit(111)
           result = pullHist.Fit('gaus','S')
           #result = pullHist.Fit('gaus','S',"",-2,2)#bing
           #if "exp3" in pdfName:
           # result = pullHist.Fit('gaus','S',"",-1.5,3)#bing
           #else:
           # #result = pullHist.Fit('gaus','S')
           # result = pullHist.Fit('gaus','S',"",-5,5)#bing
           print "#####mean: "+str(result.Parameter(1))
           mean = mean + str(result.Parameter(1)) + '\t'
           out_name = out_name + pdfName.split('_')[-1] +'\t'
           #print "mean: %.3e"%Gaus.GetParameter(1)
        #canv.SaveAs('%s.pdf'%plotName(name))
        #canv.SaveAs('%s.png'%plotName(name))
        canv.SaveAs('%s.pdf'%plotName(name,opts.outfile))
        canv.SaveAs('%s.png'%plotName(name,opts.outfile))

    file.write(mean + '\n')
    file.write(out_name + '\n')
    file.write(str(opts.expectSignal) + '\n')
