import constants
from datetime import datetime
import os 
import parser
import ForensicsLogger

forensicLogger = ForensicsLogger.createLoggerObj()
forensicLogger.info("forensic logger has been initiated")
forensicLogger.info("begin logging: ")

import ForensicsLogger

def getYAMLFiles(path_to_dir):
    valid_  = [] 
    for root_, dirs, files_ in os.walk( path_to_dir ):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if(os.path.exists(full_p_file)):
             if (full_p_file.endswith( constants.YAML_EXTENSION  ) or full_p_file.endswith( constants.YML_EXTENSION  )  ):
               valid_.append(full_p_file)
               #Adding logging statement for forensic tracking
               forensicLogger.info('file has been accessed and appended to list data structure: %s', str(full_p_file))   
    forensicLogger.info('returning list, final list is: %s', str(valid_))
    return valid_ 

def getHelmTemplateContent( templ_dir ):
    template_content_dict = {}
    template_yaml_files =  getYAMLFiles( templ_dir )
    for template_yaml_file in template_yaml_files:
        value_as_str      = parser.readYAMLAsStr( template_yaml_file )
        forensicLogger.info('file has been read: %s', str(template_yaml_file)) 
        template_content_dict[template_yaml_file] = value_as_str
        forensicLogger.info('file has been added to dictionary data structure: %s', str(template_yaml_file)) 
    return template_content_dict 

def getSHFiles(path_to_dir):
    valid_  = [] 
    for root_, _, files_ in os.walk( path_to_dir ):
       for file_ in files_:
           full_p_file = os.path.join(root_, file_)
           if(os.path.exists(full_p_file)):
             if (full_p_file.endswith( constants.SH_EXTENSION  )  ):
               valid_.append(full_p_file)
               #Adding logging statement for forensic tracking
               forensicLogger.info('file has been accessed and appended to list data structure: %s', str(full_p_file))   
    forensicLogger.info('returning list, final list is: %s', str(valid_))
    return valid_ 

def readBashAsStr( path_sh_script ):
    _as_str = constants.YAML_SKIPPING_TEXT
    with open( path_sh_script , constants.FILE_READ_FLAG) as file_:
        _as_str = file_.read()
    #Adding logging statement for forensic tracking
    forensicLogger.info('Logging file access, reading file: %s', str(file_)) #_as_str
    return _as_str

def mineServiceGraph( script_path, dict_yaml, src_val ): 
    '''
    This method looks at YAML files that have kind:Service , and checks if used in another YAML with kind:Deployment 
    Works for all types. 
    Need to provide script path, script dict, value identified as smell 
    '''
    ret_lis = [] 
    svc_dir     = os.path.dirname( script_path )  + constants.SLASH_SYMBOL    
    yaml_files  = getYAMLFiles( svc_dir )   
    forensicLogger.info('list of yaml files retrieved: %s', str(yaml_files)) 
    for yaml_f in yaml_files:
        if( parser.checkIfValidK8SYaml( yaml_f ) ):
            dict_as_list   = parser.loadMultiYAML( yaml_f )
            sink_yaml_dict = parser.getSingleDict4MultiDocs( dict_as_list )                    
            sink_val_li_   = list(  parser.getValuesRecursively(sink_yaml_dict) )
            #Adding logging statement for forensic tracking
            forensicLogger.info('Logging file access: %s', str(yaml_f)) 
            #Adding logging statement for forensic tracking
            forensicLogger.info('Logging data structure access (assigning a value): %s', str(dict_as_list))     
            #Adding logging statement for forensic tracking
            forensicLogger.info('Logging data structure access (assigning a value): %s', str(sink_yaml_dict))                  
            #Adding logging statement for forensic tracking
            forensicLogger.info('Logging data structure access (assigning a value): %s', str(sink_val_li_ ))
            if( src_val in sink_val_li_ ) and ( constants.DEPLOYMENT_KW in sink_val_li_ ): 
                    sink_keys = parser.keyMiner(sink_yaml_dict, src_val)
                    if constants.K8S_APP_KW in sink_keys: 
                        ret_lis.append( (yaml_f, sink_keys  ) )
    return ret_lis 

if __name__=='__main__':
    path = "/Users/laura/Documents/comp5710/project/BLT-SQA2023-AUBURN-1/TEST_ARTIFACTS"
    yaml_list = getYAMLFiles(path)
    dictionary = getHelmTemplateContent(path)
    sh_list = getSHFiles(path)
    bash = readBashAsStr(path + "/empty.yml")
    mineServiceGraph(path, None, 0)

