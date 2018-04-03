# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
from KBaseReport.KBaseReportClient import KBaseReport
from fast_ani_proc import FastANIProc
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
#END_HEADER


class FastANI:
    '''
    Module Name:
    FastANI

    Module Description:
    A KBase module: FastANI
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/jayrbolton/kbase-fastANI.git"
    GIT_COMMIT_HASH = "c5a9e21f9bb4c9522d4aaeae6187808ec747d328"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        #END_CONSTRUCTOR
        pass


    def fast_ani(self, ctx, params):
        """
        :param params: instance of type "FastANIParams" (fast_ani input) ->
           structure: parameter "workspace_name" of String, parameter
           "query_assembly" of String, parameter "reference_assembly" of
           String, parameter "reference_list" of list of String
        :returns: instance of type "FastANIResults" (fast_ani output) ->
           structure: parameter "report_name" of String, parameter
           "report_ref" of String, parameter "percentage_match" of Double,
           parameter "total_fragments" of Long, parameter
           "orthologous_matches" of Long
        """
        # ctx is the context object
        # return variables are: results
        #BEGIN fast_ani
        print('Starting FastANI function and validating parameters.')
        if 'workspace_name' not in params:
            raise ValueError('Parameter "workspace_name" is not set in input arguments')
        if 'reference_assembly' not in params and 'reference_list' not in params:
            raise ValueError('Pass a parameter for either "reference_assembly" or "reference_list"')
        # Download the query assembly
        assembly_util = AssemblyUtil(self.callback_url)
        query_file = assembly_util.get_assembly_as_fasta({
            'ref': params['query_assembly']
        })
        # Fetch either a single reference assembly or a list of references
        # In either case, we pass an array of references to FastANIProc
        if params['reference_assembly']:
            ref = assembly_util.get_assembly_as_fasta({'ref': params['reference_assembly']})
            refs = [ref['path']]
        else:
            refs = ['xyz']  # TODO fetch references from AssemblySet (???)
            pass
        fast_ani_proc = FastANIProc(query_file['path'])
        fast_ani_proc.run(refs)
        report_obj = {
            'objects_created': [],
            'text_message': 'Total percentage match: ' + fast_ani_proc.percentage_match
        }
        report = KBaseReport(self.callback_url)
        report_info = report.create({
            'report': report_obj,
            'workspace_name': params['workspace_name']
        })
        results = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
            'percentage_match': fast_ani_proc.percentage_match,
            'orthologous_matches': fast_ani_proc.orthologous_matches,
            'total_fragments': fast_ani_proc.total_fragments
        }
        #END fast_ani

        # At some point might do deeper type checking...
        if not isinstance(results, dict):
            raise ValueError('Method fast_ani return value ' +
                             'results is not type dict as required.')
        # return the results
        return [results]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
