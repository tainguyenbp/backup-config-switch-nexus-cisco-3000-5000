import gevent
import requests

def insecure_ssl_pushgateway_handler(url, method, timeout, headers, data):                                               
                                                                                                            
    def handler():                                                                                                       
        try:                                                                                                             
            # Disable SSL verification for the Pushgateway.                                                            
            ssl_context = ssl.create_default_context()                                                                   
            ssl_context.check_hostname = False                                                                           
            ssl_context.verify_mode = ssl.CERT_NONE                                                                      
            ssl_handler = urllib.request.HTTPSHandler(context=ssl_context)                                               
                                                                                                                         
            # Largely copied from prometheus_client.exposition.default_handler.                                          
            request = urllib.request.Request(url, data=data)                                                             
            request.get_method = lambda: method                                                                          
            for k, v in headers:                                                                                         
                request.add_header(k, v)                                                                                 
            response = urllib.request.build_opener(ssl_handler).open(                                                    
                request, timeout=timeout                                                                                 
            )                                                                                                            
            if response.getcode() >= 400:                                                                                
                logging.warning("Pushgateway metrics push failed. {} {}").format(                                        
                    response.geturl(), response.info()                                                                   
                )                                                                                                        
        except Exception as e:                                                                                           
            logging.warning("Pushgateway metrics push failed. Exception: {}".format(e))                                  
                                                                                                                         
    return handler
  
